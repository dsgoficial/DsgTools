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

    def checkLoaded(self, name):
        loadedLayers = iface.legendInterface().layers()
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
    
    def getDatabaseGroup(self):
        dbName = self.abstractDb.getDatabaseName()
        groupList =  qgis.utils.iface.legendInterface().groups()
        if dbName in groupList:
            return groupList.index(dbName)
        else:
            return self.iface.legendInterface().addGroup(dbName, -1)
    
    def createGroups(self):
        pass

    def load(self, layerList, useQml = False, idSubgrupo = None, uniqueLoad = False, useInheritance = False, stylePath = None, groupByGeom = True):
        '''
        1. Load domains;
        2. Load Layers;
        '''
        dbGroup = self.getDatabaseGroup()

        if self.schema <> 'views':
            vlayer.loadNamedStyle(vlayerQml, False)
            attrList = vlayer.pendingFields()
            for field in attrList:
                i = vlayer.fieldNameIndex(field.name())
                if vlayer.editorWidgetV2(i) == 'ValueRelation':
                    groupList = iface.legendInterface().groups()
                    groupRelationshipList = iface.legendInterface().groupLayerRelationship()
                    if database not in groupList:
                        idx = iface.legendInterface().addGroup(database, True,-1)
                        domainIdGroup = iface.legendInterface().addGroup(self.tr("Dominios"), True, idx)
                    else:
                        idx = groupList.index(database)
                        if "Dominios" not in groupList[idx::]:
                            domainIdGroup = iface.legendInterface().addGroup(self.tr("Dominios"), True, idx)
                        else:
                            domainIdGroup = groupList[idx::].index("Dominios")
    
                    valueRelationDict = vlayer.editorWidgetV2Config(i)
                    domainTableName = valueRelationDict['Layer']
                    loadedLayers = iface.legendInterface().layers()
                    domainLoaded = False
                    for ll in loadedLayers:
                        if ll.name() == domainTableName:
                            candidateUri = QgsDataSourceURI(ll.dataProvider().dataSourceUri())
                            if host == candidateUri.host() and database == candidateUri.database() and port == int(candidateUri.port()):
                                domainLoaded = True
                                domLayer = ll
                    if not domainLoaded:
                        uri = "dbname='%s' host=%s port=%s user='%s' password='%s' key=code table=\"dominios\".\"%s\" sql=" % (database, host, port, user, password, domainTableName)
                        #TODO Load domain layer into a group
                        domLayer = iface.addVectorLayer(uri, domainTableName, self.provider)
                        iface.legendInterface().moveLayer(domLayer, domainIdGroup)
                    valueRelationDict['Layer'] = domLayer.id()
                    vlayer.setEditorWidgetV2Config(i,valueRelationDict)
            self.qmlLoaded.emit()
        
        if stylePath:
            fullPath = self.getStyle(stylePath, self.qmlName)
            if fullPath:
                vlayer.applyNamedStyle(fullPath)

        iface.legendInterface().moveLayer(vlayer, idSubgrupo)
            
        if not vlayer.isValid():
            QgsMessageLog.logMessage(vlayer.error().summary(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        vlayer = self.createMeasureColumn(vlayer)
        return vlayer

    def loadLayer(self, lyrName, uniqueLoad = False, useInheritance = False, stylePath = None):
        if uniqueLoad:
            lyr = self.checkLoaded(self.layer_name)
            if lyr:
                return lyr
        if useInheritance:
            self.uri.setSql('')
        qmldir = ''
        try:
            qmldir = self.abstractDb.getQmlDir()
        except Exception as e:
            self.problemOccurred.emit(self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(e.args[0], "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return None
        vlayerQml = os.path.join(qmldir, self.qmlName+'.qml')
        vlayer = iface.addVectorLayer(self.uri.uri(), self.layer_name, self.provider)
        vlayer.setCrs(crs)
        pass

    def loadDomainTable(self,name):
        pass

    def getStyleFromDb(self, edgvVersion, className):
        return self.abstractDb.getLyrStyle(edgvVersion,className)
    
    def isLoaded(self,lyr):
        return False

    def getDomainValuesFromDb(self, lyrName):
        pass
    