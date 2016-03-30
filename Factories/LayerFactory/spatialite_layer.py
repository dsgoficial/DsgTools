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
        
        dbVersion = abstractDb.getDatabaseVersion()
        if dbVersion == 'FTer_2a_Ed' or dbVersion == '2.1.3':
            self.qmlName = '_'.join(table.replace('\r', '').split('_')[1::])
        else:
            self.qmlName = table.replace('\r','')
            
        self.uri.setDatabase(abstractDb.db.databaseName())
        self.uri.setDataSource('', table, 'GEOMETRY')

    def loadDomainTable(self,name):
        pass