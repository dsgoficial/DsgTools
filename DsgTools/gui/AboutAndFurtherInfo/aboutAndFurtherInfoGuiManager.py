# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-04-11
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


from DsgTools.core.DSGToolsProcessingAlgs.Algs.LayerManagementAlgs.spellChecker.datasets.ptBR import (
    PalavrasFileConfig,
    WordDatasetPtBRFileConfig,
)
from DsgTools.core.NetworkTools.ExternalFilesHandler import (
    ExternalFileDownloadProcessor,
)

from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtWidgets import QToolButton, QMenu, QAction
from qgis.core import Qgis
from .Options.options import Options
from .aboutdialog import AboutDialog


class AboutAndFurtherInfoGuiManager(QObject):
    def __init__(self, manager, iface, parentMenu=None, toolbar=None):
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        super(AboutAndFurtherInfoGuiManager, self).__init__()
        self.manager = manager
        self.iface = iface
        self.parentMenu = parentMenu
        self.toolbar = toolbar
        self.iconBasePath = ":/plugins/DsgTools/icons/"
        self.options = Options()
        self.options.firstTimeConfig()

    def initGui(self):
        action = self.manager.add_action(
            self.iconBasePath + "custom_tools.png",
            text=self.tr("DSGTools' Options"),
            callback=self.showOptions,
            parent=self.iface.mainWindow(),
            parentMenu=self.parentMenu,
            add_to_menu=False,
            add_to_toolbar=False,
            withShortcut=False,
        )
        action = self.manager.add_action(
            self.iconBasePath + "import.png",
            text=self.tr("Download external data"),
            callback=self.checkExternalDownloads,
            parent=self.iface.mainWindow(),
            parentMenu=self.parentMenu,
            add_to_menu=False,
            add_to_toolbar=False,
            withShortcut=False,
        )
        # self.parentMenu.addAction(action)

        icon_path = self.iconBasePath + "bug.png"
        action = self.manager.add_action(
            icon_path,
            text=self.tr("Report bug / Suggest features"),
            callback=self.showBugTracker,
            parent=self.parentMenu,
            add_to_menu=True,
            add_to_toolbar=False,
            withShortcut=False,
        )

        icon_path = self.iconBasePath + "help.png"
        action = self.manager.add_action(
            icon_path,
            text=self.tr("Help"),
            callback=self.showHelp,
            parent=self.parentMenu,
            add_to_menu=True,
            add_to_toolbar=False,
            withShortcut=False,
        )

        icon_path = self.iconBasePath + "DSGToolsIcon.png"
        action = self.manager.add_action(
            icon_path,
            text=self.tr("About DSGTools"),
            callback=self.showAbout,
            parent=self.parentMenu,
            add_to_menu=True,
            add_to_toolbar=False,
            withShortcut=False,
        )

    def unload(self):
        pass

    def showOptions(self):
        """
        Shows the options
        """
        # dlg.show()
        self.options.setInterfaceWithParametersFromConfig()
        self.checkExternalDownloads()
        result = self.options.exec_()

    def checkExternalDownloads(self):
        downloadProcessor = ExternalFileDownloadProcessor(
            parent=self.iface.mainWindow()
        )
        output = downloadProcessor.process(
            fileConfigList=[
                WordDatasetPtBRFileConfig,
                PalavrasFileConfig,
            ]
        )
        if output:
            message = (
                self.tr("Everyting up to date")
                if output == 1
                else self.tr("External files updated")
            )
            self.iface.messageBar().pushMessage(
                self.tr("Info"), message, level=Qgis.Info
            )

    def showHelp(self):
        """
        Shows the help
        """
        self.iface.openURL("https://github.com/dsgoficial/DsgTools/wiki", False)

    def showBugTracker(self):
        """
        Shows the bug tracker
        """
        self.iface.openURL("https://github.com/dsgoficial/DsgTools/issues", False)

    def showAbout(self):
        """
        Shows the about dialog
        """
        dlg = AboutDialog()
        dlg.show()
        dlg.exec_()
