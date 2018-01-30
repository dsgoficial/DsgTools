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
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.Qt import QObject

# QGIS imports
from qgis.core import QgsMapLayerRegistry, QgsVectorLayer,QgsDataSourceURI, QgsMessageLog, QgsCoordinateReferenceSystem, QgsMessageLog
from qgis.utils import iface

#DsgTools imports
from DsgTools.Factories.LayerLoaderFactory.edgvLayerLoader import EDGVLayerLoader
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

class PostGISLayerLoader(EDGVLayerLoader):
    def __init__(self, iface, abstractDb, loadCentroids):
        """Constructor."""
        super(self.__class__, self).__init__(iface, abstractDb, loadCentroids)
        
        self.provider = 'postgres'
        self.setDatabaseConnection()
        self.buildUri()

    def checkLoaded(self, name, loadedLayers):
        """
        Checks if the layers is already loaded in the QGIS' TOC
        :param name:
        :param loadedLayers:
        :return:
        """
        loaded = None
        for ll in loadedLayers:
            if ll.name() == name:
                candidateUri = QgsDataSourceURI(ll.dataProvider().dataSourceUri())
                if self.host == candidateUri.host() and self.database == candidateUri.database() and self.port == int(candidateUri.port()):
                    return ll
        return loaded
    
    def setDatabaseConnection(self):
        """
        Sets database connection parameters
        :return:
        """
        self.host = self.abstractDb.db.hostName()
        self.port = self.abstractDb.db.port()
        self.database = self.abstractDb.db.databaseName()
        self.user = self.abstractDb.db.userName()
        self.password = self.abstractDb.db.password()
    
    def buildUri(self):
        """
        Builds the database uri
        :return:
        """
        self.uri.setConnection(str(self.host),str(self.port), str(self.database), str(self.user), str(self.password))
    
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
            lyrsWithElements = self.abstractDb.getLayersWithElementsV2(layerList, useInheritance = useInheritance)
        else:
            lyrsWithElements = layerList
        if useInheritance:
            semifinalList = self.abstractDb.getLayersFilterByInheritance(lyrsWithElements)
        else:
            semifinalList = lyrsWithElements
        if len(geomFilterList) > 0:
            finalList = []
            for key in self.correspondenceDict:
                if self.correspondenceDict[key] in geomFilterList:
                    if key in self.geomTypeDict.keys():
                        for lyr in semifinalList:
                            if lyr in self.geomTypeDict[key] and  lyr not in finalList:
                                finalList.append(lyr)
        else:
            finalList = semifinalList
        return finalList

    def load(self, inputList, useQml = False, uniqueLoad = False, useInheritance = False, stylePath = None, onlyWithElements = False, geomFilterList = [], isEdgv = True, parent = None):
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
        filteredLayerList = self.filterLayerList(layerList, useInheritance, onlyWithElements, geomFilterList)
        if isDictList:
            filteredDictList = [i for i in inputList if i['tableName'] in filteredLayerList]
        else:
            filteredDictList = filteredLayerList
        edgvVersion = self.abstractDb.getDatabaseVersion()
        dbGroup = self.getDatabaseGroup(loadedGroups)
        #3. Load Domains
        #do this only if EDGV Version = FTer
        if edgvVersion in ('FTer_2a_Ed', '3.0'):
            domainGroup = self.createGroup(loadedGroups, self.tr("Domains"), dbGroup)
            domLayerDict = self.loadDomains(filteredLayerList, loadedLayers, domainGroup)
        else:
            domLayerDict = dict()
        #4. Get Aux dicts
        domainDict = self.abstractDb.getDbDomainDict(self.geomDict)
        constraintDict = self.abstractDb.getCheckConstraintDict()
        multiColumnsDict = self.abstractDb.getMultiColumnsDict()
        notNullDict = self.abstractDb.getNotNullDictV2()
        lyrDict = self.getLyrDict(filteredDictList, isEdgv=isEdgv)
        
        #5. Build Groups
        groupDict = self.prepareGroups(loadedGroups, dbGroup, lyrDict)
        #6. load layers
        loadedDict = dict()
        if parent:
            primNumber = 0
            for prim in lyrDict.keys():
                for cat in lyrDict[prim].keys():
                    for lyr in lyrDict[prim][cat]:
                        primNumber += 1
            localProgress = ProgressWidget(1, primNumber-1, self.tr('Loading layers... '), parent=parent)
        for prim in lyrDict.keys():
            for cat in lyrDict[prim].keys():
                for lyr in lyrDict[prim][cat]:
                    try:
                        vlayer = self.loadLayer(lyr, groupDict[prim][cat], loadedLayers, useInheritance, useQml, uniqueLoad, stylePath, domainDict, multiColumnsDict, domLayerDict, edgvVersion)
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

    def loadLayer(self, inputParam, idSubgrupo, loadedLayers, useInheritance, useQml, uniqueLoad, stylePath, domainDict, multiColumnsDict, domLayerDict, edgvVersion, geomColumn = None, isView = False):
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
            lyr = self.checkLoaded(tableName, loadedLayers)
            if lyr:
                return lyr
        fullName = '''"{0}"."{1}"'''.format(schema, tableName)
        pkColumn = self.abstractDb.getPrimaryKeyColumn(fullName)
        if useInheritance:
            sql = ''
        else:
            sql = self.abstractDb.gen.loadLayerFromDatabase(fullName, pkColumn=pkColumn)            
        self.setDataSource(schema, tableName, geomColumn, sql, pkColumn=pkColumn)

        vlayer = iface.addVectorLayer(self.uri.uri(), tableName, self.provider)
        crs = QgsCoordinateReferenceSystem(int(srid), QgsCoordinateReferenceSystem.EpsgCrsId)
        if vlayer:
            vlayer.setCrs(crs)
            if useQml:
                vlayer = self.setDomainsAndRestrictionsWithQml(vlayer)
            else:
                vlayer = self.setDomainsAndRestrictions(vlayer, tableName, domainDict, multiColumnsDict, domLayerDict)
            if stylePath:
                fullPath = self.getStyle(stylePath, tableName)
                if fullPath:
                    vlayer.applyNamedStyle(fullPath)
            iface.legendInterface().moveLayer(vlayer, idSubgrupo)   
            if not vlayer.isValid():
                QgsMessageLog.logMessage(vlayer.error().summary(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        vlayer = self.createMeasureColumn(vlayer)
        return vlayer

    def getDomainsFromDb(self, layerList, loadedLayers, domainDict, multiColumnsDict):
        """
        Gets domain data for each layer to be loaded
        :param layerList:
        :param loadedLayers:
        :param domainDict:
        :param multiColumnsDict:
        :return:
        """
        domainList = []
        keys = domainDict.keys()
        multiLayers = multiColumnsDict.keys()
        for lyr in layerList:
            if lyr in keys and lyr in multiLayers:
                for attr in domainDict[lyr]['columns'].keys():
                    if attr in multiColumnsDict[lyr]:
                        dom = domainDict[lyr]['columns'][attr]['references']
                        if dom not in domainList:
                            domainList.append(dom)
        return domainList
    
    def loadDomain(self, domainTableName, domainGroup):
        """
        Loads layer domains
        :param domainTableName:
        :param domainGroup:
        :return:
        """
        #TODO: Avaliar se o table = deve ser diferente
        uri = "dbname='%s' host=%s port=%s user='%s' password='%s' key=code table=\"dominios\".\"%s\" sql=" % (self.database, self.host, self.port, self.user, self.password, domainTableName)
        domLayer = iface.addVectorLayer(uri, domainTableName, self.provider)
        self.iface.legendInterface().moveLayer(domLayer, domainGroup)
        return domLayer

    def getStyleFromDb(self, edgvVersion, className):
        """
        Gets the style for this layer in the database
        :param edgvVersion:
        :param className:
        :return:
        """
        return self.abstractDb.getLyrStyle(edgvVersion, className)

    def setDomainsAndRestrictions(self, lyr, lyrName, domainDict, multiColumnsDict, domLayerDict):
        """
        Adjusts the domain restriction to all attributes in the layer
        :param lyr:
        :param lyrName:
        :param domainDict:
        :param multiColumnsDict:
        :param domLayerDict:
        :return:
        """
        lyrAttributes = [i for i in lyr.pendingFields()]
        for i in range(len(lyrAttributes)):
            attrName = lyrAttributes[i].name()
            if attrName == 'id' or 'id_' in lyrAttributes[i].name():
                lyr.setFieldEditable(i,False)
            else:
                if lyrName in domainDict.keys():
                    if attrName in domainDict[lyrName]['columns'].keys():
                        refTable = domainDict[lyrName]['columns'][attrName]['references']
                        refPk = domainDict[lyrName]['columns'][attrName]['refPk']
                        otherKey = domainDict[lyrName]['columns'][attrName]['otherKey']
                        valueDict = domainDict[lyrName]['columns'][attrName]['values']
                        isMulti = self.checkMulti(lyrName, attrName, multiColumnsDict)
                        if isMulti:
                            #Do value relation
                            lyr.setEditorWidgetV2(i,'ValueRelation')
                            #make filter
                            if 'constraintList' in domainDict[lyrName]['columns'][attrName].keys():
                                filter = '{0} in ({1})'.format(refPk,','.join(map(str,domainDict[lyrName]['columns'][attrName]['constraintList'])))
                                allowNull = domainDict[lyrName]['columns'][attrName]['nullable']
                                #make editDict
                                if lyrName in domLayerDict.keys():
                                    if attrName in domLayerDict[lyrName].keys():
                                        dom = domLayerDict[lyrName][attrName]
                                        editDict = {'Layer':dom.id(),'Key':refPk,'Value':otherKey,'AllowMulti':True,'AllowNull':allowNull,'FilterExpression':filter}
                                        lyr.setEditorWidgetV2Config(i,editDict)
                        else:
                            #Value Map
                            lyr.setEditorWidgetV2(i,'ValueMap')
                            #filter value dict
                            constraintList = domainDict[lyrName]['columns'][attrName]['constraintList']
                            valueRelationDict = dict()
                            for key in valueDict.keys():
                                if len(constraintList) > 0: 
                                    if key in constraintList:
                                        valueRelationDict[valueDict[key]] = str(key)
                                else:
                                    valueRelationDict[valueDict[key]] = str(key)
                            lyr.setEditorWidgetV2Config(i,valueRelationDict)
                            #setEditorWidgetV2Config is deprecated. We will change it eventually.
        return lyr

    def checkMulti(self, tableName, attrName, multiColumnsDict):
        """
        Checks if an attribute is a value relation
        :param tableName:
        :param attrName:
        :param multiColumnsDict:
        :return:
        """
        if tableName in multiColumnsDict.keys():
            if attrName in multiColumnsDict[tableName]:
                return True
        return False
    
    def checkNotNull(self, lyrName, notNullDict):
        """
        Checks not null attributes
        :param lyrName:
        :param notNullDict:
        :return:
        """
        allowNull = True
        if lyrName in notNullDict.keys():
            if attrName in notNullDict[lyrName]['attributes']:
                allowNull = False
        return allowNull
