# -*- coding: utf-8 -*-
"""
/***************************************************************************
 BuildMergedDataWrapper
                                 A QGIS plugin
 Widget wrapper for Build Merged Data algorithm
                              -------------------
        begin                : 2024-08-27
        copyright            : (C) 2024
        email                :
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
import json

from qgis.core import Qgis, QgsProject, QgsVectorLayer, QgsMapLayerProxyModel
from qgis.gui import QgsMessageBar, QgsMapLayerComboBox, QgsFieldExpressionWidget
from qgis.utils import iface
from qgis.PyQt.QtCore import QSize, QRegExp
from qgis.PyQt.QtGui import QRegExpValidator, QIntValidator
from qgis.PyQt.QtWidgets import (
    QWidget,
    QComboBox,
    QLineEdit,
    QVBoxLayout,
    QMessageBox,
    QSpinBox,
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


class BuildMergedDataWrapper(WidgetWrapper):
    __ATTRIBUTE_MAP_VERSION = 1.0

    def __init__(self, *args, **kwargs):
        super(BuildMergedDataWrapper, self).__init__(*args, **kwargs)
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
        cb.setFilters(QgsMapLayerProxyModel.VectorLayer)
        # Filter only Point, Line, and Polygon layers
        cb.setExceptedLayerList([])
        return cb

    def mapLayerModelDialog(self):
        """
        Retrieves widget for map layer selection in a model dialog setup.
        :return: (QLineEdit) map layer setter widget for processing dialog mode.
        """
        le = QLineEdit()
        le.setPlaceholderText(self.tr("Type a vector layer's name..."))
        return le

    def filterExpressionWidget(self):
        """
        Retrieves a new widget for filtering expression setting.
        :return: (QgsFieldExpressionWidget) expression widget.
        """
        fe = QgsFieldExpressionWidget()

        def setValueProxy(exp):
            layer = fe.layer()
            if layer and exp.strip() in layer.fields().names():
                exp = ""
            fe.setExpression(exp)

        def getValueProxy():
            layer = fe.layer()
            exp = fe.currentText()
            if layer and exp.strip() in layer.fields().names():
                exp = ""
            return exp

        fe.setExpression_ = setValueProxy
        fe.currentText_ = getValueProxy
        return fe

    def classIndexWidget(self):
        """
        Retrieves a widget for class index setting.
        :return: (QSpinBox) class index widget.
        """
        spin = QSpinBox()
        spin.setMinimum(0)
        spin.setMaximum(999999)
        spin.setValue(0)
        return spin

    def postAddRowStandard(self, row):
        """
        Sets up widgets to work as expected right after they are added to GUI.
        :param row: (int) row to have its widgets setup.
        """
        otw = self.panel.otw
        # Connect layer selection to expression widget
        mapLayerComboBox = otw.itemAt(row, 0)
        filterWidget = otw.itemAt(row, 1)

        if mapLayerComboBox and filterWidget:
            mapLayerComboBox.layerChanged.connect(filterWidget.setLayer)
            mapLayerComboBox.layerChanged.connect(
                partial(filterWidget.setExpression, "")
            )
            # First setup is manual though
            vl = mapLayerComboBox.currentLayer()
            if vl:
                filterWidget.setLayer(vl)

    def postAddRowModeler(self, row):
        """
        Sets up widgets to work as expected right after they are added to GUI.
        :param row: (int) row to have its widgets setup.
        """
        otw = self.panel.otw

        def checkLayerBeforeConnect(le, filterExp):
            lName = le.text().strip()
            for layer in QgsProject.instance().mapLayersByName(lName):
                if isinstance(layer, QgsVectorLayer) and layer.name() == lName:
                    filterExp.setLayer(layer)
                    return
            filterExp.setLayer(None)

        le = otw.itemAt(row, 0)
        filterWidget = otw.itemAt(row, 1)
        if le and filterWidget:
            le.editingFinished.connect(
                partial(checkLayerBeforeConnect, le, filterWidget)
            )

    def classNameWidget(self):
        """
        Retrieves a widget for class name setting.
        :return: (QLineEdit) class name widget.
        """
        le = QLineEdit()
        le.setPlaceholderText(self.tr("Enter class name..."))
        return le

    def standardPanel(self):
        """
        Returns the table prepared for the standard Processing GUI.
        :return: (OrderedTableWidget) customized table widget.
        """
        widget = QWidget()
        layout = QVBoxLayout()

        widget.otw = OrderedTableWidget(
            headerMap={
                0: {
                    "header": self.tr("Layer"),
                    "type": "widget",
                    "widget": self.mapLayerComboBox,
                    "setter": "setCurrentText",
                    "getter": "currentText",
                },
                1: {
                    "header": self.tr("Filter Expression (Optional)"),
                    "type": "widget",
                    "widget": self.filterExpressionWidget,
                    "setter": "setExpression_",
                    "getter": "currentText_",
                },
                2: {
                    "header": self.tr("Class Index"),
                    "type": "widget",
                    "widget": self.classIndexWidget,
                    "setter": "setValue",
                    "getter": "value",
                },
                3: {
                    "header": self.tr("Class Name"),
                    "type": "widget",
                    "widget": self.classNameWidget,
                    "setter": "setText",
                    "getter": "text",
                },
            }
        )

        widget.otw.setHeaderDoubleClickBehaviour("replicate")
        widget.otw.rowAdded.connect(self.postAddRowStandard)
        layout.addWidget(widget.otw)
        widget.setLayout(layout)
        return widget

    def batchPanel(self):
        """
        Returns the table prepared for the batch Processing GUI.
        :return: (OrderedTableWidget) customized table widget.
        """
        return self.standardPanel()

    def modelerPanel(self):
        """
        Returns the table prepared for the modeler Processing GUI.
        :return: (OrderedTableWidget) customized table widget.
        """
        widget = QWidget()
        layout = QVBoxLayout()

        widget.otw = OrderedTableWidget(
            headerMap={
                0: {
                    "header": self.tr("Layer"),
                    "type": "widget",
                    "widget": self.mapLayerModelDialog,
                    "setter": "setText",
                    "getter": "text",
                },
                1: {
                    "header": self.tr("Filter Expression (Optional)"),
                    "type": "widget",
                    "widget": self.filterExpressionWidget,
                    "setter": "setExpression_",
                    "getter": "currentText_",
                },
                2: {
                    "header": self.tr("Class Index"),
                    "type": "widget",
                    "widget": self.classIndexWidget,
                    "setter": "setValue",
                    "getter": "value",
                },
                3: {
                    "header": self.tr("Class Name"),
                    "type": "widget",
                    "widget": self.classNameWidget,
                    "setter": "setText",
                    "getter": "text",
                },
            }
        )

        widget.otw.setHeaderDoubleClickBehaviour("replicate")
        widget.otw.rowAdded.connect(self.postAddRowModeler)
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
        self.panel.otw.extension = ".layersconfig"
        self.panel.otw.fileType = self.tr("Layers Configuration File")
        self.panel.otw.setMetadata({"version": self.__ATTRIBUTE_MAP_VERSION})

        # Store original methods
        original_load = self.panel.otw.load
        original_save = self.panel.otw.save

        # Replace with our custom methods
        def new_load(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.loads(f.read())

                    # Check if it's the new format or old format
                    if isinstance(data, dict) and "configs" in data:
                        # New format - convert to old format expected by OrderedTableWidget
                        old_format_data = {"metadata": data.get("metadata", {})}
                        for i, config in enumerate(data["configs"]):
                            old_format_data[str(i)] = {
                                "0": config.get("layer", ""),
                                "1": config.get("expression", ""),
                                "2": config.get("classIndex", 0),
                                "3": config.get("className", ""),
                            }
                        self.panel.otw.restore(old_format_data)
                    elif isinstance(data, dict) and any(
                        key.isdigit() for key in data.keys()
                    ):
                        # Old format - use directly
                        self.panel.otw.restore(data)
                    else:
                        # Try to load as list (fallback)
                        if isinstance(data, list):
                            old_format_data = {
                                "metadata": {"version": self.__ATTRIBUTE_MAP_VERSION}
                            }
                            for i, config in enumerate(data):
                                old_format_data[str(i)] = {
                                    "0": config.get("layer", ""),
                                    "1": config.get("expression", ""),
                                    "2": config.get("classIndex", 0),
                                    "3": config.get("className", ""),
                                }
                            self.panel.otw.restore(old_format_data)
                        else:
                            raise ValueError("Unsupported file format")

                self.messageBar.pushMessage(
                    self.tr("Success"),
                    self.tr("Configuration loaded successfully"),
                    level=Qgis.Success,
                    duration=3,
                )
            except Exception as e:
                QMessageBox.warning(
                    iface.mainWindow(),
                    self.tr("Unable to import {0}").format(filepath),
                    "Check file {0}:\n{1}".format(filepath, str(e)),
                )
                self.panel.otw.setHeaders(self.panel.otw.headers)

        def new_save(filepath):
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    # Create data in new format for better readability
                    data = {"metadata": self.panel.otw.metadata(True), "configs": []}

                    # Read values directly from the table widgets
                    for row in range(self.panel.otw.rowCount()):
                        layerValue = self.panel.otw.getValue(row, 0)

                        # Handle layer object vs string
                        if hasattr(layerValue, "name"):
                            layerName = layerValue.name()
                        else:
                            layerName = str(layerValue) if layerValue else ""

                        config = {
                            "layer": layerName,
                            "expression": self.panel.otw.getValue(row, 1) or "",
                            "classIndex": int(self.panel.otw.getValue(row, 2) or 0),
                            "className": self.panel.otw.getValue(row, 3) or "",
                        }
                        data["configs"].append(config)

                    f.write(json.dumps(data, indent=4, ensure_ascii=False))
                    self.messageBar.pushMessage(
                        self.tr("Success"),
                        self.tr(
                            "Layers configuration successfully exported to {0}"
                        ).format(filepath),
                        level=Qgis.Success,
                        duration=5,
                    )
            except Exception as e:
                QMessageBox.warning(
                    iface.mainWindow(),
                    self.tr("Unable to export {0}").format(filepath),
                    "Check file {0}:\n{1}".format(filepath, str(e)),
                )

        # Apply our custom methods
        self.panel.otw.load = new_load
        self.panel.otw.save = new_save

        return self.panel

    def parentLayerChanged(self, layer=None):
        pass

    def setLayer(self, layer):
        pass

    def setValue(self, value):
        """
        Sets back parameters to the GUI. Method reimplementation.
        :param value: (list) list of layer configurations to be set.
        """
        if not value:
            return
        otw = self.panel.otw
        isNotModeler = self.dialogType != DIALOG_MODELER

        # Handle different input formats
        configs = []
        if isinstance(value, dict) and "configs" in value:
            # New JSON format
            configs = value["configs"]
        elif isinstance(value, list):
            # Direct list format
            configs = value
        elif isinstance(value, dict):
            # Old format - convert from numbered keys
            for key in sorted(value.keys()):
                if key.isdigit():
                    item = value[key]
                    configs.append(
                        {
                            "layer": item.get("0", ""),
                            "expression": item.get("1", ""),
                            "classIndex": int(item.get("2", 0)),
                            "className": item.get("3", ""),
                        }
                    )

        for config in configs:
            try:
                layer = config.get("layer")
                expression = config.get("expression", "")
                classIndex = int(config.get("classIndex", 0))
                className = config.get("className", "")

                if isNotModeler and isinstance(layer, str):
                    # Try to find layer by name in project
                    layers = QgsProject.instance().mapLayersByName(layer)
                    if layers:
                        layer = layers[0]
                    else:
                        # Skip if layer not found
                        continue
                elif not isNotModeler:
                    # For modeler, keep as string
                    layer = (
                        layer
                        if isinstance(layer, str)
                        else (layer.name() if hasattr(layer, "name") else str(layer))
                    )

                if layer:  # Only add if we have a valid layer
                    otw.addRow(
                        {
                            0: layer,
                            1: expression,
                            2: classIndex,
                            3: className,
                        }
                    )
            except (ValueError, TypeError) as e:
                # Skip invalid configurations
                continue

    def readStandardPanel(self):
        """
        Reads widget's contents when process' parameters are set from an
        algorithm call (e.g. Processing toolbox).
        """
        configList = []
        otw = self.panel.otw

        for row in range(otw.rowCount()):
            try:
                layer = otw.getValue(row, 0)
                expression = otw.getValue(row, 1) or ""
                classIndex = otw.getValue(row, 2)
                className = otw.getValue(row, 3) or ""

                # Ensure classIndex is an integer
                if isinstance(classIndex, str) and classIndex.isdigit():
                    classIndex = int(classIndex)
                elif not isinstance(classIndex, int):
                    classIndex = 0

                if layer:
                    configList.append(
                        {
                            "layer": layer,
                            "expression": expression.strip(),
                            "classIndex": classIndex,
                            "className": className.strip(),
                        }
                    )
            except Exception as e:
                # Skip invalid rows
                continue
        return configList

    def readModelerPanel(self):
        """
        Reads widget's contents when process' parameters are set from a modeler
        instance.
        """
        configList = []
        otw = self.panel.otw

        for row in range(otw.rowCount()):
            try:
                layerName = otw.getValue(row, 0)
                expression = otw.getValue(row, 1) or ""
                classIndex = otw.getValue(row, 2)
                className = otw.getValue(row, 3) or ""

                # Ensure classIndex is an integer
                if isinstance(classIndex, str) and classIndex.isdigit():
                    classIndex = int(classIndex)
                elif not isinstance(classIndex, int):
                    classIndex = 0

                if layerName:
                    # Try to find actual layer object
                    layer = layerName
                    if isinstance(layerName, str):
                        layers = QgsProject.instance().mapLayersByName(layerName)
                        if layers and isinstance(layers[0], QgsVectorLayer):
                            layer = layers[0]

                    configList.append(
                        {
                            "layer": layer,
                            "expression": expression.strip(),
                            "classIndex": classIndex,
                            "className": className.strip(),
                        }
                    )
            except Exception as e:
                # Skip invalid rows
                continue
        return configList

    def readBatchPanel(self):
        """
        Reads widget's contents when process' parameters are set from a batch
        processing instance.
        """
        return self.readStandardPanel()

    def validate(self, pushAlert=False):
        """
        Validates fields. Returns True if all information are filled correctly.
        :param pushAlert: (bool) whether invalidation reason should be
                          displayed on the widget.
        :return: (bool) whether set of filled parameters is valid.
        """
        inputMap = {
            DIALOG_STANDARD: self.readStandardPanel,
            DIALOG_MODELER: self.readModelerPanel,
            DIALOG_BATCH: self.readBatchPanel,
        }[self.dialogType]()

        if len(inputMap) == 0:
            if pushAlert:
                self.messageBar.pushMessage(
                    self.tr("Please provide at least 1 layer configuration."),
                    level=Qgis.Warning,
                    duration=5,
                )
            return False

        # Check for duplicate class indices
        classIndices = []
        for row, config in enumerate(inputMap):
            layer = config.get("layer")
            classIndex = config.get("classIndex")

            if not layer:
                if pushAlert:
                    self.messageBar.pushMessage(
                        self.tr("Layer is required in row {0}.").format(row + 1),
                        level=Qgis.Warning,
                        duration=5,
                    )
                return False

            # if classIndex in classIndices:
            #     if pushAlert:
            #         self.messageBar.pushMessage(
            #             self.tr("Duplicate class index {0} in row {1}.").format(
            #                 classIndex, row + 1
            #             ),
            #             level=Qgis.Warning,
            #             duration=5,
            #         )
            #     return False
            # classIndices.append(classIndex)

        return True

    def value(self):
        """
        Retrieves parameters from current widget. Method reimplementation.
        :return: (list) value currently set to the GUI.
        """
        if self.validate(pushAlert=True):
            return {
                DIALOG_STANDARD: self.readStandardPanel,
                DIALOG_MODELER: self.readModelerPanel,
                DIALOG_BATCH: self.readBatchPanel,
            }[self.dialogType]()

    def postInitialize(self, wrappers):
        pass
