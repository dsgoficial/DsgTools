# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-11-24
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
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
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.Qt import QObject

# QGIS imports
from qgis.core import QgsMapLayerRegistry, QgsVectorLayer,QgsDataSourceURI, QgsMessageLog
from qgis.utils import iface

#DsgTools imports
from DsgTools.Factories.LayerFactoryV2.edgv_layerV2 import EDGVLayerV2

class SpatialiteLayerV2(EDGVLayerV2):
    def __init__(self, iface, abstractDb):
        """Constructor."""
        super(self.__class__, self).__init__(iface, abstractDb)
        
        self.provider = 'spatialite'
        
        try:
            dbVersion = abstractDb.getDatabaseVersion()
        except Exception as e:
            QgsMessageLog.logMessage(e.args[0], 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
            return
            
        if dbVersion == '3.0' or dbVersion == '2.1.3' or dbVersion == 'FTer_2a_Ed':
            self.qmlName = '_'.join(table.replace('\r', '').split('_')[1::])
        else:
            self.qmlName = table.replace('\r','')

        self.buildUri()

    def buildUri(self):
        self.uri.setDatabase(self.abstractDb.db.databaseName())
    
    def checkLoaded(self, name, loadedLayers):
        loaded = None
        for ll in loadedLayers:
            if ll.name() == name:
                candidateUri = QgsDataSourceURI(ll.dataProvider().dataSourceUri())
                if database == candidateUri.database():
                    return ll
        return loaded

    def load(self, layerList, useQml = False, uniqueLoad = False, useInheritance = False, stylePath = None, onlyWithElements = False):
        '''
        1. Get loaded layers
        2. Filter layers;
        3. Load domains;
        4. Get Aux Dicts;
        5. Build Groups;
        6. Load Layers;
        '''
        #1. Get Loaded Layers
        loadedLayers = self.iface.legendInterface().layers()
        loadedGroups = self.iface.legendInterface().groups()
        #4. Filter Layers:
        filteredLayerList = self.filterLayerList(layerList, False, onlyWithElements)
        #2. Load Domains
        #do this only if EDGV Version = FTer
        edgvVersion = self.abstractDb.getDatabaseVersion()
        dbGroup = self.getDatabaseGroup(loadedGroups)
        if edgvVersion == 'FTer_2a_Ed':
            domainGroup = self.createGroup(loadedGroups, self.tr("Domains"), dbGroup)
            domLayerDict = self.loadDomains(filteredLayerList, loadedLayers, domainGroup)
        else:
            domLayerDict = dict()
        #3. Get Aux dicts

        lyrDict = self.getLyrDict(filteredLayerList)
        
        #4. Build Groups
        groupDict = self.prepareGroups(loadedGroups, dbGroup, lyrDict)
        #5. load layers
        loadedDict = dict()
        for prim in lyrDict.keys():
            for cat in lyrDict[prim].keys():
                for lyr in lyrDict[prim][cat]:
                    try:
                        vlayer = self.loadLayer(lyr, groupDict[prim][cat], useInheritance, useQml,uniqueLoad,stylePath,domainDict,multiColumnsDict,domLayerDict)
                        loadedDict[lyr]=vlayer
                    except Exception as e:
                        self.logErrorDict[lyr] = self.tr('Error for layer ')+lyr+': '+str(e.args[0])
                        self.logError()
        return loadedDict

    def loadLayer(self, lyrName, idSubgrupo, useInheritance, useQml, uniqueLoad,stylePath,domainDict,multiColumnsDict, domLayerDict):
        if uniqueLoad:
            lyr = self.checkLoaded(lyrName)
            if lyr:
                return lyr
        tableName = self.geomDict['tablePerspective'][lyrName]['tableName']
        geomColumn = self.geomDict['tablePerspective'][lyrName]['geometryColumn']
        srid =  self.geomDict['tablePerspective'][lyrName]['srid']
        self.setDataSource('', tableName, geomColumn, '')

        vlayer = iface.addVectorLayer(self.uri.uri(), lyrName, self.provider)
        crs = QgsCoordinateReferenceSystem(int(srid), QgsCoordinateReferenceSystem.EpsgCrsId)
        vlayer.setCrs(crs)
        vlayer = self.setDomainsAndRestrictionsWithQml(vlayer)
        
        if stylePath:
            fullPath = self.getStyle(stylePath, lyrName)
            if fullPath:
                vlayer.applyNamedStyle(fullPath)
        iface.legendInterface().moveLayer(vlayer, idSubgrupo)   
        if not vlayer.isValid():
            QgsMessageLog.logMessage(vlayer.error().summary(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        vlayer = self.createMeasureColumn(vlayer)
        return vlayer

    def loadDomain(self, domainTableName, domainGroup):
        #TODO: Avaliar se o table = deve ser diferente
        uri = QgsDataSourceURI()
        uri.setDatabase(database)
        uri.setDataSource('', 'dominios_'+domainTableName, None)
        #TODO Load domain layer into a group
        domLayer = iface.addVectorLayer(uri.uri(), domainTableName, self.provider)
        self.iface.legendInterface().moveLayer(domLayer, domainGroup)
        return domLayer

    def getStyleFromDb(self, edgvVersion, className):
        return None

    def filterLayerList(self, layerList, useInheritance, onlyWithElements):
        filterList = []
        if onlyWithElements:
            lyrsWithElements = self.abstractDb.getLayersWithElementsV2(layerList, useInheritance = False)
        else:
            lyrsWithElements = layerList

        return lyrsWithElements