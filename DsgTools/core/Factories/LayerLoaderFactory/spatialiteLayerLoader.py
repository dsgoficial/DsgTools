# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-07-16
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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
    Qgis,
    QgsProject,
    QgsMessageLog,
    QgsVectorLayer,
    QgsDataSourceUri,
    QgsEditorWidgetSetup,
    QgsCoordinateReferenceSystem,
)
from qgis.PyQt.QtSql import QSqlQuery

from .edgvLayerLoader import EDGVLayerLoader
from ....gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget


class SpatialiteLayerLoader(EDGVLayerLoader):
    def __init__(self, iface, abstractDb, loadCentroids):
        """Constructor."""
        super(SpatialiteLayerLoader, self).__init__(iface, abstractDb, loadCentroids)

        self.provider = "spatialite"

        try:
            dbVersion = abstractDb.getDatabaseVersion()
        except Exception as e:
            QgsMessageLog.logMessage(":".join(e.args), "DSGTools Plugin", Qgis.Critical)
            return

        self.buildUri()

    def buildUri(self):
        """
        Builds the database uri
        :return:
        """
        self.uri.setDatabase(self.abstractDb.db.databaseName())

    def checkLoaded(self, name):
        """
        Checks if the layers is already loaded in the QGIS' TOC
        :param name:
        :return:
        """
        loaded = None
        database = self.abstractDb.db.databaseName()
        for ll in self.iface.mapCanvas().layers():
            if ll.name() == name:
                candidateUri = QgsDataSourceUri(ll.dataProvider().dataSourceUri())
                if database == candidateUri.database():
                    return ll
        return loaded

    def specialEdgvAttributes(self):
        """
        Gets the list of attributes shared by many EDGV classes and have a different domain
        depending on which category the EDGV class belongs to.
        :return: (list-of-str) list of "special" EDGV classes.
        """
        return ["finalidade", "relacionado", "coincidecomdentrode", "tipo"]

    def tableFields(self, table):
        """
        Gets all attribute names for a table.
        :return: (list-of-str) list of attribute names.
        """
        return self.abstractDb.tableFields(table)

    def domainMapping(self, modelVersion):
        """
        Identifies wich table and attribute is related to all tables available
        in the database that has a mapping (FK to a domain table).
        :param modelVersion: (str) which model version is identified (e.g. 3.0)
        :return: (dict) mapping from each layer's attributes to its FK relative
        - Mapping format:
            {
                "schema_layer_name": {
                    "layer_attribute_name": [
                        "domain_table_name",
                        "domain_refereced_attribute_name"
                    ]
                }
            }
        """
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
            # file generated based on PostGIS FK metadata
            return json.load(fp)

    def getAllEdgvDomainsFromTableName(self, schema, table):
        """
        EDGV databases deployed by DSGTools have a set of domain tables. Gets the value map from such DB.
        It checks for all attributes found.
        :param table: (str) layer to be checked for its EDGV mapping.
        :return: (dict) value map for all attributes that have one.
        """
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
                # if domain mapping is not yet available for current version
                if fieldName in domains:
                    # replace this method over querying db for the table...
                    domainTable = domains[fieldName][0]
                else:
                    # non-mapped attribute
                    continue
                query = QSqlQuery(sql.format(field=domainTable), db)
            elif fieldName in self.specialEdgvAttributes():
                # EDGV "special" attributes that are have different domains depending on
                # which class it belongs to
                if edgv in ("2.1.3 Pro", "3.0 Pro"):
                    # Pro versions now follow the logic "{attribute}_{CLASS_NAME}"
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
        """
        1. Get loaded layers
        2. Filter layers;
        3. Load domains;
        4. Get Aux Dicts;
        5. Build Groups;
        6. Load Layers;
        """
        self.iface.mapCanvas().freeze()  # done to speedup things
        layerList, isDictList = self.preLoadStep(inputList)
        # 2. Filter Layers:
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
        # #3. Load Domains
        # #do this only if EDGV Version = FTer
        # domLayerDict = self.loadDomains(filteredLayerList, dbNode, edgvVersion)
        # NOTE: iface.interfaceLegend() has changed and loadDomain must change its signature.
        #       since this whole feature MUST be refactored and domain tables are not to be
        #       loaded in any of our current use cases, this will be ignored and set to an
        #       empty dict
        domLayerDict = dict()
        # 4. Get Aux dicts
        lyrDict = self.getLyrDict(filteredDictList, isEdgv=isEdgv)
        # 5. Build Groups
        groupDict = self.prepareGroups(dbNode, lyrDict)
        # 5. load layers
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
        self.iface.mapCanvas().freeze(False)  # done to speedup things
        return loadedDict

    def loadLayer(self, inputParam, parentNode, uniqueLoad, stylePath, domLayerDict):
        """
        Loads a layer
        :param lyrName: Layer nmae
        :param idSubgrupo: sub group id
        :param uniqueLoad: boolean to mark if the layer should only be loaded once
        :param stylePath: path to the styles used
        :param domLayerDict: domain dictionary
        :return:
        """
        lyrName, schema, geomColumn, tableName, srid = self.getParams(inputParam)
        lyr = self.checkLoaded(tableName)
        if uniqueLoad and lyr:
            return lyr
        self.setDataSource("", "_".join([schema, tableName]), geomColumn, "")

        vlayer = QgsVectorLayer(self.uri.uri(), tableName, self.provider)
        QgsProject.instance().addMapLayer(vlayer, addToLegend=False)
        crs = QgsCoordinateReferenceSystem(
            int(srid), QgsCoordinateReferenceSystem.EpsgCrsId
        )
        vlayer.setCrs(crs)
        # vlayer = self.setDomainsAndRestrictionsWithQml(vlayer)
        # vlayer = self.setMulti(vlayer, domLayerDict)
        self.setDomainMappingToLayer(vlayer, schema)
        if stylePath:
            fullPath = self.getStyle(stylePath, tableName)
            if fullPath:
                vlayer.loadNamedStyle(fullPath, True)
        parentNode.addLayer(vlayer)
        vlayer = self.createMeasureColumn(vlayer)
        return vlayer

    def setDomainMappingToLayer(self, layer, schema):
        """
        Sets the maps the attributes that are represented as value maps on the
        EDGV implementation for a given layer.
        :param layer: (QgsVectorLayer) layer to have its attributes mapped.
        :param schema: (str) first "part" of table names in SpatiaLite
                       implementations of EDGV from DSGTools. They are
                       equivalent to the schema in PostgreSQL implementations.
        """
        fields = layer.fields()
        mappings = self.getAllEdgvDomainsFromTableName(schema, layer.name())
        for field, valueMap in mappings.items():
            fieldIndex = fields.indexFromName(field)
            widgetSetup = QgsEditorWidgetSetup("ValueMap", {"map": valueMap})
            layer.setEditorWidgetSetup(fieldIndex, widgetSetup)

    def loadDomain(self, domainTableName, domainGroup):
        """
        Loads layer domains
        :param domainTableName:
        :param domainGroup:
        :return:
        """
        # TODO: Avaliar se o table = deve ser diferente
        uri = QgsDataSourceUri()
        uri.setDatabase(self.abstractDb.db.databaseName())
        uri.setDataSource("", "dominios_" + domainTableName, None)
        # TODO Load domain layer into a group
        domLayer = self.iface.addVectorLayer(uri.uri(), domainTableName, self.provider)
        self.iface.legendInterface().moveLayer(domLayer, domainGroup)
        return domLayer

    def getStyleFromDb(self, edgvVersion, className):
        return None

    def filterLayerList(
        self, layerList, useInheritance, onlyWithElements, geomFilterList
    ):
        """
        Filters the layers to be loaded
        :param layerList: list of layers
        :param useInheritance: should use inheritance
        :param onlyWithElements: should only load non empty layers?
        :param geomFilterList: geometry filter
        :return:
        """
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
        """
        Sets attributes with value relation
        :param vlayer:
        :param domLayerDict:
        :return:
        """
        # sweep vlayer to find v2
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

    def getLayerByName(self, layer):
        """
        Return the layer layer from a given layer name.
        :param layer: (str) layer name.
        :return: (QgsVectorLayer) vector layer.
        """
        # parent class reimplementation
        schema = layer.split("_")[0]
        table = layer[len(schema) + 1 :]
        lyrName, schema, geomColumn, tableName, srid = self.getParams(table)
        self.setDataSource("", layer, geomColumn, "")
        return QgsVectorLayer(self.uri.uri(), table, self.provider)
