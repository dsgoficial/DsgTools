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

from functools import partial

from qgis.core import QgsProject, QgsVectorLayer, QgsMapLayerProxyModel, QgsFieldProxyModel
from qgis.gui import QgsMapLayerComboBox, QgsFieldComboBox, QgsFieldExpressionWidget
from qgis.PyQt.QtCore import QRegExp
from qgis.PyQt.QtGui import QRegExpValidator
from qgis.PyQt.QtWidgets import (QComboBox,
                                 QLineEdit)
from processing.gui.wrappers import (WidgetWrapper,
                                     DIALOG_STANDARD,
                                     DIALOG_MODELER,
                                     DIALOG_BATCH)

from DsgTools.core.GeometricTools.spatialRelationsHandler import SpatialRelationsHandler
from DsgTools.gui.CustomWidgets.OrderedPropertyWidgets.orderedTableWidget import OrderedTableWidget


class ValidationAttributeRulesWrapper(WidgetWrapper):
    """
    Docstring
    """
    __ATTRIBUTE_MAP_VERSION = 0.1
    # enum for column ordering
    COLUMN_COUNT = 4
    InDs, Filter, InEdgv, OutDs = list(range(COLUMN_COUNT))

    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        super(ValidationAttributeRulesWrapper, self).__init__(*args, **kwargs)

    def ruleNameWidget(self):
        """
        Retrieves the widget for reading/setting rule name.
        :return: (QLineEdit)
        """
        le = QLineEdit()
        le.setPlaceholderText(self.tr("Set a name for this spatial rule..."))
        return le

    def ruleExpressionWidget(self):
        """
        Retrieves the widget for reading/setting rule expression.
        :return: (QLineEdit)
        """
        rex = QLineEdit()
        rex.setPlaceholderText(self.tr("Entire rule expression"))
        return rex

    def mapLayerComboBox(self):
        """
        Retrieves the configured map layer selection combo box.
        :return: (QgsMapLayerComboBox) configured layer selection widget. 
        """
        cb = QgsMapLayerComboBox()
        cb.setFilters(QgsMapLayerProxyModel.VectorLayer)
        return cb

    def mapFieldComboBox(self):
        """
        Retrieves the configured map layer selection combo box.
        :return: (QgsMapLayerComboBox) configured layer selection widget. 
        """
        fb = QgsFieldComboBox()
        fb.setFilters(QgsFieldProxyModel.AllTypes)
        return fb

    def mapFieldModelDialog(self):
        """
        Retrieves widget for map layer selection in a model dialog setup.
        :return: (QLineEdit) map layer setter widget for processing dialog
                 mode.
        """
        le = QLineEdit()
        le.setPlaceholderText(self.tr("Type a vector layer's name..."))
        return le

    def mapLayerModelDialog(self):
        """
        Retrieves widget for map layer selection in a model dialog setup.
        :return: (QLineEdit) map layer setter widget for processing dialog
                 mode.
        """
        le = QLineEdit()
        le.setPlaceholderText(self.tr("Type a vector layer's name..."))
        return le

    def filterExpressionWidget(self):
        """
        Retrieves a new widget for filtering expression setting.
        :return: (QgsFieldExpressionWidget) snap mode selection widget.
        """
        filterWidget = QgsFieldExpressionWidget()
        return filterWidget

    def postAddRowStandard(self, row):
        """
        Sets up widgets to work as expected right after they are added to GUI.
        """
        # in standard GUI, the layer selectors are QgsMapLayerComboBox, and its
        # layer changed signal should be connected to the filter expression
        # widget setup
        col = 2
        
        mapLayerComboBox = self.panel.itemAt(row, 1)
        mapFieldComboBox = self.panel.itemAt(row, 2)
        filterWidget = self.panel.itemAt(row, 3)
        mapLayerComboBox.layerChanged.connect(mapFieldComboBox.setLayer)
        mapFieldComboBox.fieldChanged.connect(filterWidget.setField)
        mapLayerComboBox.layerChanged.connect(
            partial(filterWidget.setExpression, "")
        )
        # first setup is manual though
        vl = mapLayerComboBox.currentLayer()
        if vl:
            filterWidget.setLayer(vl)

    def postAddRowModeler(self, row):
        """
        Sets up widgets to work as expected right after they are added to GUI.
        """
        col = 2
        def checkLayerBeforeConnect(le, filterExp):
            lName = le.text().strip()
            for layer in QgsProject.instance().mapLayersByName(lName):
                if isinstance(layer, QgsVectorLayer) and layer.name() == lName:
                    filterExp.setLayer(layer)
                    return
            filterExp.setLayer(None)
        
        le = self.panel.itemAt(row, 1)
        filterWidget = self.panel.itemAt(row, 3)
        le.editingFinished.connect(
            partial(checkLayerBeforeConnect, le, filterWidget)
        )

    def standardPanel(self):
        """
        Returns the table prepared for the standard Processing GUI.
        :return: (OrderedTableWidget) DSGTools customized table widget.
        """
        otw = OrderedTableWidget(headerMap={
            0 : {
                "header" : self.tr("Rule name"),
                "type" : "widget",
                "widget" : self.ruleNameWidget,
                "setter" : "setText",
                "getter" : "text"
            },
            1 : {
                "header" : self.tr("Layers"),
                "type" : "widget",
                "widget" : self.mapLayerComboBox,
                "setter" : "setCurrentText",
                "getter" : "currentText"
            },
            2 : {
                "header" : self.tr("Attribute"),
                "type" : "widget",
                "widget" : self.mapFieldComboBox,
                "setter" : "setExpression",
                "getter" : "currentText"
            },
            3 : {
                "header" : self.tr("Expression"),
                "type" : "widget",
                "widget" : self.filterExpressionWidget,
                "setter" : "setExpression",
                "getter" : "currentText"
            }
        })
        otw.setHeaderDoubleClickBehaviour("replicate")
        otw.rowAdded.connect(self.postAddRowStandard)
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
                "header" : self.tr("Rule name"),
                "type" : "widget",
                "widget" : self.ruleNameWidget,
                "setter" : "setText",
                "getter" : "text"
            },
            1 : {
                "header" : self.tr("Layers"),
                "type" : "widget",
                "widget" : self.mapLayerModelDialog,
                "setter" : "setText",
                "getter" : "text"
            },
            2 : {
                "header" : self.tr("Attribute"),
                "type" : "widget",
                "widget" : self.mapFieldComboBox,
                "setter" : "setExpression",
                "getter" : "currentText"
            },
            3 : {
                "header" : self.tr("Expression"),
                "type" : "widget",
                "widget" : self.filterExpressionWidget,
                "setter" : "setExpression",
                "getter" : "currentText"
            }
        })
        otw.setHeaderDoubleClickBehaviour("replicate")
        otw.rowAdded.connect(self.postAddRowModeler)
        return otw

    def createPanel(self):
        return {
            DIALOG_MODELER : self.modelerPanel,
            DIALOG_STANDARD : self.standardPanel,
            DIALOG_BATCH : self.batchPanel
        }[self.dialogType]()
    
    def createWidget(self):
        self.panel = self.createPanel()
        self.panel.showSaveLoadButtons(True)
        self.panel.extension = ".attrules"
        self.panel.fileType = self.tr("Set of DSGTools Attribute Rules")
        self.panel.setMetadata({
            "version": self.__ATTRIBUTE_MAP_VERSION
        })
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
        for valueMap in value:
            self.panel.addRow({
                0 : valueMap["name"],
                1 : valueMap["layer"],
                2 : valueMap["attribute"],
                3 : valueMap["expression"]
            })

    def readStandardPanel(self):
        """
        Reads widget's contents when process' parameters are set from an 
        algorithm call (e.g. Processing toolbox).
        """
        valueMaplist = list()
        for row in range(self.panel.rowCount()):
            values = dict()
            values["name"] = self.panel.getValue(row, 0).strip() or \
                             self.tr("Attribute Rule #{n}".format(n=row + 1))
            values["layer"] = self.panel.getValue(row, 1)
            values["attribute"] = self.panel.getValue(row, 2)
            values["expression"] = self.panel.getValue(row, 3)
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
