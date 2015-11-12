# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-11-10
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
from PyQt4.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt4.QtGui import QTableView

# QGIS imports
from qgis.core import QgsMapLayer, QgsDataSourceURI, QgsVectorLayerCache
from qgis.gui import QgsAttributeDialog, QgsAttributeTableModel, QgsAttributeTableView, QgsAttributeTableFilterModel

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'attributes_viewer.ui'))

class AttributesViewer(QtGui.QDockWidget, FORM_CLASS):
    def __init__(self, iface, parent = None):
        """Constructor."""
        super(AttributesViewer, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        self.iface = iface
        
        self.populateLayers()
        
    def populateLayers(self):
        self.layerCombo.clear()
        
        self.layerCombo.addItem(self.tr('Select a Layer'))
        
        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                self.layerCombo.addItem(layer.name())
        
    @pyqtSlot(int)
    def on_layerCombo_currentIndexChanged(self):
        if self.layerCombo.currentIndex() == 0:
            return
        
        currentLayerName = self.layerCombo.currentText()
        
        currentLayer = None
        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            if layer.name() == currentLayerName:
                currentLayer = layer
                break
            
        cache = QgsVectorLayerCache(currentLayer, 10)
        model = QgsAttributeTableModel(cache)
        model.loadLayer()
        
        self.tableView.setModel(model)