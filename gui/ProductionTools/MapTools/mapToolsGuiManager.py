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
# from DsgTools.ProductionTools.Acquisition.acquisition import Acquisition
# from DsgTools.ProductionTools.FreeHandTool.freeHandMain import FreeHandMain
# from DsgTools.ProductionTools.FlipLineTool.flipLineTool import FlipLine
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
        self.genericTool = GenericSelectionTool(self.iface)
        icon_path = self.iconBasePath + '/genericSelect.png'
        toolTip = self.tr("DSGTools: Generic Selector\nLeft Click: select feature's layer and put it on edit mode\nRight Click: Open feature's form\nControl+Left Click: add/remove feature from selection\nShift+Left Click+drag and drop: select all features that intersects rubberband.")
        self.manager.add_action(
            icon_path,
            text=self.tr('DSGTools: Generic Selector'),
            callback=self.activateGenericTool,
            add_to_menu=True,
            add_to_toolbar=True,
            withShortcut = True,
            tooltip = toolTip,
            parentToolbar = self.parentMenu
        )
    
    def activateGenericTool(self):
        self.iface.mapCanvas().setMapTool(self.genericTool)
    
    def unload(self):
        self.genericTool.unload()