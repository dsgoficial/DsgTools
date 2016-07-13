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

class SpatialiteLayer(EDGVLayer):
    def __init__(self, abstractDb, codeList, table):
        """Constructor."""
        super(SpatialiteLayer, self).__init__(abstractDb, codeList)
        
        self.provider = 'spatialite'
        
        self.schema, self.layer_name = abstractDb.getTableSchema(table)
        
        try:
            dbVersion = abstractDb.getDatabaseVersion()
        except Exception as e:
            QgsMessageLog.logMessage(e.args[0], 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
            return
            
        if dbVersion == '3.0' or dbVersion == '2.1.3' or dbVersion == 'FTer_2a_Ed':
            self.qmlName = '_'.join(table.replace('\r', '').split('_')[1::])
        else:
            self.qmlName = table.replace('\r','')
            
        self.uri.setDatabase(abstractDb.db.databaseName())
        if self.layer_name[-1] == 'c':
            geomColumn = 'CENTROID'
        else:
            geomColumn = 'GEOMETRY'
        self.uri.setDataSource('', table, geomColumn)

    def checkLoaded(self, name):
        loadedLayers = iface.legendInterface().layers()
        loaded = None
        for ll in loadedLayers:
            if ll.name() == name:
                candidateUri = QgsDataSourceURI(ll.dataProvider().dataSourceUri())
                if database == candidateUri.database():
                    return ll
        return loaded

    def load(self, crs, idSubgrupo = None, uniqueLoad = False, useInheritance = False):
        if uniqueLoad:
            lyr = self.checkLoaded(self.layer_name)
            if lyr:
                return lyr
        qmldir = ''
        try:
            qmldir = self.abstractDb.getQmlDir()
        except Exception as e:
            self.problemOccurred.emit(self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(e.args[0], "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            return None

        vlayerQml = os.path.join(qmldir, self.qmlName+'.qml')

        database = self.abstractDb.db.databaseName()

        vlayer = iface.addVectorLayer(self.uri.uri(), self.layer_name, self.provider)
        if not vlayer:
            return None

        vlayer.setCrs(crs)
        if self.schema <> 'views':
            vlayer.loadNamedStyle(vlayerQml, False)
            attrList = vlayer.pendingFields()
            for field in attrList:
                i = vlayer.fieldNameIndex(field.name())
                if vlayer.editorWidgetV2(i) == 'ValueRelation':
                    groupList = iface.legendInterface().groups()
                    groupRelationshipList = iface.legendInterface().groupLayerRelationship()
                    filename = os.path.basename(database).split('.')[0]
                    if filename not in groupList:
                        idx = iface.legendInterface().addGroup(filename, True,-1)
                        domainIdGroup = iface.legendInterface().addGroup(self.tr("Dominios"), True, idx)
                    else:
                        idx = groupList.index(filename)
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
                            if database == candidateUri.database():
                                domainLoaded = True
                                domLayer = ll
                    if not domainLoaded:
                        uri = QgsDataSourceURI()
                        uri.setDatabase(database)
                        uri.setDataSource('', 'dominios_'+domainTableName, None)
                        #TODO Load domain layer into a group
                        domLayer = iface.addVectorLayer(uri.uri(), domainTableName, self.provider)
                        iface.legendInterface().moveLayer(domLayer, domainIdGroup)
                    valueRelationDict['Layer'] = domLayer.id()
                    vlayer.setEditorWidgetV2Config(i,valueRelationDict)
    
            self.qmlLoaded.emit()

        iface.legendInterface().moveLayer(vlayer, idSubgrupo)
            
        if not vlayer.isValid():
            QgsMessageLog.logMessage(vlayer.error().summary(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)

        return vlayer

    def loadDomainTable(self,name):
        pass