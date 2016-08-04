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
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QColor
from PyQt4.QtCore import pyqtSignal, QObject
from math import sqrt, cos, sin, pi

class ShapeTool(QgsMapTool):
    toolFinished = pyqtSignal()
    def __init__(self, canvas, geometryType, param, type):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.active = False
        self.geometryType=geometryType
        self.param=param
        self.type=type       
        self.cursor=None
        self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)    
        self.setColor()
        self.reset()
        
    def setColor(self):
        if self.type == self.tr('area'):
            mFillColor = QColor( 254, 178, 76, 63 )
        else:
            mFillColor = QColor( 255, 255, 0, 63 )        
        self.rubberBand.setColor(mFillColor)
        self.rubberBand.setWidth(1)
    
    def reset(self):
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        try:
            self.rubberBand.reset(QGis.Polygon)
        except:
            pass

    def setCursor(self, cursor):
        self.cursor=cursor

    def canvasPressEvent(self, e):
        if self.cursor != None:
            self.canvas.unsetMapTool(self.cursor)
            self.toolFinished.emit()

    def canvasMoveEvent(self, e):
        self.canvas.refresh()
        self.endPoint = self.toMapCoordinates( e.pos() )
        if self.geometryType == self.tr(u"Circle"):
            self.showCircle(self.endPoint)
        elif self.geometryType == self.tr(u"Square"):
            self.showRect(self.endPoint, self.param)

    def showCircle(self, startPoint):
        if self.type == self.tr('distance'):
            r = self.param
            self.rubberBand.reset(QGis.Polygon)
            center = startPoint
            for itheta in range(100+1):
                theta = itheta*(2.0*pi/100)
                self.rubberBand.addPoint(QgsPoint(center.x()+r*cos(theta), center.y()+r*sin(theta)))
            self.rubberBand.show()
        else:
            r = sqrt(self.param/pi)
            self.rubberBand.reset(QGis.Polygon)
            center = startPoint            
            for itheta in range(100+1):
                theta = itheta*(2.0*pi/100)
                self.rubberBand.addPoint(QgsPoint(center.x()+r*cos(theta), center.y()+r*sin(theta)))
            self.rubberBand.show()
            

    def showRect(self, startPoint, param):     
        self.rubberBand.reset(QGis.Polygon)
        point1 = QgsPoint(startPoint.x() - sqrt(param)/2, startPoint.y() - sqrt(param)/2)
        point2 = QgsPoint(startPoint.x() - sqrt(param)/2, startPoint.y() + sqrt(param)/2)
        point3 = QgsPoint(startPoint.x() + sqrt(param)/2, startPoint.y() + sqrt(param)/2)
        point4 = QgsPoint(startPoint.x() + sqrt(param)/2, startPoint.y() - sqrt(param)/2)
        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, False)
        self.rubberBand.addPoint(point3, False)
        self.rubberBand.addPoint(point4, True)
        self.rubberBand.show()
    
    def deactivate(self):
        self.rubberBand.hide()
        QgsMapTool.deactivate(self)
        
    def activate(self):
        QgsMapTool.activate(self)
    
    def reproject(self, geom, canvasCrs):
        destCrs = self.reference.crs()
        if canvasCrs.authid() != destCrs.authid():
            coordinateTransformer = QgsCoordinateTransform(canvasCrs, destCrs)
            geom.transform(coordinateTransformer)
