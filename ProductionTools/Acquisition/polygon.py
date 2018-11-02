# -*- coding: utf-8 -*-

import os                                                                         

from PyQt4 import QtGui, uic 
from PyQt4.QtCore import pyqtSignal, pyqtSlot, SIGNAL, Qt
import math
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QShortcut, QKeySequence
from PyQt4.QtCore import QSettings
from geometricaAquisition import GeometricaAcquisition
from qgis.core import QgsPoint, QGis, QgsGeometry
from qgis.gui import QgsMapMouseEvent, QgsMapTool, QgsMessageBar

class Polygon(GeometricaAcquisition):
    def __init__(self, canvas, iface, action):
        super(Polygon, self).__init__(canvas, iface, action)
        self.canvas = canvas
        self.iface = iface

    def endGeometry(self):
        if len(self.geometry) > 2:
            if self.iface.activeLayer().geometryType() == QGis.Polygon:
                geom = QgsGeometry.fromPolygon([self.geometry])
            elif self.iface.activeLayer().geometryType() == QGis.Line:
                geom = QgsGeometry.fromPolyline(self.geometry)
            self.rubberBand.setToGeometry(geom,None)
            self.createGeometry(geom)

    def endGeometryFree(self):
        if len(self.geometry) > 2:
            if self.iface.activeLayer().geometryType() == QGis.Polygon:
                geom = QgsGeometry.fromPolygon([self.geometry])
            elif self.iface.activeLayer().geometryType() == QGis.Line:
                geom = QgsGeometry.fromPolyline(self.geometry + [self.geometry[0]])
            self.rubberBand.setToGeometry(geom, None)
            self.createGeometry(geom)

    def distance_acceptable(self, p1, p_n, p_n_1, p_n_2):
        d_n = self.distanceToolTip.calculateDistance(p_n, p1)
        d_n_1 = self.distanceToolTip.calculateDistance(p_n, p_n_1)
        d_n_2 = self.distanceToolTip.calculateDistance(p_n_1, p_n_2)
        if (d_n>self.minSegmentDistance) and (d_n>self.minSegmentDistance) and (d_n>self.minSegmentDistance):
            return True
        else:
            return False
        
    def canvasReleaseEvent(self, event):
        event.snapPoint(QgsMapMouseEvent.SnapProjectConfig) #snap!!!
        if self.snapCursorRubberBand:
            self.snapCursorRubberBand.reset(geometryType=QGis.Point)
            self.snapCursorRubberBand.hide()
            self.snapCursorRubberBand = None
        pointMap = QgsPoint(event.mapPoint())
        # pointMap = self.snapToLayer(event) 
        if event.button() == Qt.RightButton:
            if self.free:
                self.geometry.append(pointMap)
                self.endGeometryFree()
            else:
                if (self.qntPoint >=2):
                    if (self.qntPoint % 2 == 0):
                        point = QgsPoint(pointMap)
                        projectedMousePoint = self.projectPoint(self.geometry[-2], self.geometry[-1], point)
                        if projectedMousePoint:                            
                            new_geom, last_point = self.completePolygon(self.geometry, projectedMousePoint)
                            if self.distanceBetweenLinesTest(self.geometry, projectedMousePoint):
                                self.geometry.append(QgsPoint(projectedMousePoint.x(), projectedMousePoint.y()))        
                                self.geometry.append(last_point)   
                                self.endGeometry() 
                            else:
                                self.iface.messageBar().pushMessage(self.tr("Observation:"), self.tr("Not possible to digitalize, segment smaller than minimun distance."), level=QgsMessageBar.INFO)                        
                    else:                        
                        self.iface.messageBar().pushMessage(self.tr("Observation:"), self.tr("The right angle tool should be used only for rectangular shapes."), level=QgsMessageBar.INFO)      

        elif self.free:
            self.geometry.append(pointMap)
            self.qntPoint += 1
        else:
            if event.button() == Qt.LeftButton:
                if self.qntPoint == 0:
                    self.rubberBand = self.getRubberBand()
                    point = QgsPoint(pointMap)
                    self.geometry.append(point)
                    self.qntPoint += 1
                elif self.qntPoint == 1:                    
                    point = QgsPoint(pointMap)
                    if self.distanceToolTip.calculateDistance(self.geometry[-1], point) > self.minSegmentDistance:                        
                        self.geometry.append(point)
                        self.qntPoint += 1
                    else:
                        self.iface.messageBar().pushMessage(self.tr("Observation:"), self.tr("Not possible to digitalize, segment smaller than minimun distance."), level=QgsMessageBar.INFO)                        
                else:
                    point = QgsPoint(pointMap)
                    projectedMousePoint = self.projectPoint(self.geometry[-2], self.geometry[-1], point)
                    if projectedMousePoint:
                        if self.distanceBetweenLinesTest(self.geometry, projectedMousePoint):
                            self.geometry.append(QgsPoint(projectedMousePoint.x(), projectedMousePoint.y()))        
                            self.qntPoint += 1
                        else:
                            self.iface.messageBar().pushMessage(self.tr("Observation:"), self.tr("Not possible to digitalize, segment smaller than minimun distance."), level=QgsMessageBar.INFO)                                                                  
               
    def canvasMoveEvent(self, event):
        if self.snapCursorRubberBand:
            self.snapCursorRubberBand.hide()
            self.snapCursorRubberBand.reset(geometryType=QGis.Point)
            self.snapCursorRubberBand = None
        oldPoint = QgsPoint(event.mapPoint())
        event.snapPoint(QgsMapMouseEvent.SnapProjectConfig)
        point = QgsPoint(event.mapPoint())
        if oldPoint != point:
            self.createSnapCursor(point)
        point = QgsPoint(event.mapPoint())   
        if self.qntPoint == 1:
            self.distanceToolTip.canvasMoveEvent(self.geometry[0], point)
            geom = QgsGeometry.fromPolyline([self.geometry[0], point])
            self.rubberBand.setToGeometry(geom, None)
        elif self.qntPoint >= 2:
            self.distanceToolTip.canvasMoveEvent(self.geometry[-1], point)
            if self.free:
                geom = QgsGeometry.fromPolygon([self.geometry+[QgsPoint(point.x(), point.y())]])
                self.rubberBand.setToGeometry(geom, None)             
            else:       
                if (self.qntPoint % 2 == 1): 
                    self.setAvoidStyleSnapRubberBand()
                else:
                    self.setAllowedStyleSnapRubberBand()
                projectedMousePoint = self.projectPoint(self.geometry[-2], self.geometry[-1], point)
                if projectedMousePoint:
                    geom, pf = self.completePolygon(self.geometry, projectedMousePoint)
                    self.rubberBand.setToGeometry(geom, None)
