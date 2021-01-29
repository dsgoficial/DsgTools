# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2020-07-27
        git sha              : $Format:%H$
        copyright            : (C) 2020 by  Francisco Alves Camello Neto -
                                    Surveying Technician @ Brazilian Army
        email                : camello.francisco@eb.mil.br
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
from qgis.core import QgsProject
from qgis.gui import QgsMapLayerComboBox, QgsFieldComboBox
from qgis.PyQt import QtCore, QtGui, QtWidgets, uic
from qgis.PyQt.QtCore import Qt, pyqtSlot
from qgis.PyQt.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'layerAndFieldSelectorWidget.ui'))


class LayerAndFieldSelectorWidget(QtWidgets.QWidget, FORM_CLASS):
    """Docstring."""

    mMapLayerComboBox = QgsMapLayerComboBox()
    mFieldComboBox = QgsFieldComboBox()

    def __init__(self, parent=None):
        """Constructor."""
        super(LayerAndFieldSelectorWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.getLoadedLayers()
        self.setLayer()
        self.mMapLayerComboBox.layerChanged.connect(lambda: self.setLayer())

    def getLoadedLayers(self):
        """Docstring."""
        self.lyr_list = [layer.name()
                         for layer in QgsProject.instance().mapLayers().values()]
        return self.lyr_list

    def getCurrentLayer(self):
        """Docstring."""
        return self.mMapLayerComboBox.currentLayer()

    def getCurrentField(self):
        """Docstring."""
        return self.mFieldComboBox.currentField()

    def setLayer(self):
        """Docstring."""
        # first setup is manual though
        lyr = self.mMapLayerComboBox.currentLayer()
        if lyr:
            self.mFieldComboBox.setLayer(lyr)
            self.mFieldComboBox.setField(lyr.fields()[0].name())

    def setField(self, field):
        """Docstring."""
        return self.mFieldComboBox.setField(field)

    def fieldChanged(self, request):
        """Docstring."""
        return self.mFieldComboBox.fieldChanged.connect(request)

    def layerChanged(self, request):
        """Docstring."""
        return self.mMapLayerComboBox.layerChanged.connect(request)

    def getCurrentLayerNField(self):
        """Docstring."""
        lyr = self.mMapLayerComboBox.currentLayer().name()
        fld = self.mFieldComboBox.currentField()
        return lyr, fld

    def setCurrentLayerNField(self, _list):
        """Docstring."""
        self.mMapLayerComboBox.setCurrentText(_list[0])
        lyr = self.mMapLayerComboBox.currentLayer()
        fld = self.mFieldComboBox
        if _list[0] in self.lyr_list:
            lyrFldList = [field.name() for field in lyr.fields()]
            if _list[1] in lyrFldList:
                fld.setLayer(lyr)
                fld.setField(_list[1])
        return lyr, fld
