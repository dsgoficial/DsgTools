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
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from qgis.utils import showPluginHelp
from qgis.core import QgsApplication

try:
    import ptvsd
    ptvsd.enable_attach(address = ('localhost', 5679))
except Exception as e:
    pass

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

        #Sub menus
        # server = self.addMenu(self.dsgTools, u'server', self.tr('Server Catalog'),':/plugins/DsgTools/icons/server.png')
        # database = self.addMenu(self.dsgTools, u'database', self.tr('Database Tools'),':/plugins/DsgTools/icons/database.png')
        # layers = self.addMenu(self.dsgTools, u'layers', self.tr('Layer Tools'),':/plugins/DsgTools/icons/layers.png')
        # bdgex = self.addMenu(self.dsgTools, u'bdgex', self.tr('BDGEx'),':/plugins/DsgTools/icons/eb.png')
        # productiontools = self.addMenu(self.dsgTools, u'productiontools', self.tr('Production Tools'),':/plugins/DsgTools/icons/productiontools.png')
        # topocharts = self.addMenu(bdgex, u'topocharts', self.tr('Topographic Charts'),':/plugins/DsgTools/icons/eb.png')
        # coverageLyr = self.addMenu(bdgex, u'coverageLyr', self.tr('Coverage Layers'),':/plugins/DsgTools/icons/eb.png')
        # indexes = self.addMenu(bdgex, u'indexes', self.tr('Product Indexes'),':/plugins/DsgTools/icons/eb.png')
        # rasterIndex = self.addMenu(indexes, u'rasterindex', self.tr('Topographic Charts'),':/plugins/DsgTools/icons/eb.png')
        # vectorIndex = self.addMenu(indexes, u'vectorindex', self.tr('Vectorial Charts'),':/plugins/DsgTools/icons/eb.png')
        # dsgtoolsop = self.addMenu(self.dsgTools, u'dsgtoolsop', self.tr('Dsg Tools Military Tools'), ':/plugins/DsgTools/icons/eb.png')
        # self.createMilitaryMenu(dsgtoolsop, ':/plugins/DsgTools/icons/eb.png')

    #     icon_path = ':/plugins/DsgTools/icons/eb.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('1:250,000'),
    #         callback=self.load250kLayer,
    #         parent=topocharts,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     topocharts.addAction(action)
        
    #     icon_path = ':/plugins/DsgTools/icons/eb.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('1:100,000'),
    #         callback=self.load100kLayer,
    #         parent=topocharts,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     topocharts.addAction(action)
        
    #     icon_path = ':/plugins/DsgTools/icons/eb.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('1:50,000'),
    #         callback=self.load50kLayer,
    #         parent=topocharts,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     topocharts.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/eb.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('1:25,000'),
    #         callback=self.load25kLayer,
    #         parent=topocharts,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     topocharts.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/eb.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Landsat 7'),
    #         callback=self.loadLandsatLayer,
    #         parent=coverageLyr,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     coverageLyr.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/eb.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('RapidEye'),
    #         callback=self.loadRapidEyeLayer,
    #         parent=coverageLyr,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     coverageLyr.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/eb.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('1:250,000'),
    #         callback=self.load250kRasterIndex,
    #         parent=rasterIndex,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     rasterIndex.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/eb.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('1:100,000'),
    #         callback=self.load100kRasterIndex,
    #         parent=rasterIndex,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     rasterIndex.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/eb.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('1:50,000'),
    #         callback=self.load50kRasterIndex,
    #         parent=rasterIndex,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     rasterIndex.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/eb.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('1:25,000'),
    #         callback=self.load25kRasterIndex,
    #         parent=rasterIndex,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     rasterIndex.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/eb.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('1:250,000'),
    #         callback=self.load250kVectorIndex,
    #         parent=vectorIndex,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     vectorIndex.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/eb.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('1:100,000'),
    #         callback=self.load100kVectorIndex,
    #         parent=vectorIndex,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     vectorIndex.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/eb.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('1:50,000'),
    #         callback=self.load50kVectorIndex,
    #         parent=vectorIndex,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     vectorIndex.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/eb.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('1:25,000'),
    #         callback=self.load25kVectorIndex,
    #         parent=vectorIndex,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     vectorIndex.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/server.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Configure Servers'),
    #         callback=self.viewServers,
    #         parent=server,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     server.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/server.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Manage Databases from Server'),
    #         callback=self.batchDbManager,
    #         parent=server,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     server.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/histogram.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Image tools'),
    #         callback=self.showImageProcessor,
    #         parent=self.dsgTools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     self.dsgTools.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/inventory.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Inventory tools'),
    #         callback=self.showInventoryTool,
    #         parent=self.dsgTools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     self.dsgTools.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/install.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Models and Scripts Installer'),
    #         callback=self.installModelsAndScripts,
    #         parent=self.dsgTools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     self.dsgTools.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/install.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Convert Database'),
    #         callback=self.showConvertDatabase,
    #         parent=self.dsgTools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     self.dsgTools.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/custom_tools.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Options'),
    #         callback=self.showOptions,
    #         parent=self.dsgTools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     self.dsgTools.addAction(action)
    #     Options().firstTimeConfig()

    #     icon_path = ':/plugins/DsgTools/icons/dsg.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('About'),
    #         callback=self.showAbout,
    #         parent=self.dsgTools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     self.dsgTools.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/bug.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Report bug / Suggest features'),
    #         callback=self.showBugTracker,
    #         parent=self.dsgTools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     self.dsgTools.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/help.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Help'),
    #         callback=self.showHelp,
    #         parent=self.dsgTools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     self.dsgTools.addAction(action)

    #     #QToolButtons
    #     self.databaseButton = self.createToolButton(self.toolbar, u'DatabaseTools')
    #     self.layerButton = self.createToolButton(self.toolbar, u'LayerTools')
    #     self.productionButton = self.createToolButton(self.toolbar, u'ProductionTools')

    #     icon_path = ':/plugins/DsgTools/icons/postgis.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Create PostGIS'),
    #         callback=self.createPostGISDatabase,
    #         parent=database,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     database.addAction(action)
    #     self.databaseButton.addAction(action)
    #     self.databaseButton.setDefaultAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/spatialite.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Create Spatialite'),
    #         callback=self.createSpatialiteDatabase,
    #         parent=database,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     database.addAction(action)
    #     self.databaseButton.addAction(action) 
        
    #     icon_path = ':/plugins/DsgTools/icons/batchDatabase.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Batch Database Creation'),
    #         callback=self.batchDatabaseCreation,
    #         parent=database,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     database.addAction(action)
    #     self.databaseButton.addAction(action) 

    #     icon_path = ':/plugins/DsgTools/icons/validationtools.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Perform database validation'),
    #         callback=self.showValidationToolbox,
    #         parent=productiontools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     productiontools.addAction(action)
    #     self.productionButton.addAction(action)
    #     self.productionButton.setDefaultAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/fieldToolbox.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Feature (Re)classification Tool'),
    #         callback=self.showFieldToolbox,
    #         parent=productiontools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     productiontools.addAction(action)
    #     self.productionButton.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/frame.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Create Frame'),
    #         callback=self.createFrame,
    #         parent=productiontools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     productiontools.addAction(action)
    #     self.productionButton.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/frame.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Raster Info Tool'),
    #         callback=self.showRasterInfoDock,
    #         parent=productiontools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     productiontools.addAction(action)
    #     self.productionButton.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/complex.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Build Complex Structures'),
    #         callback=self.showComplexDock,
    #         parent=productiontools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     productiontools.addAction(action)
    #     self.productionButton.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/calccontour.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Assign Contour Values'),
    #         callback=self.showCalcContour,
    #         parent=productiontools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     productiontools.addAction(action)
    #     self.productionButton.addAction(action)
    #     #enable shortcut config
    #     self.iface.registerMainWindowAction(action, '')

    #     #removed until bugs are removed
    #     # icon_path = ':/plugins/DsgTools/icons/attributeSelector.png'
    #     # action = self.add_action(
    #     #     icon_path,
    #     #     text=self.tr('Copy and Paste Attribute Set'),
    #     #     callback=self.copyPasteTool.copyPaste,
    #     #     parent=productiontools,
    #     #     add_to_menu=False,
    #     #     add_to_toolbar=False)
    #     # productiontools.addAction(action)
    #     # self.productionButton.addAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/codelist.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('View Code List Codes and Values'),
    #         callback=self.showCodeList,
    #         parent=productiontools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     productiontools.addAction(action)
    #     self.productionButton.addAction(action)
    
    #     icon_path = ':/plugins/DsgTools/icons/category.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Load Layers'),
    #         callback=self.loadLayersFromServer,
    #         parent=layers,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     layers.addAction(action)
    #     self.layerButton.addAction(action)
    #     self.layerButton.setDefaultAction(action)

    #     icon_path = ':/plugins/DsgTools/icons/centroid.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('Load Auxiliar Structure'),
    #         callback=self.loadAuxStruct,
    #         parent=layers,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     layers.addAction(action)
    #     self.layerButton.addAction(action)


    #     icon_path = ':/plugins/DsgTools/icons/flipLineTool.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('DSGTools: Flip Line Tool'),
    #         callback=self.flipLineTool.startFlipLineTool,
    #         parent=productiontools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     productiontools.addAction(action)
    #     self.toolbar.addAction(action)
    #     self.flipLineTool.setAction(action)
    #     #enable shortcut config
    #     self.iface.registerMainWindowAction(action, '')
    #     action.setToolTip(self.tr("DSGTools: Flip Line Tool\nInsert tool tip for Flip Line Tool."))

    #     icon_path = ':/plugins/DsgTools/icons/home.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('DSGTools: Right Degree Angle Digitizing'),
    #         callback=self.acquisition.acquisitionNinetyDegrees,
    #         parent=productiontools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     productiontools.addAction(action)
    #     self.toolbar.addAction(action)
    #     self.acquisition.setPolygonAction(action)
    #     #enable shortcut config
    #     self.iface.registerMainWindowAction(action, '')
    #     action.setToolTip(self.tr("DSGTools: Right Degree Angle Digitizing\nControl modifier: disables tool while control is pressed."))

    #     icon_path = ':/plugins/DsgTools/icons/circle.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('DSGTools: Circle Digitizing'),
    #         callback=self.acquisition.acquisitionCircle,
    #         parent=productiontools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     productiontools.addAction(action)
    #     self.toolbar.addAction(action)
    #     self.acquisition.setCircleAction(action)
    #     #enable shortcut config
    #     self.iface.registerMainWindowAction(action, '')

    #     icon_path = ':/plugins/DsgTools/icons/free_hand.png'
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('DSGTools: Free Hand Acquisition'),
    #         callback=self.freeHandAcquisiton.run,
    #         parent=productiontools,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     self.freeHandAcquisiton.setAction(action)
    #     action.setEnabled(False)
    #     productiontools.addAction(action)
    #     self.toolbar.addAction(action)
    #     #enable shortcut config
    #     self.iface.registerMainWindowAction(action, '')
    #     self.inspectFeatures = InspectFeatures(self.iface, parent = productiontools)
    #     self.minimumAreaTool = MinimumAreaTool(self.iface, parent = productiontools)
    #     self.dsgRasterInfoTool = DsgRasterInfoTool(self.iface, parent = productiontools)
    #     self.toolbar.addWidget(self.minimumAreaTool)
    #     self.toolbar.addWidget(self.inspectFeatures)
    #     # self.inspectFeatures.enableShortcuts()
    #     # self.iface.registerMainWindowAction(self.inspectFeatures.action, '')
    #     self.toolbar.addWidget(self.styleManagerTool)
    #     self.toolbar.addWidget(self.dsgRasterInfoTool)
        

    
    # def createMilitaryMenu(self, parentMenu, icon_path):
    #     self.opInstaller = DsgToolsOpInstaller(self.iface, parent=self, parentMenu=parentMenu)
    #     action = self.add_action(
    #         icon_path,
    #         text=self.tr('DsgTools Op Installer'),
    #         callback=self.installDsgToolsOp,
    #         parent=parentMenu,
    #         add_to_menu=False,
    #         add_to_toolbar=False)
    #     parentMenu.addAction(action)
    #     # if already installed, make the uninstall action and load tool actions
    #     if self.opInstaller.checkIfInstalled():
    #         self.opInstaller.loadTools()

    # def installDsgToolsOp(self):
    #     """
    #     Installs DsgTools Op
    #     """
    #     dlg = DsgToolsOpInstallerDialog(self.opInstaller)
    #     dlg.show()
    #     result = dlg.exec_()
    #     if result:
    #         pass
    
    # def uninstallDsgToolsOp(self):
    #     """
    #     Uninstall dsgtoolsop
    #     """
    #     self.opInstaller.uninstallDsgToolsOp()
    #     self.unload()
    #     self.initGui()

    # def showConvertDatabase(self):
    #     """
    #     Show sthe convert database dialog
    #     """
    #     dlg = ConvertDatabase()
    #     dlg.show()
    #     result = dlg.exec_()
    #     if result:
    #         pass
        
    # def showImageProcessor(self):
    #     """
    #     Shows the processing tools dialog
    #     """
    #     dlg = ProcessingTools(self.iface)
    #     result = dlg.exec_()
    #     if result == 1:
    #         (filesList, rasterType, minOutValue, maxOutValue, outDir, percent, epsg) = dlg.getParameters()
    #         #creating the separate process
    #         self.processManager.createDpiProcess(filesList, rasterType, minOutValue, maxOutValue, outDir, percent, epsg)

    # def showInventoryTool(self):
    #     """
    #     Shows the inventory tools dialog
    #     """
    #     dlg = InventoryTools(self.iface)
    #     result = dlg.exec_()
    #     if result == 1:
    #         (parentFolder, outputFile, makeCopy, destinationFolder, formatsList, isWhitelist, isOnlyGeo) = dlg.getParameters()
    #         #creating the separate process
    #         self.processManager.createInventoryProcess(parentFolder, outputFile, makeCopy, destinationFolder, formatsList, isWhitelist, isOnlyGeo)
            
    # def useGenericSelector(self):
    #     """
    #     Shows the countour dock
    #     """
    #     if self.contourDock:
    #         self.iface.removeDockWidget(self.contourDock)
    #     else:
    #         self.contourDock = CalcContour(self.iface)
    #     self.contourDock.activateTool()
    #     self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.contourDock)
    
    # def showCalcContour(self):
    #     """
    #     Shows the countour dock
    #     """
    #     if self.contourDock:
    #         self.iface.removeDockWidget(self.contourDock)
    #     else:
    #         self.contourDock = CalcContour(self.iface)
    #     self.contourDock.activateTool()
    #     self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.contourDock)
    
    # def showCodeList(self):
    #     """
    #     Shows the Code list Dock
    #     """
    #     pass
    #     # if self.codeList:
    #     #     self.iface.removeDockWidget(self.codeList)
    #     # self.iface.addDockWidget(Qt.RightDockWidgetArea, self.codeList)

    # def showFieldToolbox(self):
    #     """
    #     Shows the reclassification tool box dock
    #     """
    #     if self.fieldDock:
    #         self.iface.removeDockWidget(self.fieldToolbox)
    #     else:
    #         self.fieldToolbox = FieldToolbox(self.iface)
    #     self.iface.addDockWidget(Qt.RightDockWidgetArea, self.fieldToolbox)
    
    # def showValidationToolbox(self):
    #     """
    #     Shows the Validation Dock
    #     """
    #     if self.validationToolbox:
    #         self.iface.removeDockWidget(self.validationToolbox)
    #     else:
    #         self.validationToolbox = ValidationToolbox(self.iface)
    #     self.iface.addDockWidget(Qt.RightDockWidgetArea, self.validationToolbox)
    
    # def showRasterInfoDock(self):
    #     """
    #     Shows the Raster Info dock
    #     """
    #     if self.rasterInfoDock:
    #         self.iface.removeDockWidget(self.rasterInfoDock)
    #     else:
    #         self.rasterInfoDock = DsgRasterInfoTool(self.iface)
    #     self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.rasterInfoDock)

    # def showComplexDock(self):
    #     """
    #     Shows the Manage Complex features Dock
    #     """
    #     if self.complexWindow:
    #         self.iface.removeDockWidget(self.complexWindow)
    #     else:
    #         self.complexWindow = ComplexWindow(self.iface)
    #     self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.complexWindow)
            
    # def installModelsAndScripts(self):
    #     """
    #     Shows the model and scripts installer dialog
    #     """
    #     dlg = ModelsAndScriptsInstaller()
    #     result = dlg.exec_()
    #     if result == 1:
    #         pass

    # def createSpatialiteDatabase(self):
    #     """
    #     Shows the create spatialite dialog
    #     """
    #     try:
    #         self.databaseButton.setDefaultAction(self.toolbar.sender())
    #     except:
    #         pass
    #     dlg = CriaSpatialiteDialog()
    #     result = dlg.exec_()
    #     if result:
    #         pass
    
    # def batchDatabaseCreation(self):
    #     """
    #     Shows the batch database creation dialog
    #     """
    #     try:
    #         self.databaseButton.setDefaultAction(self.toolbar.sender())
    #     except:
    #         pass
    #     dlg = BatchDbCreator()
    #     result = dlg.exec_()
    #     if result:
    #         pass

    # def createPostGISDatabase(self):
    #     """
    #     Shows the create postgis dialog
    #     """
    #     try:
    #         self.databaseButton.setDefaultAction(self.toolbar.sender())
    #     except:
    #         pass
    #     dlg = PostgisDBTool(self.iface)
    #     result = dlg.exec_()
    #     if result == 1:
    #         (dbName, abstractDb , version, epsg) = dlg.getParameters()
    #         #creating the separate process
    #         self.processManager.createPostgisDatabaseProcess(dbName,abstractDb, version, epsg)


    # def loadAuxStruct(self):
    #     """
    #     Shows the load line-centroid configuration dialog
    #     """
    #     try:
    #         self.layerButton.setDefaultAction(self.toolbar.sender())
    #     except:
    #         pass
    #     dlg = LoadAuxStruct(self.iface)
    #     dlg.show()
    #     result = dlg.exec_()
    #     if result:
    #         pass
    
    # def loadLayersFromServer(self):
    #     """
    #     Shows the dialog that loads layers from server
    #     """
    #     dlg = LoadLayersFromServer(self.iface)
    #     dlg.show()
    #     result = dlg.exec_()
    #     if result:
    #         pass

    # def createFrame(self):
    #     """
    #     Shows the create frame dialog
    #     """
    #     try:
    #         self.layerButton.setDefaultAction(self.toolbar.sender())
    #     except:
    #         pass
    #     dlg = CreateInomDialog(self.iface)
    #     dlg.show()
    #     result = dlg.exec_()
    #     if result:
    #         pass

    # def viewServers(self):
    #     """
    #     Shows the view servers dialog
    #     """
    #     dlg = ViewServers(self.iface)
    #     dlg.show()
    #     result = dlg.exec_()
    #     if result:
    #         pass
    
    # def exploreDB(self):
    #     """
    #     Shows the explore database dialog
    #     """
    #     dlg = ExploreDb()
    #     dlg.show()
    #     result = dlg.exec_()
    #     if result:
    #         pass

    # def batchDbManager(self):
    #     """
    #     Shows the database manager dialog
    #     """
    #     dlg = BatchDbManager()
    #     dlg.show()
    #     result = dlg.exec_()
    #     if result:
    #         pass

    # def loadRapidEyeLayer(self):
    #     """
    #     Loads rapideye layer
    #     """
    #     urlWithParams = self.BDGExTools.getTileCache('RapidEye')
    #     if not urlWithParams:
    #         return
    #     self.iface.addRasterLayer(urlWithParams, 'RapidEye','wms')

    # def loadLandsatLayer(self):
    #     """
    #     Loads landsat layer
    #     """
    #     urlWithParams = self.BDGExTools.getTileCache('Landsat7')
    #     if not urlWithParams:
    #         return
    #     self.iface.addRasterLayer(urlWithParams, 'Landsat7', 'wms')

    # def load250kLayer(self):
    #     """
    #     Loads landsat layer
    #     """
    #     urlWithParams = self.BDGExTools.getTileCache('1:250k')
    #     if not urlWithParams:
    #         return
    #     self.iface.addRasterLayer(urlWithParams, '1:250k', 'wms')
    
    # def load100kLayer(self):
    #     """
    #     Loads 100k layer
    #     """
    #     urlWithParams = self.BDGExTools.getTileCache('1:100k')
    #     if not urlWithParams:
    #         return
    #     self.iface.addRasterLayer(urlWithParams, '1:100k', 'wms')

    # def load50kLayer(self):
    #     """
    #     Loads 50k layer
    #     """
    #     urlWithParams = self.BDGExTools.getTileCache('1:50k')
    #     if not urlWithParams:
    #         return
    #     self.iface.addRasterLayer(urlWithParams, '1:50k', 'wms')

    # def load25kLayer(self):
    #     """
    #     Loads 25k layer
    #     """
    #     urlWithParams = self.BDGExTools.getTileCache('1:25k')
    #     if not urlWithParams:
    #         return
    #     self.iface.addRasterLayer(urlWithParams, '1:25k', 'wms')

    # def load250kRasterIndex(self):
    #     """
    #     Loads 250k raster index layer
    #     """
    #     urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F250_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
    #     self.iface.addRasterLayer(urlWithParams, self.tr('1:250k Available Raster Charts'), 'wms')

    # def load100kRasterIndex(self):
    #     """
    #     Loads 100k raster index layer
    #     """
    #     urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F100_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
    #     self.iface.addRasterLayer(urlWithParams, self.tr('1:100k Available Raster Charts'), 'wms')

    # def load50kRasterIndex(self):
    #     """
    #     Loads 50 raster index layer
    #     """
    #     urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F50_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
    #     self.iface.addRasterLayer(urlWithParams, self.tr('1:50k Available Raster Charts'), 'wms')

    # def load25kRasterIndex(self):
    #     """
    #     Loads 25k raster index layer
    #     """
    #     urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F25_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
    #     self.iface.addRasterLayer(urlWithParams, self.tr('1:25k Available Raster Charts'), 'wms')

    # def load250kVectorIndex(self):
    #     """
    #     Loads 250k vector index layer
    #     """
    #     urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F250_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
    #     self.iface.addRasterLayer(urlWithParams, self.tr('1:250k Available Vectorial Charts'), 'wms')

    # def load100kVectorIndex(self):
    #     """
    #     Loads 100k vector index layer
    #     """
    #     urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F100_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
    #     self.iface.addRasterLayer(urlWithParams, self.tr('1:100k Available Vectorial Charts'), 'wms')

    # def load50kVectorIndex(self):
    #     """
    #     Loads 50k vector index layer
    #     """
    #     urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F50_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
    #     self.iface.addRasterLayer(urlWithParams, self.tr('1:50k Available Vectorial Charts'), 'wms')

    # def load25kVectorIndex(self):
    #     """
    #     Loads 25k vector index layer
    #     """
    #     urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F25_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
    #     self.iface.addRasterLayer(urlWithParams, self.tr('1:25k Available Vectorial Charts'),'wms')
