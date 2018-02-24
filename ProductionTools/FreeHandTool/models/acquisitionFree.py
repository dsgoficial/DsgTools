# -*- coding: utf-8 -*-
"""
/***************************************************************************
                             -------------------
        begin                : 2016-08-02
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

from PyQt4 import QtCore, QtGui, Qt
from qgis import core, gui
import math, json

class AcquisitionFree(gui.QgsMapTool):
 
    acquisitionFinished = QtCore.pyqtSignal('QgsGeometry*')

    def __init__(self, canvas):
        #construtor
        super(AcquisitionFree, self).__init__(canvas)
        self.canvas = canvas
        self.rubberBand = None
        self.rubberBandToStopState = None
        self.drawing = False
        self.snapCursorRubberBand = None
        self.active = False
        self.contadorVert = 0
        self.stopState = False
        self.cur = QtGui.QCursor(QtGui.QPixmap(["18 13 4 1",
                                    "           c None",
                                    "#          c #FF0000",
                                    ".          c #FF0000",
                                    "+          c #1210f3",
                                    "                 ", 
                                    "   +++++++++++   ",
                                    "  +     #     +  ",
                                    " +      #      + ",
                                    "+       #       +",
                                    "+       #       +",
                                    "++#############++", 
                                    "+       #       +",
                                    "+       #       +",
                                    " +      #      +",
                                    "  +     #     +  ",
                                    "   +++++++++++   ",
                                    "                 ",]))

    def setCursor(self, cursor):
        self.cur = cursor 

    def getCursor(self):
        return self.cur

    def setCanvas(self, canvas):
        self.canvas = canvas

    def getCanvas(self):
        return self.canvas

    def setActiveState(self, state):
        self.active = state 
    
    def getActiveState(self):
        return self.active
     
    def setStopedState(self, state):
        self.stopState = state
    
    def getStopedState(self):
        return self.stopState

    def setDrawingState(self, state):
        self.drawing = state

    def getDrawingState(self):
        return self.drawing

    def setRubberBand(self, rb):
        self.rubberBand = rb

    def getRubberBand(self):
        return self.rubberBand

    def setRubberBandToStopState(self, rb):
        self.rubberBandToStopState = rb

    def getRubberBandToStopState(self):
        return self.rubberBandToStopState

    def setGeometryType(self, geomType):
        self.geometryType = geomType

    def getGeometryType(self):
        return self.geometryType

    def setSnapRubberBand(self, snapRb):
        self.snapCursorRubberBand = snapRb   

    def getSnapRubberBand(self):
        return self.snapCursorRubberBand

    def isPolygon(self):
        return (self.getGeometryType() != core.QGis.Line)
        
    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Delete, QtCore.Qt.Key_Backspace]:
            self.setStopedState(True)
            self.removeVertice()
            event.ignore()
        if event.key() == QtCore.Qt.Key_Escape:
            self.cancelEdition()
            event.ignore()
    
    def cancelEdition(self):    
        self.getRubberBand().reset() if self.getRubberBand() else None
        self.setRubberBand(None)
        self.setDrawingState(False)
        self.setActiveState(False)
        self.contadorVert = 0
        self.getCanvas().refresh()
   
    def removeVertice(self):
        rubberBand = self.getRubberBand()
        if rubberBand and rubberBand.numberOfVertices() > 50:
            for x in range(50):
                rubberBand.removeLastPoint()
            if self.isPolygon():
                lastPoint = rubberBand.asGeometry().asPolygon()[-2]
            else:
                lastPoint = rubberBand.asGeometry().asPolyline()[-1]
            self.startRubberBandToStopState(
                core.QgsPoint(
                    lastPoint[0], lastPoint[1]
                )
            )
        elif rubberBand:
            self.setStopedState(False)
            self.getRubberBandToStopState().reset()
            self.cancelEdition()
        
               
    def createSnapRubberBand(self):
        rubberBand = self.getSnapRubberBand()
        if rubberBand:
            rubberBand.reset()
        else:
            rubberBand = gui.QgsRubberBand(
                self.getCanvas(), 
                geometryType = core.QGis.Point
            )
        rubberBand.setFillColor(QtGui.QColor(255, 0, 0, 40))
        rubberBand.setBorderColor(QtGui.QColor(255, 0, 0, 200))
        rubberBand.setWidth(5)
        rubberBand.setIcon(gui.QgsRubberBand.ICON_X)
        return rubberBand 

    def createSnapCursor(self, point):
        snapRubberBand = self.createSnapRubberBand()
        snapRubberBand.addPoint(point)
        self.setSnapRubberBand(snapRubberBand) 
		    
    def canvasReleaseEvent(self, event):
        self.getRubberBandToStopState().reset() if self.getRubberBandToStopState() else ''
        if self.getStopedState():
            self.setStopedState(False)
        elif self.getActiveState():
            self.setActiveState(False)
            self.finishEdition(event)
        else:
            self.setActiveState(True)
            self.startEdition(event)

    def startEdition(self, event):
        event.snapPoint(gui.QgsMapMouseEvent.SnapProjectConfig)
        snapRubberBand = self.getSnapRubberBand()
        if snapRubberBand:
            snapRubberBand.reset(geometryType=core.QGis.Point)
            snapRubberBand.hide()
            self.setSnapRubberBand(None)
        pointMap = core.QgsPoint(event.mapPoint())
        layer = self.getCanvas().currentLayer()
        if layer:
            self.startRubberBand(pointMap, layer)

    def startRubberBandToStopState(self, point):
        rubberBandToStopState = self.getRubberBandToStopState()
        if rubberBandToStopState:
            rubberBandToStopState.reset()
        if self.isPolygon():
            rubberBand = gui.QgsRubberBand(self.getCanvas(), core.QGis.Polygon)
            rubberBand.setColor(QtGui.QColor(255, 0, 0, 63))
            rubberBand.setWidth(2)
        else:
            rubberBand = gui.QgsRubberBand(self.getCanvas(), core.QGis.Line)
            rubberBand.setColor(QtGui.QColor(255, 0, 0, 150))
            rubberBand.setWidth(1)
        rubberBand.setLineStyle(QtCore.Qt.DotLine)
        rubberBand.addPoint(point)
        self.setRubberBandToStopState(rubberBand)
    
    def startRubberBand(self, pointMap, layer):
        self.setDrawingState(True)
        self.setGeometryType(layer.geometryType())
        if self.isPolygon():
            rubberBand = gui.QgsRubberBand(self.getCanvas(), core.QGis.Polygon)
            rubberBand.setColor(QtGui.QColor(255, 0, 0, 63))
            rubberBand.setWidth(2)
        else:
            rubberBand = gui.QgsRubberBand(self.getCanvas(), core.QGis.Line)
            rubberBand.setColor(QtGui.QColor(255, 0, 0, 150))
            rubberBand.setWidth(1)
        rubberBand.addPoint(pointMap)
        self.setRubberBand(rubberBand)
        
    def canvasMoveEvent(self, event):
        if self.getRubberBand():
            endPoint = self.toMapCoordinates( event.pos() )
        snapRubberBand = self.getSnapRubberBand()
        if not(self.getStopedState()):
            if snapRubberBand:
                snapRubberBand.hide()
                snapRubberBand.reset(geometryType=core.QGis.Point)
                self.setSnapRubberBand(None)
            oldPoint = core.QgsPoint(event.mapPoint())
            event.snapPoint(gui.QgsMapMouseEvent.SnapProjectConfig)
            point = core.QgsPoint(event.mapPoint())
            if oldPoint != point:
                self.createSnapCursor(point)
            if self.getRubberBand():
                if self.contadorVert == 0:        
                    self.getRubberBand().addPoint(point)
                    self.contadorVert+=1
                else:
                    self.getRubberBand().addPoint(oldPoint)
        if self.getRubberBandToStopState():
            self.updateRubberBandToStopState(
                self.toMapCoordinates( event.pos() )
            )

    def updateRubberBandToStopState(self, point):
        rubberBand = self.getRubberBandToStopState()
        if rubberBand.asGeometry():
            listPoints = rubberBand.asGeometry().asPolygon() if self.isPolygon() else rubberBand.asGeometry().asPolyline()
            if self.isPolygon() and len(listPoints) >= 3:
                rubberBand.removeLastPoint()
            elif not(self.isPolygon()) and len(listPoints) >= 2:
                rubberBand.removeLastPoint()
            rubberBand.addPoint(point)

    def finishEdition(self, event):
        event.snapPoint(gui.QgsMapMouseEvent.SnapProjectConfig)
        point = core.QgsPoint(event.mapPoint())
        if self.getRubberBand():
            self.getRubberBand().addPoint(point)
        if not self.getRubberBand():
            return
        if self.getRubberBand().numberOfVertices() > 2:
            geom = self.getRubberBand().asGeometry()
            self.acquisitionFinished.emit(geom)
        self.cancelEdition()

    def activate(self):
        mc = self.getCanvas()
        mc.setCursor(self.getCursor())

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True

  