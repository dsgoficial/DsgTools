# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-12-02
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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

from qgis.gui import QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import QComboBox, QLineEdit, QDoubleSpinBox
from processing.gui.wrappers import (
    WidgetWrapper,
    DIALOG_STANDARD,
    DIALOG_MODELER,
    DIALOG_BATCH,
)
from DsgTools.gui.CustomWidgets.SelectionWidgets.selectFileWidget import (
    SelectFileWidget,
)

from DsgTools.gui.CustomWidgets.OrderedPropertyWidgets.orderedTableWidget import (
    OrderedTableWidget,
)


class DbConversionWrapper(WidgetWrapper):
    def __init__(self, *args, **kwargs):
        super(DbConversionWrapper, self).__init__(*args, **kwargs)

    def conversionFileSelector(self, filepath=None):
        """
        Retrieves the configured map layer selection combo box.
        :return: (QgsMapLayerComboBox) configured layer selection widget.
        """
        widget = SelectFileWidget()
        widget.label.hide()
        widget.selectFilePushButton.setText("...")
        widget.selectFilePushButton.setMaximumWidth(32)
        widget.lineEdit.setPlaceholderText(self.tr("Select a conversion json..."))
        widget.lineEdit.setFrame(False)
        widget.setCaption(self.tr("Select a conversion json file"))
        widget.setFilter(self.tr("Select a conversion json file (*json)"))
        # defining setter and getter methods for composed widgets into OTW
        widget.setText = widget.lineEdit.setText
        widget.text = widget.lineEdit.text
        if filepath is not None:
            widget.setText(filepath)
        return widget

    def modeComboBox(self):
        """
        Retrieves a new widget for snap mode selection.
        :return: (QComboBox) snap mode selection widget.
        """
        cb = QComboBox()
        cb.addItems(
            [
                self.tr("A=>B"),
                self.tr("B=>A"),
            ]
        )
        return cb

    def standardPanel(self):
        """
        Returns the table prepared for the standard Processing GUI.
        :return: (OrderedTableWidget) DSGTools customized table widget.
        """
        otw = OrderedTableWidget(
            headerMap={
                0: {
                    "header": self.tr("Layer"),
                    "type": "widget",
                    "widget": self.conversionFileSelector,
                    "setter": "setText",
                    "getter": "text",
                },
                1: {
                    "header": self.tr("Conversion mode"),
                    "type": "widget",
                    "widget": self.modeComboBox,
                    "setter": "setCurrentIndex",
                    "getter": "currentText",
                },
            }
        )
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
        otw = OrderedTableWidget(
            headerMap={
                0: {
                    "header": self.tr("Layer"),
                    "type": "widget",
                    "widget": self.conversionFileSelector,
                    "setter": "setText",
                    "getter": "text",
                },
                1: {
                    "header": self.tr("Conversion mode"),
                    "type": "widget",
                    "widget": self.modeComboBox,
                    "setter": "setCurrentIndex",
                    "getter": "currentText",
                },
            }
        )
        otw.setHeaderDoubleClickBehaviour("replicate")
        return otw

    def createPanel(self):
        return {
            DIALOG_MODELER: self.modelerPanel,
            DIALOG_STANDARD: self.standardPanel,
            DIALOG_BATCH: self.batchPanel,
        }[self.dialogType]()

    def createWidget(self):
        self.panel = self.createPanel()
        self.panel.showSaveLoadButtons(True)
        self.panel.extension = ".json"
        self.panel.fileType = self.tr("JSON file")
        return self.panel

    def parentLayerChanged(self, layer=None):
        pass

    def setValue(self, value):
        """
        Sets back parameters to the GUI. Method reimplementation.
        :param value: (str) value to be set to GUI to retrieve its last state.
        """
        if value is None:
            return
        for valueMap in value:
            self.panel.addRow(
                {
                    0: valueMap["conversionJson"],
                    1: valueMap["mode"],
                }
            )

    def readStandardPanel(self):
        """
        Reads widget's contents when process' parameters are set from an
        algorithm call (e.g. Processing toolbox).
        """
        valueMaplist = list()
        for row in range(self.panel.rowCount()):
            values = dict()
            values["conversionJson"] = self.panel.getValue(row, 0)
            values["mode"] = self.panel.getValue(row, 1)
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
            DIALOG_BATCH: self.readBatchPanel,
        }[self.dialogType]()

    def postInitialize(self, wrappers):
        pass
