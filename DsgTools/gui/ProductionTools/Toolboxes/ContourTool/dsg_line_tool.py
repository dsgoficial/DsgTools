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

from qgis.PyQt.QtCore import Qt, QSettings, pyqtSignal
from qgis.PyQt.QtGui import QColor
from qgis.gui import QgsMapTool, QgsRubberBand
from qgis.core import QgsGeometry, QgsWkbTypes

class DsgLineTool(QgsMapTool):

    lineCreated = pyqtSignal(QgsGeometry)

    def __init__(self, canvas):
        """
        Constructor
        """
        super(DsgLineTool, self).__init__(canvas)
        
        self.canvas = canvas
        self.rubberBand = None
        self.reset()

    def deactivate(self):
        """
        Deativates this tool
        """
        self.canvas.scene().removeItem(self.rubberBand)
        super(DsgLineTool, self).deactivate()
        
    def defineRubberBand(self):
        """
        Defines the rubber band style
        """
        settings = QSettings()
        myRed = int(settings.value("/qgis/default_measure_color_red", 222))
        myGreen = int(settings.value("/qgis/default_measure_color_green", 155))
        myBlue = int(settings.value("/qgis/default_measure_color_blue", 67))

        self.rubberBand = QgsRubberBand(self.canvas)
        self.rubberBand.setColor(QColor(myRed, myGreen, myBlue, 100))
        self.rubberBand.setWidth(3)
        
    def reset(self):
        """
        Resets the tool
        """
        if self.rubberBand:
            self.rubberBand.reset(QgsWkbTypes.LineGeometry)
        self.isEmittingPoint = False
        self.defineRubberBand()

    def canvasPressEvent(self, e):
        """
        Reimplementation to add a point to the rubber band or reset it
        """
        if self.isEmittingPoint:
            point = self.snapPoint(e.pos())
            self.rubberBand.addPoint(point, True)
        else:
            self.reset()

        self.isEmittingPoint = True
        
    def canvasReleaseEvent(self, e):
        """
        Reimplementation to add a vertex to the rubber band or to finish the rubber band according to the button used
        """
        point = self.snapPoint(e.pos())
        if e.button() == Qt.RightButton:
            geom = self.rubberBand.asGeometry()
            self.reset()
            self.lineCreated.emit(geom)
        elif e.button() == Qt.LeftButton:
            self.isEmittingPoint = True
            
        self.rubberBand.addPoint(point, True)

    def canvasMoveEvent(self, e):
        """
        Reimplementation to move the rubber band
        """
        if not self.isEmittingPoint:
            return
        
        point = self.snapPoint(e.pos())
        self.rubberBand.movePoint(point)
        
    def snapPoint(self, p):
        """
        Reimplementation to make use of the snap
        """
        m = self.canvas.snappingUtils().snapToMap(p)
        if m.isValid():
            return m.point()
        else:
            return self.canvas.getCoordinateTransform().toMapCoordinates(p)  