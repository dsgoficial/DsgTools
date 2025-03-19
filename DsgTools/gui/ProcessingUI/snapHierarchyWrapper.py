# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-09-19
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import json
from qgis.core import Qgis
from qgis.gui import QgsMapLayerComboBox, QgsMessageBar
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.utils import iface
from qgis.PyQt.QtWidgets import QComboBox, QLineEdit, QDoubleSpinBox
from qgis.PyQt.QtCore import QSize, QRegExp
from processing.gui.wrappers import (
    WidgetWrapper,
    DIALOG_STANDARD,
    DIALOG_MODELER,
    DIALOG_BATCH,
)

from DsgTools.gui.CustomWidgets.OrderedPropertyWidgets.orderedTableWidget import (
    OrderedTableWidget,
)


class SnapHierarchyWrapper(WidgetWrapper):
    def __init__(self, *args, **kwargs):
        super(SnapHierarchyWrapper, self).__init__(*args, **kwargs)
        self.messageBar = QgsMessageBar(self.panel)

    def mapLayerComboBox(self):
        """
        Retrieves the configured map layer selection combo box.
        :return: (QgsMapLayerComboBox) configured layer selection widget.
        """
        cb = QgsMapLayerComboBox()
        return cb

    def doubleSpinBox(self):
        """
        Retrieves the configured map layer selection combo box.
        :return: (QgsMapLayerComboBox) configured layer selection widget.
        """
        sb = QDoubleSpinBox()
        sb.setDecimals(10)
        return sb

    def mapLayerModelDialog(self):
        """
        Retrieves widget for map layer selection in a model dialog setup.
        :return: (QLineEdit) map layer setter widget for processing dialog
                 mode.
        """
        le = QLineEdit()
        le.setPlaceholderText(self.tr("Set layer name..."))
        return le

    def modeComboBox(self):
        """
        Retrieves a new widget for snap mode selection.
        :return: (QComboBox) snap mode selection widget.
        """
        cb = QComboBox()
        cb.addItems(
            [
                self.tr("Prefer aligning nodes, insert extra vertices where required"),
                self.tr("Prefer closest point, insert extra vertices where required"),
                self.tr("Prefer aligning nodes, don't insert new vertices"),
                self.tr("Prefer closest point, don't insert new vertices"),
                self.tr("Move end points only, prefer aligning nodes"),
                self.tr("Move end points only, prefer closest point"),
                self.tr("Snap end points to end points only"),
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
                    "widget": self.mapLayerComboBox,
                    "setter": "setCurrentText",
                    "getter": "currentText",
                },
                1: {
                    "header": self.tr("Snap"),
                    "type": "widget",
                    "widget": self.doubleSpinBox,
                    "setter": "setValue",
                    "getter": "value",
                },
                2: {
                    "header": self.tr("Snap mode"),
                    "type": "widget",
                    "widget": self.modeComboBox,
                    "setter": "setCurrentIndex",
                    "getter": "currentIndex",
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
                    "widget": self.mapLayerModelDialog,
                    "setter": "setText",
                    "getter": "text",
                },
                1: {
                    "header": self.tr("Snap"),
                    "type": "widget",
                    "widget": self.doubleSpinBox,
                    "setter": "setValue",
                    "getter": "value",
                },
                2: {
                    "header": self.tr("Snap mode"),
                    "type": "widget",
                    "widget": self.modeComboBox,
                    "setter": "setCurrentIndex",
                    "getter": "currentIndex",
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
        
        # Create message bar specifically for this panel
        self.messageBar = QgsMessageBar(self.panel)
        
        # Initial positioning of the message bar
        self.messageBar.move(0, 0)
        self.messageBar.resize(self.panel.width(), 30)
        
        # Store the original resize event method
        original_resize_event = self.panel.resizeEvent
        
        # Define a new resize event method that properly handles the message bar
        def custom_resize_event(event):
            # Position the message bar at the top with the full width
            self.messageBar.move(0, 0)
            self.messageBar.resize(self.panel.width(), 30)
            
            # Call the original resize event handler
            if original_resize_event:
                original_resize_event(event)
        
        # Replace the panel's resize event with our custom handler
        self.panel.resizeEvent = custom_resize_event
        
        # Store original methods
        original_load = self.panel.load
        original_save = self.panel.save
        
        # Capture the message bar in the closure for the save function
        messageBar = self.messageBar
        
        # Replace with our custom methods
        def new_load(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.loads(f.read())
                    
                    # Convert new format to old format if needed
                    if self._isNewFormat(data):
                        data = self._convertNewFormatToOld(data)
                    
                    # Use original restore method with data in old format
                    self.panel.restore(data)
                    
                    # Show success message
                    messageBar.pushMessage(
                        self.tr("Success"),
                        self.tr("Snap settings successfully loaded from {0}").format(filepath),
                        level=Qgis.Success,
                        duration=5
                    )
            except Exception as e:
                QMessageBox.warning(
                    iface.mainWindow(),
                    self.tr("Unable to import {0}").format(filepath),
                    "Check file {0}:\n{1}".format(filepath, "\n".join(e.args)),
                )
                self.panel.setHeaders(self.panel.headers)
        
        def new_save(filepath):
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    # Create new format structure
                    new_data = {
                        "metadata": self.panel.metadata(True),
                        "snapSettings": []
                    }
                    
                    # Read values directly from the table
                    for row in range(self.panel.rowCount()):
                        setting = {
                            "layer": self.panel.getValue(row, 0),
                            "snap": self.panel.getValue(row, 1),
                            "mode": self.panel.getValue(row, 2)
                        }
                        new_data["snapSettings"].append(setting)
                    
                    # Save in the new format
                    f.write(json.dumps(new_data, indent=4))
                    
                    # Show success message using the captured message bar
                    messageBar.pushMessage(
                        self.tr("Success"),
                        self.tr("Snap settings successfully exported to {0}").format(filepath),
                        level=Qgis.Success,
                        duration=5
                    )
            except Exception as e:
                QMessageBox.warning(
                    iface.mainWindow(),
                    self.tr("Unable to export {0}").format(filepath),
                    "Check file {0}:\n{1}".format(filepath, "\n".join(e.args)),
                )
        
        # Apply our custom methods
        self.panel.load = new_load
        self.panel.save = new_save
        
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
            self.panel.addRow(
                {
                    0: valueMap["referenceLayer"],
                    1: valueMap["snap"],
                    2: valueMap["mode"],
                }
            )

    def readStandardPanel(self):
        """
        Reads widget's contents when process' parameters are set from an
        algorithm call (e.g. Processing toolbox).
        """
        valueMaplist = list()
        layers = [self.panel.getValue(r, 0) for r in range(self.panel.rowCount())]
        for row in range(self.panel.rowCount()):
            values = dict()
            values["referenceLayer"] = self.panel.getValue(row, 0)
            values["snap"] = self.panel.getValue(row, 1)
            values["mode"] = self.panel.getValue(row, 2)
            values["snapLayerList"] = [l for l in layers[(row + 1) : :]]
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

    def _isNewFormat(self, data):
        """
        Detects if the data is in the new format.
        :param data: (dict) The data to check
        :return: (bool) True if new format, False otherwise
        """
        return isinstance(data, dict) and "snapSettings" in data

    def _convertNewFormatToOld(self, data):
        """
        Converts data from new format to old format for compatibility.
        :param data: (dict) Data in new format
        :return: (dict) Data in old format
        """
        result = {"metadata": data.get("metadata", {})}
        
        for i, setting in enumerate(data.get("snapSettings", [])):
            result[str(i)] = {
                "0": setting.get("layer", ""),
                "1": setting.get("snap", ""),
                "2": setting.get("mode", "")
            }
        
        return result
