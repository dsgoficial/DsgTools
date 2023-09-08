# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2020-07-27
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Pedro Martins - Cartographic Engineer @ Brazilian Army
        email                : pedromartins.souza@eb.mil.br
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


from qgis.core import Qgis, QgsProject, QgsVectorLayer, QgsMapLayerProxyModel
from qgis.gui import QgsMessageBar, QgsMapLayerComboBox
from qgis.PyQt.QtCore import QSize
from qgis.PyQt.QtWidgets import (
    QWidget,
    QLineEdit,
    QDoubleSpinBox,
    QVBoxLayout,
    QMessageBox,
)
from processing.gui.wrappers import (
    WidgetWrapper,
    DIALOG_STANDARD,
    DIALOG_MODELER,
    DIALOG_BATCH,
)

from DsgTools.gui.CustomWidgets.OrderedPropertyWidgets.orderedTableWidget import (
    OrderedTableWidget,
)


class SmallObjectsOnLayersWrapper(WidgetWrapper):
    __DISTANCE_VERSION = 0.2

    def __init__(self, *args, **kwargs):
        self.layerIndex = 0
        self.tolIndex = 1
        super(SmallObjectsOnLayersWrapper, self).__init__(*args, **kwargs)
        self.messageBar = QgsMessageBar(self.panel)
        self.panel.resizeEvent = self.resizeEvent
        self._lastError = ""

    def resizeEvent(self, e):
        """
        Resize QgsMessageBar to widget's width
        """
        self.messageBar.resize(QSize(self.panel.parent().geometry().size().width(), 30))

    def mapLayerComboBox(self):
        """
        Retrieves the configured map layer selection combo box.
        :return: (QgsMapLayerComboBox) configured layer selection widget.
        """
        cb = QgsMapLayerComboBox()
        cb.setFilters(
            QgsMapLayerProxyModel.LineLayer | QgsMapLayerProxyModel.PolygonLayer
        )
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

    def doubleSpinBox(self):
        """
        Retrieves a widget for selecting double values.
        :return: (QDoubleSpinBox) double spin box widget for float input.
        """
        sb = QDoubleSpinBox()
        sb.setDecimals(6)
        sb.setMaximum(999999)
        return sb

    def standardPanel(self):
        """
        Returns the table prepared for the standard Processing GUI.
        :return: (OrderedTableWidget) DSGTools customized table widget.
        """
        widget = QWidget()
        layout = QVBoxLayout()
        widget.otw = OrderedTableWidget(
            headerMap={
                self.layerIndex: {
                    "header": self.tr("Layer"),
                    "type": "widget",
                    "widget": self.mapLayerComboBox,
                    "setter": "setCurrentText",
                    "getter": "currentText",
                },
                self.tolIndex: {
                    "header": self.tr("Tol"),
                    "type": "widget",
                    "widget": self.doubleSpinBox,
                    "setter": "setValue",
                    "getter": "value",
                },
            }
        )

        widget.otw.setHeaderDoubleClickBehaviour("replicate")
        layout.addWidget(widget.otw)
        widget.setLayout(layout)
        return widget

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
        widget = QWidget()
        layout = QVBoxLayout()
        widget.otw = OrderedTableWidget(
            headerMap={
                self.layerIndex: {
                    "header": self.tr("Layer"),
                    "type": "widget",
                    "widget": self.mapLayerModelDialog,
                    "setter": "setText",
                    "getter": "text",
                },
                self.tolIndex: {
                    "header": self.tr("Tol"),
                    "type": "widget",
                    "widget": self.doubleSpinBox,
                    "setter": "setValue",
                    "getter": "value",
                },
            }
        )

        widget.otw.setHeaderDoubleClickBehaviour("replicate")
        layout.addWidget(widget.otw)
        widget.setLayout(layout)
        return widget

    def createPanel(self):
        return {
            DIALOG_MODELER: self.modelerPanel,
            DIALOG_STANDARD: self.standardPanel,
            DIALOG_BATCH: self.batchPanel,
        }[self.dialogType]()

    def createWidget(self):
        self.panel = self.createPanel()
        self.panel.otw.showSaveLoadButtons(True)
        self.panel.otw.extension = ".json"
        self.panel.otw.fileType = self.tr("JSON file")
        self.panel.otw.setMetadata({"version": self.__DISTANCE_VERSION})
        return self.panel

    def parentLayerChanged(self, layer=None):
        pass

    def setLayer(self, layer):
        pass

    def showLoadingMsg(self, invalidValues=None, msgType=None):
        """
        Shows a message box to user if successfully loaded data or not.
        If not, shows to user a list of not loaded layers and allows user
        to choice between ignore and continue or cancel the importation.
        :param lyrList: (list) a list of not loaded layers.
        :param msgType: (str) type of message box - warning or information.
        :return: (signal) value returned from the clicked button.
        """
        msg = QMessageBox()
        msg.setWindowTitle(self.tr("DSGTools: importing table"))
        if invalidValues and msgType == "warning":
            msg.setIcon(QMessageBox.Warning)
            msg.setText(self.tr("Some rows have not been loaded"))
            msg.setInformativeText(
                self.tr("Do you want to ignore and continue or cancel?")
            )
            msgString = "\n".join(
                (f"""{v["layer"]}, {v["tol"]}""" for v in invalidValues)
            )
            formatedMsgString = self.tr(
                "The following rows have not been loaded:\n{0}"
            ).format(msgString)
            msg.setDetailedText(formatedMsgString)
            msg.setStandardButtons(QMessageBox.Ignore | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
        else:
            msg.setIcon(QMessageBox.Information)
            msg.setText(self.tr("Successfully loaded!"))
        choice = msg.exec_()
        return choice

    def setValue(self, value):
        """
        Sets back parameters to the GUI. Method reimplementation.
        """
        if not value:
            return
        otw = self.panel.otw
        isNotModeler = self.dialogType != DIALOG_MODELER
        invalids = list()
        for valueMap in value:
            if not (
                self.validateLayerName(valueMap["layer"], checkLoaded=isNotModeler)
            ):
                invalids.append(valueMap)
                continue
            otw.addRow(
                {
                    self.layerIndex: valueMap["layer"],
                    self.tolIndex: valueMap["tol"],
                }
            )
        choice = self.showLoadingMsg(invalids, "warning" if invalids else "")
        if choice == QMessageBox.Cancel:
            otw.clear()

    def readStandardPanel(self):
        """
        Reads widget's contents when process' parameters are set from an
        algorithm call (e.g. Processing toolbox).
        """
        rowList = list()
        otw = self.panel.otw
        for row in range(otw.rowCount()):
            rowList.append(
                {
                    "layer": otw.getValue(row, self.layerIndex),
                    "tol": otw.getValue(row, self.tolIndex),
                }
            )
        return rowList

    def readModelerPanel(self):
        """
        Reads widget's contents when process' parameters are set from a modeler
        instance.
        """
        return self.readStandardPanel()

    def validateLayerName(self, layer, checkLoaded=False):
        """
        Checks whether a provided layer name is a valid setting. This method
        may take its availability on canvas into consideration, if necessary.
        :param layer: (str) layer name to be checked.
        :param checkLoaded: (bool) whether canvas availability should be considered.
        :return: (bool) provided layer name's validity.
        """
        isLoaded = False
        if checkLoaded:
            for vl in QgsProject.instance().mapLayersByName(layer):
                if isinstance(vl, QgsVectorLayer):
                    isLoaded = True
                    break
        return (not (checkLoaded and not isLoaded)) and layer != ""

    def readBatchPanel(self):
        """
        Reads widget's contents when process' parameters are set from a batch
        processing instance.
        """
        return self.readStandardPanel()

    def validate(self, pushAlert=False):
        """
        Validates fields. Returns True if all information are filled correctly.
        :param pushAlert: (bool) whether invalidation reason should be displayed on the widget.
        :return: (bool) whether set of filled parameters if valid.
        """
        inputMap = {
            DIALOG_STANDARD: self.readStandardPanel,
            DIALOG_MODELER: self.readModelerPanel,
            DIALOG_BATCH: self.readBatchPanel,
        }[self.dialogType]()
        if len(inputMap) == 0:
            if pushAlert:
                self.messageBar.pushMessage(
                    self.tr("Please provide at least layer."),
                    level=Qgis.Warning,
                    duration=5,
                )
            return False
        return True

    def value(self):
        """
        Retrieves parameters from current widget. Method reimplementation.
        :return: (dict) value currently set to the GUI.
        """
        if self.validate(pushAlert=True):
            return {
                DIALOG_STANDARD: self.readStandardPanel,
                DIALOG_MODELER: self.readModelerPanel,
                DIALOG_BATCH: self.readBatchPanel,
            }[self.dialogType]()

    def postInitialize(self, wrappers):
        pass
