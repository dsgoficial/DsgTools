# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-11-06
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

from qgis.PyQt.QtCore import QObject

from DsgTools.gui.ServerTools.ViewServersGui.viewServersGui import ViewServersGui
from DsgTools.gui.ServerTools.BatchDbManagerGui.batchDbManagerGui import (
    BatchDbManagerGui,
)


class ServerToolsGuiManager(QObject):
    def __init__(self, manager, iface, parentMenu=None, toolbar=None):
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        super(ServerToolsGuiManager, self).__init__()
        self.manager = manager
        self.iface = iface
        self.parentMenu = parentMenu
        # self.dbAbstract = dbAbstract
        self.toolbar = toolbar
        self.menu = self.manager.addMenu(
            "server", self.tr("Servers Tools"), "server.png"
        )
        self.iconBasePath = ":/plugins/DsgTools/icons/"

    def addTool(self, text, callback, parentMenu, icon):
        """
        Prepares the funcionalities to be added to both the DSGTools menu and it's shortcut button into QGIS main interface.
        :param text: (str) text to be shown when the action is hovered over.
        :param callback: (method/function) desired behavior for when action is activated.
        :param parentMenu: (QMenu) menu to which action will be added.
        :param parentButton: (QButton) button to which action will be associated.
        """
        icon_path = self.iconBasePath + icon
        action = self.manager.add_action(
            icon_path,
            text=text,
            callback=callback,
            add_to_menu=False,
            add_to_toolbar=False,
            withShortcut=False,
            parentToolbar=parentMenu,
            isCheckable=False,
        )

    def initGui(self):
        """
        Instantiates all available database creation GUI.
        """
        self.viewServersGui = ViewServersGui(manager=self, parentMenu=self.menu)
        self.viewServersGui.initGui()
        self.batchDbManagerGui = BatchDbManagerGui(manager=self, parentMenu=self.menu)
        self.batchDbManagerGui.initGui()

    def unload(self):
        """
        Unloads all loaded GUI.
        """
        self.viewServersGui.unload()
        self.batchDbManagerGui.unload()
