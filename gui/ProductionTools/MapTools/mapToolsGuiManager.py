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

from ...guiManager import GuiManager

class MapToolsGuiManager(GuiManager):

    def __init__(self, iface, parentMenu = None, toolbar = None):
        """Constructor.
        """
        super(MapToolsGuiManager, self).__init__(iface, parentMenu = parentMenu, toolbar = toolbar)
    
    def initGui(self):
        self.genericTool = GenericSelectionTool(self.iface)
        icon_path = self.iconBasePath + '/genericSelect.png'
        toolTip = self.tr("DSGTools: Generic Selector\nLeft Click: select feature's layer and put it on edit mode\nRight Click: Open feature's form\nControl+Left Click: add/remove feature from selection\nShift+Left Click+drag and drop: select all features that intersects rubberband.")
        self.add_action(
            icon_path,
            text=self.tr('DSGTools: Generic Selector'),
            callback=self.genericTool.activate,
            add_to_menu=True,
            add_to_toolbar=True,
            withShortcut = True,
            toolTip = toolTip
        )
    
    def unload(self):
        self.genericTool.unload()