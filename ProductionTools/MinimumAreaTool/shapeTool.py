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
from qgis.gui import QgsRubberBand, QgsMapTool
from qgis.core import QgsPoint, QGis
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtGui import QColor, QCursor, QWidget
from PyQt4.QtCore import pyqtSignal, QObject, Qt as Qt2, QPoint
from math import sqrt, cos, sin, pi, atan2

class ShapeTool(QgsMapTool):
    #signal emitted when the mouse is clicked. This indicates that the tool finished its job
    toolFinished = pyqtSignal()
    def __init__(self, canvas, geometryType, param, type, color = QColor( 254, 178, 76, 63 )):
        """
        Constructor
        """
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.active = False
        self.geometryType = geometryType
        self.param=param
        self.type=type       
        self.cursor=None
        self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)     
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
            self.rubberBand.reset(QGis.Polygon)
        except:
            pass

    def rotateRect(self, centroid, e):
        """
        Calculates the angle for the rotation.
        """
        item_position = self.toMapCoordinates(e.pos())
        rotAngle = atan2(item_position.y() - centroid.y(), item_position.x() - centroid.x()) / pi * 180
        return (90 - rotAngle)

    def canvasPressEvent(self, e):
        """
        When the canvas is pressed the tool finishes its job
        """
        self.canvas.unsetMapTool(self)
        self.toolFinished.emit()

    def canvasMoveEvent(self, e):
        """
        Deals with mouse move event to update the rubber band position in the canvas
        """
        
        if e.button() != None and not (QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier):
            QtGui.QApplication.restoreOverrideCursor()
            if self.rotate:
                QtGui.QApplication.restoreOverrideCursor()
                mousePos = self.toCanvasCoordinates(self.currentCentroid)
                self.endPoint = self.toMapCoordinates(mousePos)
                mousePos = self.canvas.mapToGlobal(mousePos)
                QtGui.QCursor.setPos(mousePos)
                self.rotate = False
                print self.toCanvasCoordinates(self.currentCentroid), e.pos(), mousePos
            else:
                QtGui.QApplication.restoreOverrideCursor()
                self.endPoint = self.toMapCoordinates( e.pos() )
            if self.geometryType == self.tr(u"Circle"):
                self.showCircle(self.endPoint)
            elif self.geometryType == self.tr(u"Square"):
                self.showRect(self.endPoint, sqrt(self.param)/2, self.rotAngle)
        elif e.button() != None and \
            (QtGui.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier)\
            and self.geometryType == self.tr(u"Square"):
            QtGui.QApplication.setOverrideCursor(QCursor(Qt2.BlankCursor))
            self.rotAngle = self.rotateRect(self.currentCentroid, e)
            self.showRect(self.endPoint, sqrt(self.param)/2, self.rotAngle) 
            # to inform the program that there was a rotation applied and 
            # direct flow to redrawing 
            self.rotate = True           
    
    def showCircle(self, startPoint):
        """
        Draws a circle in the canvas
        """
        nPoints = 50
        x = startPoint.x()
        y = startPoint.y()
        if self.type == self.tr('distance'):
            r = self.param
            self.rubberBand.reset(QGis.Polygon)
            for itheta in range(nPoints+1):
                theta = itheta*(2.0*pi/nPoints)
                self.rubberBand.addPoint(QgsPoint(x+r*cos(theta), y+r*sin(theta)))
            self.rubberBand.show()
        else:
            r = sqrt(self.param/pi)
            self.rubberBand.reset(QGis.Polygon)
            for itheta in range(nPoints+1):
                theta = itheta*(2.0*pi/nPoints)
                self.rubberBand.addPoint(QgsPoint(x+r*cos(theta), y+r*sin(theta)))
            self.rubberBand.show()

    def showRect(self, startPoint, param, rotAngle=0):   
        """
        Draws a rectangle in the canvas
        """  
        self.rubberBand.reset(QGis.Polygon)
        x = startPoint.x()
        y = startPoint.y()
        point1 = QgsPoint(x - param, y - param)
        point2 = QgsPoint(x - param, y + param)
        point3 = QgsPoint(x + param, y + param)
        point4 = QgsPoint(x + param, y - param)
        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, False)
        self.rubberBand.addPoint(point3, False)
        self.rubberBand.addPoint(point4, True)
        self.rubberBand.setRotation(rotAngle)
        self.rubberBand.show()
        self.currentCentroid = self.rubberBand.asGeometry().centroid().asPoint()
        return self.rubberBand.asGeometry().centroid().asPoint()
        
    def deactivate(self):
        """
        Deactivates the tool and hides the rubber band
        """
        self.rubberBand.hide()
        QgsMapTool.deactivate(self)
        
    def activate(self):
        """
        Activates the tool
        """
        QgsMapTool.activate(self)
    
    def reproject(self, geom, canvasCrs):
        """
        Reprojects geom from the canvas crs to the reference crs
        geom: geometry to be reprojected
        canvasCrs: canvas crs (from crs)
        """
        destCrs = self.reference.crs()
        if canvasCrs.authid() != destCrs.authid():
            coordinateTransformer = QgsCoordinateTransform(canvasCrs, destCrs)
            geom.transform(coordinateTransformer)