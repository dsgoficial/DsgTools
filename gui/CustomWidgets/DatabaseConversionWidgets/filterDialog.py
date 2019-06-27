# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2019-06-27
        git sha              : $Format:%H$
        copyright            : (C) 2019 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
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

from qgis.core import QgsProject
from qgis.utils import iface
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'filterDialog.ui'))

class FilterDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """
        Class constructor.
        :param parent: (QtWidgets) any widget that should be parent to newly 
                       instantiated object.
        """
        super(FilterDialog, self).__init__(parent)
        self.setupUi(self)
        self.setupSpatialFilters()

    def layerNamesFromCanvas(self):
        """
        Gets all available layers from map canvas.
        :return: (list-of-str) map cointaing layer name to vector layer object.
        """
        return sorted([l.name() for l in iface.mapCanvas().layers()])

    def layerFromLayerName(self, layerName):
        """
        Gets vector layer object from its name.
        :param layerName: (str) 
        :return: (QgsVectorLayer) map cointaing layer name to vector layer object.
        """
        l = QgsProject.instance().mapLayersByName(layerName)
        return l[0] if l else None

    def fillSpatialFilterLayers(self):
        """
        Spatial filters are only applied considering layers currently loaded to
        map canvas.
        """
        self.spatialComboBox.clear()
        self.spatialComboBox.addItems(
            [self.tr("Select a layer...")] + self.layerNamesFromCanvas()
        )

    @pyqtSlot(int, name='on_spatialComboBox_currentIndexChanged')
    def setSpatialLayer(self):
        """
        Sets spatial layer to its filter expression widget.
        """
        self.mFieldExpressionWidget.setLayer(
            self.layerFromLayerName(self.spatialComboBox.currentText())
        )

    def fillPredicates(self):
        """
        Populates the combo box with all available predicates.
        """
        self.predicateComboBox.clear()
        self.predicateComboBox.addItems(
            sorted([self.tr('Clip'), self.tr('Buffer'), self.tr('Intersects')])
        )

    def fillClipOptions(self):
        """
        Clip options are given by choosing the area to be kept.
        """
        self.comboBox.clear()
        self.comboBox.addItems([
            self.tr('Choose a region...'),
            self.tr('Inside Features'),
            self.tr('Outside Features')
        ])

    @pyqtSlot(int, name='on_predicateComboBox_currentIndexChanged')
    def setPredicateWidget(self):
        """
        Sets the widget for capturing the topological relationship comparison parameter.
        :param idx: current topological operation index.
        """
        if self.predicateComboBox.currentText() == self.tr("Clip"):
            self.comboBox.show()
            self.doubleSpinBox.setValue(0)
            self.doubleSpinBox.hide()
        elif self.predicateComboBox.currentText() == self.tr("Buffer"):
            self.doubleSpinBox.show()
            self.comboBox.setCurrentIndex(0)
            self.comboBox.hide()
        else:
            self.comboBox.setCurrentIndex(0)
            self.comboBox.hide()
            self.doubleSpinBox.setValue(0)
            self.doubleSpinBox.hide()

    def setupSpatialFilters(self):
        """
        Sets up spatial filters to its intial state.
        """
        self.fillSpatialFilterLayers()
        self.fillPredicates()
        self.fillClipOptions()
        self.setPredicateWidget()