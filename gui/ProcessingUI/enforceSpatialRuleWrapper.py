# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-11-14
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

from qgis.core import QgsVectorLayer, QgsMapLayerProxyModel
from qgis.gui import QgsMapLayerComboBox, QgsFieldExpressionWidget
from qgis.PyQt.QtWidgets import (QComboBox,
                                 QLineEdit)
from processing.gui.wrappers import (WidgetWrapper,
                                     DIALOG_STANDARD,
                                     DIALOG_MODELER,
                                     DIALOG_BATCH)

from DsgTools.gui.CustomWidgets.OrderedPropertyWidgets.orderedTableWidget import OrderedTableWidget

class EnforceSpatialRuleWrapper(WidgetWrapper):
    def __init__(self, *args, **kwargs):
        super(EnforceSpatialRuleWrapper, self).__init__(*args, **kwargs)

    def mapLayerComboBox(self):
        """
        Retrieves the configured map layer selection combo box.
        :return: (QgsMapLayerComboBox) configured layer selection widget. 
        """
        cb = QgsMapLayerComboBox()
        cb.setFilters(QgsMapLayerProxyModel.VectorLayer)
        return cb

    def mapLayerModelDialog(self):
        """
        Retrieves widget for map layer selection in a model dialog setup.
        :return: (QLineEdit) map layer setter widget for processing dialog
                 mode.
        """
        le = QLineEdit()
        le.setPlaceholderText(self.tr("Set layer name..."))
        return le

    def filterExpressionWidget(self, layer=None):
        """
        Retrieves a new widget for filtering expression setting.
        :param layer: (QgsVectorLayer) vector layer on which filter should be
                      applied to.
        :return: (QgsFieldExpressionWidget) snap mode selection widget.
        """
        filterWidget = QgsFieldExpressionWidget()
        if isinstance(layer, QgsVectorLayer):
            filterWidget.setLayer(layer)
        return filterWidget

    def predicateComboBox(self):
        """
        Retrieves widget for spatial predicate selection.
        :return: (QComboBox) a combo box with all available predicates.
        """
        cb = QComboBox()
        cb.addItems([
            self.tr("contains"),
            self.tr("does not contain"),
            self.tr("is contained"),
            self.tr("is not contained"),
            self.tr("intersects"),
            self.tr("does not intersect"),
            self.tr("touches"),
            self.tr("does not touch")
        ])
        return cb

    def cardinalityWidget(self):
        """
        Retrieves a widget for cardinality setting.
        :return: (QLineEdit) cardinality widget with its content validation
                 applied.
        """
        le = QLineEdit()
        le.setPlaceholderText("0..*")
        return le

    def standardPanel(self):
        """
        Returns the table prepared for the standard Processing GUI.
        :return: (OrderedTableWidget) DSGTools customized table widget.
        """
        otw = OrderedTableWidget(headerMap={
            0 : {
                "header" : self.tr("Layer A"),
                "type" : "widget",
                "widget" : self.mapLayerComboBox,
                "setter" : "setCurrentText",
                "getter" : "currentText"
            },
            1 : {
                "header" : self.tr("Filter A"),
                "type" : "widget",
                # problema: conectar o sinal da mapLayerComboBox no filterexpression
                "widget" : self.filterExpressionWidget,
                "setter" : "setExpression",
                "getter" : "currentText"
            },
            2 : {
                "header" : self.tr("Predicate"),
                "type" : "widget",
                "widget" : self.predicateComboBox,
                "setter" : "setCurrentIndex",
                "getter" : "currentIndex"
            },
            3 : {
                "header" : self.tr("Layer B"),
                "type" : "widget",
                "widget" : self.mapLayerComboBox,
                "setter" : "setCurrentText",
                "getter" : "currentText"
            },
            4 : {
                "header" : self.tr("Filter B"),
                "type" : "widget",
                # problema: conectar o sinal da mapLayerComboBox no filterexpression
                "widget" : self.filterExpressionWidget,
                "setter" : "setExpression",
                "getter" : "currentText"
            },
            5 : {
                "header" : self.tr("Cardinality"),
                "type" : "widget",
                # problema: conectar o sinal da mapLayerComboBox no filterexpression
                "widget" : self.cardinalityWidget,
                "setter" : "setCurrentText",
                "getter" : "currentText"
            }
        })
        otw.setHeaderDoubleClickBehaviour("replicate")
        return otw

    def batchPanel(self):
        """
        Returns the table prepared for the batch Processing GUI.
        :return: (OrderedTableWidget) DSGTools customized table widget.
        """
        return self.standardPanel()

    def modelerPanel(self):
        """
        Returns the table prepared for the modeler Processing GUI.
        :return: (OrderedTableWidget) DSGTools customized table widget.
        """
        otw = OrderedTableWidget(headerMap={
            0 : {
                "header" : self.tr("Layer A"),
                "type" : "widget",
                "widget" : self.mapLayerModelDialog,
                "setter" : "setText",
                "getter" : "text"
            },
            1 : {
                "header" : self.tr("Filter A"),
                "type" : "widget",
                # problema: conectar o sinal da mapLayerComboBox no filterexpression
                "widget" : self.filterExpressionWidget,
                "setter" : "setExpression",
                "getter" : "currentText"
            },
            2 : {
                "header" : self.tr("Predicate"),
                "type" : "widget",
                "widget" : self.predicateComboBox,
                "setter" : "setCurrentIndex",
                "getter" : "currentIndex"
            },
            3 : {
                "header" : self.tr("Layer B"),
                "type" : "widget",
                "widget" : self.mapLayerModelDialog,
                "setter" : "setText",
                "getter" : "text"
            },
            4 : {
                "header" : self.tr("Filter B"),
                "type" : "widget",
                # problema: conectar o sinal da mapLayerComboBox no filterexpression
                "widget" : self.filterExpressionWidget,
                "setter" : "setExpression",
                "getter" : "currentText"
            },
            5 : {
                "header" : self.tr("Cardinality"),
                "type" : "widget",
                # problema: conectar o sinal da mapLayerComboBox no filterexpression
                "widget" : self.cardinalityWidget,
                "setter" : "setCurrentText",
                "getter" : "currentText"
            }
        })
        otw.setHeaderDoubleClickBehaviour("replicate")
        return otw

    def createPanel(self):
        return {
            DIALOG_MODELER : self.modelerPanel,
            DIALOG_STANDARD : self.standardPanel,
            DIALOG_BATCH : self.batchPanel
        }[self.dialogType]()
    
    def createWidget(self):
        self.panel = self.createPanel()
        # self.panel.dialogType = self.dialogType
        return self.panel
    
    def parentLayerChanged(self, layer=None):
        pass
    
    def setLayer(self, layer):
        pass
    
    def setValue(self, value):
        """
        Sets back parameters to the GUI. Method reimplementation.
        :param value: (str) value to be set to GUI to retrieve its last state.
        """
        if value is None:
            return
        # for valueMap in value:
        #     self.panel.addRow({
        #         0 : valueMap["referenceLayer"],
        #         1 : valueMap["snap"],
        #         2 : valueMap["mode"]
        #     })

    def readStandardPanel(self):
        """
        Reads widget's contents when process' parameters are set from an 
        algorithm call (e.g. Processing toolbox).
        """
        valueMaplist = list()
        for row in range(self.panel.rowCount()):
            values = dict()
            values["layer_a"] = self.panel.getValue(row, 0)
            values["filter_a"] = self.panel.getValue(row, 1)
            values["predicate"] = self.panel.getValue(row, 2)
            values["layer_b"] = self.panel.getValue(row, 3)
            values["filter_b"] = self.panel.getValue(row, 4)
            values["cardinality"] = self.panel.getValue(row, 5)
            valueMaplist.append(values)
        return valueMaplist

    def readModelerPanel(self):
        """
        Reads widget's contents when process' parameters are set from a modeler
        instance.
        """
        return self.readStandardPanel()

    def readBatchPanel(self):
        """
        Reads widget's contents when process' parameters are set from a batch
        processing instance.
        """
        return self.readStandardPanel()

    def value(self):
        """
        Retrieves parameters from current widget. Method reimplementation.
        :return: (dict) value currently set to the GUI.
        """
        return {
            DIALOG_STANDARD : self.readStandardPanel,
            DIALOG_MODELER : self.readModelerPanel,
            DIALOG_BATCH : self.readBatchPanel
        }[self.dialogType]()
    
    def postInitialize(self, wrappers):
        pass
