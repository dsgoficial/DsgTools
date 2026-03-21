# -*- coding: utf-8 -*-
"""
/***************************************************************************
ShapeTool
                                 A QGIS plugin
Builds a temp rubberband with a given size and shape.
                             -------------------
        begin                : 2016-08-02
        git sha              : $Format:%H$
        copyright            : (C) 2016 by  Jossan Costa - Surveying Technician @ Brazilian Army
                                            Felipe Diniz - Cartographic Engineer @ Brazilian Army
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

from math import sqrt, cos, sin, pi, atan2

from qgis.gui import QgsRubberBand, QgsMapTool
from qgis.core import (
    Qgis,
    QgsPointXY,
    QgsGeometry,
    QgsProject,
    QgsDistanceArea,
    QgsCoordinateTransform,
    QgsCoordinateTransformContext,
    QgsCoordinateReferenceSystem,
)
from qgis.PyQt import QtGui, QtCore, QtWidgets
from qgis.PyQt.QtCore import pyqtSignal, Qt
from qgis.PyQt.QtGui import QColor, QCursor
from qgis.PyQt.QtWidgets import QApplication


class ShapeTool(QgsMapTool):
    # signal emitted when the mouse is clicked. This indicates that the tool finished its job
    toolFinished = pyqtSignal()

    def __init__(
        self, canvas, geometryType, param, type, color=QColor(254, 178, 76, 63)
    ):
        """
        Constructor
        """
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.active = False
        self.geometryType = self.tr(geometryType)
        self.param = param
        self.type = type
        self.cursor = None
        self.rubberBand = QgsRubberBand(self.canvas, Qgis.GeometryType.Polygon)
        self.setColor(color)
        self.reset()
        self.rotAngle = 0
        self.currentCentroid = None
        self.rotate = False

    def setColor(self, mFillColor):
        """
        Adjusting the color to create the rubber band
        """

        self.rubberBand.setColor(mFillColor)
        self.rubberBand.setWidth(1)

    def reset(self):
        """
        Resetting the rubber band
        """
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        try:
            self.rubberBand.reset(Qgis.GeometryType.Polygon)
        except Exception:
            pass

    def rotateRect(self, centroid, e):
        """
        Calculates the angle for the rotation.
        """
        item_position = self.canvas.mapToGlobal(e.pos())
        c = self.toCanvasCoordinates(centroid)
        c = self.canvas.mapToGlobal(c)
        rotAngle = pi - atan2(item_position.y() - c.y(), item_position.x() - c.x())
        return rotAngle

    def canvasPressEvent(self, e):
        """
        When the canvas is pressed the tool finishes its job
        """
        # enforce mouse restoring if clicked right after rotation
        QApplication.restoreOverrideCursor()
        self.canvas.unsetMapTool(self)
        self.toolFinished.emit()

    def _baseDistanceInMeters(self):
        """
        Calculates the distance in meters of 2 points 1 unit map away on
        current canvas CRS.
        :return: (float) distance in meters between two points 1 map unit apart
                 from each other.
        """
        source_crs = self.canvas.mapSettings().destinationCrs()
        dest_crs = QgsCoordinateReferenceSystem.fromEpsgId(3857)
        tr = QgsCoordinateTransform(
            source_crs, dest_crs, QgsCoordinateTransformContext()
        )
        p1t = QgsGeometry().fromPointXY(QgsPointXY(1, 0))
        p1t.transform(tr)
        p2t = QgsGeometry().fromPointXY(QgsPointXY(0, 0))
        p2t.transform(tr)
        return QgsDistanceArea().measureLine(p1t.asPoint(), p2t.asPoint())

    def getAdjustedSize(self, size):
        """
        If map unit is not metric, the figure to be drawn needs to have its
        size adjusted. This is necessary because input parameters are designed
        to be meters on tool's GUI.
        :param size: (float) tool's radius/length reference size in meters.
        :return: (float)
        """
        source_crs = self.canvas.mapSettings().destinationCrs()
        if source_crs.mapUnits() != Qgis.DistanceUnit.Meters:
            return size / self._baseDistanceInMeters()
        return size

    def canvasMoveEvent(self, e):
        """
        Deals with mouse move event to update the rubber band position in the canvas
        """
        ctrlIsHeld = QApplication.keyboardModifiers() == Qt.KeyboardModifier.ControlModifier
        if e.button() != None and not ctrlIsHeld:
            if self.rotate:
                # change rotate status
                self.rotate = False
            QApplication.restoreOverrideCursor()
            self.endPoint = self.toMapCoordinates(e.pos())
        elif (
            e.button() != None and ctrlIsHeld and self.geometryType == self.tr("Square")
        ):
            # calculate angle between mouse and last rubberband centroid before holding control
            self.rotAngle = self.rotateRect(self.currentCentroid, e)
            if not self.rotate:
                # only override mouse if it is not overriden already
                QApplication.setOverrideCursor(QCursor(Qt.CursorShape.BlankCursor))
                self.rotate = True
        if self.geometryType == self.tr("Circle"):
            self.showCircle(self.endPoint, self.param)
        elif self.geometryType == self.tr("Square"):
            self.showRect(self.endPoint, self.param, self.rotAngle)

    def showCircle(self, startPoint, param):
        """
        Draws a circle in the canvas
        """
        nPoints = 50
        x = startPoint.x()
        y = startPoint.y()
        if self.type == self.tr("distance"):
            r = self.getAdjustedSize(self.param)
        else:
            r = self.getAdjustedSize(sqrt(self.param / pi))
        self.rubberBand.reset(Qgis.GeometryType.Polygon)
        for itheta in range(nPoints + 1):
            theta = itheta * (2.0 * pi / nPoints)
            self.rubberBand.addPoint(
                QgsPointXY(x + r * cos(theta), y + r * sin(theta))
            )
        self.rubberBand.show()

    def showRect(self, startPoint, param, rotAngle=0):
        """
        Draws a rectangle in the canvas
        """
        if not (self.type == self.tr("distance")):
            param = sqrt(param) / 2
        # param = self.convertDistance( param )

        self.rubberBand.reset(Qgis.GeometryType.Polygon)
        x = startPoint.x()  # center point x
        y = startPoint.y()  # center point y
        # rotation angle is always applied in reference to center point
        # to avoid unnecessary calculations
        c = cos(rotAngle)
        s = sin(rotAngle)
        # translating coordinate system to rubberband centroid
        param = self.getAdjustedSize(param)
        for posx, posy in ((-1, -1), (-1, 1), (1, 1), (1, -1)):
            px = posx * param
            py = posy * param
            pnt = QgsPointXY(px * c - py * s + x, py * c + px * s + y)
            self.rubberBand.addPoint(pnt, False)
        self.rubberBand.setVisible(True)
        self.rubberBand.updateRect()
        self.rubberBand.update()
        self.rubberBand.show()
        self.currentCentroid = startPoint

    def convertDistance(self, distance):
        distanceArea = QgsDistanceArea()
        distanceArea.setSourceCrs(
            QgsCoordinateReferenceSystem.fromEpsgId(3857), QgsCoordinateTransformContext()
        )
        return distanceArea.convertLengthMeasurement(
            distance, self.canvas.mapSettings().destinationCrs().mapUnits()
        )

    def deactivate(self):
        """
        Deactivates the tool and hides the rubber band
        """
        self.rubberBand.hide()
        QgsMapTool.deactivate(self)
        # restore mouse in case tool is disabled right after rotation
        QApplication.restoreOverrideCursor()

    def activate(self):
        """
        Activates the tool
        """
        QgsMapTool.activate(self)
