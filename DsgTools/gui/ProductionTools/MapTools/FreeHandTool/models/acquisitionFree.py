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

from qgis.PyQt import QtCore, QtGui, QtWidgets
from qgis import core, gui
from qgis.utils import iface
from qgis.core import (
    QgsGeometry,
    QgsUnitTypes,
    QgsDistanceArea,
    QgsCoordinateTransformContext,
    QgsProject,
    QgsWkbTypes,
)


class AcquisitionFree(gui.QgsMapTool):

    # Sinal usado para enviar a geometria adquirida ao finalizar aquisição
    acquisitionFinished = QtCore.pyqtSignal(QgsGeometry, bool)
    reshapeLineCreated = QtCore.pyqtSignal(QgsGeometry)

    def __init__(self, iface):
        # construtor
        self.iface = iface
        self.canvas = iface.mapCanvas()
        super(AcquisitionFree, self).__init__(self.canvas)
        self.rubberBand = None
        self.rubberBandToStopState = None
        self.drawing = False
        self.snapCursorRubberBand = None
        self.active = False
        self.contadorVert = 0
        self.stopState = False
        self.cur = QtGui.QCursor(
            QtGui.QPixmap(
                [
                    "18 13 4 1",
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
                    "                 ",
                ]
            )
        )
        self.controlPressed = False
        self.measureAction = None
        self.tooltip = None
        self.firstPoint = None

    def setCursor(self, cursor):
        # Método para definir cursor da ferramenta
        # Parâmetro de entrada: cursor (cursor usado na ferramenta)
        self.cur = cursor

    def getCursor(self):
        # Método para obter cursor da ferramenta
        # Parâmetro de retorno: cursor (cursor usado na ferramenta)
        return self.cur

    def setCanvas(self, canvas):
        # Método para definir o canvas do Qgis
        # Parâmetro de entrada: canvas (Canvas do Qgis)
        self.canvas = canvas

    def getCanvas(self):
        # Método para obter o canvas do Qgis
        # Parâmetro de retorno: canvas (Canvas do Qgis)
        return self.canvas

    def setActiveState(self, state):
        # Método para definir se a ferramenta está ativa ou não
        # Parâmetro de entrada: state (Boleano)
        self.active = state

    def getActiveState(self):
        # Método para obter se a ferramenta está ativa ou não
        # Parâmetro de retorno: state (Boleano)
        return self.active

    def setStopedState(self, state):
        # Método para definir se a ferramenta está pausada
        # Parâmetro de entrada: state (Boleano)
        self.stopState = state

    def getStopedState(self):
        # Método para obter se a ferramenta está pausada
        # Parâmetro de retorno: state (Boleano)
        return self.stopState

    def setDrawingState(self, state):
        # Método para definir se a ferramenta está desenhando
        # Parâmetro de entrada: state (Boleano)
        self.drawing = state

    def getDrawingState(self):
        # Método para obter se a ferramenta está desenhando
        # Parâmetro de retorno: state (Boleano)
        return self.drawing

    def setRubberBand(self, rb):
        # Método para definir o rubberBand de aquisição
        # Parâmetro de entrada: rb (rubberBand)
        self.rubberBand = rb

    def getRubberBand(self):
        # Método para obter o rubberBand de aquisição
        # Parâmetro de retorno: rb (rubberBand)
        return self.rubberBand

    def setRubberBandToStopState(self, rb):
        # Método para definir o rubberBand de pausa da ferramenta
        # Parâmetro de entrada: rb (rubberBand)
        self.rubberBandToStopState = rb

    def getRubberBandToStopState(self):
        # Método para obter o rubberBand de pausa da ferramenta
        # Parâmetro de retorno: rb (rubberBand)
        return self.rubberBandToStopState

    def setGeometryType(self, geomType):
        # Método para definir o tipo da geometria
        # Parâmetro de entrada: geomType (Tipo da geometria)
        self.geometryType = geomType

    def getGeometryType(self):
        # Método para obter o tipo da geometria
        # Parâmetro de retorno: geomType (Tipo da geometria)
        return self.geometryType

    def setSnapRubberBand(self, snapRb):
        # Método para definir o rubberBand do snap
        # Parâmetro de entrada: rb (rubberBand)
        self.snapCursorRubberBand = snapRb

    def getSnapRubberBand(self):
        # Método para obter o rubberBand do snap
        # Parâmetro de entrada: rb (rubberBand)
        return self.snapCursorRubberBand

    def isPolygon(self):
        # Método para testar se a camada atual é polígono
        # Parâmetro de retorno: isPolygon (Boleano)
        isPolygon = self.getGeometryType() != core.QgsWkbTypes.LineGeometry
        return isPolygon

    def keyPressEvent(self, event):
        # Método para receber os eventos do teclado
        # Parâmetro de entrada: event (Evento que chamou o método)
        if event.key() in [QtCore.Qt.Key_Delete, QtCore.Qt.Key_Backspace]:
            self.setStopedState(True)
            self.removeVertice()
            event.ignore()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.cancelEdition()
            self.showMeasureTooltip()
            event.ignore()

    def cancelEdition(self):
        # Método para cancelar aquisição
        self.getRubberBand().reset() if self.getRubberBand() else None
        self.getRubberBandToStopState().reset() if self.getRubberBandToStopState() else None
        self.setRubberBand(None)
        self.setDrawingState(False)
        self.setActiveState(False)
        self.contadorVert = 0
        self.getCanvas().refresh()

    def getParametersFromConfig(self):
        # Método para obter as configurações da tool do QSettings
        # Parâmetro de retorno: parameters (Todas os parâmetros do QSettings usado na ferramenta)
        settings = QtCore.QSettings()
        settings.beginGroup("PythonPlugins/DsgTools/Options")
        undoPoints = settings.value("undoPoints")
        settings.endGroup()
        return int(undoPoints)

    def getCloseLineTolerance(self):
        # Método para obter as configurações da tool do QSettings
        # Parâmetro de retorno: parameters (Todas os parâmetros do QSettings usado na ferramenta)
        # return 0.001
        settings = QtCore.QSettings()
        settings.beginGroup("PythonPlugins/DsgTools/Options")
        closeLineTolerancePx = settings.value("freeHandCloseLineTolerance")
        settings.endGroup()
        closeLineTolerance = self.canvas.mapUnitsPerPixel() * float(
            closeLineTolerancePx
        )
        return float(closeLineTolerance)

    def removeVertice(self):
        # Método para remover vertices
        firstPoint = None
        lastPoint = None
        rubberBand = self.getRubberBand()
        qtnUndoPoints = self.getParametersFromConfig()
        if rubberBand and rubberBand.numberOfVertices() > qtnUndoPoints:
            for x in range(qtnUndoPoints):
                rubberBand.removeLastPoint()
            if not self.isPolygon():
                lastPoint = rubberBand.asGeometry().asPolyline()[-1]
                new_rubberBand = gui.QgsRubberBand(
                    self.getCanvas(), core.QgsWkbTypes.LineGeometry
                )
                new_rubberBand.setColor(QtGui.QColor(255, 0, 0, 150))
            else:
                if len(rubberBand.asGeometry().asPolygon()[0]) > 1:
                    firstPoint = rubberBand.asGeometry().asPolygon()[0][0]
                    lastPoint = rubberBand.asGeometry().asPolygon()[0][-2]
                new_rubberBand = gui.QgsRubberBand(
                    self.getCanvas(), core.QgsWkbTypes.PolygonGeometry
                )
                new_rubberBand.setColor(QtGui.QColor(255, 0, 0, 63))
            new_rubberBand.setWidth(1)
            rubberBandToStopState = self.getRubberBandToStopState()
            if rubberBandToStopState:
                rubberBandToStopState.reset()
            new_rubberBand.setLineStyle(QtCore.Qt.DotLine)
            new_rubberBand.addPoint(lastPoint)
            if firstPoint:
                new_rubberBand.addPoint(firstPoint)
            self.setRubberBandToStopState(new_rubberBand)
        elif rubberBand:
            self.setStopedState(False)
            self.getRubberBandToStopState().reset() if self.getRubberBandToStopState() else ""
            self.cancelEdition()

    def createSnapCursor(self, point):
        # Método para criar rubberBand do snap
        rubberBand = self.getSnapRubberBand()
        if rubberBand:
            rubberBand.reset()
        else:
            rubberBand = gui.QgsRubberBand(
                self.getCanvas(), geometryType=core.QgsWkbTypes.PointGeometry
            )
        rubberBand.setColor(QtGui.QColor(255, 0, 0, 200))
        rubberBand.setFillColor(QtGui.QColor(255, 0, 0, 40))
        rubberBand.setWidth(5)
        rubberBand.setIcon(gui.QgsRubberBand.ICON_X)
        rubberBand.addPoint(point)
        self.setSnapRubberBand(rubberBand)

    def canvasReleaseEvent(self, event):
        # Método para receber os eventos release do canvas do Qgis
        # Parâmetro de entrada: event (Evento que chamou o método)
        self.getRubberBandToStopState().reset() if self.getRubberBandToStopState() else ""
        if self.getStopedState():
            self.setStopedState(False)
        elif self.getActiveState():
            self.setActiveState(False)
            self.finishEdition(event)
        else:
            self.setActiveState(True)
            self.startEdition(event)

    def startEdition(self, event):
        # Método para iniciar a aquisição
        # Parâmetro de entrada: event (Evento)
        snapRubberBand = self.getSnapRubberBand()
        if snapRubberBand:
            snapRubberBand.reset(geometryType=core.QgsWkbTypes.PointGeometry)
            snapRubberBand.hide()
            self.setSnapRubberBand(None)
        layer = self.getCanvas().currentLayer()
        if layer:
            mapPoint = event.snapPoint()
            self.firstPoint = mapPoint
            self.startRubberBand(mapPoint, layer)

    def startRubberBand(self, pointMap, layer):
        # Método para iniciar o rubberBand da aquisição
        # Parâmetro de entrada: pointMap (Primeiro ponto da feição em aquisição), layer (Camada ativa)
        self.setDrawingState(True)
        self.setGeometryType(layer.geometryType())
        if self.isPolygon():
            rubberBand = gui.QgsRubberBand(
                self.getCanvas(), core.QgsWkbTypes.PolygonGeometry
            )
            rubberBand.setColor(QtGui.QColor(255, 0, 0, 63))
            rubberBand.setWidth(2)
        else:
            rubberBand = gui.QgsRubberBand(
                self.getCanvas(), core.QgsWkbTypes.LineGeometry
            )
            rubberBand.setColor(QtGui.QColor(255, 0, 0, 150))
            rubberBand.setWidth(1)
        rubberBand.addPoint(pointMap)
        self.setRubberBand(rubberBand)

    def canvasMoveEvent(self, event):
        # Método para receber os eventos canvas move do Qgis
        # Parâmetro de entrada: event (Evento que chamou o método)
        self.dist_area = QgsDistanceArea()
        projCrs = QgsProject.instance().crs()
        self.dist_area.setSourceCrs(projCrs, QgsCoordinateTransformContext())
        ellipsoidAcronym = projCrs.ellipsoidAcronym()
        if ellipsoidAcronym != "":
            self.dist_area.setEllipsoid(ellipsoidAcronym)
        if not (self.getStopedState()):
            snapRubberBand = self.getSnapRubberBand()
            if snapRubberBand:
                snapRubberBand.hide()
                snapRubberBand.reset(geometryType=core.QgsWkbTypes.PointGeometry)
                self.setSnapRubberBand(None)
            oldPoint = event.mapPoint()
            event.snapPoint()
            point = event.mapPoint()
            closeLineTolerance = self.getCloseLineTolerance()
            self.createSnapCursor(point) if oldPoint != point or self.closeToFirstPoint(
                self.firstPoint, oldPoint, closeLineTolerance
            ) else ""
            if self.getRubberBand() and self.getRubberBand().numberOfVertices() == 0:
                self.getRubberBand().addPoint(point)
            elif self.getRubberBand():
                self.getRubberBand().addPoint(oldPoint)
        if self.getRubberBandToStopState():
            self.updateRubberBandToStopState(self.toMapCoordinates(event.pos()))
        self.showMeasureTooltip()

    def isFirstPointCloseToLastPoint(self, geometry: QgsGeometry, tolerance):
        # Método para verificar se o primeiro ponto é proximo do último ponto da linha
        # Parâmetro de entrada: geometry ( QgsGeometry ), tolerance ( float )
        if geometry.isNull() or geometry.isEmpty():
            return False
        if not geometry.wkbType() in (
            QgsWkbTypes.LineString,
            QgsWkbTypes.MultiLineString,
        ):
            return False
        multiLine = (
            geometry.asMultiPolyline()
            if geometry.isMultipart()
            else [geometry.asPolyline()]
        )
        line = multiLine[-1]
        return self.closeToFirstPoint(line[0], line[-1], tolerance)

    def closeToFirstPoint(self, firstPoint, point, tolerance):
        if firstPoint is None or point is None:
            return False
        return point.distance(firstPoint) < tolerance

    def showMeasureTooltip(self):
        if self.measureAction is None or not self.measureAction.isChecked():
            if self.tooltip is not None:
                self.tooltip.hideText()
            self.tooltip = None
            return
        rubberBand = self.getRubberBand()
        if not rubberBand:
            if self.tooltip is not None:
                self.tooltip.hideText()
            self.tooltip = None
            return
        geom = rubberBand.asGeometry()
        self.tooltip = QtWidgets.QToolTip
        if geom.type() == core.QgsWkbTypes.LineGeometry:
            length = geom.length()
            if length != None or length == 0:
                measure_dist = self.dist_area.measureLength(geom)
                dist = self.dist_area.convertLengthMeasurement(
                    measure_dist, QgsUnitTypes.DistanceMeters
                )
                # Tr
                txt = f"<b>Length: {dist:.3f} m</b><br/>"
                self.tooltip.showText(
                    self.canvas.mapToGlobal(self.canvas.mouseLastXY()),
                    txt,
                    self.canvas,
                    QtCore.QRect(),
                    5000,
                )
            else:
                self.tooltip.hideText()
        elif geom.type() == core.QgsWkbTypes.PolygonGeometry:
            area = geom.area()
            if area != None or area == 0:
                measure_dist = self.dist_area.measureArea(geom)
                dist = self.dist_area.convertAreaMeasurement(
                    measure_dist, QgsUnitTypes.AreaSquareMeters
                )
                # Tr
                txt = f"<b>Area: {dist:.3f} m²</b><br/>"
                self.tooltip.showText(
                    self.canvas.mapToGlobal(self.canvas.mouseLastXY()),
                    txt,
                    self.canvas,
                    QtCore.QRect(),
                    5000,
                )
            else:
                self.tooltip.hideText()

    def updateRubberBandToStopState(self, point):
        # Método para atualizar o rubberband do pause da ferramenta
        rubberBand = self.getRubberBandToStopState()
        if rubberBand.asGeometry():
            listPoints = (
                rubberBand.asGeometry().asPolygon()
                if self.isPolygon()
                else rubberBand.asGeometry().asPolyline()
            )
            if self.isPolygon() and self.getRubberBand():
                rubberBand.reset(geometryType=core.QgsWkbTypes.PolygonGeometry)
                firstPoint = self.getRubberBand().asGeometry().asPolygon()[0][0]
                secondPoint = self.getRubberBand().asGeometry().asPolygon()[0][-2]
                rubberBand.addPoint(secondPoint)
                rubberBand.addPoint(point)
                rubberBand.addPoint(firstPoint)
            elif not (self.isPolygon()) and len(listPoints) >= 1:
                rubberBand.removeLastPoint()
                rubberBand.addPoint(point)

    def finishEdition(self, event):
        # Método para finalizar a aquisição
        self.firstPoint = None
        if self.getRubberBand():
            event.snapPoint()
            self.getRubberBand().addPoint(event.mapPoint())
        if not self.getRubberBand():
            return
        if self.getRubberBand().numberOfVertices() > 2:
            geom = self.getRubberBand().asGeometry()
            if not self.controlPressed:
                self.acquisitionFinished.emit(
                    geom,
                    self.isFirstPointCloseToLastPoint(
                        geom, self.getCloseLineTolerance()
                    ),
                )
            else:
                self.doReshape(geom)
        self.cancelEdition()

    def doReshape(self, geom):
        line = ""
        if geom.type() == core.QgsWkbTypes.LineGeometry:
            line = geom.asPolyline()
        elif geom.type() == core.QgsWkbTypes.PolygonGeometry:
            if geom.isMultipart():
                line = geom.asMultiPolygon()[0][0]
            else:
                line = geom.asPolygon()[0]
            del line[-1]

        self.reshapeLineCreated.emit(QgsGeometry.fromPolylineXY(line))

    def setMeasureAction(self):
        self.measureAction = None
        for toolbar in iface.mainWindow().findChildren(QtWidgets.QToolBar):
            if not toolbar.objectName().lower() == "dsgtools":
                continue
            for action in toolbar.actions():
                if not action.text() == "DSGTools: Measure while digitizing":
                    continue
                self.measureAction = action

    def activate(self):
        # Método chamado ao ativar a ferramenta
        mapCanvas = self.getCanvas()
        mapCanvas.setCursor(self.getCursor())
        self.setMeasureAction()

    def deactivate(self):
        snapRubberBand = self.getSnapRubberBand()
        if snapRubberBand:
            snapRubberBand.reset(geometryType=core.QgsWkbTypes.PointGeometry)
            snapRubberBand.hide()
            self.setSnapRubberBand(None)
        QtWidgets.QApplication.restoreOverrideCursor()
        gui.QgsMapTool.deactivate(self)
        self.measureAction = None
