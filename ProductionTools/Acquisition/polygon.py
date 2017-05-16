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

class Polygon(GeometricaAcquisition):
    def __init__(self, canvas, iface, action):
        super(Polygon, self).__init__(canvas, iface, action)
        self.canvas = canvas
        self.iface = iface
        self.rubberBand = None
        self.initVariable()
        
    def initVariable(self):
        if self.rubberBand:
            self.rubberBand.reset(True)
            self.rubberBand = None
        self.qntPoint = 0
        self.geometry = []

    def endGeometry(self):
        if len(self.geometry) > 2:
            inter = self.lineIntersection(self.geometry[1],self.geometry[0],self.geometry[-2],self.geometry[-1])
            if inter:
                geom = QgsGeometry.fromPolygon([self.geometry+[inter]])
                self.rubberBand.setToGeometry(geom,None)
                self.createGeometry(geom)

    def endGeometryFree(self):
        if len(self.geometry) > 2:
            geom = QgsGeometry.fromPolygon([self.geometry])
            self.rubberBand.setToGeometry(geom, None)
            self.createGeometry(geom)
  
    def canvasReleaseEvent(self, event):
        pointMap = self.snapToLayer(event) 
        if event.button() == Qt.RightButton:
            if self.free:
                self.endGeometryFree()
            else:
                self.endGeometry()        
        elif self.free:
            self.geometry.append(point)
            self.qntPoint += 1
        else:
            if event.button() == Qt.LeftButton:
                if self.qntPoint == 0:
                    self.rubberBand = self.getRubberBand()
                    point = QgsPoint(pointMap)
                    self.geometry.append(point)
                elif self.qntPoint == 1:
                    point = QgsPoint(pointMap)
                    self.geometry.append(point)
                else:
                    point = QgsPoint(pointMap)
                    testgeom = self.projectPoint(self.geometry[-2], self.geometry[-1], point)
                    if testgeom:
                        self.geometry.append(QgsPoint(testgeom.x(), testgeom.y()))        
                self.qntPoint += 1
               
    def canvasMoveEvent(self, event):
        point = QgsPoint(event.mapPoint())
        point = self.snapToLayer(event)     
        if self.qntPoint == 1:
            geom = QgsGeometry.fromPolyline([self.geometry[0], point])
            self.rubberBand.setToGeometry(geom, None)
        elif self.qntPoint >= 2:
            if self.free:
                geom = QgsGeometry.fromPolygon([self.geometry+[QgsPoint(point.x(), point.y())]])
                self.rubberBand.setToGeometry(geom, None)             
            else:        
                testgeom = self.projectPoint(self.geometry[-2], self.geometry[-1], point)
                if testgeom:
                    geom = QgsGeometry.fromPolygon([self.geometry+[QgsPoint(testgeom.x(), testgeom.y())]])
                    self.rubberBand.setToGeometry(geom, None)

    def snapToLayer(self, event):
        snapMode = self.canvas.snappingUtils().snapToMapMode()
        snapper = QgsMapCanvasSnapper(self.canvas)
        snapMode, snapTolerance, dumpUnits = self.getSnapSettings()
        (retval,result) = snapper.snapToCurrentLayer(event.pos(), snapMode, snappingTol = snapTolerance)
        if result <> []:
            return QgsPoint(result[0].snappedVertex)
        else:
            return QgsPoint(event.mapPoint())
    
    def getSnapSettings(self):
        dumpSplit = self.canvas.snappingUtils().dump().split('\n')[2].split(' ') #snappingUtils().dump() returns a string with current snap settins
        snapMode = dumpSplit[1] #Snap to vertex, segment or both
        snapTolerance = dumpSplit[5]
        dumpUnits = dumpSplit[-1]
        return int(snapMode), int(snapTolerance), int(dumpUnits)

    
    def createSnapCursor(self, point):
        pass
