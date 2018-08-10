#! -*- coding: UTF-8 -*-
"""
/***************************************************************************
                             -------------------
        begin                : 2018-04-02
        git sha              : $Format:%H$
        copyright            : (C) 2017 by  Jossan Costa - Surveying Technician @ Brazilian Army
        email                : jossan.costa@eb.mil.br
 ***************************************************************************/
Some parts were inspired by QGIS plugin FreeHandEditting
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

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
from qgis.gui import QgsMapMouseEvent, QgsMapTool, QgsMessageBar

class Polygon(GeometricaAcquisition):
    def __init__(self, canvas, iface, action):
        super(Polygon, self).__init__(canvas, iface, action)
        self.canvas = canvas
        self.iface = iface

    def endGeometry(self):
        if len(self.geometry) > 2:
            if self.iface.activeLayer().geometryType() == QgsWkbTypes.PolygonGeometry:
                geom = QgsGeometry.fromPolygonXY([self.geometry])
            elif self.iface.activeLayer().geometryType() == QgsWkbTypes.LineGeometry:
                geom = QgsGeometry.fromPolylineXY(self.geometry)
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
        if event.button() == Qt.RightButton:
            if self.free:
                self.geometry.append(pointMap)
                self.endGeometryFree()
            else:
                if (self.qntPoint >=2):
                    if (self.qntPoint % 2 == 0):
                        point = QgsPointXY(pointMap)
                        testgeom = self.projectPoint(self.geometry[-2], self.geometry[-1], point)
                        if testgeom:
                            new_geom, pf = self.completePolygon(self.geometry, testgeom)
                            self.geometry.append(QgsPointXY(testgeom.x(), testgeom.y()))        
                            self.geometry.append(pf)   
                        self.endGeometry()                         
                    else:
                        msg = self.tr("Tool is designed for straight angles composed features.")
                        self.iface.messageBar().pushInfo(self.tr("Warning!"), msg)
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
            self.distanceToolTip.canvasMoveEvent(self.geometry[0], point)
            geom = QgsGeometry.fromPolylineXY([self.geometry[0], point])
            self.rubberBand.setToGeometry(geom, None)
        elif self.qntPoint >= 2:
            self.distanceToolTip.canvasMoveEvent(self.geometry[-1], point)
            if self.free:
                geom = QgsGeometry.fromPolygonXY([self.geometry+[QgsPointXY(point.x(), point.y())]])
                self.rubberBand.setToGeometry(geom, None)             
            else:   
                if (self.qntPoint % 2 == 1): 
                    self.setAvoidStyleSnapRubberBand()
                else:
                    self.setAllowedStyleSnapRubberBand()     
                testgeom = self.projectPoint(self.geometry[-2], self.geometry[-1], point)
                if testgeom:
                    geom, pf = self.completePolygon(self.geometry, testgeom)
                    self.rubberBand.setToGeometry(geom, None)
