# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-04-12
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

from .ReviewTools.reviewToolbar import ReviewToolbar

from .MinimumAreaTool.minimumAreaTool import MinimumAreaTool
from .InspectFeatures.inspectFeatures import InspectFeatures
from .StyleManagerTool.styleManagerTool import StyleManagerTool
from .DsgRasterInfoTool.dsgRasterInfoTool import DsgRasterInfoTool
from .DataValidationTool.dataValidationTool import DataValidationTool
from qgis.PyQt.QtCore import QObject

class ToolbarsGuiManager(QObject):

    def __init__(self, manager, iface, parentMenu = None, toolbar = None):
        """Constructor.
        """
        super(ToolbarsGuiManager, self).__init__()
        self.manager = manager
        self.iface = iface
        self.parentMenu = parentMenu
        self.toolbar = toolbar
        self.toolbarList = []
        self.iconBasePath = ':/plugins/DsgTools/icons/'
    
    def initGui(self):
        #adding minimum area tool
        self.minimumAreaTool = MinimumAreaTool(self.iface, parent = self.parentMenu)
        self.createToolbarAndAddWidget(
            name=u'DSGTools_Minimum_Area_Tool',
            widget=self.minimumAreaTool
        )
        #adding inspect feature tool
        self.inspectFeaturesTool = InspectFeatures(self.iface, parent = self.parentMenu)
        self.createToolbarAndAddWidget(
            name=u'DSGTools_Inspect_Features',
            widget=self.inspectFeaturesTool
        )
        #adding review tool
        self.reviewTool = ReviewToolbar(self.iface, parent = self.parentMenu)
        self.createToolbarAndAddWidget(
            name=u'DSGTools_Review_Toolbar',
            widget=self.reviewTool
        )
        #adding style tools
        self.styleManagerTool = StyleManagerTool(self.iface, parent = self.parentMenu)
        self.createToolbarAndAddWidget(
            name=u'DSGTools_Style_Manager',
            widget=self.styleManagerTool
        )
        #adding raster info tool
        self.rasterInfoTool = DsgRasterInfoTool(self.iface, parent = self.parentMenu)
        self.createToolbarAndAddWidget(
            name=u'DSGTools_Raster_Info',
            widget=self.rasterInfoTool
        )
        #adding raster info tool
        self.dataValidationTool = DataValidationTool(self.iface, parent = self.parentMenu)
        self.createToolbarAndAddWidget(
            name=u'DSGTools_Data_Validation',
            widget=self.dataValidationTool
        )
    
    def createToolbar(self, name):
        toolbar = self.iface.addToolBar(name)
        toolbar.setObjectName(name)
        self.toolbarList.append(toolbar)
        return toolbar
    
    def createToolbarAndAddWidget(self, name, widget):
        toolbar = self.createToolbar(name)
        toolbar.addWidget(widget)
    
    def unload(self):
        self.minimumAreaTool.unload()
        self.inspectFeaturesTool.unload()
        self.reviewTool.unload()
        self.rasterInfoTool.unload()
        self.dataValidationTool.unload()
        for toolbar in self.toolbarList:
            self.iface.mainWindow().removeToolBar(toolbar)
            del toolbar
