from qgis import gui, core
from qgis.utils import iface
from PyQt5 import QtCore, uic, QtWidgets, QtGui


class SelectRaster:
    def __init__(self):
        self.rasters = []

    def execute(self):
        self.rasters = self.getRasters()
        if not (len(self.rasters) > 0):
            return
        self.openRastersMenu(self.rasters)

    def getRasters(self):
        rasters = []
        rect = self.getCursorRect()
        layers = core.QgsProject.instance().mapLayers().values()
        for layer in layers:
            if not isinstance(layer, core.QgsRasterLayer):
                continue
            bbRect = iface.mapCanvas().mapSettings().mapToLayerCoordinates(layer, rect)
            if not layer.extent().intersects(bbRect):
                continue
            rasters.append(layer)
        return rasters

    def getCursorRect(self):
        p = gui.QgsMapTool(iface.mapCanvas()).toMapCoordinates(
            iface.mapCanvas().mouseLastXY()
        )
        w = iface.mapCanvas().mapUnitsPerPixel() * 10
        return core.QgsRectangle(p.x() - w, p.y() - w, p.x() + w, p.y() + w)

    def openRastersMenu(self, rasters):
        menu = QtWidgets.QMenu()
        self.addRasterMenu(menu, rasters)
        menu.exec_(QtGui.QCursor.pos())

    def addRasterMenu(self, menu, rasters):
        rasterMenu = menu  # QtWidgets.QMenu(title="Rasters", parent=menu)
        for raster in rasters:
            action = rasterMenu.addAction(raster.name())
            action.triggered.connect(lambda b, raster=raster: self.selectOnly(raster))
        # menu.addMenu(rasterMenu)

    def selectOnly(self, raster):
        for otherRaster in self.rasters:
            if otherRaster.id() == raster.id():
                iface.layerTreeView().setLayerVisible(otherRaster, True)
                continue
            iface.layerTreeView().setLayerVisible(otherRaster, False)
