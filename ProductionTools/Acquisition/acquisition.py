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

    def acquisitionNinetyDegrees(self):
        self.run(Polygon)

    def acquisitionCircle(self):
        self.run(Circle)
            
    def run(self, func):
        layer = self.canvas.currentLayer()
        if layer in self.iface.editableLayers():
            if layer.geometryType() == 2:
                self.tool = func(self.canvas, self.iface)
                self.canvas.setMapTool(self.tool)
            else:
                self.iface.messageBar().pushMessage(u"Aviso", u"Ferramenta utilizada apenas em polígonos !",
                                                                    level=QgsMessageBar.INFO, duration=6)
        else:
            self.iface.messageBar().pushMessage(u"Aviso", u"Inicie a Edição da Feição!",
                                                                    level=QgsMessageBar.INFO, duration=6)
            
