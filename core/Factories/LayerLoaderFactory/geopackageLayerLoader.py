# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-10-24
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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
from qgis.PyQt.Qt import QObject

# QGIS imports
from qgis.core import QgsVectorLayer,QgsDataSourceUri, QgsMessageLog, QgsCoordinateReferenceSystem, QgsMessageLog, Qgis, QgsProject, QgsEditorWidgetSetup
from qgis.utils import iface

#DsgTools imports
from .spatialiteLayerLoader import SpatialiteLayerLoader
from ....gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget

class GeopackageLayerLoader(SpatialiteLayerLoader):
    def __init__(self, iface, abstractDb, loadCentroids):
        """Constructor."""
        super(GeopackageLayerLoader, self).__init__(iface, abstractDb, loadCentroids)
        
        self.provider = 'geopackage'
        
        try:
            dbVersion = abstractDb.getDatabaseVersion()
        except Exception as e:
            QgsMessageLog.logMessage(':'.join(e.args), 'DSG Tools Plugin', Qgis.Critical)
            return

        self.buildUri()
