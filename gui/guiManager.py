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

from qgis.PyQt.QtCore import QObject, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QToolButton, QMenu, QAction

from .BDGExTools.bdgexGuiManager import BDGExGuiManager
from .LayerTools.layerToolsGuiManager import LayerToolsGuiManager
from .ProductionTools.productionToolsGuiManager import ProductionToolsGuiManager
from .DatabaseTools.databaseManager import DatabaseGuiManager
from .ServerTools.serverToolsGuiManager import ServerToolsGuiManager
from .AboutAndFurtherInfo.aboutAndFurtherInfoGuiManager import AboutAndFurtherInfoGuiManager

class GuiManager(QObject):

    def __init__(self, iface, parentMenu = None, toolbar = None):
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        super(GuiManager, self).__init__()
        self.iface = iface
        self.menu = parentMenu
        self.iconBasePath = ':/plugins/DsgTools/icons/'
        self.actions = []
        self.managerList = []
        self.menuList = []
        self.toolbar = toolbar

    def addMenu(self, name, title, icon_file, parentMenu = None):
        """
        Adds a QMenu
        """
        child = QMenu(self.menu)
        child.setObjectName(name)
        child.setTitle(self.tr(title))
        child.setIcon(QIcon(self.iconBasePath+icon_file))
        if parentMenu:
            parentMenu.addMenu(child)
        else:
            self.menu.addMenu(child)
        self.menuList.append(child)
        return child

    def createToolButton(self, parent, text):
        """
        Creates a tool button (pop up menu)
        """
        button = QToolButton(parent)
        button.setObjectName(text)
        button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button.setPopupMode(QToolButton.MenuButtonPopup)
        parent.addWidget(button)
        self.actions.append(button)
        return button
    
    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None,
        parentMenu = None,
        withShortcut=False,
        tooltip = None,
        parentToolbar = None,
        parentButton = None,
        isCheckable = False):
        """Add a toolbar icon to the InaSAFE toolbar.
        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str
        :param text: Text that should be shown in menu items for this action.
        :type text: str
        :param callback: Function to be called when the action is triggered.
        :type callback: function
        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool
        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool
        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool
        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str
        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget
        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.
        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)
        if whats_this is not None:
            action.setWhatsThis(whats_this)
        if add_to_toolbar:
            self.toolbar.addAction(action)
        if add_to_menu:
            self.menu.addAction(action)
        if parentMenu:
            parentMenu.addAction(action)
        if withShortcut:
            self.iface.registerMainWindowAction(action, '')
        if isCheckable:
            action.setCheckable(True)
        if tooltip:
            action.setToolTip(tooltip)
        if parentToolbar:
            parentToolbar.addAction(action)
        if parentButton:
            parentButton.addAction(action)
        self.actions.append(action)
        return action
    
    def instantiateManagers(self):
        self.serverToolsGuiManager = ServerToolsGuiManager(self, self.iface, parentMenu=self.menu, toolbar=self.toolbar)
        self.managerList.append(self.serverToolsGuiManager)
        self.databaseGuiManager = DatabaseGuiManager(self, self.iface, parentMenu=self.menu, toolbar=self.toolbar)
        self.managerList.append(self.databaseGuiManager)
        self.layerToolsGuiManager = LayerToolsGuiManager(self, self.iface, parentMenu = self.menu, toolbar = self.toolbar)
        self.managerList.append(self.layerToolsGuiManager)
        self.bdgexGuiManager = BDGExGuiManager(self, self.iface, parentMenu = self.menu, toolbar = self.toolbar)
        self.managerList.append(self.bdgexGuiManager)
        self.productionToolsGuiManager = ProductionToolsGuiManager(self, self.iface, parentMenu = self.menu, toolbar = self.toolbar)
        self.managerList.append(self.productionToolsGuiManager)
        self.aboutAndFurtherGuiManager = AboutAndFurtherInfoGuiManager(self, self.iface, parentMenu = self.menu, toolbar = self.toolbar)
        self.managerList.append(self.aboutAndFurtherGuiManager)
    
    def initGui(self):
        self.instantiateManagers()
        for manager in self.managerList:
            manager.initGui()
    
    def unload(self):
        for manager in self.managerList:
            manager.unload()
        for action in self.actions:
            try:
                self.iface.unregisterMainWindowAction(action)
            except:
                pass