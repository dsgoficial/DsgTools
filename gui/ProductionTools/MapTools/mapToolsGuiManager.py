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

from .GenericSelectionTool.genericSelectionTool import GenericSelectionTool
from .Acquisition.acquisition import Acquisition
from .FlipLineTool.flipLineTool import FlipLine
from .FreeHandTool.freeHandMain import FreeHandMain
from qgis.PyQt.QtCore import QObject

class MapToolsGuiManager(QObject):

    def __init__(self, manager, iface, parentMenu = None, toolbar = None):
        """Constructor.
        """
        super(MapToolsGuiManager, self).__init__()
        self.manager = manager
        self.iface = iface
        self.parentMenu = parentMenu
        self.toolbar = toolbar
        self.iconBasePath = ':/plugins/DsgTools/icons/'
    
    def initGui(self):
        #adding generic selection tool
        self.genericTool = GenericSelectionTool(self.iface)
        self.genericTool.addTool(self.manager, self.activateGenericTool, self.parentMenu, self.iconBasePath)
        #adding flip line tool
        self.flipLineTool = FlipLine(self.iface)
        self.flipLineTool.addTool(self.manager, self.flipLineTool.startFlipLineTool, self.parentMenu, self.iconBasePath)
        #adding acquisition
        self.acquisition = Acquisition(self.iface)
        self.acquisition.addTool(self.manager, None, self.parentMenu, self.iconBasePath)
        #adding free hand tool
        self.freeHandAcquisiton = FreeHandMain(self.iface)
        self.freeHandAcquisiton.addTool(self.manager, None, self.parentMenu, self.iconBasePath)
        
    
    def activateGenericTool(self):
        self.iface.mapCanvas().setMapTool(self.genericTool)
    
    def unload(self):
        self.genericTool.unload()