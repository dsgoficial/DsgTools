# -*- coding: utf-8 -*-
from PyQt4.QtGui import QIcon, QPixmap, QAction
from qgis.gui import QgsMessageBar
from circle import Circle
from polygon import Polygon

class Acquisition:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.tool = None

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
            if layer.geometryType() == 2:
                self.tool = func(self.canvas, self.iface, action)
                self.tool.setAction(action)
                self.canvas.setMapTool(self.tool)
            else:
                self.iface.messageBar().pushMessage(u"Aviso", u"Ferramenta utilizada apenas em polígonos !",
                                                                    level=QgsMessageBar.INFO, duration=6)
                self.tool.deactivate()
        else:
            self.iface.messageBar().pushMessage(u"Aviso", u"Inicie a Edição da Feição!", level=QgsMessageBar.INFO, duration=6)
            self.tool.deactivate()
                                    
            
