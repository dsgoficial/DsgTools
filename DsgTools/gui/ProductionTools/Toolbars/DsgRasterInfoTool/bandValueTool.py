# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2018-03-29
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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

import os
from qgis.core import QgsRasterLayer, QgsRaster, QgsGeometry, QgsPoint
from qgis.gui import QgsMapTool, QgsMapToolEmitPoint
from qgis.PyQt import QtGui, uic
from qgis.PyQt.QtCore import QTimer
from qgis.PyQt.QtWidgets import QToolTip

from .....core.GeometricTools.geometryHandler import GeometryHandler

class BandValueTool(QgsMapTool):
    """
    This class is supposed to help revision operators. It shows, on mouse hovering
    raster layer's band values. For a MDS product, altimetry is, then, given.
    Tool Behaviour:
    1- On hoverring a pixel: expose band value(s)
    2- On mouse click: create a new instance of desired layer (filled on config).
        * behaviour 2 is an extrapolation of first conception
    """
    def __init__(self, iface, parent):
        """
        Class constructor.
        """
        # super(QgsRasterLayer, self).__init__()
        self.canvas = iface.mapCanvas()
        super(BandValueTool, self).__init__(self.canvas)
        self.parent = parent
        self.iface = iface
        self.toolAction = None
        self.QgsMapToolEmitPoint = QgsMapToolEmitPoint(self.canvas)
        self.geometryHandler = GeometryHandler(iface)
        self.timerMapTips = QTimer( self.canvas )
        self.timerMapTips.timeout.connect( self.showToolTip )
        self.activated = False
        self.canvasCrs = self.canvas.mapRenderer().destinationCrs()
    
    def setAction(self, action):
        """
        
        """
        self.toolAction = action

    def activate(self):
        """
        Activates tool.
        """
        if self.toolAction:
            self.activated = True
        QgsMapTool.activate(self)
        self.canvas.setMapTool(self)
    
    def deactivate(self):
        """
        Deactivates tool.
        """
        self.timerMapTips.stop()
        try:
            if self.toolAction:
                self.activated = False
                self.toolAction.setChecked(False)
            if self is not None:
                QgsMapTool.deactivate(self)
        except:
            pass        

    def canvasMoveEvent(self, e):
        QToolTip.hideText()
        self.timerMapTips.start( 500 ) # time in milliseconds
        self.showToolTip()               
    
    def getPixelValue(self, rasterLayer):
        """
        
        """
        rasterCrs = rasterLayer.crs()
        mousePos = self.QgsMapToolEmitPoint.toMapCoordinates(self.canvas.mouseLastXY())
        mousePosGeom = QgsGeometry.fromPoint(mousePos)
        self.geometryHandler.reprojectFeature(mousePosGeom, rasterCrs, self.canvasCrs)
        mousePos = mousePosGeom.asPoint()
        # identify pixel(s) information
        i = rasterLayer.dataProvider().identify( mousePos, QgsRaster.IdentifyFormatValue )
        if i.isValid():
            text = ", ".join(['{0:g}'.format(r) for r in list(i.results().values()) if r is not None] )
        else:
            text = ""
        return text

    def showToolTip(self):
        """
        
        """
        self.timerMapTips.stop()
        if self.canvas.underMouse():
            raster = self.parent.rasterComboBox.currentLayer()
            if raster:
                text = self.getPixelValue(raster)
                p = self.canvas.mapToGlobal( self.canvas.mouseLastXY() )
                QToolTip.showText( p, text, self.canvas )