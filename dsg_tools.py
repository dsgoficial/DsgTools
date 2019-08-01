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
from __future__ import absolute_import
from builtins import object
from qgis.PyQt.QtCore import QSettings, qVersion, QCoreApplication, QTranslator, Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QToolButton, QMenu, QAction

import os.path
import sys

# Initialize Qt resources from file resources_rc.py
from . import resources_rc

currentPath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(currentPath))

from qgis.utils import showPluginHelp
from qgis.core import QgsApplication

try:
    import ptvsd
    ptvsd.enable_attach(address = ('localhost', 5679))
except Exception as e:
    pass

# try:
#     # check version in metadata
#     with open(os.path.join(currentPath, 'metadata.txt'), 'r') as meta:
#         metadata = meta.read()
#         for line in metadata.split("\n"):
#             if line.strip().startswith("version="):
#                 version = line.split("=")[1].strip()
#         if "dev" in version:
#             commit = os.popen("cd {} && git log -1".format(currentPath)).readlines()[0].strip().split(" ")[1]
#             # add the last commit to version tag
#             if commit not in version:
#                 with open(os.path.join(currentPath, 'metadata.txt'), 'w') as meta:
#                     metadata = metadata.replace(version, "{0}_{1}".format(version, commit))
#                     meta.write(metadata)
# except Exception as e:
#     pass

from .gui.guiManager import GuiManager
from .core.DSGToolsProcessingAlgs.dsgtoolsProcessingAlgorithmProvider import DSGToolsProcessingAlgorithmProvider

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
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'DsgTools_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        # Declare instance attributes
        self.actions = []
        self.menu = '&DSGTools'
        self.toolbar = self.iface.addToolBar(u'DsgTools')
        self.toolbar.setObjectName(u'DsgTools')

        self.dsgTools = None
        self.menuBar = self.iface.mainWindow().menuBar()
        self.provider = DSGToolsProcessingAlgorithmProvider()

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
        return QCoreApplication.translate('DsgTools', message)

    def unload(self):
        """
        Removes the plugin menu item and icon from QGIS GUI
        """
        self.guiManager.unload()
        for action in self.actions:
            self.iface.removePluginMenu(
                '&DSGTools',
                action)
            self.iface.removeToolBarIcon(action)
            self.iface.unregisterMainWindowAction(action)

        if self.dsgTools is not None:
            self.menuBar.removeAction(self.dsgTools.menuAction())
        self.iface.mainWindow().removeToolBar(self.toolbar)
        QgsApplication.processingRegistry().removeProvider(self.provider)
        del self.dsgTools
        del self.toolbar

    def initGui(self):
        """
        Create the menu entries and toolbar icons inside the QGIS GUI
        """

        self.dsgTools = QMenu(self.iface.mainWindow())
        self.dsgTools.setObjectName(u'DsgTools')
        self.dsgTools.setTitle(u'DSGTools')
        self.menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.dsgTools)
        #GuiManager
        self.guiManager = GuiManager(self.iface, parentMenu = self.dsgTools, toolbar = self.toolbar)
        self.guiManager.initGui()
        #provider
        QgsApplication.processingRegistry().addProvider(self.provider)