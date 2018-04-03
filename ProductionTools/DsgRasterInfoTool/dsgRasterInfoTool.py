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

from qgis.core import QgsGeometry, QgsRaster

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QTimer
from PyQt4.QtGui import QWidget, QToolTip, QAction, QIcon

from DsgTools.ProductionTools.DsgRasterInfoTool.bandValueTool import BandValueTool
from DsgTools.GeometricTools.DsgGeometryHandler import DsgGeometryHandler

# FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'dsgRasterInfoTool.ui'))
from DsgTools.ProductionTools.DsgRasterInfoTool.dsgRasterInfoTool_ui import Ui_DsgRasterInfoTool

class DsgRasterInfoTool(QWidget, Ui_DsgRasterInfoTool):
    """
    This class is supposed to help revision operators. It shows, on mouse hovering
    raster layer's band values. For a MDS product, altimetry is, then, given.
    Tool Behaviour:
    1- On hoverring a pixel: expose band value(s)
    2- On mouse click: create a new instance of desired layer (filled on config).
        * behaviour 2 is an extrapolation of first conception
    """
    def __init__(self, iface, parent = None):
        """
        Class constructor.
        """
        # super(QgsRasterLayer, self).__init__()
        self.canvas = iface.mapCanvas()
        super(DsgRasterInfoTool, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.splitter.hide()
        self.iface = iface
        self.timerMapTips = QTimer( self.canvas )
        self.DsgGeometryHandler = DsgGeometryHandler(iface)
        self.addShortcuts()
    
    def add_action(self, icon_path, text, callback, parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        if parent:
            parent.addAction(action)
        return action

    def addShortcuts(self):
        icon_path = ':/plugins/DsgTools/icons/rasterToolTip.png'
        text = self.tr('DSGTools: Raster information tool')
        self.activateToolAction = self.add_action(icon_path, text, self.rasterInfoPushButton.toggle, parent = self.parent)
        self.iface.registerMainWindowAction(self.activateToolAction, '')
        icon_path = ':/plugins/DsgTools/icons/band_tooltip.png'
        text = self.tr('DSGTools: Band tooltip')
        self.bandTooltipButtonAction = self.add_action(icon_path, text, self.bandTooltipButton.toggle, parent = self.parent)
        self.iface.registerMainWindowAction(self.bandTooltipButtonAction, '')
        icon_path = ':/plugins/DsgTools/icons/dynamic_histogram_viewer.png'
        text = self.tr('DSGTools: Dynamic Histogram Viewer')
        self.dynamicHistogramButtonAction = self.add_action(icon_path, text, self.dynamicHistogramButton.toggle, parent = self.parent)
        self.iface.registerMainWindowAction(self.dynamicHistogramButtonAction, '')
        # self.timerMapTips.timeout.connect( self.showToolTip )
    
    def deactivate(self):
        self.activateBandValueTool(False)
        self.activateStretchTool(False)

    @pyqtSlot(bool, name = 'on_rasterInfoPushButton_toggled')
    def toggleBar(self, toggled=None):
        """
        Shows/Hides the tool bar
        """
        if toggled is None:
            toggled = self.rasterInfoPushButton.isChecked()
        if toggled:
            self.splitter.show()
        else:
            self.splitter.hide()      
    
    @pyqtSlot(bool, name = 'on_bandTooltipButton_toggled')
    def activateBandValueTool(self, state):
        if state:
            self.iface.mapCanvas().xyCoordinates.connect(self.showToolTip)
        else:
            self.iface.mapCanvas().xyCoordinates.disconnect(self.showToolTip)
    
    @pyqtSlot(bool, name = 'on_dynamicHistogramButton_toggled')
    def activateStretchTool(self, state):
        if state:
            self.iface.mapCanvas().extentsChanged.connect(self.stretch_raster)
        else:
            self.iface.mapCanvas().extentsChanged.disconnect(self.stretch_raster)
    
    def stretch_raster(self):
        try:
            layer = self.rasterComboBox.currentLayer()
            self.iface.mainWindow().findChild( QAction, 'mActionLocalCumulativeCutStretch' ).trigger()
        except AttributeError:
            pass
    
    def getPixelValue(self, mousePos, rasterLayer):
        """
        
        """
        rasterCrs = rasterLayer.crs()
        mousePosGeom = QgsGeometry.fromPoint(mousePos)
        canvasCrs = self.canvas.mapRenderer().destinationCrs()
        self.DsgGeometryHandler.reprojectFeature(mousePosGeom, rasterCrs, canvasCrs)
        mousePos = mousePosGeom.asPoint()
        # identify pixel(s) information
        i = rasterLayer.dataProvider().identify( mousePos, QgsRaster.IdentifyFormatValue )
        if i.isValid():
            text = ", ".join(['{0:g}'.format(r) for r in i.results().values() if r is not None] )
        else:
            text = ""
        return text

    def showToolTip(self, qgsPoint):
        """
        
        """
        self.timerMapTips.stop()
        self.timerMapTips.start( 6000 ) # time in milliseconds
        if self.canvas.underMouse():
            raster = self.rasterComboBox.currentLayer()
            if raster:
                text = self.getPixelValue(qgsPoint, raster)
                p = self.canvas.mapToGlobal( self.canvas.mouseLastXY() )
                QToolTip.showText( p, text, self.canvas )