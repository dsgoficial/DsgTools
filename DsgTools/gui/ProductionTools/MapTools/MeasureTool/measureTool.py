# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2023-05-17
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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


from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QPushButton

from qgis.core import QgsDistanceArea, QgsWkbTypes, QgsVectorLayer
from qgis.gui import QgisInterface, QgsMapToolDigitizeFeature

from .EventFilter import EventFilter
from .PointList import PointList


class MeasureTool(QObject):
    def __init__(self, iface: QgisInterface):
        """
        Hides or show active layers labels.
        """
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        super(MeasureTool, self).__init__()
        self.toolAction = None
        self.distance_area = QgsDistanceArea()
        self.acquisitionTooltipButton = QPushButton()
        self.acquisitionTooltipButton.setToolTip(self.tr("Show acquisition tooltip"))
        self.pointList = PointList()
        self.eventFilter = None

    def addTool(self, manager, callback, parentToolbar, stackButton, iconBasePath):
        self.stackButton = stackButton
        icon_path = iconBasePath + "/measure_tool.png"
        toolTip = self.tr("DSGTools: Measure while digitizing")
        action = manager.add_action(
            icon_path,
            text=self.tr("DSGTools: Measure while digitizing"),
            callback=self.activateTool,
            add_to_menu=False,
            add_to_toolbar=True,
            withShortcut=True,
            tooltip=toolTip,
            parentButton=stackButton,
            isCheckable=True,
        )
        self.setAction(action)

    def activateTool(self):
        state = self.toolAction.isChecked()
        if state:
            self.canvas.mapToolSet.connect(self.activateFilterMapTool)
            if not isinstance(self.canvas.mapTool(), QgsMapToolDigitizeFeature):
                return
        else:
            try:
                self.canvas.mapToolSet.disconnect(self.activateFilterMapTool)
            except TypeError:
                pass
        self.activateFilter(state)

    def activateFilterMapTool(self, mapTool):
        state = isinstance(mapTool, QgsMapToolDigitizeFeature)
        self.activateFilter(state)

    def setToolEnabled(self):
        layer = self.iface.activeLayer()
        if (
            not isinstance(layer, QgsVectorLayer)
            or layer.geometryType() == QgsWkbTypes.PointGeometry
            or not layer.isEditable()
        ):
            enabled = False
        else:
            enabled = True
        if not enabled:
            self.closeAndRemoveEventFilter()
            self.toolAction.setChecked(False)
        self.toolAction.setEnabled(enabled)
        return enabled

    def activateFilter(self, state: bool):
        if state:
            self.eventFilter = EventFilter(self.iface, self.pointList)
            self.canvas.viewport().setMouseTracking(True)
            self.canvas.viewport().installEventFilter(self.eventFilter)
            self.canvas.installEventFilter(self.eventFilter)
        else:
            self.closeAndRemoveEventFilter()

    def setAction(self, action):
        self.toolAction = action
        self.toolAction.setCheckable(True)
        self.setToolEnabled()

    def closeAndRemoveEventFilter(self):
        if self.eventFilter is None:
            return
        self.eventFilter.close()
        self.canvas.viewport().removeEventFilter(self.eventFilter)
        self.canvas.removeEventFilter(self.eventFilter)
        self.eventFilter = None
        try:
            self.canvas.mapToolSet.disconnect(self.activateFilterMapTool)
        except TypeError:
            pass

    def unload(self):
        self.closeAndRemoveEventFilter()
