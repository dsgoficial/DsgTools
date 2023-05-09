# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-05-23
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Ronaldo Martins da Silva Junior - Cartographic Engineer @ Brazilian Army
        email                : ronaldomartins.silva@eb.mil.br
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

from qgis.core import (
    QgsDistanceArea,
    QgsCoordinateTransformContext,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsProject,
    QgsGeometry,
)

from DsgTools.gui.ProductionTools.MapTools.Acquisition.toolTip import ToolTip


class DistanceToolTip(ToolTip):
    def __init__(self, iface, minSegmentDistance, decimals):
        super(DistanceToolTip, self).__init__(iface)
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.last_distance = 0
        self.showing = False
        self.minSegmentDistance = minSegmentDistance
        self.decimals = decimals

    def calculateDistance(self, p1, p2):
        source_crs = self.iface.mapCanvas().mapSettings().destinationCrs()
        dest_crs = QgsCoordinateReferenceSystem(3857)
        tr = QgsCoordinateTransform(
            source_crs, dest_crs, QgsCoordinateTransformContext()
        )
        p1t = QgsGeometry().fromPointXY(p1)
        p1t.transform(tr)
        p2t = QgsGeometry().fromPointXY(p2)
        p2t.transform(tr)
        distance = QgsDistanceArea()
        m = distance.measureLine(p1t.asPoint(), p2t.asPoint())
        return m

    def canvasMoveEvent(self, last_p, current_p):
        m = float(self.calculateDistance(last_p, current_p))
        if self.showing:
            if m != self.last_distance:
                color = "red"
                if m >= self.minSegmentDistance:
                    color = "green"
                txt = f"<p style='color:{color}'><b>{m:.{self.decimals}f}</b></p>"
                self.show(txt, current_p)
                self.last_distance = m
        else:
            if m > 1:
                color = "red"
                if m >= self.minSegmentDistance:
                    color = "green"
                txt = f"<p style='color:{color}'><b>{m:.{self.decimals}f}</b></p>"
                super(DistanceToolTip, self).show(txt, current_p)
                self.last_distance = m
                self.showing = True

    def deactivate(self):
        self.deactivate()
        self.showing = False
