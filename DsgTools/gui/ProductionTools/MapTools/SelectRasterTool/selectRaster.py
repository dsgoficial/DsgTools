# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2021-11-09
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Jossan Costa - Surveying Technician @ Brazilian Army
                               (C) 2022 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : jossan.costa@eb.mil.br
                               borba.philipe@eb.mil.br
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.core import QgsRasterLayer, QgsRectangle, QgsProject
from qgis.gui import QgsMapTool
from PyQt5 import QtWidgets, QtGui


class SelectRasterTool(QgsMapTool):
    def __init__(self, iface):
        self.rasters = []
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        super(SelectRasterTool, self).__init__(self.canvas)

    def addTool(self, manager, callback, parentToolbar, iconBasePath):
        icon_path = iconBasePath + "/selectRaster.png"
        toolTip = self.tr("DSGTools: Select Raster")
        action = manager.add_action(
            icon_path,
            text=self.tr("DSGTools: Select Raster"),
            callback=callback,
            add_to_menu=False,
            add_to_toolbar=False,
            withShortcut=True,
            tooltip=toolTip,
            parentToolbar=parentToolbar,
            isCheckable=True,
        )
        self.setAction(action)

    def setAction(self, action):
        self.toolAction = action
        self.toolAction.setCheckable(True)

    def canvasPressEvent(self, e):
        self.run()

    def run(self):
        self.rasters = self.getRasters()
        if not (len(self.rasters) > 0):
            return
        self.openRastersMenu(self.rasters)

    def getRasters(self):
        rasters = []
        rect = self.getCursorRect()
        for layer in QgsProject.instance().mapLayers().values():
            if not isinstance(layer, QgsRasterLayer):
                continue
            bbRect = (
                self.iface.mapCanvas().mapSettings().mapToLayerCoordinates(layer, rect)
            )
            if not layer.extent().intersects(bbRect):
                continue
            rasters.append(layer)
        return rasters

    def getCursorRect(self):
        p = QgsMapTool(self.iface.mapCanvas()).toMapCoordinates(
            self.iface.mapCanvas().mouseLastXY()
        )
        w = self.iface.mapCanvas().mapUnitsPerPixel() * 10
        return QgsRectangle(p.x() - w, p.y() - w, p.x() + w, p.y() + w)

    def openRastersMenu(self, rasters):
        menu = QtWidgets.QMenu()
        self.addRasterMenu(menu, rasters)
        menu.exec_(QtGui.QCursor.pos())

    def addRasterMenu(self, menu, rasters):
        rasterMenu = menu  # QtWidgets.QMenu(title="Rasters", parent=menu)
        for raster in rasters:
            action = rasterMenu.addAction(raster.name())
            action.triggered.connect(lambda b, raster=raster: self.selectOnly(raster))
        dummyAction = rasterMenu.addAction("")
        dummyAction.setSeparator(True)
        action = rasterMenu.addAction(self.tr("Deselect all rasters"))
        action.triggered.connect(lambda x: self.selectAll(visible=False))

    def selectOnly(self, raster):
        for otherRaster in self.rasters:
            self.iface.layerTreeView().setLayerVisible(
                otherRaster, otherRaster.id() == raster.id()
            )
        self.toolAction.setChecked(False)

    def selectAll(self, visible=True):
        for otherRaster in self.rasters:
            self.iface.layerTreeView().setLayerVisible(otherRaster, visible)
        self.toolAction.setChecked(False)

    def unload(self):
        self.deactivate()
        try:
            self.iface.unregisterMainWindowAction(self.toolAction)
        except:
            pass
