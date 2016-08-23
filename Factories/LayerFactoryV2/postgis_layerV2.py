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
from qgis.core import QgsMapLayerRegistry, QgsVectorLayer,QgsDataSourceURI, QgsMessageLog, QgsCoordinateReferenceSystem, QgsMessageLog
from qgis.utils import iface

#DsgTools imports
from DsgTools.Factories.LayerFactoryV2.edgv_layerV2 import EDGVLayerV2

class PostGISLayerV2(EDGVLayerV2):
    def __init__(self, iface, abstractDb):
        """Constructor."""
        super(self.__class__, self).__init__(iface, abstractDb)
        
        self.provider = 'postgres'
        self.setDatabaseConnection()
        self.buildUri()
        self.geomDict = self.abstractDb.getGeomDict()

    def checkLoaded(self, name, loadedLayers):
        loaded = None
        for ll in loadedLayers:
            if ll.name() == name:
                candidateUri = QgsDataSourceURI(ll.dataProvider().dataSourceUri())
                if self.host == candidateUri.host() and self.database == candidateUri.database() and self.port == int(candidateUri.port()):
                    return ll
        return loaded
    
    def setDatabaseConnection(self):
        self.host = self.abstractDb.db.hostName()
        self.port = self.abstractDb.db.port()
        self.database = self.abstractDb.db.databaseName()
        self.user = self.abstractDb.db.userName()
        self.password = self.abstractDb.db.password()
    
    def buildUri(self):
        self.uri.setConnection(str(self.host),str(self.port), str(self.database), str(self.user), str(self.password))
    
    def setDataSource(self, schema, layer, geomColumn, sql):
        self.uri.setDataSource(schema, layer, geomColumn, sql, 'id')
        self.uri.disableSelectAtId(True)
    
    def getDatabaseGroup(self, groupList):
        dbName = self.abstractDb.getDatabaseName()
        if dbName in groupList:
            return groupList.index(dbName)
        else:
            return self.iface.legendInterface().addGroup(dbName, True, -1)
    
    def getLyrDict(self, lyrList):
        #redo
        lyrDict = dict()
        lyrList.sort()
        for lyr in lyrList:
            cat = lyr.split('_')[0]
            if lyr[-1] == 'p':
                if self.tr('Point') not in lyrDict.keys():
                    lyrDict[self.tr('Point')] = dict()
                if cat not in lyrDict[self.tr('Point')].keys():
                    lyrDict[self.tr('Point')][cat] = []
                lyrDict[self.tr('Point')][cat].append(lyr)
            if lyr[-1] == 'l':
                if self.tr('Line') not in lyrDict.keys():
                    lyrDict[self.tr('Line')] = dict()
                if cat not in lyrDict[self.tr('Line')].keys():
                    lyrDict[self.tr('Line')][cat] = []
                lyrDict[self.tr('Line')][cat].append(lyr)
            if lyr[-1] == 'a':
                if self.tr('Area') not in lyrDict.keys():
                    lyrDict[self.tr('Area')] = dict()
                if cat not in lyrDict[self.tr('Area')].keys():
                    lyrDict[self.tr('Area')][cat] = []
                lyrDict[self.tr('Area')][cat].append(lyr)
        return lyrDict
    
    def prepareGroups(self, groupList, parent, lyrDict):
        aux = dict()
        groupDict = dict()
        for geomNode in lyrDict.keys():
            groupDict[geomNode] = dict()
            aux = self.createGroup(groupList, geomNode, parent)
            for catNode in lyrDict[geomNode].keys():
                groupDict[geomNode][catNode] = self.createGroup(groupList, catNode, aux)
        return groupDict
    
    def createGroup(self, groupList, groupName, parent):
        subgroup = groupList[parent::]
        if groupName in subgroup:
            return parent+subgroup.index(groupName) #verificar
        else:
            return self.iface.legendInterface().addGroup(groupName, True, parent)
    
    def filterLayerList(self, layerList, useInheritance, onlyWithElements):
        filterList = []
        if onlyWithElements:
            lyrsWithElements = self.abstractDb.getLayersWithElementsV2(layerList)
        else:
            lyrsWithElements = layerList
        if useInheritance:
            finalList = self.abstractDb.getLayersFilterByInheritance(lyrsWithElements)
        else:
            finalList = lyrsWithElements
        return finalList

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
        filteredLayerList = self.filterLayerList(layerList, useInheritance, onlyWithElements)
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
        geomDict = self.abstractDb.getGeomDict()
        domainDict = self.abstractDb.getDbDomainDict()
        constraintDict = self.abstractDb.getCheckConstraintDict()
        multiColumnsDict = self.abstractDb.getMultiColumnsDict()
        notNullDict = self.abstractDb.getNotNullDictV2()
        lyrDict = self.getLyrDict(filteredLayerList)
        
        
        #4. Build Groups
        groupDict = self.prepareGroups(loadedGroups, dbGroup, lyrDict)
        #5. load layers
        for prim in lyrDict.keys():
            for cat in lyrDict[prim].keys():
                for lyr in lyrDict[prim][cat]:
                    self.loadLayer(lyr, groupDict[prim][cat], useInheritance, useQml,uniqueLoad,stylePath,geomDict,domainDict,multiColumnsDict,domLayerDict)

    def loadLayer(self, lyrName, idSubgrupo, useInheritance, useQml, uniqueLoad,stylePath,geomDict,domainDict,multiColumnsDict, domLayerDict):
        if uniqueLoad:
            lyr = self.checkLoaded(lyrName)
            if lyr:
                return lyr
        schema = geomDict['tablePerspective'][lyrName]['schema']
        geomColumn = geomDict['tablePerspective'][lyrName]['geometryColumn']
        srid =  geomDict['tablePerspective'][lyrName]['srid']
        if useInheritance:
            sql = ''
        else:
            sql = self.abstractDb.gen.loadLayerFromDatabase(schema+'.'+lyrName)            
        self.setDataSource(schema, lyrName, geomColumn, sql)

        vlayer = iface.addVectorLayer(self.uri.uri(), lyrName, self.provider)
        crs = QgsCoordinateReferenceSystem(int(srid), QgsCoordinateReferenceSystem.EpsgCrsId)
        vlayer.setCrs(crs)
        if useQml:
            vlayer = self.setDomainsAndRestrictionsWithQml(vlayer)
        else:
            vlayer = self.setDomainsAndRestrictions(vlayer, lyrName, domainDict, multiColumnsDict, domLayerDict)
        if stylePath:
            fullPath = self.getStyle(stylePath, lyrName)
            if fullPath:
                vlayer.applyNamedStyle(fullPath)
        iface.legendInterface().moveLayer(vlayer, idSubgrupo)   
        if not vlayer.isValid():
            QgsMessageLog.logMessage(vlayer.error().summary(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        vlayer = self.createMeasureColumn(vlayer)

    def setDomainsAndRestrictionsWithQml(self, vlayer):
        qmldir = ''
        try:
            qmldir = self.abstractDb.getQmlDir()
        except Exception as e:
            self.problemOccurred.emit(self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(e.args[0], "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return None
        vlayerQml = os.path.join(qmldir, vlayer.name()+'.qml')
        #treat case of qml with multi
        vlayer.loadNamedStyle(vlayerQml, False)
        return vlayer

    def getDomainsFromDb(self, layerList, loadedLayers, domainDict, multiColumnsDict):
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

    def loadDomains(self, layerList, loadedLayers, domainGroup):
        domLayerDict = dict()
        qmlPath = self.abstractDb.getQmlDir()
        qmlDict = self.utils.parseMultiQml(qmlPath, layerList)
        for lyr in layerList:
            for attr in qmlDict[lyr].keys():
                domain = qmlDict[lyr][attr]
                domLyr = self.checkLoaded(domain, loadedLayers)
                if not domLyr:
                    domLyr = self.loadDomain(domain, domainGroup)
                    loadedLayers.append(domLyr)
                domLyrName = domLyr.name()
                if lyr not in domLayerDict.keys():
                    domLayerDict[lyr] = dict()
                if attr not in domLayerDict[lyr].keys():
                    domLayerDict[lyr][attr] = domLyr
        return domLayerDict
    
    def loadDomain(self, domainTableName, domainGroup):
        uri = "dbname='%s' host=%s port=%s user='%s' password='%s' key=code table=\"dominios\".\"%s\" sql=" % (self.database, self.host, self.port, self.user, self.password, domainTableName)
        domLayer = iface.addVectorLayer(uri, domainTableName, self.provider)
        self.iface.legendInterface().moveLayer(domLayer, domainGroup)
        return domLayer

    def getStyleFromDb(self, edgvVersion, className):
        return self.abstractDb.getLyrStyle(edgvVersion,className)
    
    def isLoaded(self,lyr):
        return False

    def setDomainsAndRestrictions(self, lyr, lyrName, domainDict, multiColumnsDict, domLayerDict):
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
                            filter = '{0} in ({1})'.format(refPk,','.join(map(str,domainDict[lyrName]['columns'][attrName]['constraintList'])))
                            allowNull = domainDict[lyrName]['columns'][attrName]['nullable']
                            #make editDict
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
        if tableName in multiColumnsDict.keys():
            if attrName in multiColumnsDict[tableName]:
                return True
        return False
    
    def checkNotNull(self, lyrName, notNullDict):
        allowNull = True
        if lyrName in notNullDict.keys():
            if attrName in notNullDict[lyrName]['attributes']:
                allowNull = False
        return allowNull