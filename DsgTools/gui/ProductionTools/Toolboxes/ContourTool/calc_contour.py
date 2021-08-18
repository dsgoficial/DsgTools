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
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QMessageBox

# QGIS imports
from qgis.core import QgsVectorLayer, QgsGeometry, Qgis, QgsProject, QgsWkbTypes

#DSGTools imports
from DsgTools.gui.ProductionTools.Toolboxes.ContourTool.dsg_line_tool import DsgLineTool
from DsgTools.gui.ProductionTools.Toolboxes.ContourTool.contour_tool import ContourTool

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'calc_contour.ui'))

class CalcContour(QtWidgets.QDockWidget, FORM_CLASS):
    def __init__(self, iface, parent = None):
        """
        Constructor
        """
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
        QgsProject.instance().layersAdded.connect(self.addLayers)
        QgsProject.instance().layersRemoved.connect(self.populateLayers)

    @pyqtSlot(bool, name = 'on_reactivatePushButton_clicked')
    def activateTool(self):
        """
        Sets this tool as the current active qgis tool
        """

        self.tool.reset()
        self.iface.mapCanvas().setMapTool(self.tool)

    def addLayers(self, layers):
        """
        Add layer in the layer combo box
        layers: layer to be added
        """
        for layer in layers:
            if isinstance(layer, QgsVectorLayer):
                self.layerCombo.addItem(layer.name())

    def populateLayers(self):
        """
        Populates the layer combo box
        """
        self.layerCombo.clear()
        
        self.layerCombo.addItem(self.tr('Select a Layer'))
        
        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            if isinstance(layer, QgsVectorLayer) and layer.geometryType() == QgsWkbTypes.LineGeometry:
                self.layerCombo.addItem(layer.name())

    def getLayer(self):
        """
        Gets the leayer selected in the combo box
        """
        currentLayerName = self.layerCombo.currentText()

        layers = self.iface.mapCanvas().layers()
        for layer in layers:
            if layer.name() == currentLayerName:
                return layer

        return None

    @pyqtSlot(QgsGeometry)
    def updateLayer(self, geom):
        """
        Updates the layer
        """
        if self.layerCombo.currentIndex() == 0:
            self.iface.messageBar().pushMessage(self.tr('Information'), self.tr('A layer must be selected!'), level=Qgis.Info, duration=3)
            return

        if self.attributeCombo.currentIndex() == 0:
            self.iface.messageBar().pushMessage(self.tr('Information'), self.tr('A field must be selected!'), level=Qgis.Info, duration=3)
            return

        #canvas crs to be used in case a reprojection is needed
        canvasCrs = self.iface.mapCanvas().mapSettings().destinationCrs()
        if self.ascendingRadioButton.isChecked():
            signal = 1
        else:
            signal = -1
        ret = self.contourTool.assignValues(self.attributeCombo.currentText(), signal*self.spinBox.value(), geom, canvasCrs)
        self.iface.mapCanvas().refresh()
        if ret == 1:
            self.iface.messageBar().pushMessage(self.tr('Information!'), self.tr('Layer successfully updated!'), level=Qgis.Info, duration=3)
        elif ret == 0:
            self.iface.messageBar().pushMessage(self.tr('Critical!'), self.tr('Could not update features!'), level=Qgis.Critical, duration=3)
        elif ret == -1:
            self.iface.messageBar().pushMessage(self.tr('Critical!'), self.tr('Problem ordering the features!'), level=Qgis.Critical, duration=3)
        elif ret == -2:
            self.iface.messageBar().pushMessage(self.tr('Critical!'), self.tr('The line created does not cross any features in the selected layer!'), level=Qgis.Critical, duration=3)
        elif ret == -3:
            self.iface.messageBar().pushMessage(self.tr('Critical!'), self.tr('Assign a value for the selected attribute of the first crossed feature!'), level=Qgis.Critical, duration=3)

    @pyqtSlot(int)
    def on_layerCombo_currentIndexChanged(self):
        """
        Slot to update the layer when the current index changes in the layer combo
        """
        if self.layerCombo.currentIndex() == 0:
            return
        
        currentLayer = self.getLayer()
        if not currentLayer:
            return

        #updating the reference layer
        self.contourTool.updateReference(self.getLayer())

        fields = currentLayer.fields()
        field_names = [field.name() for field in fields]
        self.attributeCombo.clear()
        self.attributeCombo.addItem('Select a field')
        self.attributeCombo.addItems(field_names)