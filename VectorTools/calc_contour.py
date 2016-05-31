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
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtGui import QMessageBox

# QGIS imports
from qgis.core import QgsMapLayer, QgsGeometry, QgsMapLayerRegistry
from qgis.gui import QgsMessageBar

#DSGTools imports
from DsgTools.VectorTools.dsg_line_tool import DsgLineTool
from DsgTools.VectorTools.contour_tool import ContourTool

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'calc_contour.ui'))

class CalcContour(QtGui.QDockWidget, FORM_CLASS):
    def __init__(self, iface, parent = None):
        """Constructor."""
        super(CalcContour, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        self.iface = iface

        #insert layers into the combobox
        self.populateLayers()

        #instance of the QgsMapTool derived class (line tool)
        self.tool = DsgLineTool(self.iface.mapCanvas())
        self.tool.lineCreated.connect(self.updateLayer)

        #instance of the class responsible to update layer features
        self.contourTool = ContourTool()

        #Connecting slot to deal with adition/removal of layers
        QgsMapLayerRegistry.instance().layersAdded.connect(self.addLayers)
        QgsMapLayerRegistry.instance().layersRemoved.connect(self.populateLayers)

    def activateTool(self):
        self.tool.reset()
        self.iface.mapCanvas().setMapTool(self.tool)

    def addLayers(self, layers):
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                self.layerCombo.addItem(layer.name())

    def populateLayers(self):
        self.layerCombo.clear()
        
        self.layerCombo.addItem(self.tr('Select a Layer'))
        
        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:
                self.layerCombo.addItem(layer.name())

    def getLayer(self):
        currentLayerName = self.layerCombo.currentText()

        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            if layer.name() == currentLayerName:
                return layer

        return None

    @pyqtSlot(QgsGeometry)
    def updateLayer(self, geom):
        if self.layerCombo.currentIndex() == 0:
            QMessageBox.information(None, self.tr('Information'), self.tr('A layer must be selected!'))
            return

        if self.attributeCombo.currentIndex() == 0:
            QMessageBox.information(None, self.tr('Information'), self.tr('A field must be selected!'))
            return

        #canvas crs to be used in case a reprojection is needed
        canvasCrs = self.iface.mapCanvas().mapRenderer().destinationCrs()
        ret = self.contourTool.assignValues(self.attributeCombo.currentText(), self.spinBox.value(), geom, canvasCrs)
        if ret == 1:
            self.iface.messageBar().pushMessage(self.tr('Information!'), self.tr('Layer successfully updated!'), level=QgsMessageBar.INFO, duration=3)
        elif ret == 0:
            self.iface.messageBar().pushMessage(self.tr('Critical!'), self.tr('Could not update features!'), level=QgsMessageBar.CRITICAL, duration=3)
        elif ret == -1:
            self.iface.messageBar().pushMessage(self.tr('Critical!'), self.tr('Problem ordering the features!'), level=QgsMessageBar.CRITICAL, duration=3)
        elif ret == -2:
            self.iface.messageBar().pushMessage(self.tr('Critical!'), self.tr('The line created does not cross any features in the selected layer!'), level=QgsMessageBar.CRITICAL, duration=3)
        
    @pyqtSlot(int)
    def on_layerCombo_currentIndexChanged(self):
        if self.layerCombo.currentIndex() == 0:
            return
        
        currentLayer = self.getLayer()
        if not currentLayer:
            return

        #updating the reference layer
        self.contourTool.updateReference(self.getLayer())

        fields = currentLayer.pendingFields()
        field_names = [field.name() for field in fields]
        self.attributeCombo.clear()
        self.attributeCombo.addItem('Select a field')
        self.attributeCombo.addItems(field_names)