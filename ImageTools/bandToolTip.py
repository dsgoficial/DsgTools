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
from PyQt4 import QtGui, uic
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QToolTip

from DsgTools.GeometricTools.DsgGeometryHandler import DsgGeometryHandler

FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'bandToolTip.ui'))

class PxBandValueToolTip(QgsMapTool, FORM_CLASS):
    """
    This class is supposed to help revision operators. It shows, on mouse hovering
    raster layer's band values. For a MDS product, altimetry is, then, given.
    Tool Behaviour:
    1- On hoverring a pixel: expose band value(s)
    2- On mouse click: create a new instance of desired layer (filled on config).
        * behaviour 2 is an extrapolation of first conception
    """
    def __init__(self, iface):
        """
        Class constructor.
        """
        # super(QgsRasterLayer, self).__init__()
        self.canvas = iface.mapCanvas()
        super(QgsMapTool, self).__init__(self.canvas)
        self.iface = iface
        self.toolAction = None
        self.QgsMapToolEmitPoint = QgsMapToolEmitPoint(self.canvas)
        self.timerMapTips = QTimer( self.canvas )
        self.timerMapTips.timeout.connect( self.showToolTip )
        self.DsgGeometryHandler = DsgGeometryHandler(iface)
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
            self.toolAction.setChecked(True)
        QgsMapTool.activate(self)
    
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

    def canvasPressEvent(self, e):
        """
        Create a feature of Selected Layer.
        TODO
        """
        pass

    def canvasMoveEvent(self, e):
        QToolTip.hideText()
        self.timerMapTips.start( 500 ) # time in milliseconds
        self.showToolTip()

    def getRasterLayers(self):
        """
        Gets all loaded raster layers.
        """
        rasters = []
        lyrs = self.canvas.layers()
        for lyr in lyrs:
            if isinstance(lyr, QgsRasterLayer):
                rasters.append(lyr)
        return rasters                
    
    def getPixelValue(self, rasterLayer):
        """
        
        """
        rasterCrs = rasterLayer.crs()
        mousePos = self.QgsMapToolEmitPoint.toMapCoordinates(self.canvas.mouseLastXY())
        mousePosGeom = QgsGeometry.fromPoint(mousePos)
        self.DsgGeometryHandler.reprojectFeature(mousePosGeom, rasterCrs, self.canvasCrs)
        mousePos = mousePosGeom.asPoint()
        # identify pixel(s) information
        i = rasterLayer.dataProvider().identify( mousePos, QgsRaster.IdentifyFormatValue )
        if i.isValid():
            text = ", ".join(['{0:g}'.format(r) for r in i.results().values() if r is not None] )
        else:
            text = ""
        return text

    def showToolTip(self):
        """
        
        """
        self.timerMapTips.stop()
        if self.canvas.underMouse():
            raster = self.getRasterLayers()
            raster = raster[0] if raster else None
            if raster:
                text = self.getPixelValue(raster)
                p = self.canvas.mapToGlobal( self.canvas.mouseLastXY() )
                QToolTip.showText( p, text, self.canvas )

    def openDialog(self):
        self.canvas.setMapTool(PxBandValueToolTip(self.iface))