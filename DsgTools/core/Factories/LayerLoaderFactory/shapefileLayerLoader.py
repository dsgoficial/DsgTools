# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-11-12
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

# Qt imports
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal
from qgis.PyQt.Qt import QObject

# QGIS imports
from qgis.core import QgsVectorLayer, QgsDataSourceUri, QgsMessageLog, QgsCoordinateReferenceSystem, QgsMessageLog, Qgis, QgsProject, QgsEditorWidgetSetup

#DsgTools imports
from .edgvLayerLoader import EDGVLayerLoader
from ....gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget

class ShapefileLayerLoader(EDGVLayerLoader):
    def __init__(self, iface, abstractDb):
        """
        Class constructor.
        :param iface: (QgsInterface) QGIS interface to be used to get runtime access to layers/features.
        :param abstractDb: (AbstractDb) database object as designed in DSGTools plugin. Check driver concordance.
        """
        # no reason for centroids to be used, so it'll be set to False always (parent requirement to init)
        super(ShapefileLayerLoader, self).__init__(iface, abstractDb, False)
        self.provider = 'shapefile'
        try:
            dbVersion = abstractDb.getDatabaseVersion()
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), 'DSGTools Plugin', Qgis.Critical)
            return
        self.buildUri()

    def buildUri(self):
        """
        Builds the database uri
        :return:
        """
        self.uri.setDatabase(self.abstractDb.databaseName())
    
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

    def load(self, inputList, useQml=False, uniqueLoad=False, useInheritance=False, stylePath=None, onlyWithElements=False, geomFilterList=[], isEdgv=True, customForm=False, editingDict=None, parent=None):
        """
        1. Get loaded layers
        2. Filter layers;
        3. Load domains;
        4. Get Aux Dicts;
        5. Build Groups;
        6. Load Layers;
        """
        self.iface.mapCanvas().freeze() #done to speedup things
        layerList, isDictList = self.preLoadStep(inputList)
        #2. Filter Layers:
        filteredLayerList = self.filterLayerList(layerList, False, onlyWithElements, geomFilterList)
        filteredDictList = [i for i in inputList if i['tableName'] in filteredLayerList] if isDictList else filteredLayerList
        edgvVersion = self.abstractDb.getDatabaseVersion()
        rootNode = QgsProject.instance().layerTreeRoot()
        dbNode = self.getDatabaseGroup(rootNode)
        #3. Load Domains
        #do this only if EDGV Version = FTer
        domLayerDict = self.loadDomains(filteredLayerList, dbNode, edgvVersion)
        #4. Get Aux dicts
        lyrDict = self.getLyrDict(filteredDictList, isEdgv = isEdgv)
        #5. Build Groups
        groupDict = self.prepareGroups(dbNode, lyrDict)
        #5. load layers
        if parent:
            primNumber = 0
            for prim in list(lyrDict.keys()):
                for cat in list(lyrDict[prim].keys()):
                    for lyr in lyrDict[prim][cat]:
                        primNumber += 1
            localProgress = ProgressWidget(1, primNumber-1, self.tr('Loading layers... '), parent=parent)
        loadedDict = dict()
        for prim in list(lyrDict.keys()):
            for cat in list(lyrDict[prim].keys()):
                for lyr in lyrDict[prim][cat]:
                    try:
                        vlayer = self.loadLayer(lyr, groupDict[prim][cat], uniqueLoad, stylePath, domLayerDict)
                        if vlayer:
                            if isinstance(lyr, dict):
                                key = lyr['lyrName']
                            else:
                                key = lyr
                            loadedDict[key]=vlayer
                    except Exception as e:
                        if isinstance(lyr, dict):
                            key = lyr['lyrName']
                        else:
                            key = lyr
                        self.logErrorDict[key] = self.tr('Error for layer ')+key+': '+':'.join(e.args)
                        self.logError()
                    if parent:
                        localProgress.step()
        self.removeEmptyNodes(dbNode)
        self.iface.mapCanvas().freeze(False) #done to speedup things
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
        self.setDataSource('', '_'.join([schema,tableName]), geomColumn, '')

        vlayer = QgsVectorLayer(self.uri.uri(), tableName, self.provider)
        QgsProject.instance().addMapLayer(vlayer, addToLegend = False)
        crs = QgsCoordinateReferenceSystem(int(srid), QgsCoordinateReferenceSystem.EpsgCrsId)
        vlayer.setCrs(crs)
        vlayer = self.setDomainsAndRestrictionsWithQml(vlayer)
        vlayer = self.setMulti(vlayer,domLayerDict)
        if stylePath:
            fullPath = self.getStyle(stylePath, tableName)
            if fullPath:
                vlayer.loadNamedStyle(fullPath, True)
        parentNode.addLayer(vlayer) 
        if not vlayer.isValid():
            QgsMessageLog.logMessage(vlayer.error().summary(), "DSGTools Plugin", Qgis.Critical)
        vlayer = self.createMeasureColumn(vlayer)
        return vlayer

    def loadDomain(self, domainTableName, domainGroup):
        """
        Loads layer domains
        :param domainTableName:
        :param domainGroup:
        :return:
        """
        #TODO: Avaliar se o table = deve ser diferente
        uri = QgsDataSourceUri()
        uri.setDatabase(self.abstractDb.db.databaseName())
        uri.setDataSource('', 'dominios_'+domainTableName, None)
        #TODO Load domain layer into a group
        domLayer = iface.addVectorLayer(uri.uri(), domainTableName, self.provider)
        self.iface.legendInterface().moveLayer(domLayer, domainGroup)
        return domLayer

    def getStyleFromDb(self, edgvVersion, className):
        return None

    def filterLayerList(self, layerList, useInheritance, onlyWithElements, geomFilterList):
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
            semifinalList = self.abstractDb.getLayersWithElementsV2(layerList, useInheritance=False)
        else:
            semifinalList = layerList
        if len(geomFilterList) > 0:
            finalList = []
            for key in self.correspondenceDict:
                if self.correspondenceDict[key] in geomFilterList:
                    if key in self.geomTypeDict:
                        for lyr in semifinalList:
                            if lyr in self.geomTypeDict[key] and  lyr not in finalList:
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
        #sweep vlayer to find v2
        attrList = vlayer.fields()
        for field in attrList:
            i = attrList.lookupField(field.name())
            editorWidgetSetup = vlayer.editorWidgetSetup(i)
            if editorWidgetSetup.type() == 'ValueRelation':
                valueRelationDict = editorWidgetSetup.config()
                domLayer = domLayerDict[vlayer.name()][field.name()]
                valueRelationDict['Layer'] = domLayer.id()
                vlayer.setEditorWidgetSetup(i, valueRelationDict)
        return vlayer

    def getLayerByName(self, layer):
        """
        Return the layer layer from a given layer name.
        :param layer: (str) layer name.
        :return: (QgsVectorLayer) vector layer. 
        """
        # parent class reimplementation
        path = os.path.join(self.abstractDb.databaseName(), "{0}.shp".format(layer))
        schema = layer.split('_')[0]
        table = layer[len(schema) + 1:].lower()
        return QgsVectorLayer(path, table, "ogr")
