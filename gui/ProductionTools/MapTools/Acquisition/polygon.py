# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os                                                                         

from qgis.PyQt import QtGui, uic 
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot, Qt
import math
from qgis.PyQt import QtCore, QtGui
from qgis.PyQt.QtWidgets import QShortcut
from qgis.PyQt.QtGui import QKeySequence
from qgis.PyQt.QtCore import QSettings
from .geometricaAquisition import GeometricaAcquisition
from qgis.core import QgsPointXY, Qgis, QgsGeometry, QgsWkbTypes
from qgis.gui import QgsMapMouseEvent, QgsMapTool

class Polygon(GeometricaAcquisition):
    def __init__(self, canvas, iface, action):
        super(Polygon, self).__init__(canvas, iface, action)
        self.canvas = canvas
        self.iface = iface

    def endGeometry(self):
        if len(self.geometry) > 2:
            inter = self.lineIntersection(self.geometry[1],self.geometry[0],self.geometry[-2],self.geometry[-1])
            if inter:
                if self.iface.activeLayer().geometryType() == QgsWkbTypes.PolygonGeometry:
                    geom = QgsGeometry.fromPolygonXY([self.geometry+[inter]])
                elif self.iface.activeLayer().geometryType() == QgsWkbTypes.LineGeometry:
                    geom = QgsGeometry.fromPolylineXY(self.geometry+[inter])
                self.rubberBand.setToGeometry(geom,None)
                self.createGeometry(geom)

    def endGeometryFree(self):
        if len(self.geometry) > 2:
            if self.iface.activeLayer().geometryType() == QgsWkbTypes.PolygonGeometry:
                geom = QgsGeometry.fromPolygonXY([self.geometry])
            elif self.iface.activeLayer().geometryType() == QgsWkbTypes.LineGeometry:
                geom = QgsGeometry.fromPolylineXY(self.geometry + [self.geometry[0]])
            self.rubberBand.setToGeometry(geom, None)
            self.createGeometry(geom)
  
    def canvasReleaseEvent(self, event):
        event.snapPoint() #snap!!!
        if self.snapCursorRubberBand:
            self.snapCursorRubberBand.reset(geometryType=QgsWkbTypes.PointGeometry)
            self.snapCursorRubberBand.hide()
            self.snapCursorRubberBand = None
        pointMap = QgsPointXY(event.mapPoint())
        # pointMap = self.snapToLayer(event) 
        if event.button() == Qt.RightButton:
            if self.free:
                self.geometry.append(pointMap)
                self.endGeometryFree()
            else:
                self.endGeometry()        
        elif self.free:
            self.geometry.append(pointMap)
            self.qntPoint += 1
        else:
            if event.button() == Qt.LeftButton:
                if self.qntPoint == 0:
                    self.rubberBand = self.getRubberBand()
                    point = QgsPointXY(pointMap)
                    self.geometry.append(point)
                elif self.qntPoint == 1:
                    point = QgsPointXY(pointMap)
                    self.geometry.append(point)
                else:
                    point = QgsPointXY(pointMap)
                    testgeom = self.projectPoint(self.geometry[-2], self.geometry[-1], point)
                    if testgeom:
                        self.geometry.append(QgsPointXY(testgeom.x(), testgeom.y()))        
                self.qntPoint += 1
               
    def canvasMoveEvent(self, event):
        if self.snapCursorRubberBand:
            self.snapCursorRubberBand.hide()
            self.snapCursorRubberBand.reset(geometryType=QgsWkbTypes.PointGeometry)
            self.snapCursorRubberBand = None
        oldPoint = QgsPointXY(event.mapPoint())
        event.snapPoint()
        point = QgsPointXY(event.mapPoint())
        if oldPoint != point:
            self.createSnapCursor(point)
        point = QgsPointXY(event.mapPoint())   
        if self.qntPoint == 1:
            geom = QgsGeometry.fromPolylineXY([self.geometry[0], point])
            self.rubberBand.setToGeometry(geom, None)
        elif self.qntPoint >= 2:
            if self.free:
                geom = QgsGeometry.fromPolygonXY([self.geometry+[QgsPointXY(point.x(), point.y())]])
                self.rubberBand.setToGeometry(geom, None)             
            else:        
                testgeom = self.projectPoint(self.geometry[-2], self.geometry[-1], point)
                if testgeom:
                    geom = QgsGeometry.fromPolygonXY([self.geometry+[QgsPointXY(testgeom.x(), testgeom.y())]])
                    self.rubberBand.setToGeometry(geom, None)
