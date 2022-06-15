# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-04-08
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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

from __future__ import absolute_import
from builtins import object
import os.path
import sys
from DsgTools.gui.ProductionTools.MapTools.SelectRasterTool.selectRaster import SelectRasterTool

from qgis.PyQt.QtCore import pyqtSignal
from qgis.core import QgsVectorLayer

from .GenericSelectionTool.genericSelectionTool import GenericSelectionTool
from .Acquisition.acquisition import Acquisition
from .FlipLineTool.flipLineTool import FlipLine
from .FreeHandTool.freeHandMain import FreeHandMain
from .FreeHandTool.freeHandReshape import FreeHandReshape
from .LabelTogglingTool.labelTogglingTool import LabelTogglingTool
from .ShortcutTool.shortcutTool import ShortcutTool
from qgis.PyQt.QtCore import QObject

class MapToolsGuiManager(QObject):
    # signals to replicate current layer's editing started/stopped signal
    editingStarted = pyqtSignal()
    editingStopped = pyqtSignal()

    def __init__(self, manager, iface, parentMenu = None, toolbar = None):
        """Constructor.
        """
        super(MapToolsGuiManager, self).__init__()
        self.manager = manager
        self.iface = iface
        self.parentMenu = parentMenu
        self.toolbar = toolbar
        self.iconBasePath = ':/plugins/DsgTools/icons/'
        # initiate current layer and make sure signals are connected
        self.currentLayer = None
        self.resetCurrentLayerSignals()
        self.iface.currentLayerChanged.connect(self.resetCurrentLayerSignals)

    def initGui(self):
        #adding generic selection tool
        self.genericTool = GenericSelectionTool(self.iface)
        self.genericTool.addTool(self.manager, self.activateGenericTool, self.parentMenu, self.iconBasePath)
        #adding select raster
        self.rasterSelectTool = SelectRasterTool(self.iface)
        self.rasterSelectTool.addTool(self.manager, self.rasterSelectTool.run, self.parentMenu, self.iconBasePath)
        #adding flip line tool
        self.flipLineTool = FlipLine(self.iface)
        self.flipLineTool.addTool(self.manager, self.flipLineTool.startFlipLineTool, self.parentMenu, self.iconBasePath)
        self.flipLineTool.setToolEnabled(self.iface.mapCanvas().currentLayer())
        #adding acquisition
        self.acquisition = Acquisition(self.iface)
        self.acquisition.addTool(self.manager, None, self.parentMenu, self.iconBasePath)
        self.acquisition.setToolEnabled()
        #adding stack
        self.freeHandStackButton = self.manager.createToolButton(self.toolbar, u'FreeHandTools')
        #adding free hand tool (acquisition)
        self.freeHandAcquisiton = FreeHandMain(self.iface)
        self.freeHandAcquisiton.addTool(self.manager, None, self.parentMenu, self.iconBasePath, parentButton=self.freeHandStackButton, defaultButton=True)
        self.freeHandAcquisiton.acquisitionFreeController.setToolEnabled()
        #adding free hand tool (acquisition)
        self.freeHandReshape = FreeHandReshape(self.iface)
        self.freeHandReshape.addTool(self.manager, None, self.parentMenu, self.iconBasePath, parentButton=self.freeHandStackButton)
        self.freeHandReshape.acquisitionFreeController.setToolEnabled()
        #adding label toggling tool
        self.labelStackButton = self.manager.createToolButton(self.toolbar, u'LabelTools')
        self.labelTool = LabelTogglingTool(self.iface)
        self.labelTool.addTool(self.manager, None, self.toolbar, self.labelStackButton, self.iconBasePath)
        #adding shortcuts tools
        self.shortcutsTool = ShortcutTool(self.iface)
        self.shortcutsTool.addTool(self.manager, None, self.toolbar, self.labelStackButton, self.iconBasePath)

        #initiate tools signals
        self.initiateToolsSignals()

    def resetCurrentLayerSignals(self):
        """
        Resets all signals used from current layer connected to maptools to current selection.
        """
        if isinstance(self.currentLayer, QgsVectorLayer):
            # disconnect previous selection's signals, if any
            try:
                self.currentLayer.editingStarted.disconnect(self.editingStarted)
                self.currentLayer.editingStopped.disconnect(self.editingStopped)
            except:
                pass
        # now retrieve current selection and reset signal connection
        self.currentLayer = self.iface.mapCanvas().currentLayer()
        if isinstance(self.currentLayer, QgsVectorLayer):
            self.currentLayer.editingStarted.connect(self.editingStarted)
            self.currentLayer.editingStopped.connect(self.editingStopped)

    def initiateToolsSignals(self):
        """
        Connects all tools' signals.
        """
        for tool in [self.flipLineTool, self.acquisition, self.freeHandAcquisiton.acquisitionFreeController, \
                     self.freeHandReshape.acquisitionFreeController]:
            # connect current layer changed signal to all tools that use it
            self.iface.currentLayerChanged.connect(tool.setToolEnabled)
            # connect editing started/stopped signals to all tools that use it
            self.editingStarted.connect(tool.setToolEnabled)
            self.editingStopped.connect(tool.setToolEnabled)
            # connect edit button toggling signal to all tools that use it
            self.iface.actionToggleEditing().triggered.connect(tool.setToolEnabled)
        # free hand has its own signal connected when started
        for free_hand_tool in [self.freeHandAcquisiton, self.freeHandReshape]:
            free_hand_tool.acquisitionFreeController.actionAcquisitionFree.triggered.connect(\
                    free_hand_tool.acquisitionFreeController.activateTool)
            free_hand_tool.acquisitionFreeController.acquisitionFree.acquisitionFinished.connect(\
                    free_hand_tool.acquisitionFreeController.createFeature)
            free_hand_tool.acquisitionFreeController.acquisitionFree.reshapeLineCreated.connect(\
                    free_hand_tool.acquisitionFreeController.reshapeSimplify)

    def activateGenericTool(self):
        self.iface.mapCanvas().setMapTool(self.genericTool)
    
    def activateRasterSelectTool(self):
        self.iface.mapCanvas().setMapTool(self.rasterSelectTool)

    def unload(self):
        self.genericTool.unload()
        self.rasterSelectTool.unload()