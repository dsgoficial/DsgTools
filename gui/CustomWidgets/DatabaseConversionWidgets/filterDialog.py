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
    def __init__(self, spatialLayers, complexLayers, parent=None):
        """
        Class constructor.
        :param spatialLayers: (list-of-QgsVectorLayer) list of spatial layers.
        :param complexLayers: (list-of-QgsVectorLayer) list of complex layers.
        :param parent: (QtWidgets) any widget that should be parent to newly 
                       instantiated object.
        """
        super(FilterDialog, self).__init__(parent)
        self.setupUi(self)
        self.spatialLayers = spatialLayers
        self.complexLayers = complexLayers
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
    def setSpatialFilterLayer(self):
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
    
    def setupLayerFilters(self):
        """
        Sets all layers to GUI.
        """
        self.setupGroupBoxFilters()
        if self.complexLayers:
            # in case complex layers are provided
            self.setupGroupBoxFilters(isSpatial=False)

    def setupGroupBoxFilters(self, isSpatial=True):
        """
        Sets up the part the sptial/complex layers' GUI part.
        :param isSpatial: (bool) indicates whether groupbox to be set is spatial (or complex).
        """
        gb = self.mGroupBox if isSpatial else self.mGroupBox_2
        layers = self.spatialLayers if isSpatial else self.complexLayers
        # self.filterDlg.vLayout.addWidget(gb)
        # # add a grid layout to add the widgets
        # layout = QtWidgets.QGridLayout(gb)
        # # gb.addLayout(layout)
        # # initiate row counter
        # row = 0
        # # eliminate schema from layer name
        # abstractDb = self.connectionWidget.getDatasource()
        # for layerName, featCount in layers.items():
        #     if layerName:
        #         # add a new checkbox widget to layout for each layer found and a field expression widget
        #         checkBoxWidget, fieldExpressionWidget = QtWidgets.QCheckBox(), QgsFieldExpressionWidget()
        #         # set current check box status based on previous filters, if any
        #         # eliminate schema from layer name
        #         _, layer = abstractDb.getTableSchema(layerName)
        #         previousFilters = not self.filters['layer'] or layer in self.filters['layer']
        #         checkBoxWidget.setChecked(previousFilters)
        #         # allow filtering option only when layer is marked to be filtered
        #         checkBoxWidget.toggled.connect(fieldExpressionWidget.setEnabled)
        #         msg = self.tr('{0} ({1} features)') if featCount > 1 else self.tr('{0} ({1} feature)')
        #         checkBoxWidget.setText(msg.format(layerName, featCount))
        #         if previousFilters:
        #             # if layer is among the filtered ones, or if there are no previous filters, set it checked.__init__(self, *args, **kwargs):
        #             checkBoxWidget.setChecked(True)
        #             # in case no filters are added or if layer is among the filtered ones, set it checked
        #         if layerName in self.filters['layer_filter']:
        #             # if a layer feature filter was set, refill it back to UI
        #             fieldExpressionWidget.setExpression(self.filters['layer_filter'][layerName])
        #         # set layer to filter expression
        #         layer = getLayerAlias(layerName)
        #         if layer is not None and layer.isValid():
        #             fieldExpressionWidget.setLayer(layer)
        #         else:
        #             checkBoxWidget.toggled.disconnect(fieldExpressionWidget.setEnabled)
        #             fieldExpressionWidget.setEnabled(False)
        #         layout.addWidget(checkBoxWidget, row, 0)
        #         layout.addWidget(fieldExpressionWidget, row, 1)
        #         row += 1