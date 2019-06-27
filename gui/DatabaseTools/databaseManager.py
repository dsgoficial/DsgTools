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

from DsgTools.gui.DatabaseTools.DbTools.SingleDbCreator.singleDbCreator import CreateSingleDatabase
from DsgTools.gui.DatabaseTools.DbTools.BatchDbCreator.batchDbCreator import BatchDbCreator
from DsgTools.gui.DatabaseTools.ConversionTools.datasourceConversion import DatasourceConversion

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
        """
        Prepares the funcionalities to be added to both the DSGTools menu and it's shortcut button into QGIS main interface.
        :param text: (str) text to be shown when the action is hovered over.
        :param callback: (method/function) desired behavior for when action is activated.
        :param parentMenu: (QMenu) menu to which action will be added.
        :param parentButton: (QButton) button to which action will be associated.
        :param defaultButton: (bool) considering it is a stack button (button overloaded with >1 actions associated), it indicates
                              whether the included action will be the default one (e.g. if it will the action representative and 
                              1st to be displayed).
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
            parentButton=self.stackButton
        )
        if defaultButton:
            self.stackButton.setDefaultAction(action)

    def initGui(self):
        """
        Instantiates all available database creation GUI. 
        """
        self.singleDbCreator = CreateSingleDatabase(manager=self, parentButton=self.stackButton, parentMenu=self.menu)
        self.singleDbCreator.initGui()
        self.batchCreator = BatchDbCreator(manager=self, parentButton=self.stackButton, parentMenu=self.menu)
        self.batchCreator.initGui()
        self.datasourceConversion = DatasourceConversion(manager=self, parentMenu=self.menu, parentButton=self.stackButton)
        self.datasourceConversion.initGui()

    def unload(self):
        """
        Unloads all loaded GUI.
        """
        self.singleDbCreator.unload()
        self.batchCreator.unload()
        self.datasourceConversion.unload()

    def createDatabase(self, isBatchCreation):
        """
        Shows the dialog for desired database creation.
        :param isBatchCreation: (bool) indicates whether creation is in batch or not.
        """
        try:
            self.stackButton.setDefaultAction(self.sender())
        except:
            pass
        if not isBatchCreation:
            dlg = self.singleDbCreator
        else:
            dlg = self.batchCreator
        if dlg:
            result = dlg.exec_()
            if result:
                pass
