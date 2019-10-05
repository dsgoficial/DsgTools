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

from qgis.gui import QgsMapLayerComboBox
from qgis.PyQt.QtWidgets import QDoubleSpinBox, QComboBox
from processing.gui.wrappers import (WidgetWrapper,
                                     DIALOG_STANDARD,
                                     DIALOG_MODELER,
                                     DIALOG_BATCH)

from DsgTools.gui.CustomWidgets.OrderedPropertyWidgets.orderedTableWidget import OrderedTableWidget

class SnapHierarchyWrapper(WidgetWrapper):
    def __init__(self, *args, **kwargs):
        super(SnapHierarchyWrapper, self).__init__(*args, **kwargs)

    def mapLayerComboBox(self):
        """
        Retrieves the configured map layer selection combo box.
        :return: (QgsMapLayerComboBox) configured layer selection widget. 
        """
        cb = QgsMapLayerComboBox()
        return cb

    def modeComboBox(self):
        """
        Retrieves a new widget for snap mode selection.
        """
        cb = QComboBox()
        cb.addItems([
            self.tr('Prefer aligning nodes, insert extra vertices where required'),
            self.tr('Prefer closest point, insert extra vertices where required'),
            self.tr('Prefer aligning nodes, don\'t insert new vertices'),
            self.tr('Prefer closest point, don\'t insert new vertices'),
            self.tr('Move end points only, prefer aligning nodes'),
            self.tr('Move end points only, prefer closest point'),
            self.tr('Snap end points to end points only')
        ])
        return cb

    def createPanel(self):
        return OrderedTableWidget(headerMap={
            0 : {
                "header" : self.tr("Layer"),
                "type" : "widget",
                "widget" : QgsMapLayerComboBox,
                "setter" : "setCurrentText",
                "getter" : "currentText"
            },
            1 : {
                "header" : self.tr("Snap"),
                "type" : "widget",
                "widget" : QDoubleSpinBox,
                "setter" : "setValue",
                "getter" : "value"
            },
            2 : {
                "header" : self.tr("Snap mode"),
                "type" : "widget",
                "widget" : self.modeComboBox,
                "setter" : "setCurrentIndex",
                "getter" : "currentIndex"
            }
        })
    
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
        value = json.loads(value)
        # self.panel = self.createPanel()
        for valueMap in value:
            self.panel.addRow({
                0 : valueMap["referenceLayer"],
                1 : valueMap["snap"],
                2 : valueMap["mode"]
            })

    def readStandardPanel(self):
        """
        Reads widget's contents when process' parameters are set from an 
        algorithm call (e.g. Processing toolbox).
        """
        valueMaplist = list()
        layers = [
            self.panel.getValue(r, 0) for r in range(self.panel.rowCount())
        ]
        for row in range(self.panel.rowCount()):
            values = dict()
            values["referenceLayer"] = self.panel.getValue(row, 0)
            values["snap"] = self.panel.getValue(row, 1)
            values["mode"] = self.panel.getValue(row, 2)
            values["snapLayerList"] = [l for l in layers[(row + 1)::]]
            valueMaplist.append(values)
        return json.dumps(valueMaplist)

    def readModelerPanel(self):
        """
        Reads widget's contents when process' parameters are set from a modeler
        instance.
        """
        return self.readStandardPanel()

    def readBatchPanel(self):
        """
        
        """
        return

    def value(self):
        """
        Retrieves parameters from current widget. Method reimplementation.
        :return: (dict) value currently set to the GUI.
        """
        x = {
            DIALOG_STANDARD : self.readStandardPanel,
            DIALOG_MODELER : self.readModelerPanel,
            DIALOG_BATCH : self.readBatchPanel
        }[self.dialogType]()
        return x
    
    def postInitialize(self, wrappers):
        pass
        # for wrapper in wrappers:
        #     if wrapper.parameterDefinition().name() == self.parameterDefinition().parentLayerParameter():
        #         pass
