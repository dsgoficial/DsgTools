# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2021-06-08
        git sha              : $Format:%H$
        copyright            : (C) 2021 by Jossan Costa - Surveying Technician @ Brazilian Army
        email                : jossan.costa@eb.mil.br
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

from qgis import gui, core
from qgis.utils import iface
from PyQt5 import QtGui, QtCore


class SpatialFilter:
    def __init__(self):
        self.previousMapTool = iface.mapCanvas().mapTool()
        self.myMapTool = gui.QgsMapToolEmitPoint(iface.mapCanvas())
        self.coordinates = []
        self.isEditing = 0
        self.isActive = False
        self.myMapTool.canvasClicked.connect(self.mouseClick)
        self.myMapTool.keyReleaseEvent = (
            lambda event: self.disconnect()
            if event.key() == QtCore.Qt.Key_Escape
            else ""
        )

    def start(self):
        self.isActive = not self.isActive
        if self.isActive:
            self.myRubberBand = gui.QgsRubberBand(
                iface.mapCanvas(), core.QgsWkbTypes.PolygonGeometry
            )
            color = QtGui.QColor(78, 97, 114)
            color.setAlpha(190)
            self.myRubberBand.setColor(color)
            self.myRubberBand.setFillColor(QtGui.QColor(255, 0, 0, 40))

            # Set MapTool
            iface.mapCanvas().setMapTool(self.myMapTool)
            iface.mapCanvas().xyCoordinates.connect(self.mouseMove)
        else:
            self.disconnect()

    def disconnect(self):
        self.isActive = False
        self.coordinates = []
        iface.mapCanvas().unsetMapTool(self.myMapTool)
        try:
            iface.mapCanvas().xyCoordinates.disconnect(self.mouseMove)
        except:
            pass

        try:
            self.myRubberBand.reset()
        except:
            pass

    def mouseClick(self, currentPos, clickedButton):
        if (
            clickedButton == QtCore.Qt.LeftButton
        ):  # and myRubberBand.numberOfVertices() == 0:
            self.myRubberBand.addPoint(core.QgsPointXY(currentPos))
            self.coordinates.append(core.QgsPointXY(currentPos))
            self.isEditing = 1

        elif (
            clickedButton == QtCore.Qt.RightButton
            and self.myRubberBand.numberOfVertices() > 2
        ):
            self.isEditing = 0

            # create feature and set geometry.

            poly = core.QgsFeature()
            geomP = self.myRubberBand.asGeometry()
            poly.setGeometry(geomP)
            g = geomP.asWkt()  # Get WKT coordenates.

            canvas = iface.mapCanvas()

            c = canvas.mapSettings().destinationCrs().authid()  # Get EPSG.
            rep = c.replace("EPSG:", "")

            vlyr = core.QgsVectorLayer(
                "?query=SELECT geom_from_wkt('%s') as geometry&geometry=geometry:3:%s"
                % (g, rep),
                "Polygon_Reference",
                "virtual",
            )

            core.QgsProject.instance().addMapLayer(vlyr)
            self.myRubberBand.reset(core.QgsWkbTypes.PolygonGeometry)
            string = f"(geom && ST_GEOMFROMEWKT('SRID={rep};{g}')) AND ST_INTERSECTS(geom, ST_GEOMFROMEWKT('SRID={rep};{g}'))"
            layers = core.QgsProject.instance().mapLayers().values()

            layersBacklist = self.getLayersBacklist()

            for layer in layers:
                if (
                    not isinstance(layer, core.QgsVectorLayer)
                    or layer.dataProvider().name() != "postgres"
                    or layer.dataProvider().uri().table() in layersBacklist
                ):
                    continue
                try:
                    layer.setSubsetString(string)
                except Exception:
                    pass

            self.myRubberBand.reset(core.QgsWkbTypes.PolygonGeometry)
            self.disconnect()

    def getLayersBacklist(self):
        return ["aux_moldura_a"]

    def mouseMove(self, currentPos):
        if self.isEditing == 1:
            self.myRubberBand.movePoint(core.QgsPointXY(currentPos))
