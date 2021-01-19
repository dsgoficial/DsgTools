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
import json
from functools import partial

from qgis.core import QgsProject, QgsVectorLayer, QgsMapLayerProxyModel, QgsFieldProxyModel, QgsMessageLog
from qgis.gui import QgsColorButton, QgsMapLayerComboBox, QgsFieldComboBox, QgsFieldExpressionWidget
from qgis.PyQt import QtCore
from qgis.PyQt.QtCore import Qt, QRegExp, pyqtSlot
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import (QHBoxLayout, QVBoxLayout,
                                 QWidget,
                                 QComboBox,
                                 QLineEdit)
from processing.gui.wrappers import (WidgetWrapper,
                                     DIALOG_STANDARD,
                                     DIALOG_MODELER,
                                     DIALOG_BATCH)

from DsgTools.gui.CustomWidgets.OrderedPropertyWidgets.orderedTableWidget import OrderedTableWidget
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.colorSelectorWidget import ColorSelectorWidget
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.layerAndFieldSelectorWidget import LayerAndFieldSelectorWidget


class ValidationAttributeRulesWrapper(WidgetWrapper):
    """
    Docstring
    fazer check de versao de __ATTRIBUTE_MAP_VERSION ao importar o json
    """
    __ATTRIBUTE_MAP_VERSION = 0.1
    # enum for column ordering
    COLUMN_COUNT = 5
    descFld, lyrFld, expFld, errFld, colorFld = list(range(COLUMN_COUNT))

    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        super(ValidationAttributeRulesWrapper, self).__init__(*args, **kwargs)
        self.getLoadedLayers()
        self.layerList = [layer.name()
                          for layer in QgsProject.instance().mapLayers().values()]

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

    def maplyrAndFieldComboBox(self):
        """
        Retrieves the configured map layer selection combo box.
        :return: (QgsMapLayerComboBox) configured layer selection widget.
        """
        cb = LayerAndFieldSelectorWidget()
        return cb

    def errorTypeComboBox(self):
        """
        Retrieves the configured map layer selection combo box.
        :return: (QgsMapLayerComboBox) configured layer selection widget.
        """
        errorTypeList = ['Atributo com valor incomum',
                         'Atributo com valor incorreto',
                         'Preencher atributo',
                         ]
        cb = QComboBox()
        cb.addItem(self.tr('Select an error type'))
        cb.addItems(errorTypeList)
        return cb

    def mapLayerModelDialog(self):
        """
        Retrieves widget for map layer selection in a model dialog setup.
        :return: (QLineEdit) map layer setter widget for processing dialog
        mode.
        """
        le = QLineEdit()
        le.setPlaceholderText(self.tr("Type a vector layer's name..."))
        return le

    def mapFieldModelDialog(self):
        """
        Retrieves widget for map field selection in a model dialog setup.
        :return: (QLineEdit) map field setter widget for processing dialog
        mode.
        """
        le = QLineEdit()
        le.setPlaceholderText(self.tr("Type a field layer's name..."))
        return le

    def colorSelectionWidget(self):
        """
        Retrieves a new widget for selecting colors.
        :return: (QgsColorButton) color selection widget.
        """
        cw = ColorSelectorWidget()
        return cw

    def filterExpressionWidget(self):
        """
        Retrieves a new widget for filtering expression setting.
        :return: (QgsFieldExpressionWidget) snap mode selection widget.
        """
        filterWidget = QgsFieldExpressionWidget()
        return filterWidget

    def getLoadedLayers(self):
        self.loaded = {}
        layers = QgsProject.instance().mapLayers().values()
        for layer in layers:
            self.loaded.setdefault(
                layer.name(), [field.name() for field in layer.fields()])

        return self.loaded

    def test(self, _dict):
        """
        {
            0: {
                '0': 'ghsshsghghshgs',
                '1': ('hid_terreno_suj_inundacao_a', 'periodicidadeinunda'),
                '2': 'periodicidadeinunda',
                '3': 'Atributo com valor incomum',
                '4': '#33a02c'
            }
        }
        """
        d = {}
        l = []
        for k, v in _dict.items():
            if k == 'metadata':
                continue
            # print(k, ':', v)
            elif v['1'][0] not in self.loaded or v['1'][1] not in self.loaded[v['1'][0]]:
                l.append(v['1'][0])
                QgsMessageLog.logMessage("Not loaded layers", l)
                # print('elif: ', v['1'][0])
            else:
                d.setdefault(k, v)

        _dict.clear()
        for k, v in d.items():
            _dict.setdefault(k, v)

        # return d

    def postAddRowStandard(self, row):
        """
        Sets up widgets to work as expected right after they are added to GUI.
        """
        # in standard GUI, the layer selectors are QgsMapLayerComboBox, and its
        # layer changed signal should be connected to the filter expression
        # widget setup

        # a = OrderedTableWidget.dataLoaded.connect(test)

        lyrAndFieldComboBox = self.panel.itemAt(row, self.lyrFld)
        cl = lyrAndFieldComboBox.getCurrentLayer()
        filterWidget = self.panel.itemAt(row, self.expFld)

        lyrAndFieldComboBox.layerChanged(filterWidget.setLayer)
        lyrAndFieldComboBox.fieldChanged(filterWidget.setField)
        lyrAndFieldComboBox.layerChanged(
            partial(filterWidget.setExpression, str(cl.fields()[0].name()))
        )

        # first setup is manual though
        if cl:
            filterWidget.setLayer(cl)

    def postAddRowModeler(self, row):
        """
        Sets up widgets to work as expected right after they are added to GUI.
        """

        def checkLayerBeforeConnect(le, filterExp):
            lName = le.text().strip()
            for layer in QgsProject.instance().mapLayersByName(lName):
                if isinstance(layer, QgsVectorLayer) and layer.name() == lName:
                    filterExp.setLayer(layer)
                    return
            filterExp.setLayer(None)

        le = self.panel.itemAt(row, self.lyrFld)
        filterWidget = self.panel.itemAt(row, self.expFld)
        le.editingFinished.connect(
            partial(checkLayerBeforeConnect, le, filterWidget)
        )

    def standardPanel(self):
        """
        Returns the table prepared for the standard Processing GUI.
        :return: (OrderedTableWidget) DSGTools customized table widget.
        """
        otw = OrderedTableWidget(headerMap={
            0: {
                "header": self.tr("Description"),
                "type": "widget",
                "widget": self.ruleNameWidget,
                "setter": "setText",
                "getter": "text"
            },
            1: {
                "header": self.tr("Layer and field"),
                "type": "widget",
                "widget": self.maplyrAndFieldComboBox,
                "setter": "setCurrentLayerNField",
                "getter": "getCurrentLayerNField"
            },
            2: {
                "header": self.tr("Expression"),
                "type": "widget",
                "widget": self.filterExpressionWidget,
                "setter": "setExpression",
                "getter": "currentText"
            },
            3: {
                "header": self.tr("Error type"),
                "type": "widget",
                "widget": self.errorTypeComboBox,
                "setter": "setCurrentText",
                "getter": "currentText"
            },
            4: {
                "header": self.tr("Color"),
                "type": "widget",
                "widget": self.colorSelectionWidget,
                "setter": "setCurrentColor",
                "getter": "getCurrentColor"
            },

        })
        otw.setHeaderDoubleClickBehaviour("order")
        otw.dataLoaded.connect(self.test)
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
            0: {
                "header": self.tr("Rule description"),
                "type": "widget",
                "widget": self.ruleNameWidget,
                "setter": "setText",
                "getter": "text"
            },
            1: {
                "header": self.tr("Layer"),
                "type": "widget",
                "widget": self.mapLayerModelDialog,
                "setter": "setText",
                "getter": "text"
            },
            2: {
                "header": self.tr("Field"),
                "type": "widget",
                "widget": self.mapFieldComboBox,
                "setter": "setExpression",
                "getter": "currentText"
            },
            3: {
                "header": self.tr("Expression"),
                "type": "widget",
                "widget": self.filterExpressionWidget,
                "setter": "setExpression",
                "getter": "currentText"
            },
            4: {
                "header": self.tr("Color"),
                "type": "widget",
                "widget": self.colorSelectionWidget,
                "setter": "setExpression",
                "getter": json.dumps("color", separators=(','))
            }
        })
        otw.setHeaderDoubleClickBehaviour("order")
        otw.rowAdded.connect(self.postAddRowModeler)
        return otw

    def createPanel(self):
        """ Docstring """
        return {
            DIALOG_MODELER: self.modelerPanel,
            DIALOG_STANDARD: self.standardPanel,
            DIALOG_BATCH: self.batchPanel
        }[self.dialogType]()

    def createWidget(self):
        """ Docstring """
        self.panel = self.createPanel()
        self.panel.showSaveLoadButtons(True)
        self.panel.extension = ".json"
        self.panel.fileType = self.tr("Set of DSGTools Attribute Rules")
        self.panel.setMetadata({
            "version": self.__ATTRIBUTE_MAP_VERSION
        })
        return self.panel

    def parentLayerChanged(self, layer=None):
        """ Docstring """
        pass

    def setLayer(self, layer):
        """ Docstring """
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
                0: valueMap["name"],
                1: valueMap["layerNField"],
                2: valueMap["expression"],
                3: valueMap["color"],
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
            values["layerNField"] = self.panel.getValue(row, 1)
            values["expression"] = self.panel.getValue(row, 2)
            values["color"] = self.panel.getValue(row, 3)
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
            DIALOG_STANDARD: self.readStandardPanel,
            DIALOG_MODELER: self.readModelerPanel,
            DIALOG_BATCH: self.readBatchPanel
        }[self.dialogType]()

    def postInitialize(self, wrappers):
        """ Docstring """
        pass
