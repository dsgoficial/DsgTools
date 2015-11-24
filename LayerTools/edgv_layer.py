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
from qgis.core import QgsMapLayerRegistry, QgsVectorLayer,QgsDataSourceURI
from qgis.utils import iface

class EDGVLayer(QObject):
    qmlLoaded = pyqtSignal()
    
    def __init__(self, codeList):
        """Constructor."""
        super(EDGVLayer, self).__init__()
        
        self.codeList = codeList
        self.qmlLoaded.connect(self.codeList.setState)

    def loadEDGVLayer(self, uri, layer_name, provider, crs, isSpatialite, dbVersion, qmlPath, idSubgrupo = None):
        vlayer = QgsVectorLayer(uri.uri(), layer_name, provider)
        vlayer.setCrs(crs)
        
        QgsMapLayerRegistry.instance().addMapLayer(vlayer) #added due to api changes
        
        if isSpatialite and (dbVersion == '3.0' or dbVersion == '2.1.3'):
            lyr = '_'.join(layer_name.replace('\r', '').split('_')[1::])
        else:
            lyr = layer_name.replace('\r','')
            
        vlayerQml = os.path.join(qmlPath, lyr+'.qml')
        vlayer.loadNamedStyle(vlayerQml, False)
        
        self.qmlLoaded.emit()
        
        QgsMapLayerRegistry.instance().addMapLayer(vlayer)
        
        if idSubgrupo:
            iface.legendInterface().moveLayer(vlayer, idSubgrupo)
            
        if not vlayer.isValid():
            QgsMessageLog.logMessage(vlayer.error().summary(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
