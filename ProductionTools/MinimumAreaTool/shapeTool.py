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
    #signal emitted when the mouse is clicked. This indicates that the tool finished its job
    toolFinished = pyqtSignal()
    def __init__(self, canvas, geometryType, param, type):
        '''
        Constructor
        '''
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
        '''
        Adjusting the color to create the rubber band
        '''
        if self.type == self.tr('area'):
            mFillColor = QColor( 254, 178, 76, 63 )
        else:
            mFillColor = QColor( 255, 255, 0, 63 )        
        self.rubberBand.setColor(mFillColor)
        self.rubberBand.setWidth(1)
    
    def reset(self):
        '''
        Resetting the rubber band
        '''
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        try:
            self.rubberBand.reset(QGis.Polygon)
        except:
            pass

    def canvasPressEvent(self, e):
        '''
        When the canvas is pressed the tool finishes its job
        '''
        self.canvas.unsetMapTool(self)
        self.toolFinished.emit()

    def canvasMoveEvent(self, e):
        '''
        Deals with mouse move event to update the rubber band position in the canvas
        '''
        self.canvas.refresh()
        self.endPoint = self.toMapCoordinates( e.pos() )
        if self.geometryType == self.tr(u"Circle"):
            self.showCircle(self.endPoint)
        elif self.geometryType == self.tr(u"Square"):
            self.showRect(self.endPoint, self.param)

    def showCircle(self, startPoint):
        '''
        Draws a circle in the canvas
        '''
        nPoints = 50
        if self.type == self.tr('distance'):
            r = self.param
            self.rubberBand.reset(QGis.Polygon)
            center = startPoint
            for itheta in range(nPoints+1):
                theta = itheta*(2.0*pi/nPoints)
                self.rubberBand.addPoint(QgsPoint(center.x()+r*cos(theta), center.y()+r*sin(theta)))
            self.rubberBand.show()
        else:
            r = sqrt(self.param/pi)
            self.rubberBand.reset(QGis.Polygon)
            center = startPoint            
            for itheta in range(nPoints+1):
                theta = itheta*(2.0*pi/nPoints)
                self.rubberBand.addPoint(QgsPoint(center.x()+r*cos(theta), center.y()+r*sin(theta)))
            self.rubberBand.show()

    def showRect(self, startPoint, param):   
        '''
        Draws a rectangle in the canvas
        '''  
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
        '''
        Deactivates the tool and hides the rubber band
        '''
        self.rubberBand.hide()
        QgsMapTool.deactivate(self)
        
    def activate(self):
        '''
        Activates the tool
        '''
        QgsMapTool.activate(self)
    
    def reproject(self, geom, canvasCrs):
        '''
        Reprojects geom from the canvas crs to the reference crs
        geom: geometry to be reprojected
        canvasCrs: canvas crs (from crs)
        '''
        destCrs = self.reference.crs()
        if canvasCrs.authid() != destCrs.authid():
            coordinateTransformer = QgsCoordinateTransform(canvasCrs, destCrs)
            geom.transform(coordinateTransformer)
