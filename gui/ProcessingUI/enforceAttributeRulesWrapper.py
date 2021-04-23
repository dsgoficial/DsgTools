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

from qgis.core import QgsProject, QgsVectorLayer, QgsMapLayerProxyModel, QgsFieldProxyModel
from qgis.gui import QgsColorButton, QgsMapLayerComboBox, QgsFieldComboBox, QgsFieldExpressionWidget
from qgis.PyQt import QtCore
from qgis.PyQt.QtCore import Qt, QRegExp, pyqtSlot
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import (QHBoxLayout, QVBoxLayout, QMessageBox, QHeaderView,
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


class EnforceAttributeRulesWrapper(WidgetWrapper):
    """
    Docstring
    fazer check de versao de __ATTRIBUTE_MAP_VERSION ao importar o json
    """
    __ATTRIBUTE_MAP_VERSION = 0.1
    # enum for column ordering
    STD_COLUMN_COUNT = 5
    MODELER_COLUMN_COUNT = 6
    descStd, lyrStd, expStd, errStd, colorStd = list(range(STD_COLUMN_COUNT))
    descMd, lyrMd, fldMd, expMd, errMd, colorMd = list(
        range(MODELER_COLUMN_COUNT))

    def __init__(self, *args, **kwargs):
        """
        Constructor
        """
        super(EnforceAttributeRulesWrapper, self).__init__(*args, **kwargs)
        self.getLoadedLayers()

    def stringDataWidget(self, text):
        """
        Retrieves the widget for reading/setting string data.
        :return: (QLineEdit)
        """
        le = QLineEdit()
        le.setPlaceholderText(self.tr(text))
        le.setAlignment(Qt.AlignLeft)
        return le

    def ruleExpressionWidget(self):
        """
        Retrieves the widget for reading/setting rule expression.
        :return: (QLineEdit)
        """
        rex = QLineEdit()
        rex.setPlaceholderText(self.tr("Entire rule expression"))
        rex.setAlignment(Qt.AlignLeft)
        return rex

    def mapLyrAndFieldComboBox(self):
        """
        Retrieves the configured map layer selection combo box.
        :return: (QgsMapLayerComboBox) configured layer selection widget.
        """
        cb = LayerAndFieldSelectorWidget()
        return cb

    def errorTypeComboBox(self):
        """
        Retrieves the configured error type selection combo box.
        :return: (QComboBox) configured error selection widget.
        """
        errorTypeList = ['Atributo com valor incomum',
                         'Atributo com valor incorreto',
                         'Preencher atributo',
                         ]
        cb = QComboBox()
        cb.addItem(self.tr('Select an error type'))
        cb.addItems(errorTypeList)
        cbSize = cb.minimumSizeHint()
        cb.setMinimumSize(cbSize)
        return cb

    def colorSelectionWidget(self):
        """
        Retrieves a new widget for selecting colors.
        :return: (ColorSelectorWidget) color selection widget.
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
        """
        Gets data from the canvas and returns a dictionary with layers as
        keys and a list of layers fields as values.
        :return: (dict) with data loaded in canvas.
        """
        self.loaded = dict()
        layers = QgsProject.instance().mapLayers().values()
        for layer in layers:
            self.loaded[layer.name()] = [field.name()
                                         for field in layer.fields()]

        return self.loaded

    def modifyStateDict(self, stateDict):
        """
        Compares loaded layers in canvas with input data from JSON file and
        returns only the data that contain the already loaded layers to fill
        the standard panel GUI.
        :param stateDict: (dict) of the state of the otw interface.
        :return: (dict) with data loaded in canvas.
        """
        newDict = dict()
        notLoadedLyr = []
        for k, v in stateDict.items():
            if k == 'metadata':
                continue
            if v['1'][0] not in self.loaded or \
                    v['1'][1] not in self.loaded[v['1'][0]]:
                notLoadedLyr.append(v['1'][0])
            else:
                newDict[k] = v
        warning = self.showLoadingMsg(notLoadedLyr, 'warning')
        if notLoadedLyr:
            if warning == QMessageBox.Ignore:
                stateDict.clear()
                for k, v in newDict.items():
                    stateDict[k] = v
            else:
                stateDict.clear()
        else:
            self.showLoadingMsg()

    def modifyStateDictModeler(self, stateDict):
        """
        Compares loaded layers in canvas with input data from JSON file and
        returns only the data that contain the already loaded layers to fill
        the modeler GUI.
        :param stateDict: (dict) of the state of the otw interface.
        :return: (dict) with data loaded in canvas.
        """
        newDict = dict()
        notLoadedLyr = []
        for k, v in stateDict.items():
            if k == 'metadata':
                continue
            if v['1'][0] not in self.loaded or \
                    v['1'][1] not in self.loaded[v['1'][0]]:
                notLoadedLyr.append(v['1'][0])
            else:
                if isinstance(v['1'], (list, tuple)):
                    value = dict()
                    value['0'] = v['0']
                    value['1'] = v['1'][0]
                    value['2'] = v['1'][1]
                    value['3'] = v['2']
                    value['4'] = v['3']
                    value['5'] = v['4']
                newDict[k] = value
        warning = self.showLoadingMsg(notLoadedLyr, 'warning')
        if notLoadedLyr:
            if warning == QMessageBox.Ignore:
                stateDict.clear()
                for k, v in newDict.items():
                    stateDict[k] = v
            else:
                stateDict.clear()
        else:
            self.showLoadingMsg()

    def showLoadingMsg(self, lyrList=None, msgType=None):
        """
        Shows a message box to user if successfully loaded data or not.
        If not, shows to user a list of not loaded layers and allows user
        to choice between ignore and continue or cancel the importation.
        :param lyrList: (list) a list of not loaded layers.
        :param msgType: (str) type of message box - warning or information.
        :return: (signal) value returned from the clicked button.
        """
        msg = QMessageBox()
        msg.setWindowTitle(self.tr("Import Rules Information"))

        if lyrList and msgType == 'warning':
            msg.setIcon(QMessageBox.Warning)
            msg.setText(self.tr("Some rules have not been loaded"))
            msg.setInformativeText(
                self.tr("Do you want to ignore and continue or cancel?"))

            textLyrList = sorted(set(lyrList))
            formatedLyrList = ['{}' for item in textLyrList]
            msgString = ','.join(formatedLyrList).replace(',', '\n')
            formatedMsgString = self.tr(
                'The following layers have not been loaded:\n') + \
                msgString.format(*textLyrList)

            msg.setDetailedText(formatedMsgString)
            msg.setStandardButtons(QMessageBox.Ignore | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setText(self.tr("Successfully loaded rules!"))

        choice = msg.exec_()
        return choice

    def postAddRowStandard(self, row):
        """
        Sets up widgets to work as expected right after they are added to GUI.
        """
        # in standard GUI, the layer selectors are QgsMapLayerComboBox, and its
        # layer changed signal should be connected to the filter expression
        # widget setup

        lyrAndFieldComboBox = self.panel.itemAt(row, self.lyrStd)
        cLyr = lyrAndFieldComboBox.getCurrentLayer()
        filterWidget = self.panel.itemAt(row, self.expStd)

        lyrAndFieldComboBox.layerChanged(filterWidget.setLayer)
        lyrAndFieldComboBox.fieldChanged(filterWidget.setField)
        lyrAndFieldComboBox.layerChanged(
            partial(filterWidget.setExpression, str(cLyr.fields()[0].name()))
        )

        # first setup is manual though
        if cLyr:
            filterWidget.setLayer(cLyr)

    def postAddRowModeler(self, row):
        """
        Sets up widgets to work as expected right after they are added to GUI.
        """
        # when it's directly typed it worked, but when we have
        # to import the data it's NOT WORKING
        def checkLayerBeforeConnect(le, filterExp):
            lName = le.text().strip()
            layers = QgsProject.instance().mapLayersByName(lName)
            for layer in layers:
                if isinstance(layer, QgsVectorLayer) and layer.name() == lName:
                    filterExp.setLayer(layer)
                    return
            filterExp.setLayer(None)

        lyrLe = self.panel.itemAt(row, self.lyrMd)
        filterWidget = self.panel.itemAt(row, self.expMd)
        lyrLe.editingFinished.connect(
            partial(checkLayerBeforeConnect, lyrLe, filterWidget)
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
                "widget": lambda: self.stringDataWidget(
                    'Set a name for this attribute rule...'),
                "setter": "setText",
                "getter": "text"
            },
            1: {
                "header": self.tr("Layer and field"),
                "type": "widget",
                "widget": self.mapLyrAndFieldComboBox,
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
        for row in [1, 3, 4]:
            otw.horizontalHeader().setSectionResizeMode(
                row, QHeaderView.ResizeToContents)
        otw.setHeaderDoubleClickBehaviour("order")
        otw.dataLoaded.connect(self.modifyStateDict)
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
                "widget": lambda: self.stringDataWidget(
                    'Set a name for this attribute rule...'),
                "setter": "setText",
                "getter": "text"
            },
            1: {
                "header": self.tr("Layer"),
                "type": "widget",
                "widget": lambda: self.stringDataWidget(
                    'Type a vector layer name...'),
                "setter": "setText",
                "getter": "text"
            },
            2: {
                "header": self.tr("Field"),
                "type": "widget",
                "widget": lambda: self.stringDataWidget(
                    'Type a field layer name...'),
                "setter": "setText",
                "getter": "text"
            },
            3: {
                "header": self.tr("Expression"),
                "type": "widget",
                "widget": self.filterExpressionWidget,
                "setter": "setExpression",
                "getter": "currentText"
            },
            4: {
                "header": self.tr("Error type"),
                "type": "widget",
                "widget": lambda: self.stringDataWidget(
                    'Type an error type...'),
                "setter": "setText",
                "getter": "text"
            },
            5: {
                "header": self.tr("Color"),
                "type": "widget",
                "widget": self.colorSelectionWidget,
                "setter": "setCurrentColor",
                "getter": "getCurrentColor"
            }
        })
        otw.setHeaderDoubleClickBehaviour("order")
        otw.dataLoaded.connect(self.modifyStateDictModeler)
        otw.rowAdded.connect(self.postAddRowModeler)
        return otw

    def createPanel(self):
        """ Docstring """
        return {
            DIALOG_MODELER: self.modelerPanel,
            # DIALOG_MODELER: self.standardPanel,
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
                0: valueMap["description"],
                1: valueMap["layerField"],
                2: valueMap["expression"],
                3: valueMap["errorType"],
                4: valueMap["color"],
            })

    def readStandardPanel(self):
        """
        Reads widget's contents when process' parameters are set from an
        algorithm call (e.g. Processing toolbox).
        """
        valueMaplist = dict()
        count = 0
        for row in range(self.panel.rowCount()):
            values = dict()
            values["description"] = self.panel.getValue(row, 0).strip()
            values["layerField"] = self.panel.getValue(row, 1)
            values["expression"] = self.panel.getValue(row, 2)
            values["errorType"] = self.panel.getValue(row, 3)
            values["color"] = self.panel.getValue(row, 4)
            valueMaplist[count] = values
            count += 1
        return valueMaplist

    def readModelerPanel(self):
        """
        Reads widget's contents when process' parameters are set from a modeler
        instance.
        """
        valueMaplist = dict()
        count = 0
        for row in range(self.panel.rowCount()):
            values = dict()
            values["description"] = self.panel.getValue(row, 0).strip()
            values["layerField"] = [self.panel.getValue(row, 1),
                                    self.panel.getValue(row, 2)]
            values["expression"] = self.panel.getValue(row, 3)
            values["errorType"] = self.panel.getValue(row, 4)
            values["color"] = self.panel.getValue(row, 5)
            valueMaplist[count] = values
            count += 1
        return valueMaplist

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
