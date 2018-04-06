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

# Qt imports
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal
from PyQt4.Qt import QObject

# QGIS imports
from qgis.core import QgsMapLayerRegistry, QgsVectorLayer,QgsDataSourceURI, QgsMessageLog, QgsCoordinateReferenceSystem, QgsMessageLog
from qgis.utils import iface

#DsgTools imports
from DsgTools.Factories.LayerLoaderFactory.edgvLayerLoader import EDGVLayerLoader
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

class SpatialiteLayerLoader(EDGVLayerLoader):
    def __init__(self, iface, abstractDb, loadCentroids):
        """Constructor."""
        super(self.__class__, self).__init__(iface, abstractDb, loadCentroids)
        
        self.provider = 'spatialite'
        
        try:
            dbVersion = abstractDb.getDatabaseVersion()
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
            return

        self.buildUri()

    def buildUri(self):
        """
        Builds the database uri
        :return:
        """
        self.uri.setDatabase(self.abstractDb.db.databaseName())
    
    def checkLoaded(self, name, loadedLayers):
        """
        Checks if the layers is already loaded in the QGIS' TOC
        :param name: 
        :param loadedLayers: 
        :return:
        """
        loaded = None
        database = self.abstractDb.db.databaseName()
        for ll in loadedLayers:
            if ll.name() == name:
                candidateUri = QgsDataSourceURI(ll.dataProvider().dataSourceUri())
                if database == candidateUri.database():
                    return ll
        return loaded

    def load(self, inputList, useQml = False, uniqueLoad = False, useInheritance = False, stylePath = None, onlyWithElements = False, geomFilterList = [], isEdgv = True, customForm = False, parent = None):
        """
        1. Get loaded layers
        2. Filter layers;
        3. Load domains;
        4. Get Aux Dicts;
        5. Build Groups;
        6. Load Layers;
        """
        layerList, isDictList = self.preLoadStep(inputList)
        #1. Get Loaded Layers
        loadedLayers = self.iface.legendInterface().layers()
        loadedGroups = self.iface.legendInterface().groups()
        #2. Filter Layers:
        filteredLayerList = self.filterLayerList(layerList, False, onlyWithElements, geomFilterList)
        if isDictList:
            filteredDictList = [i for i in inputList if i['tableName'] in filteredLayerList]
        else:
            filteredDictList = filteredLayerList
        #3. Load Domains
        #do this only if EDGV Version = FTer
        edgvVersion = self.abstractDb.getDatabaseVersion()
        dbGroup = self.getDatabaseGroup(loadedGroups)
        if edgvVersion in ('FTer_2a_Ed', '3.0'):
            domainGroup = self.createGroup(loadedGroups, self.tr("Domains"), dbGroup)
            domLayerDict = self.loadDomains(filteredLayerList, loadedLayers, domainGroup)
        else:
            domLayerDict = dict()
        #4. Get Aux dicts

        lyrDict = self.getLyrDict(filteredDictList, isEdgv = isEdgv)
        
        #5. Build Groups
        groupDict = self.prepareGroups(loadedGroups, dbGroup, lyrDict)
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
                        vlayer = self.loadLayer(lyr, loadedLayers, groupDict[prim][cat], uniqueLoad, stylePath, domLayerDict)
                        if vlayer:
                            loadedLayers.append(vlayer)
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
        return loadedDict

    def loadLayer(self, inputParam, loadedLayers, idSubgrupo, uniqueLoad, stylePath, domLayerDict):
        """
        Loads a layer
        :param lyrName: Layer nmae
        :param loadedLayers: list of loaded layers
        :param idSubgrupo: sub group id
        :param uniqueLoad: boolean to mark if the layer should only be loaded once
        :param stylePath: path to the styles used
        :param domLayerDict: domain dictionary
        :return:
        """
        if isinstance(inputParam,dict):
            lyrName = inputParam['lyrName']
            schema = inputParam['tableSchema']
            geomColumn = inputParam['geom']
            tableName = inputParam['tableName']
            srid =  self.geomDict['tablePerspective'][tableName]['srid']
        else:
            lyrName = inputParam
            tableName = self.geomDict['tablePerspective'][lyrName]['tableName']
            schema = self.geomDict['tablePerspective'][lyrName]['schema']
            geomColumn = self.geomDict['tablePerspective'][lyrName]['geometryColumn']
            srid =  self.geomDict['tablePerspective'][lyrName]['srid']
        if uniqueLoad:
            lyr = self.checkLoaded(lyrName, loadedLayers)
            if lyr:
                return lyr
        self.setDataSource('', '_'.join([schema,tableName]), geomColumn, '')

        vlayer = iface.addVectorLayer(self.uri.uri(), tableName, self.provider)
        crs = QgsCoordinateReferenceSystem(int(srid), QgsCoordinateReferenceSystem.EpsgCrsId)
        vlayer.setCrs(crs)
        vlayer = self.setDomainsAndRestrictionsWithQml(vlayer)
        vlayer = self.setMulti(vlayer,domLayerDict)
        if stylePath:
            fullPath = self.getStyle(stylePath, tableName)
            if fullPath:
                vlayer.applyNamedStyle(fullPath)
        iface.legendInterface().moveLayer(vlayer, idSubgrupo)   
        if not vlayer.isValid():
            QgsMessageLog.logMessage(vlayer.error().summary(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
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
        uri = QgsDataSourceURI()
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
        attrList = vlayer.pendingFields()
        for field in attrList:
            i = vlayer.fieldNameIndex(field.name())
            if vlayer.editorWidgetV2(i) == 'ValueRelation':
                valueRelationDict = vlayer.editorWidgetV2Config(i)
                domLayer = domLayerDict[vlayer.name()][field.name()]
                valueRelationDict['Layer'] = domLayer.id()
                vlayer.setEditorWidgetV2Config(i, valueRelationDict)
        return vlayer