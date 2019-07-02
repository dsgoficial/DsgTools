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
from functools import partial

from qgis.core import QgsProject
from qgis.gui import QgsFieldExpressionWidget
from qgis.utils import iface
from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import QDialog, QCheckBox

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'filterDialog.ui'))

class FilterDialog(QDialog, FORM_CLASS):
    def __init__(self, spatialLayers, complexLayers, abstractDb, parent=None):
        """
        Class constructor.
        :param spatialLayers: (list-of-QgsVectorLayer) list of spatial layers.
        :param complexLayers: (list-of-QgsVectorLayer) list of complex layers.
        :param complexLayers: (AbstractDb) database object for data handling.
        :param parent: (QtWidgets) any widget that should be parent to newly 
                       instantiated object.
        """
        super(FilterDialog, self).__init__(parent)
        self.setupUi(self)
        self.spatialLayers = spatialLayers
        self.complexLayers = complexLayers
        self._currentSelection = dict()
        self._abstractDb = abstractDb
        self.setupSpatialFilters()
        self.setupLayerFilters()

    def filters(self):
        """
        Since current filter selection is stored in a protected attribute,
        this method is used to acces such filters.
        :return: (dict) a map to current filters applied.
        """
        return self._currentSelection

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

    def clearSelection(self):
        """
        Clears the dict to its initial state.
        """
        self._currentSelection = {}
        
    def setupLayerFilters(self):
        """
        Sets all layers to GUI.
        """
        self.setupGroupBoxFilters()
        if self.complexLayers:
            self.mGroupBox_2.show()
            self.setupGroupBoxFilters(isSpatial=False)
        else:
            self.mGroupBox_2.hide()
        self._currentSelection = self.readFilters()

    def fetchSpatialParameter(self, predicate):
        """
        Return the topological predicate's parameter.
        :param predicate: (str) target predicate.
        :return: (tuple) spatial filter settings.
        """
        return {
            self.tr('Clip') : self.comboBox.currentText() if self.comboBox.currentIndex() > 0 else None,
            self.tr('Buffer') : self.doubleSpinBox.value(),
            self.tr('Intersects') : None,
            '' : None
        }[predicate]

    def setPredicateParameter(self, predicate, parameter):
        """
        Sets given parameter to the GUI.
        :param predicate: (str) predicate to which the parameter refers to.
        :param parameter: (obj) parameter value to be filled. 
        """
        actionMap = {
            self.tr('Clip') : self.comboBox.setCurrentText,
            self.tr('Buffer') : self.doubleSpinBox.setValue,
            self.tr('Intersects') : lambda : None
        }
        return actionMap[predicate](parameter) if parameter in actionMap else None


    def setupGroupBoxFilters(self, isSpatial=True):
        """
        Sets up the part the spatial/complex layers' GUI part. It does not handle selection (e.g.
        everyone is selected).
        :param isSpatial: (bool) indicates whether groupbox to be set is spatial (or complex).
        """
        gb = self.mGroupBox if isSpatial else self.mGroupBox_2
        layers = self.spatialLayers if isSpatial else self.complexLayers
        layout = self.spatialGridLayout if isSpatial else self.complexGridLayout
        for row, (layerName, layerFcMap) in enumerate(layers.items()):
            checkBoxWidget, fieldExpressionWidget = QCheckBox(), QgsFieldExpressionWidget()
            _, layer = self._abstractDb.getTableSchema(layerName)
            checkBoxWidget.setChecked(True)
            # allow filtering option only when layer is marked to be filtered
            checkBoxWidget.toggled.connect(fieldExpressionWidget.setEnabled)
            checkBoxWidget.toggled.connect(partial(fieldExpressionWidget.setExpression, ""))
            msg = self.tr('{0} ({1} features)') if layerFcMap['featureCount'] > 1 else self.tr('{0} ({1} feature)')
            checkBoxWidget.setText(msg.format(layer, layerFcMap['featureCount']))
            fieldExpressionWidget.setLayer(layerFcMap['layer'])
            layout.addWidget(checkBoxWidget, row, 0)
            layout.addWidget(fieldExpressionWidget, row, 1)

    def validateSpatialFilter(self, layer, expression, predicate, parameter=None):
        """
        Validates current selection of spatial filters settings.
        :param layer: (str) layer (name) used as spatial reference.
        :param expression: (str) filtering expression applied to reference layer.
        :param predicate: (str) topological predicate to be applied to the dataset.
        :param parameter: (object) topological predicate's parameter.
        :return: (bool) whether the set of spatial filter settings may be applied to the dataset.
        """
        if predicate == self.tr("Clip"):
            return parameter is not None and parameter != self.tr('Choose a region...')
        elif predicate == self.tr("Buffer"):
            return parameter is not None
        return True

    def readFilters(self):
        """
        Read filters from the interface.
        :return: (dict) filters mapping.
        """
        layerFilters = dict()
        # read layer filtering options
        for layout in [self.spatialGridLayout, self.complexGridLayout]:
            for row in range(layout.rowCount()):
                if row == 0:
                    # for some reason the first row is behaving differently... 'Sem tempo, irmao'
                    checkBox = layout.itemAt(1)
                    if checkBox is not None:
                        checkBox = layout.itemAt(1).widget()
                else:
                    checkBox = layout.itemAtPosition(row, 0).widget()
                if checkBox is None or not checkBox.isChecked():
                    continue
                label = checkBox.text().replace('&', '') # still no idea why the '&' got in there...
                layer = label.split(' (')[0]
                fieldExpressionWidget = layout.itemAtPosition(row, 1).widget()
                layerFilters[layer] = dict()
                layerFilters[layer]['featureCount'] = int(label.split(' (')[1].split(' ')[0])
                layerFilters[layer]['expression'] = fieldExpressionWidget.currentText()
        # read spatial filtering options
        spatialFilters = dict()
        spatialFilters['layer'] = self.spatialComboBox.currentText() \
                                    if self.spatialComboBox.currentIndex() else ""
        spatialFilters['expression'] = self.mFieldExpressionWidget.currentText()
        spatialFilters['predicate'] = self.predicateComboBox.currentText()
        spatialFilters['parameter'] = self.fetchSpatialParameter(spatialFilters['predicate'])
        return {'layer_filter' : layerFilters, 'spatial_filter' : spatialFilters}

    def resetSelection(self):
        """
        Resets layer selection to last state preserved into the private attribute holding current
        layer selection.
        """
        prevLayerFilter = self._currentSelection['layer_filter']
        for layout in [self.spatialGridLayout, self.complexGridLayout]:
            for row in range(layout.rowCount()):
                if row == 0:
                    # for some reason the first row is behaving differently... 'Sem tempo, irmao'
                    checkBox = layout.itemAt(1)
                    if checkBox is not None:
                        checkBox = layout.itemAt(1).widget()
                else:
                    checkBox = layout.itemAtPosition(row, 0).widget()
                if not checkBox:
                    continue
                fieldExpressionWidget = layout.itemAtPosition(row, 1).widget()
                label = checkBox.text().replace('&', '') # still no idea why the '&' got in there...
                layer = label.split(' (')[0]
                checkBox.setChecked(layer in prevLayerFilter)
                exp = prevLayerFilter[layer]['expression'] if layer in prevLayerFilter else ""
                fieldExpressionWidget.setExpression(exp)
        # reset spatial filters
        self.spatialComboBox.setCurrentText(self._currentSelection['spatial_filter']['layer'])
        self.mFieldExpressionWidget.setExpression(self._currentSelection['spatial_filter']['expression'])
        self.predicateComboBox.setCurrentText(self._currentSelection['spatial_filter']['predicate'])
        self.setPredicateParameter(
            self._currentSelection['spatial_filter']['predicate'],
            self._currentSelection['spatial_filter']['parameter']
        )

    def on_okPushButton_clicked(self):
        """
        Closes the dialog and informs the exit code. And save current selection.
        :return: (int) exit code.
        """
        self._currentSelection = self.readFilters()
        self.close()
        return 0

    def on_cancelPushButton_clicked(self):
        """
        Closes the dialog and informs the exit code. Selection is restored.
        :return: (int) exit code.
        """
        self.resetSelection()
        self.close()
        return 1
