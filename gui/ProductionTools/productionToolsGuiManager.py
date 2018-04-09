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

from ..guiManager import GuiManager 
# from .MapTools.mapToolsGuiManager import MapToolsGuiManager

class ProductionToolsGuiManager(GuiManager):

    def __init__(self, iface, parentMenu = None, toolbar = None):
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interfa
        super(ProductionToolsGuiManager, self).__init__(iface, parentMenu = parentMenu, toolbar = toolbar)
        self.menu = self.addMenu(u'productiontools', self.tr('Production Tools'),'productiontools.png')
        self.stackButton = self.createToolButton(self.toolbar, u'ProductionTools')
    
    def initGui(self):
        pass
        # self.mapToolsGuiManager = MapToolsGuiManager(self.iface, parentMenu=self.menu, toolbar = self.toolbar)
        # self.mapToolsGuiManager.initGui()