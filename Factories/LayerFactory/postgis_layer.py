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
    def __init__(self, abstractDb, codeList, table):
        """Constructor."""
        super(PostGISLayer, self).__init__(abstractDb, codeList)
        
        self.provider = 'postgres'
        
        self.schema, self.layer_name = abstractDb.getTableSchema(table)
        sql = abstractDb.gen.loadLayerFromDatabase(table)

        self.qmlName = self.layer_name.replace('\r','')

        host = abstractDb.db.hostName()
        port = abstractDb.db.port()
        database = abstractDb.db.databaseName()
        user = abstractDb.db.userName()
        password = abstractDb.db.password()
        
        self.uri.setConnection(str(host),str(port), str(database), str(user), str(password))
        if self.layer_name[-1] == 'c':
            geomColumn = 'centroid'
        else:
            geomColumn = 'geom'
        self.uri.setDataSource(self.schema, self.layer_name, geomColumn, sql, 'id')
        self.uri.disableSelectAtId(True)
    
    def loadDomainTable(self,name):
        pass
