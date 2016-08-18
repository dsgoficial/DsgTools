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
from DsgTools.Factories.LayerFactory.edgv_layer import EDGVLayer

class PostGISLayer(EDGVLayer):
    def __init__(self, iface, abstractDb, codeList, table=None):
        """Constructor."""
        super(PostGISLayer, self).__init__(iface, bstractDb, codeList)
        
        self.provider = 'postgres'
#         self.qmlName = layer.replace('\r','')
        self.setDatabaseConnection()
        self.setDataSource(schema, layer, geomColumn, sql)
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
        if groupName in groupList:
            return groupList.index(groupName)
        else:
            return self.iface.legendInterface().addGroup(groupName, parent)
    
    def getLyrDict(self, lyrList):
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
                groupDict[geomNode][catNode] = self.createGroup(groupList, catNode, geomNode)
        return groupDict
    
    def createGroup(self, groupList, groupName, parent):
        if groupName in groupList:
            return groupList.index(groupName) #verificar
        else:
            return self.iface.legendInterface().addGroup(groupName, parent)
    
    def filterLayerList(self, layerList, useInheritance, onlyWithElements):
        filterList = []
        if onlyWithElements:
            lyrsWithElements = self.abstractDb.getLayersWithElements(layerList)
        else:
            lyrsWithElements = layerList
        if useInheritance:
            finalList = self.abstractDb.getLayersFilterByInheritance(lyrsWithElements)
        else:
            finalList = layerList
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
        #TODO: load only domains of multi
        dbGroup = self.getDatabaseGroup(loadedGroups)
        domainGroup = self.createGroup(loadedGroups, self.tr("Domains"), dbGroup)
        domLayerDict = self.loadDomains(filteredLayerList, loadedLayers, domainGroup)
        #3. Get Aux dicts
        geomDict = self.abstractDb.getGeomDict()
        domainDict = self.abstractDb.getDbDomainDict()
        constraintDict = self.abstractDb.getCheckConstraintDict()
        multiColumnsDict = self.abstractDb.getMultiColumnsDict()
        notNullDict = self.abstractDb.getNotNullDictV2()
        lyrDict = self.getLyrDict(filteredLayerList)
        #4. Build Groups
        groupDict = self.prepareGroups(loadedGroups, dbGroup, filteredLayerList)
        #5. load layers
        for prim in lyrDict.keys():
            for cat in lyrDict[prim].keys():
                self.loadLayer(lyrDict[prim][cat],groupDict[prim][cat], useInheritance, useQml,uniqueLoad,stylePath,geomDict,domainDict,constraintDict,multiColumnsDict,notNullDict,domLayerDict)
        self.qmlLoaded.emit()


    def loadLayer(self, lyrName, idSubgrupo, useInheritance, useQml, uniqueLoad,stylePath,geomDict,domainDict,constraintDict,multiColumnsDict, notNullDict, domLayerDict):
        if uniqueLoad:
            lyr = self.checkLoaded(lyrName)
            if lyr:
                return lyr
        if useInheritance:
            sql = ''
        schema = geomDict['tablePerspective'][lyrName]['schema']
        geomColumn = geomDict['tablePerspective'][lyrName]['geometryColumn']
        crs =  geomDict['tablePerspective'][lyrName]['srid']
        sql = self.abstractDb.gen.loadLayerFromDatabase(schema+'.'+lyrName)
        self.setDataSource(schema, layer, geomColumn, sql)

        vlayer = iface.addVectorLayer(self.uri.uri(), lyrName, self.provider)
        vlayer.setCrs(crs)
        if useQml:
            vlayer = self.setDomainsAndRestrictionsWithQml(vlayer)
        else:
            vlayer = self.setDomainsAndRestrictions(vlayer, lyrName, domainDict, constraintDict, multiColumnsDict, domLayerDict)
        if stylePath:
            fullPath = self.getStyle(stylePath, self.qmlName)
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
        vlayerQml = os.path.join(qmldir, self.qmlName+'.qml')
        #treat case of qml with multi
        vlayer.loadNamedStyle(vlayerQml, False)
        return vlayer

    def getDomainsFromDb(self, layerList, loadedLayers, multiColumnsDict):
        domainDict = self.abstractDb.getDomainDictV2()
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

    def getDomainsToBeLoaded(self, layerList, loadedLayers, multiColumnsDict):
        domains = self.getDomainsFromDb(layerList, loadedLayers, multiColumnsDict)
        loadedDomains = []
        for domain in domains:
            domLyr = self.checkLoaded(domain, loadedLayers)
            if domLyr:
                loadedDomains.append(domLyr.name())
        domainsToBeLoaded = []
        for domain in domains:
            if domain not in loadedDomains:
                domainsToBeLoaded.append(domain)
        return domainsToBeLoaded

    def loadDomains(self, layerList, loadedLayers, domainGroup):
        domainsToBeLoaded = self.getDomainsToBeLoaded(layerList, loadedLayers)
        domainsToBeLoaded.sort(reverse=True)
        domLayerDict = dict()
        for domainTableName in domainsToBeLoaded:
            uri = "dbname='%s' host=%s port=%s user='%s' password='%s' key=code table=\"dominios\".\"%s\" sql=" % (self.database, self.host, self.port, self.user, self.password, domainTableName)
            domLayer = iface.addVectorLayer(uri, domainTableName, self.provider)
            domLayerDict[domainTableName] = domLayer
            iface.legendInterface().moveLayer(domLayer, domainIdGroup)
        return domLayerDict

    def getStyleFromDb(self, edgvVersion, className):
        return self.abstractDb.getLyrStyle(edgvVersion,className)
    
    def isLoaded(self,lyr):
        return False

    def setDomainsAndRestrictions(self, lyr, lyrName, domainDict, constraintDict, multiColumnsDict, notNullDict, domLayerDict):
        lyrAttributes = lyr.pendingFields()
        constraintKeys = constraintDict.keys()
        #TODO: UPDATE code with new dict from getDbDomainDict
        for i in len(lyrAttributes):
            attrName = lyrAttributes[i].name()
            if attrName == 'id' or 'id_' in lyrAttributes[i]:
                lyr.setFieldEditable(i,False)
            else:
                if lyrName in domainDict.keys():
                    if attrName in domainDict[lyrName]['columns'].keys():
                        refTable = domainDict[lyrName]['columns'][attr]['references']
                        refPk = domainDict[lyrName]['columns'][attr]['refPk']
                        otherKey = domainDict[lyrName]['columns'][attr]['otherKey']
                        valueDict = domainDict[lyrName]['columns'][attr]['values']
                        #TODO: treat both cases: Value Relation and Value Map
                        #TODO: implement checkMulti
                        isMulti = self.checkMulti(tableName, attrName, multiColumnsDict, domainDict)
                        allowNull = self.checkNotNull(tableName, attrName, notNullDict)
                        if isMulti:
                            #Do value relation
                            
                            #make filter
                            
                            #make editDict
                            editDict = {'Layer':dom.id(),'Key':refPk,'Value':otherKey,'AllowMulti':True,'AllowNull':allowNull}
                            pass
                        else:
                            #Value Map
                            lyr.setEditorWidgetV2(i,'ValueMap')
                            #filter value dict
                            if lyrName in constraintDict.keys():
                                if attrName in constraintDict[lyrName].keys():
                                    for filterValue in constraintDict[lyrName][attrName]:
                                        valueDict.pop(filterValue)
                            #check if not null
                            lyr.setEditorWidgetV2Config(i,valueDict)
                        #setEditorWidgetV2Config is deprecated. We will change it eventually.
                                        
                        
        return lyr

    def checkMulti(self, tableName, attrName, multiColumnsDict, domainDict):
        #TODO: Implement
        pass
    
    def checkNotNull(self, lyrName, notNullDict):
        allowNull = True
        if lyrName in notNullDict.keys():
            if attrName in notNullDict[lyrName]['attributes']:
                allowNull = False
        return allowNull