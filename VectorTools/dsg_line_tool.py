# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-11-10
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
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

from PyQt4.QtCore import Qt, QSettings, pyqtSignal
from PyQt4.QtGui import QColor
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.core import QgsGeometry, QGis

class DsgLineTool(QgsMapTool):

    lineCreated = pyqtSignal(QgsGeometry)

    def __init__(self, canvas):
        super(DsgLineTool, self).__init__(canvas)
        
        self.canvas = canvas
        self.defineRubberBand()
        self.reset()

    def deactivate(self):
        self.canvas.scene().removeItem(self.rubberBand)
        super(DsgLineTool, self).deactivate()
        
    def defineRubberBand(self):
        settings = QSettings()
        myRed = int(settings.value("/qgis/default_measure_color_red", 222))
        myGreen = int(settings.value("/qgis/default_measure_color_green", 155))
        myBlue = int(settings.value("/qgis/default_measure_color_blue", 67))

        self.rubberBand = QgsRubberBand(self.canvas)
        self.rubberBand.setColor(QColor(myRed, myGreen, myBlue, 100))
        self.rubberBand.setWidth(3)
        
    def reset(self):
        self.isEmittingPoint = False
        self.rubberBand.reset(QGis.Line)

    def canvasPressEvent(self, e):
        if self.isEmittingPoint:
            point = self.snapPoint(e.pos())
            self.rubberBand.addPoint(point, True)
        else:
            self.reset()

        self.isEmittingPoint = True
        
    def canvasReleaseEvent(self, e):
        point = self.snapPoint(e.pos())
        if e.button() == Qt.RightButton:
            geom = self.rubberBand.asGeometry()
            self.reset()
            self.lineCreated.emit(geom)
        elif e.button() == Qt.LeftButton:
            self.isEmittingPoint = True
            
        self.rubberBand.addPoint(point, True)

    def canvasMoveEvent(self, e):
        if not self.isEmittingPoint:
            return
        
        point = self.snapPoint(e.pos())
        self.rubberBand.movePoint(point)
        
    def snapPoint(self, p):
        m = self.canvas.snappingUtils().snapToMap(p)
        if m.isValid():
            return m.point()
        else:
            return self.canvas.getCoordinateTransform().toMapCoordinates(p)  