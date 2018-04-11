# -*- coding: utf-8 -*-

from __future__ import absolute_import
from builtins import range
import os

from qgis.PyQt import QtGui, uic
from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot, Qt
import math
from qgis.PyQt import QtCore, QtGui
from qgis.PyQt.QtWidgets import QShortcut
from qgis.PyQt.QtGui import QKeySequence
from qgis.PyQt.QtCore import QSettings
from .geometricaAquisition import GeometricaAcquisition
from qgis.core import QgsPointXY, Qgis, QgsWkbTypes
from qgis.gui import QgsMapMouseEvent, QgsMapTool

class Circle(GeometricaAcquisition):
    def __init__(self, canvas, iface, action):
        super(Circle, self).__init__(canvas, iface, action)
        self.canvas = canvas
        self.iface = iface
        self.rubberBand = None
        self.initVariable()
        
    def initVariable(self):
        if self.rubberBand:
            self.rubberBand.reset(True)
            self.rubberBand = None
        self.startPoint = None
        self.endPoint = None
        self.qntPoint = 0
        self.geometry = []
        
    def showCircle(self, startPoint, endPoint):
        nPoints = 50
        x = startPoint.x()
        y = startPoint.y()
        r = math.sqrt((endPoint.x() - startPoint.x())**2 + (endPoint.y() - startPoint.y())**2)
        self.rubberBand.reset(self.iface.activeLayer().geometryType())

        for itheta in range(nPoints+1):
            theta = itheta*(2.0*math.pi/nPoints)
            self.rubberBand.addPoint(QgsPointXY(x+r*math.cos(theta), y+r*math.sin(theta)))
        self.rubberBand.closePoints()

    def endGeometry(self):
        self.geometry = self.rubberBand.asGeometry()
        self.createGeometry(self.geometry)
  
    def canvasReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.startPoint:
                self.startPoint = QgsPointXY(event.mapPoint())
                self.rubberBand = self.getRubberBand()
        if event.button() == Qt.RightButton:
            self.endGeometry()
               
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
        if self.startPoint:
            self.endPoint = QgsPointXY(event.mapPoint())
            self.showCircle(self.startPoint, self.endPoint)
