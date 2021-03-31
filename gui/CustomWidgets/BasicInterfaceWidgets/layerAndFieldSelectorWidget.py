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
from qgis.PyQt import QtCore, QtWidgets, uic
from qgis.PyQt.QtCore import QSize
from qgis.PyQt.QtWidgets import QWidget

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'layerAndFieldSelectorWidget.ui'))


class LayerAndFieldSelectorWidget(QWidget, FORM_CLASS):
    """
    Widget to get a field from a loaded layer. It was necessary to develop
    a custom widget to use when the attribute rules are imported because
    of the OTW's behavior.
    """

    mMapLayerComboBox = QgsMapLayerComboBox()
    mFieldComboBox = QgsFieldComboBox()

    def __init__(self, parent=None):
        """
        Constructor.
        """
        super(LayerAndFieldSelectorWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.widgetSizeHint()
        self.project = QgsProject.instance()
        self.getLoadedLayers()
        self.setLayer()
        self.mMapLayerComboBox.layerChanged.connect(self.setLayer)

    def getLoadedLayers(self):
        """
        Retrieves a loaded layers list.
        :return lyrList: (list) a string list for layers' names.
        """
        lyrList = [layer.name()
                   for layer in self.project.mapLayers().values()]
        return lyrList

    def getCurrentLayer(self):
        """
        Gets the current layer from a QgsMapLayerComboBox.
        :return: (QgsVectorLayer) returns the current layer selected
            in the combo box.
        """
        return self.mMapLayerComboBox.currentLayer()

    def getCurrentField(self):
        """
        Gets the current field related to the current layer
            from a QgsFieldComboBox.
        :return: (QgsField): returns the currently selected field.
        """
        return self.mFieldComboBox.currentField()

    def setLayer(self):
        """
        Sets a layer to be used with OTW.
        :return: (QgsVectorLayer): returns the currently set layer.
        """
        # first setup is manual though
        lyr = self.getCurrentLayer()
        if lyr:
            self.mFieldComboBox.setLayer(lyr)
            self.setField(lyr.fields()[0].name())

    def setField(self, field):
        """
        Sets the currently selected field to be used with OTW.
        :param field: (str) a string for the field' name;
        :return: (QgsField): returns the currently set field.
        """
        return self.mFieldComboBox.setField(field)

    def fieldChanged(self, request):
        """
        Signal emmited when a field is changed.
        :param request: (function) request for the signal's receiver;
        :return: (signal) a fieldChanged emitted signal.
        """
        return self.mFieldComboBox.fieldChanged.connect(request)

    def layerChanged(self, request):
        """
        Signal emmited when a layer is changed.
        :param request: (function) request for the signal's receiver.
        :return: (signal) a layerChanged emitted signal.
        """
        return self.mMapLayerComboBox.layerChanged.connect(request)

    def getCurrentLayerNField(self):
        """
        Retrieves a tuple of layer and field.
        :return: (QgsField): returns the currently set field.
        """
        lyr = self.mMapLayerComboBox.currentLayer().name()
        fld = self.mFieldComboBox.currentField()
        return lyr, fld

    def setCurrentLayerNField(self, layerFieldList):
        """
        Sets the current field related to the current
        layer to be used with OTW.
        :param layerFieldList: (list) list of layers' and fields' names
            respectively.
        """
        self.mMapLayerComboBox.setCurrentText(layerFieldList[0])
        lyr = self.getCurrentLayer()
        lyrList = self.getLoadedLayers()
        if layerFieldList[0] in lyrList:
            lyrFldList = [field.name() for field in lyr.fields()]
            if layerFieldList[1] in lyrFldList:
                self.mFieldComboBox.setLayer(lyr)
                self.setField(layerFieldList[1])

    def widgetSizeHint(self):
        """
        Sets the minimum size for the composed widget to fit it with
        the OTW's resize policies.
        """
        mMapLayerComboBoxSize = self.mMapLayerComboBox.size()
        mFieldComboBoxSize = self.mFieldComboBox.size()
        minW = mMapLayerComboBoxSize.width() + mFieldComboBoxSize.width() + 5
        minH = (mMapLayerComboBoxSize.height() +
                mFieldComboBoxSize.height()) // 2
        self.setMinimumSize(QSize(minW, minH))
