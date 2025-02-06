# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-04-16
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

from qgis.PyQt.QtCore import QObject, Qt
from .LoadLayersFromServer.loadLayersFromServer import LoadLayersFromServer
from .CreateFrameTool.ui_create_inom_dialog import CreateInomDialog


class LayerToolsGuiManager(QObject):
    def __init__(self, manager, iface, parentMenu=None, toolbar=None):
        """Constructor."""
        super(LayerToolsGuiManager, self).__init__()
        self.manager = manager
        self.iface = iface
        self.parentMenu = parentMenu
        self.toolbar = toolbar
        self.menu = self.manager.addMenu("layers", self.tr("Layer Tools"), "layers.png")
        self.stackButton = self.manager.createToolButton(self.toolbar, "LayerTools")
        self.iconBasePath = ":/plugins/DsgTools/icons/"

    def addTool(self, text, callback, parentMenu, icon, defaultButton=False):
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
        self.stackButton.addAction(action)
        if defaultButton:
            self.stackButton.setDefaultAction(action)

    def initGui(self):
        # adding minimum area tool
        self.addTool(
            self.tr("Load Layers"),
            self.loadLayersFromServer,
            self.menu,
            "category.png",
            defaultButton=True,
        )
        self.addTool(
            self.tr("Create Frame"),
            self.createFrame,
            self.menu,
            "frame.png",
            defaultButton=False,
        )

    def unload(self):
        pass

    def loadLayersFromServer(self):
        """
        Shows the dialog that loads layers from server
        """
        dlg = LoadLayersFromServer(self.iface)
        dlg.setWindowFlags(dlg.windowFlags() | Qt.WindowStaysOnTopHint)
        dlg.show()
        result = dlg.exec_()
        if result:
            pass

    def createFrame(self):
        """
        Shows the create frame dialog
        """

        dlg = CreateInomDialog(self.iface)
        dlg.show()
        result = dlg.exec_()
        if result:
            pass
