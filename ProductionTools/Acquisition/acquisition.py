# -*- coding: utf-8 -*-
from PyQt4.QtGui import QIcon, QPixmap, QAction
from PyQt4.Qt import QObject
from qgis.gui import QgsMessageBar
from qgis.core import QGis, QgsVectorLayer
from circle import Circle
from polygon import Polygon

class Acquisition(QObject):
    def __init__(self, iface):
        super(Acquisition, self).__init__()
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.tool = None
        self.iface.currentLayerChanged.connect(self.checkToDeactivate)
        self.iface.actionToggleEditing().triggered.connect(self.setToolsEnabled)
        self.polygonAction = None
        self.circleAction = None

    def setPolygonAction(self, action):
        self.polygonAction = action
    
    def setCircleAction(self, action):
        self.circleAction = action

    def acquisitionNinetyDegrees(self):
        self.run(Polygon, self.polygonAction)

    def acquisitionCircle(self):
        self.run(Circle, self.circleAction)
    
    def checkToDeactivate(self, layer):
        enabled = self.setToolsEnabled(layer)
        if not enabled and self.tool:
            self.tool.deactivate()
    
    def setToolsEnabled(self, layer):
        if isinstance(self.sender(), QAction):
            layer = self.iface.mapCanvas().currentLayer()
        if not layer or not isinstance(layer, QgsVectorLayer) or layer.geometryType() == QGis.Point or not layer.isEditable():
            enabled = False
        else:
            enabled = True
        if self.polygonAction:
            self.polygonAction.setEnabled(enabled)
        if self.circleAction:
            self.circleAction.setEnabled(enabled)
        return enabled
            
    def run(self, func, action):
        layer = self.canvas.currentLayer()
        if layer in self.iface.editableLayers():
            if layer.geometryType() in [QGis.Line , QGis.Polygon]:
                if self.tool:
                    self.tool.deactivate()
                self.tool = func(self.canvas, self.iface, action)
                self.tool.setAction(action)
                self.canvas.setMapTool(self.tool)
            else:
                self.iface.messageBar().pushMessage(self.tr('Warning'), self.tr('Tool not defined for points'),
                                                                    level=QgsMessageBar.INFO, duration=3)
                self.tool.deactivate() if self.tool else ""
        else:
            self.iface.messageBar().pushMessage(self.tr('Warning'), self.tr('Start editing in current layer!'), level=QgsMessageBar.INFO, duration=3)
            self.tool.deactivate() if self.tool else ""
                                    
            
