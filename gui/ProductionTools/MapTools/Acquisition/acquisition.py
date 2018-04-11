# -*- coding: utf-8 -*-
from __future__ import absolute_import
from qgis.PyQt.QtGui import QIcon, QPixmap
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.Qt import QObject
from qgis.gui import QgsMessageBar
from qgis.core import Qgis, Qgis, QgsWkbTypes
from .circle import Circle
from .polygon import Polygon

class Acquisition(QObject):
    def __init__(self, iface):
        super(Acquisition, self).__init__()
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.tool = None
    
    def addTool(self, manager, callback, parentMenu, iconBasePath):
        icon_path = iconBasePath + 'home.png'
        toolTip = self.tr("DSGTools: Right Degree Angle Digitizing\nControl modifier: disables tool while control is pressed.")
        action = manager.add_action(
            icon_path,
            text=self.tr('DSGTools: Right Degree Angle Digitizing'),
            callback=self.acquisitionNinetyDegrees,
            add_to_menu=True,
            add_to_toolbar=True,
            withShortcut = True,
            tooltip = toolTip,
            parentToolbar =parentMenu
            )
        self.setPolygonAction(action)

        icon_path = iconBasePath +'circle.png'
        action = manager.add_action(
            icon_path,
            text=self.tr('DSGTools: Circle Digitizing'),
            callback=self.acquisitionCircle,
            add_to_menu=True,
            add_to_toolbar=True,
            withShortcut = True,
            parentToolbar =parentMenu)
        self.setCircleAction(action)

    def setPolygonAction(self, action):
        self.polygonAction = action
    
    def setCircleAction(self, action):
        self.circleAction = action

    def acquisitionNinetyDegrees(self):
        self.run(Polygon, self.polygonAction)

    def acquisitionCircle(self):
        self.run(Circle, self.circleAction)
            
    def run(self, func, action):
        layer = self.canvas.currentLayer()
        if layer in self.iface.editableLayers():
            if layer.geometryType() in [QgsWkbTypes.LineGeometry , QgsWkbTypes.PolygonGeometry]:
                if self.tool:
                    self.tool.deactivate()
                self.tool = func(self.canvas, self.iface, action)
                self.tool.setAction(action)
                self.canvas.setMapTool(self.tool)
            else:
                self.iface.messageBar().pushMessage(self.tr('Warning'), self.tr('Tool not defined for points'),
                                                                    level=Qgis.Info, duration=3)
                self.tool.deactivate() if self.tool else ""
        else:
            self.iface.messageBar().pushMessage(self.tr('Warning'), self.tr('Start editing in current layer!'), level=Qgis.Info, duration=3)
            self.tool.deactivate() if self.tool else ""
                                    
            
