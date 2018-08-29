# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-04-08
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

from __future__ import absolute_import

from qgis.PyQt.QtCore import QObject

from DsgTools.gui.DatabaseTools.DbTools.PostGISTool.postgisDBTool import PostgisDBTool
from DsgTools.gui.DatabaseTools.DbTools.SpatialiteTool.cria_spatialite_dialog import CriaSpatialiteDialog

class DatabaseGuiManager(QObject):

    def __init__(self, manager, iface, parentMenu=None, toolbar=None):
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        super(DatabaseGuiManager, self).__init__()
        self.manager = manager
        self.iface = iface
        self.parentMenu = parentMenu
        # self.dbAbstract = dbAbstract
        self.toolbar = toolbar
        self.menu = self.manager.addMenu(u'databasetools', self.tr('Database Tools'),'database.png')
        self.stackButton = self.manager.createToolButton(self.toolbar, u'DatabaseTools')
        self.iconBasePath = ':/plugins/DsgTools/icons/'
    
    def addTool(self, text, callback, parentMenu, icon, parentButton=None, defaultButton=False):
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
            parentButton=self.stackButton
        )
        if defaultButton:
            self.stackButton.setDefaultAction(action)

    def initGui(self):
        # self.postgisManager = (self.manager, self.iface, parentMenu=self.menu, stackButton=self.stackButton)
        # self.postgisManager.initGui()
        self.spatialiteDialog = CriaSpatialiteDialog(manager=self, parentButton=self.stackButton, parentMenu=self.menu)
        self.spatialiteDialog.initGui()

    def unload(self):
        # self.postgisManager.unload()
        self.spatialiteDialog.unload()

    def createDatabase(self, isSpatialite):
        """
        Shows the dialog for desired database creation.
        :param isSpatialite: (bool) indicates whether target db is a SpatiaLite db or not (PostGIS).
        """
        try:
            self.stackButton.setDefaultAction(self.toolbar.sender())
        except:
            pass
        if isSpatialite:
            dlg = self.spatialiteDialog
        # else:
        #     dlg = self.postgisManager
        if dlg:
            result = dlg.exec_()
            if result:
                pass
