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
from math import sqrt

class ShapeTool(QgsMapTool):
    toolFinished = pyqtSignal()
    def __init__(self, canvas, geometryType, area, type):
        self.canvas = canvas
        self.active = False
        self.geometryType=geometryType
        self.area=area
        self.type=type
        self.cursor=None
        QgsMapTool.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, QGis.Polygon)    
        if self.type == self.tr('area'):
            mFillColor = QColor( 254, 178, 76, 63 )
        else:
            mFillColor = QColor( 255, 255, 0, 63 )        
        self.rubberBand.setColor(mFillColor)
        self.rubberBand.setWidth(1)
        self.reset()
    
    
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
        self.endPoint = self.toMapCoordinates( e.pos() )
        if self.geometryType == self.tr(u"Hexagon"):
            self.showHex(self.endPoint, self.area)
        elif self.geometryType == self.tr(u"Square"):
            self.showRect(self.endPoint, self.area)

    def showHex(self, startPoint, area):
        self.rubberBand.reset(QGis.Polygon)        
        if self.type == self.tr('area'):
            lado = sqrt(2*area*sqrt(3))/3
            point1 = QgsPoint(startPoint.x() - lado, startPoint.y())
            point2 = QgsPoint(startPoint.x() - lado/2, startPoint.y() + lado*sqrt(3)/2)
            point3 = QgsPoint(startPoint.x() + lado/2, startPoint.y() + lado*sqrt(3)/2)
            point4 = QgsPoint(startPoint.x() + lado, startPoint.y())
            point5 = QgsPoint(startPoint.x() + lado/2, startPoint.y() - lado*sqrt(3)/2)
            point6 = QgsPoint(startPoint.x() - lado/2, startPoint.y() - lado*sqrt(3)/2)
        else:
            lado = area
            point1 = QgsPoint(startPoint.x() - lado, startPoint.y())
            point2 = QgsPoint(startPoint.x() - lado/2, startPoint.y() + lado*sqrt(3)/2)
            point3 = QgsPoint(startPoint.x() + lado/2, startPoint.y() + lado*sqrt(3)/2)
            point4 = QgsPoint(startPoint.x() + lado, startPoint.y())
            point5 = QgsPoint(startPoint.x() + lado/2, startPoint.y() - lado*sqrt(3)/2)
            point6 = QgsPoint(startPoint.x() - lado/2, startPoint.y() - lado*sqrt(3)/2)
        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, False)
        self.rubberBand.addPoint(point3, False)
        self.rubberBand.addPoint(point4, False)
        self.rubberBand.addPoint(point5, False) 
        self.rubberBand.addPoint(point6, True)    # true to update canvas
        self.rubberBand.show()

    def showRect(self, startPoint, area):     
        self.rubberBand.reset(QGis.Polygon)
        point1 = QgsPoint(startPoint.x() - sqrt(area)/2, startPoint.y() - sqrt(area)/2)
        point2 = QgsPoint(startPoint.x() - sqrt(area)/2, startPoint.y() + sqrt(area)/2)
        point3 = QgsPoint(startPoint.x() + sqrt(area)/2, startPoint.y() + sqrt(area)/2)
        point4 = QgsPoint(startPoint.x() + sqrt(area)/2, startPoint.y() - sqrt(area)/2)
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
        
