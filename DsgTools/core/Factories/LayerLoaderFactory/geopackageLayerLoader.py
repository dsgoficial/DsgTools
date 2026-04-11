# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-10-24
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os
import json
from collections import defaultdict

from qgis.core import (
    QgsVectorLayer,
    QgsMessageLog,
    QgsCoordinateReferenceSystem,
    QgsDataSourceUri,
    QgsEditorWidgetSetup,
    Qgis,
    QgsProject,
)
from qgis.PyQt.QtSql import QSqlQuery

from .edgvLayerLoader import EDGVLayerLoader
from ....gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget


class GeopackageLayerLoader(EDGVLayerLoader):
    def __init__(self, iface, abstractDb, loadCentroids):
        """Constructor."""
        super(GeopackageLayerLoader, self).__init__(iface, abstractDb, loadCentroids)

        self.provider = "geopackage"

        try:
            dbVersion = abstractDb.getDatabaseVersion()
        except Exception as e:
            QgsMessageLog.logMessage(
                ":".join(e.args), "DSGTools Plugin", Qgis.MessageLevel.Critical
            )
            return

        self.buildUri()

    # ------------------------------------------------------------------ #
    # Methods copied from SpatialiteLayerLoader                           #
    # ------------------------------------------------------------------ #

    def buildUri(self):
        self.uri.setDatabase(self.abstractDb.db.databaseName())

    def checkLoaded(self, name):
        loaded = None
        database = self.abstractDb.db.databaseName()
        for ll in self.iface.mapCanvas().layers():
            if ll.name() == name:
                candidateUri = QgsDataSourceUri(ll.dataProvider().dataSourceUri())
                if database == candidateUri.database():
                    return ll
        return loaded

    def specialEdgvAttributes(self):
        return ["finalidade", "relacionado", "coincidecomdentrode", "tipo"]

    def tableFields(self, table):
        return self.abstractDb.tableFields(table)

    def domainMapping(self, modelVersion):
        basePath = os.path.join(
            os.path.dirname(__file__), "..", "..", "DbModels", "DomainMapping"
        )
        path = {
            "EDGV 3.0": os.path.join(basePath, "edgv_3.json"),
            "3.0": os.path.join(basePath, "edgv_3.json"),
            "EDGV 2.1.3 Pro": os.path.join(basePath, "edgv_213_pro.json"),
            "2.1.3 Pro": os.path.join(basePath, "edgv_213_pro.json"),
            "EDGV 2.1.3": os.path.join(basePath, "edgv_213.json"),
            "2.1.3": os.path.join(basePath, "edgv_213.json"),
        }.pop(modelVersion, None)
        if path is None or not os.path.exists(path):
            return dict()
        with open(path, "r") as fp:
            return json.load(fp)

    def getAllEdgvDomainsFromTableName(self, schema, table):
        self.abstractDb.checkAndOpenDb()
        ret = defaultdict(dict)
        db = self.abstractDb.db
        edgv = self.abstractDb.getDatabaseVersion()
        domainMap = self.domainMapping(edgv)
        fullTablaName = schema + "_" + table
        sql = "select code, code_name from dominios_{field} order by code"
        for fieldName in self.tableFields(fullTablaName):
            if fullTablaName in domainMap:
                domains = domainMap[fullTablaName]
                if fieldName in domains:
                    domainTable = domains[fieldName][0]
                else:
                    continue
                query = QSqlQuery(sql.format(field=domainTable), db)
            elif fieldName in self.specialEdgvAttributes():
                if edgv in ("2.1.3 Pro", "3.0 Pro"):
                    cat = table.rsplit("_", 1)[0].split("_", 1)[-1]
                else:
                    cat = table.split("_")[0]
                attrTable = "{attribute}_{cat}".format(attribute=fieldName, cat=cat)
                query = QSqlQuery(sql.format(field=attrTable), db)
            else:
                query = QSqlQuery(sql.format(field=fieldName), db)
            if not query.isActive():
                continue
            while query.next():
                code = str(query.value(0))
                code_name = query.value(1)
                ret[fieldName][code_name] = code
        return ret

    def load(
        self,
        inputList,
        useQml=False,
        uniqueLoad=False,
        useInheritance=False,
        stylePath=None,
        onlyWithElements=False,
        geomFilterList=[],
        customForm=False,
        editingDict=None,
        parent=None,
    ):
        self.iface.mapCanvas().freeze()
        layerList, isDictList = self.preLoadStep(inputList)
        filteredLayerList = self.filterLayerList(
            layerList, False, onlyWithElements, geomFilterList
        )
        filteredDictList = (
            [i for i in inputList if i["tableName"] in filteredLayerList]
            if isDictList
            else filteredLayerList
        )
        edgvVersion = self.abstractDb.getDatabaseVersion()
        isEdgv = not edgvVersion == "Non_EDGV"
        rootNode = QgsProject.instance().layerTreeRoot()
        dbNode = self.getDatabaseGroup(rootNode)
        domLayerDict = dict()
        lyrDict = self.getLyrDict(filteredDictList, isEdgv=isEdgv)
        groupDict = self.prepareGroups(dbNode, lyrDict)
        if parent:
            primNumber = 0
            for prim in list(lyrDict.keys()):
                for cat in list(lyrDict[prim].keys()):
                    for lyr in lyrDict[prim][cat]:
                        primNumber += 1
            localProgress = ProgressWidget(
                1, primNumber - 1, self.tr("Loading layers... "), parent=parent
            )
        loadedDict = dict()
        for prim in list(lyrDict.keys()):
            for cat in list(lyrDict[prim].keys()):
                for lyr in lyrDict[prim][cat]:
                    try:
                        vlayer = self.loadLayer(
                            lyr,
                            groupDict[prim][cat],
                            uniqueLoad,
                            stylePath,
                            domLayerDict,
                        )
                        if vlayer:
                            if isinstance(lyr, dict):
                                key = lyr["lyrName"]
                            else:
                                key = lyr
                            loadedDict[key] = vlayer
                    except Exception as e:
                        if isinstance(lyr, dict):
                            key = lyr["lyrName"]
                        else:
                            key = lyr
                        self.logErrorDict[key] = (
                            self.tr("Error for layer ") + key + ": " + ":".join(e.args)
                        )
                        self.logError()
                    if parent:
                        localProgress.step()
        self.removeEmptyNodes(dbNode)
        self.iface.mapCanvas().freeze(False)
        return loadedDict

    def setDomainMappingToLayer(self, layer, schema):
        fields = layer.fields()
        mappings = self.getAllEdgvDomainsFromTableName(schema, layer.name())
        for field, valueMap in mappings.items():
            fieldIndex = fields.indexFromName(field)
            widgetSetup = QgsEditorWidgetSetup("ValueMap", {"map": valueMap})
            layer.setEditorWidgetSetup(fieldIndex, widgetSetup)

    def getStyleFromDb(self, edgvVersion, className):
        return None

    def filterLayerList(
        self, layerList, useInheritance, onlyWithElements, geomFilterList
    ):
        filterList = []
        if onlyWithElements:
            semifinalList = self.abstractDb.getLayersWithElementsV2(
                layerList, useInheritance=False
            )
        else:
            semifinalList = layerList
        if len(geomFilterList) > 0:
            finalList = []
            for key in self.correspondenceDict:
                if self.correspondenceDict[key] in geomFilterList:
                    if key in self.geomTypeDict:
                        for lyr in semifinalList:
                            if lyr in self.geomTypeDict[key] and lyr not in finalList:
                                finalList.append(lyr)
        else:
            finalList = semifinalList
        return finalList

    def setMulti(self, vlayer, domLayerDict):
        attrList = vlayer.fields()
        for field in attrList:
            i = attrList.lookupField(field.name())
            editorWidgetSetup = vlayer.editorWidgetSetup(i)
            if editorWidgetSetup.type() == "ValueRelation":
                valueRelationDict = editorWidgetSetup.config()
                domLayer = domLayerDict[vlayer.name()][field.name()]
                valueRelationDict["Layer"] = domLayer.id()
                vlayer.setEditorWidgetSetup(i, valueRelationDict)
        return vlayer

    # ------------------------------------------------------------------ #
    # GeoPackage-specific overrides                                        #
    # ------------------------------------------------------------------ #

    def loadLayer(self, inputParam, parentNode, uniqueLoad, stylePath, domLayerDict):
        lyrName, schema, geomColumn, tableName, srid = self.getParams(inputParam)
        lyr = self.checkLoaded(tableName)
        if uniqueLoad and lyr:
            return lyr
        vlayer = self.getLayerByName("{0}_{1}".format(schema, tableName))
        if not vlayer.isValid():
            QgsMessageLog.logMessage(
                vlayer.error().summary(), "DSGTools Plugin", Qgis.MessageLevel.Critical
            )
        QgsProject.instance().addMapLayer(vlayer, addToLegend=False)
        crs = QgsCoordinateReferenceSystem(
            int(srid), QgsCoordinateReferenceSystem.EpsgCrsId
        )
        vlayer.setCrs(crs)
        vlayer = self.setDomainsAndRestrictionsWithQml(vlayer)
        vlayer = self.setMulti(vlayer, domLayerDict)
        if stylePath:
            fullPath = self.getStyle(stylePath, tableName)
            if fullPath:
                vlayer.loadNamedStyle(fullPath, True)
        parentNode.addLayer(vlayer)
        vlayer = self.createMeasureColumn(vlayer)
        return vlayer

    def getLayerByName(self, layer):
        schema = layer.split("_")[0]
        table = layer[len(schema) + 1 :]
        lyrName, schema, geomColumn, tableName, srid = self.getParams(table)
        self.setDataSource("", layer, geomColumn, "")
        return QgsVectorLayer(
            "{0}|layername={1}".format(self.abstractDb.db.databaseName(), layer),
            table,
            "ogr",
        )
