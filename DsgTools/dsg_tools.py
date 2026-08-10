# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-10-09
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        mod history          : 2015-04-12 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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

from builtins import object
from qgis.PyQt.QtCore import QSettings, qVersion, QCoreApplication, QTranslator
from qgis.PyQt.QtWidgets import QMenu

import os.path
import sys

# Initialize Qt resources from file resources.py
from . import resources

currentPath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(currentPath))

from qgis.core import QgsApplication

from .core.DSGToolsProcessingAlgs.dsgtoolsProcessingAlgorithmProvider import (
    DSGToolsProcessingAlgorithmProvider,
)


class DsgTools(object):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale", "en_US")[0:2]
        locale_path = os.path.join(
            self.plugin_dir, "i18n", "DsgTools_{}.qm".format(locale)
        )

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > "4.3.3":
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        # Declare instance attributes
        self.actions = []
        self.menu = "&DSGTools"
        self.provider = None
        self.dsgTools = None
        # When the plugin is loaded in headless mode (e.g. through the
        # qgis_process command line tool), QGIS instantiates it with iface=None
        # and never calls initGui(). Building GUI elements here would crash with
        # "'NoneType' object has no attribute 'addToolBar'", so only do it when
        # running inside the QGIS desktop.
        if self.iface is not None:
            self.toolbar = self.iface.addToolBar(self.tr("DsgTools"))
            self.toolbar.setObjectName("DsgTools")
            self.menuBar = self.iface.mainWindow().menuBar()
        else:
            self.toolbar = None
            self.menuBar = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.
        We implement this ourselves since we do not inherit QObject.
        :param message: String for translation.
        :type message: str, QString
        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate("DsgTools", message)

    def unload(self):
        """
        Removes the plugin menu item and icon from QGIS GUI.

        Must also work in headless mode (qgis_process), where there is no GUI
        and guiManager was never created.
        """
        if self.iface is not None and hasattr(self, "guiManager"):
            self.guiManager.unload()
            for action in self.actions:
                if action is None:
                    continue
                self.iface.removePluginMenu("&DSGTools", action)
                self.iface.removeToolBarIcon(action)
                self.iface.unregisterMainWindowAction(action)
                del action

            if self.dsgTools is not None:
                self.menuBar.removeAction(self.dsgTools.menuAction())
            if self.toolbar is not None:
                self.iface.mainWindow().removeToolBar(self.toolbar)
            del self.guiManager

        if self.provider is not None:
            QgsApplication.processingRegistry().removeProvider(self.provider)
            self.provider = None
        self.dsgTools = None

    def initGui(self):
        """
        Create the menu entries and toolbar icons inside the QGIS GUI
        """
        from .gui.guiManager import GuiManager

        self.dsgTools = QMenu(self.iface.mainWindow())
        self.dsgTools.setObjectName("DsgTools")
        self.dsgTools.setTitle(self.tr("DSGTools"))
        self.menuBar.insertMenu(
            self.iface.firstRightStandardMenu().menuAction(), self.dsgTools
        )
        # GuiManager
        self.guiManager = GuiManager(
            self.iface, parentMenu=self.dsgTools, toolbar=self.toolbar
        )
        self.guiManager.initGui()
        # provider
        self.initProcessing()

    def initProcessing(self):
        """
        Registers the DSGTools processing provider.

        This is called both by initGui() (when running inside the QGIS desktop)
        and directly by QGIS when the plugin is loaded in headless mode, e.g.
        through the qgis_process command line tool, which never calls initGui().
        For headless support the plugin must declare hasProcessingProvider=yes
        in metadata.txt and expose this exact method name. It is idempotent so
        it can safely be called from both paths.
        """
        if self.provider is None:
            self.provider = DSGToolsProcessingAlgorithmProvider()
            QgsApplication.processingRegistry().addProvider(self.provider)
