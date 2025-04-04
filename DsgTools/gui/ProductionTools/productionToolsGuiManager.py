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



from qgis.PyQt.QtCore import QObject
from .Toolboxes.toolBoxesGuiManager import ToolBoxesGuiManager
from .MapTools.mapToolsGuiManager import MapToolsGuiManager
from .Toolbars.toolBarsGuiManager import ToolbarsGuiManager


class ProductionToolsGuiManager(QObject):
    def __init__(self, manager, iface, parentMenu=None, toolbar=None):
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        super(ProductionToolsGuiManager, self).__init__()
        self.manager = manager
        self.iface = iface
        self.parentMenu = parentMenu
        self.toolbar = toolbar
        self.menu = self.manager.addMenu(
            "productiontools", self.tr("Production Tools"), "productiontools.png"
        )
        self.stackButton = self.manager.createToolButton(
            self.toolbar, "ProductionTools"
        )
        self.iconBasePath = ":/plugins/DsgTools/icons/"

    def initGui(self):
        self.toolBoxesGuiManager = ToolBoxesGuiManager(
            self.manager, self.iface, parentMenu=self.menu, stackButton=self.stackButton
        )
        self.toolBoxesGuiManager.initGui()
        self.menu.addSeparator()
        self.mapToolsGuiManager = MapToolsGuiManager(
            self.manager, self.iface, parentMenu=self.menu, toolbar=self.toolbar
        )
        self.mapToolsGuiManager.initGui()
        self.menu.addSeparator()
        self.toolbarsGuiManager = ToolbarsGuiManager(
            self.manager, self.iface, parentMenu=self.menu, toolbar=self.toolbar
        )
        self.toolbarsGuiManager.initGui()

    def unload(self):
        self.toolBoxesGuiManager.unload()
        del self.toolBoxesGuiManager
        self.mapToolsGuiManager.unload()
        del self.mapToolsGuiManager
        self.toolbarsGuiManager.unload()
        del self.toolbarsGuiManager
        del self.stackButton
