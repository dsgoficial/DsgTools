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

from functools import partial

from qgis.PyQt.QtCore import QSettings, QObject

from qgis.core import QgsProject, QgsVectorLayer
from qgis.gui import QgsMapTool

from .EventFilter import EventFilter
from .PointList import PointList


class MeasureTool(QObject):
    def __init__(self, iface):
        """
        Hides or show active layers labels.
        """
        self.iface = iface
        super(MeasureTool, self).__init__()
        self.toolAction = None
        self.pointList = PointList()

    def addTool(self, manager, callback, parentToolbar, stackButton, iconBasePath):
        self.stackButton = stackButton
        icon_path = iconBasePath + "/measure_tool.png"
        toolTip = self.tr("DSGTools: Measure while digititizing")
        action = manager.add_action(
            icon_path,
            text=self.tr("DSGTools: Measure while digititizing"),
            callback=self.measure,
            add_to_menu=False,
            add_to_toolbar=True,
            withShortcut=True,
            tooltip=toolTip,
            parentButton=stackButton,
            isCheckable=True,
        )
        self.setAction(action)
    
    def setAction(self, action):
        self.toolAction = action
        self.toolAction.setCheckable(True)
        self.eventFilter = EventFilter(self.iface, self.pointList, self.toolAction)
        self.iface.mapCanvas().viewport().setMouseTracking(True)
        self.iface.mapCanvas().viewport().installEventFilter( self.eventFilter )
        self.iface.mapCanvas().installEventFilter( self.eventFilter )
        self.iface.mapCanvas().mapToolSet.connect(self.maptoolChanged)
    
    def measure(self):
        pass

    def maptoolChanged(self):
        self.eventFilter.active = (self.iface.mapCanvas().mapTool() is not None and self.iface.mapCanvas().mapTool().flags() == QgsMapTool.EditTool)

    def unload(self):
        self.eventFilter.close()
        self.iface.mapCanvas().viewport().removeEventFilter( self.eventFilter )
        self.iface.mapCanvas().removeEventFilter( self.eventFilter )

        # e remova o sinal maptoolchanded isEditTool
        self.iface.mapCanvas().mapToolSet.disconnect( self.maptoolChanged )
