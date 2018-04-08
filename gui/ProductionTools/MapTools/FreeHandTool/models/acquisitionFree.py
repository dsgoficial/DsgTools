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

from builtins import range
from qgis.PyQt import QtCore, QtGui
from qgis import core, gui
import math, json

class AcquisitionFree(gui.QgsMapTool):
 
    #Sinal usado para enviar a geometria adquirida ao finalizar aquisição
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
        #Método para definir cursor da ferramenta
        #Parâmetro de entrada: cursor (cursor usado na ferramenta)
        self.cur = cursor 

    def getCursor(self):
        #Método para obter cursor da ferramenta
        #Parâmetro de retorno: cursor (cursor usado na ferramenta)
        return self.cur

    def setCanvas(self, canvas):
        #Método para definir o canvas do Qgis
        #Parâmetro de entrada: canvas (Canvas do Qgis)
        self.canvas = canvas

    def getCanvas(self):
        #Método para obter o canvas do Qgis
        #Parâmetro de retorno: canvas (Canvas do Qgis)
        return self.canvas

    def setActiveState(self, state):
        #Método para definir se a ferramenta está ativa ou não
        #Parâmetro de entrada: state (Boleano)
        self.active = state 
    
    def getActiveState(self):
        #Método para obter se a ferramenta está ativa ou não
        #Parâmetro de retorno: state (Boleano)
        return self.active
     
    def setStopedState(self, state):
        #Método para definir se a ferramenta está pausada
        #Parâmetro de entrada: state (Boleano)
        self.stopState = state
    
    def getStopedState(self):
        #Método para obter se a ferramenta está pausada
        #Parâmetro de retorno: state (Boleano)
        return self.stopState

    def setDrawingState(self, state):
        #Método para definir se a ferramenta está desenhando
        #Parâmetro de entrada: state (Boleano)
        self.drawing = state

    def getDrawingState(self):
        #Método para obter se a ferramenta está desenhando
        #Parâmetro de retorno: state (Boleano)
        return self.drawing

    def setRubberBand(self, rb):
        #Método para definir o rubberBand de aquisição
        #Parâmetro de entrada: rb (rubberBand)
        self.rubberBand = rb

    def getRubberBand(self):
        #Método para obter o rubberBand de aquisição
        #Parâmetro de retorno: rb (rubberBand)
        return self.rubberBand

    def setRubberBandToStopState(self, rb):
        #Método para definir o rubberBand de pausa da ferramenta
        #Parâmetro de entrada: rb (rubberBand)
        self.rubberBandToStopState = rb

    def getRubberBandToStopState(self):
        #Método para obter o rubberBand de pausa da ferramenta
        #Parâmetro de retorno: rb (rubberBand)
        return self.rubberBandToStopState

    def setGeometryType(self, geomType):
        #Método para definir o tipo da geometria
        #Parâmetro de entrada: geomType (Tipo da geometria)
        self.geometryType = geomType

    def getGeometryType(self):
        #Método para obter o tipo da geometria
        #Parâmetro de retorno: geomType (Tipo da geometria)
        return self.geometryType

    def setSnapRubberBand(self, snapRb):
        #Método para definir o rubberBand do snap
        #Parâmetro de entrada: rb (rubberBand)
        self.snapCursorRubberBand = snapRb   

    def getSnapRubberBand(self):
        #Método para obter o rubberBand do snap
        #Parâmetro de entrada: rb (rubberBand)
        return self.snapCursorRubberBand

    def isPolygon(self):
        #Método para testar se a camada atual é polígono
        #Parâmetro de retorno: isPolygon (Boleano)
        isPolygon = (self.getGeometryType() != core.Qgis.Line)
        return isPolygon
        
    def keyPressEvent(self, event):
        #Método para receber os eventos do teclado
        #Parâmetro de entrada: event (Evento que chamou o método)
        if event.key() in [QtCore.Qt.Key_Delete, QtCore.Qt.Key_Backspace]:
            self.setStopedState(True)
            self.removeVertice()
            event.ignore()
        if event.key() == QtCore.Qt.Key_Escape:
            self.cancelEdition()
            event.ignore()
    
    def cancelEdition(self): 
        #Método para cancelar aquisição
        self.getRubberBand().reset() if self.getRubberBand() else None
        self.setRubberBand(None)
        self.setDrawingState(False)
        self.setActiveState(False)
        self.contadorVert = 0
        self.getCanvas().refresh()
    
    def getParametersFromConfig(self):
        #Método para obter as configurações da tool do QSettings
        #Parâmetro de retorno: parameters (Todas os parâmetros do QSettings usado na ferramenta)
        settings = QtCore.QSettings()
        settings.beginGroup('PythonPlugins/DsgTools/Options')
        undoPoints = settings.value('undoPoints')
        settings.endGroup()
        return undoPoints
   
    def removeVertice(self):
        #Método para remover vertices
        rubberBand = self.getRubberBand()
        qtnUndoPoints = self.getParametersFromConfig()
        if rubberBand and rubberBand.numberOfVertices() > qtnUndoPoints:
            for x in range(qtnUndoPoints):
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
        
               
    def createSnapCursor(self, point):
        #Método para criar rubberBand do snap
        rubberBand = self.getSnapRubberBand()
        if rubberBand:
            rubberBand.reset()
        else:
            rubberBand = gui.QgsRubberBand(
                self.getCanvas(), 
                geometryType = core.Qgis.Point
            )
        rubberBand.setFillColor(QtGui.QColor(255, 0, 0, 40))
        rubberBand.setBorderColor(QtGui.QColor(255, 0, 0, 200))
        rubberBand.setWidth(5)
        rubberBand.setIcon(gui.QgsRubberBand.ICON_X)
        rubberBand.addPoint(point)
        self.setSnapRubberBand(rubberBand)         
		    
    def canvasReleaseEvent(self, event):
        #Método para receber os eventos release do canvas do Qgis
        #Parâmetro de entrada: event (Evento que chamou o método)
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
        #Método para iniciar a aquisição
        #Parâmetro de entrada: event (Evento)
        event.snapPoint(gui.QgsMapMouseEvent.SnapProjectConfig)
        snapRubberBand = self.getSnapRubberBand()
        if snapRubberBand:
            snapRubberBand.reset(geometryType=core.Qgis.Point)
            snapRubberBand.hide()
            self.setSnapRubberBand(None)
        pointMap = core.QgsPoint(event.mapPoint())
        layer = self.getCanvas().currentLayer()
        if layer:
            self.startRubberBand(pointMap, layer)

    def startRubberBandToStopState(self, point):
        #Método para iniciar o rubberBand do pause da ferramenta
        #Parâmetro de entrada: point (Último ponto da feição em aquisição)
        rubberBandToStopState = self.getRubberBandToStopState()
        if rubberBandToStopState:
            rubberBandToStopState.reset()
        if self.isPolygon():
            rubberBand = gui.QgsRubberBand(self.getCanvas(), core.Qgis.Polygon)
            rubberBand.setColor(QtGui.QColor(255, 0, 0, 63))
            rubberBand.setWidth(2)
        else:
            rubberBand = gui.QgsRubberBand(self.getCanvas(), core.Qgis.Line)
            rubberBand.setColor(QtGui.QColor(255, 0, 0, 150))
            rubberBand.setWidth(1)
        rubberBand.setLineStyle(QtCore.Qt.DotLine)
        rubberBand.addPoint(point)
        self.setRubberBandToStopState(rubberBand)
    
    def startRubberBand(self, pointMap, layer):
        #Método para iniciar o rubberBand da aquisição
        #Parâmetro de entrada: pointMap (Primeiro ponto da feição em aquisição), layer (Camada ativa)
        self.setDrawingState(True)
        self.setGeometryType(layer.geometryType())
        if self.isPolygon():
            rubberBand = gui.QgsRubberBand(self.getCanvas(), core.Qgis.Polygon)
            rubberBand.setColor(QtGui.QColor(255, 0, 0, 63))
            rubberBand.setWidth(2)
        else:
            rubberBand = gui.QgsRubberBand(self.getCanvas(), core.Qgis.Line)
            rubberBand.setColor(QtGui.QColor(255, 0, 0, 150))
            rubberBand.setWidth(1)
        rubberBand.addPoint(pointMap)
        self.setRubberBand(rubberBand)
        
    def canvasMoveEvent(self, event):
        #Método para receber os eventos canvas move do Qgis
        #Parâmetro de entrada: event (Evento que chamou o método)
        if self.getRubberBand():
            endPoint = self.toMapCoordinates( event.pos() )
        snapRubberBand = self.getSnapRubberBand()
        if not(self.getStopedState()):
            if snapRubberBand:
                snapRubberBand.hide()
                snapRubberBand.reset(geometryType=core.Qgis.Point)
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
        #Método para atualizar o rubberband do pause da ferramenta
        rubberBand = self.getRubberBandToStopState()
        if rubberBand.asGeometry():
            listPoints = rubberBand.asGeometry().asPolygon() if self.isPolygon() else rubberBand.asGeometry().asPolyline()
            if self.isPolygon() and len(listPoints) >= 3:
                rubberBand.removeLastPoint()
            elif not(self.isPolygon()) and len(listPoints) >= 2:
                rubberBand.removeLastPoint()
            rubberBand.addPoint(point)

    def finishEdition(self, event):
        #Método para finalizar a aquisição
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
        #Método chamado ao ativar a ferramenta
        mapCanvas = self.getCanvas()
        mapCanvas.setCursor(self.getCursor())