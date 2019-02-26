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

from qgis.PyQt.QtCore import Qt
from qgis.core import QgsPointXY, Qgis, QgsGeometry, QgsWkbTypes

from .geometricaAquisition import GeometricaAcquisition

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
            self.rubberBand.setToGeometry(geom, self.iface.activeLayer())
            self.createGeometry(geom)

    def endGeometryFree(self):
        if len(self.geometry) > 2:
            if self.iface.activeLayer().geometryType() == QgsWkbTypes.PolygonGeometry:
                geom = QgsGeometry.fromPolygonXY([self.geometry])
            elif self.iface.activeLayer().geometryType() == QgsWkbTypes.LineGeometry:
                geom = QgsGeometry.fromPolylineXY(self.geometry + [self.geometry[0]])
            self.rubberBand.setToGeometry(geom, self.iface.activeLayer())
            self.createGeometry(geom)

    def distance_acceptable(self, p1, p_n, p_n_1, p_n_2):
        d_n = self.distanceToolTip.calculateDistance(p_n, p1)
        d_n_1 = self.distanceToolTip.calculateDistance(p_n, p_n_1)
        d_n_2 = self.distanceToolTip.calculateDistance(p_n_1, p_n_2)
        return (d_n > self.minSegmentDistance) and (d_n_1 > self.minSegmentDistance) and (d_n_2 > self.minSegmentDistance)

    def canvasReleaseEvent(self, event):
        event.snapPoint() #snap!!!
        if self.snapCursorRubberBand:
            self.snapCursorRubberBand.reset(geometryType=QgsWkbTypes.PointGeometry)
            self.snapCursorRubberBand.hide()
            self.snapCursorRubberBand = None
        pointMap = QgsPointXY(event.mapPoint())
        if event.button() == Qt.RightButton:
            if not self.rubberBand:
                self.geometry = []
                self.qntPoint = 0
                return
            if self.free:
                self.geometry.append(pointMap)
                self.endGeometryFree()
                self.qntPoint = 0
            else:
                if (self.qntPoint >=2):
                    if (self.qntPoint % 2 == 0):
                        point = QgsPointXY(pointMap)
                        projectedMousePoint = self.projectPoint(self.geometry[-2], self.geometry[-1], point)
                        if projectedMousePoint:                            
                            new_geom, last_point = self.completePolygon(self.geometry, projectedMousePoint)
                            if self.bufferDistanceTest(self.geometry, projectedMousePoint, last_point):
                                self.geometry.append(QgsPointXY(projectedMousePoint.x(), projectedMousePoint.y()))        
                                self.geometry.append(last_point)   
                                self.endGeometry() 
                            else:
                                self.iface.messageBar().pushMessage(
                                        self.tr("Observation:"),
                                        self.tr("Not possible to digitalize, segment smaller than minimun distance."),
                                        level=Qgis.Info
                                    )                        
                    else:
                        self.iface.messageBar().pushMessage(
                                self.tr("Observation:"),
                                self.tr("The right angle tool should be used only for rectangular shapes."),
                                level=Qgis.Info
                            )
        elif self.free:
            self.geometry.append(pointMap)
            self.qntPoint += 1
        else:
            if event.button() == Qt.LeftButton:
                if self.qntPoint == 0:
                    self.rubberBand = self.getRubberBand()
                    point = QgsPointXY(pointMap)
                    self.geometry.append(point)
                    self.qntPoint += 1
                elif self.qntPoint == 1:
                    point = QgsPointXY(pointMap)
                    if self.distanceToolTip.calculateDistance(self.geometry[-1], point) > self.minSegmentDistance:
                        self.geometry.append(point)
                        self.qntPoint += 1
                    else:
                        self.iface.messageBar().pushMessage(
                                self.tr("Observation:"),
                                self.tr("Not possible to digitalize, segment smaller than minimun distance."),
                                level=Qgis.Info
                            )
                else:
                    point = QgsPointXY(pointMap)
                    projectedMousePoint = self.projectPoint(self.geometry[-2], self.geometry[-1], point)
                    if projectedMousePoint:
                        new_geom, last_point = self.completePolygon(self.geometry, projectedMousePoint)                        
                        testando = self.bufferDistanceTest(self.geometry, projectedMousePoint, last_point)
                        
                        if self.bufferDistanceTest(self.geometry, projectedMousePoint, last_point):
                            self.geometry.append(QgsPointXY(projectedMousePoint.x(), projectedMousePoint.y()))        
                            self.qntPoint += 1
                        else:
                            self.iface.messageBar().pushMessage(
                                    self.tr("Observation:"),
                                    self.tr("Not possible to digitalize, segment smaller than minimun distance."),
                                    level=Qgis.Info
                                )

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
        if self.rubberBand:
            if self.qntPoint == 1:
                self.distanceToolTip.canvasMoveEvent(self.geometry[0], point)
                geom = QgsGeometry.fromPolylineXY([self.geometry[0], point])
                self.rubberBand.setToGeometry(geom, self.iface.activeLayer())
            elif self.qntPoint >= 2:
                self.distanceToolTip.canvasMoveEvent(self.geometry[-1], point)
                if self.free:
                    geom = QgsGeometry.fromPolygonXY([self.geometry+[QgsPointXY(point.x(), point.y())]])
                    self.rubberBand.setToGeometry(geom, self.iface.activeLayer())
                else:   
                    if (self.qntPoint % 2 == 1): 
                        self.setAvoidStyleSnapRubberBand()
                    else:
                        self.setAllowedStyleSnapRubberBand()     
                    projectedMousePoint = self.projectPoint(self.geometry[-2], self.geometry[-1], point)
                    if projectedMousePoint:
                        geom, pf = self.completePolygon(self.geometry, projectedMousePoint)
                        #print('oldPoint:', oldPoint)
                        #print('point:', point)
                        #print('pf:', pf)
                        self.rubberBand.setToGeometry(geom, None)
        else:
            self.initVariable()
