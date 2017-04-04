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
from PyQt4.QtCore import QSettings, qVersion, QCoreApplication, QTranslator, Qt
from PyQt4.QtGui import QIcon, QToolButton, QMenu, QAction

import os.path
import sys

# Initialize Qt resources from file resources_rc.py
import resources_rc

currentPath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from DsgTools.LayerTools.LoadLayersFromServer.loadLayersFromServer import LoadLayersFromServer
from DsgTools.LayerTools.loadAuxStruct import LoadAuxStruct
from DsgTools.LayerTools.CreateFrameTool.ui_create_inom_dialog import CreateInomDialog
from DsgTools.DbTools.SpatialiteTool.cria_spatialite_dialog import CriaSpatialiteDialog
from DsgTools.DbTools.PostGISTool.postgisDBTool import PostgisDBTool
from DsgTools.ComplexTools.complexWindow import ComplexWindow
from DsgTools.ServerTools.viewServers import ViewServers
from DsgTools.ServerTools.exploreDb import ExploreDb
from DsgTools.ServerTools.batchDbManager import BatchDbManager
from DsgTools.ImageTools.processingTools import ProcessingTools
from DsgTools.ProcessingTools.processManager import ProcessManager
from DsgTools.BDGExTools.BDGExTools import BDGExTools
from DsgTools.InventoryTools.inventoryTools import InventoryTools
from DsgTools.ToolboxTools.models_and_scripts_installer import ModelsAndScriptsInstaller
from DsgTools.ConversionTools.convert_database import ConvertDatabase
from DsgTools.aboutdialog import AboutDialog
from DsgTools.ProductionTools.ContourTool.calc_contour import CalcContour
from DsgTools.ProductionTools.FieldToolBox.field_toolbox import FieldToolbox
from DsgTools.AttributeTools.code_list import CodeList
from DsgTools.AttributeTools.attributes_viewer import AttributesViewer
from DsgTools.ValidationTools.validation_toolbox import ValidationToolbox
from DsgTools.ProductionTools.MinimumAreaTool.minimumAreaTool import MinimumAreaTool
from DsgTools.ProductionTools.InspectFeatures.inspectFeatures import InspectFeatures
from DsgTools.DbTools.BatchDbCreator.batchDbCreator import BatchDbCreator
from DsgTools.DsgToolsOp.dsgToolsOpInstaller import DsgToolsOpInstaller

from qgis.utils import showPluginHelp
try:
    import ptvsd
    ptvsd.enable_attach(secret='my_secret', address = ('localhost', 5679))
except:
    pass

class DsgTools:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
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
        self.menu = self.tr('&DSG Tools')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'DsgTools')
        self.toolbar.setObjectName(u'DsgTools')

        self.dsgTools = None
        self.menuBar = self.iface.mainWindow().menuBar()

        #QDockWidgets
        self.complexWindow = None
        self.codeList = CodeList(iface)
        #self.attributesViewer = AttributesViewer(iface)
        self.validationToolbox = None
        self.contourDock = None
        self.fieldDock = None
        self.militaryDock = None

        self.processManager = ProcessManager(iface)

        self.BDGExTools = BDGExTools()
        self.minimumAreaTool = MinimumAreaTool(iface)
        self.inspectFeatures = InspectFeatures(iface)

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
        parent=None):
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
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def addMenu(self, parent, name, title, icon_path):
        """
        Adds a QMenu
        """
        child = QMenu(parent)
        child.setObjectName(name)
        child.setTitle(self.tr(title))
        child.setIcon(QIcon(icon_path))
        parent.addMenu(child)
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
        return button

    def initGui(self):
        """
        Create the menu entries and toolbar icons inside the QGIS GUI
        """

        self.dsgTools = QMenu(self.iface.mainWindow())
        self.dsgTools.setObjectName(u'DsgTools')
        self.dsgTools.setTitle(self.tr('DSG Tools'))
        self.fieldToolbox = None

        self.menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.dsgTools)

        #Sub menus
        server = self.addMenu(self.dsgTools, u'server', self.tr('Server Catalog'),':/plugins/DsgTools/icons/server.png')
        database = self.addMenu(self.dsgTools, u'database', self.tr('Database Tools'),':/plugins/DsgTools/icons/database.png')
        dbcreation = self.addMenu(database, u'dbcreation', self.tr('Database Creation Tools'),':/plugins/DsgTools/icons/database.png')
        layers = self.addMenu(self.dsgTools, u'layers', self.tr('Layer Tools'),':/plugins/DsgTools/icons/layers.png')
        bdgex = self.addMenu(self.dsgTools, u'bdgex', self.tr('BDGEx'),':/plugins/DsgTools/icons/eb.png')
        productiontools = self.addMenu(self.dsgTools, u'productiontools', self.tr('Production Tools'),':/plugins/DsgTools/icons/productiontools.png')
        validationtools = self.addMenu(productiontools, u'validationtools', self.tr('Validation Tools'),':/plugins/DsgTools/icons/validationtools.png')
        topocharts = self.addMenu(bdgex, u'topocharts', self.tr('Topographic Charts'),':/plugins/DsgTools/icons/eb.png')
        coverageLyr = self.addMenu(bdgex, u'coverageLyr', self.tr('Coverage Layers'),':/plugins/DsgTools/icons/eb.png')
        indexes = self.addMenu(bdgex, u'indexes', self.tr('Product Indexes'),':/plugins/DsgTools/icons/eb.png')
        rasterIndex = self.addMenu(indexes, u'rasterindex', self.tr('Topographic Charts'),':/plugins/DsgTools/icons/eb.png')
        vectorIndex = self.addMenu(indexes, u'vectorindex', self.tr('Vectorial Charts'),':/plugins/DsgTools/icons/eb.png')

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('1:250,000'),
            callback=self.load250kLayer,
            parent=topocharts,
            add_to_menu=False,
            add_to_toolbar=False)
        topocharts.addAction(action)
        
        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('1:100,000'),
            callback=self.load100kLayer,
            parent=topocharts,
            add_to_menu=False,
            add_to_toolbar=False)
        topocharts.addAction(action)
        
        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('1:50,000'),
            callback=self.load50kLayer,
            parent=topocharts,
            add_to_menu=False,
            add_to_toolbar=False)
        topocharts.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('1:25,000'),
            callback=self.load25kLayer,
            parent=topocharts,
            add_to_menu=False,
            add_to_toolbar=False)
        topocharts.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Landsat 7'),
            callback=self.loadLandsatLayer,
            parent=coverageLyr,
            add_to_menu=False,
            add_to_toolbar=False)
        coverageLyr.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('RapidEye'),
            callback=self.loadRapidEyeLayer,
            parent=coverageLyr,
            add_to_menu=False,
            add_to_toolbar=False)
        coverageLyr.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('1:250,000'),
            callback=self.load250kRasterIndex,
            parent=rasterIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        rasterIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('1:100,000'),
            callback=self.load100kRasterIndex,
            parent=rasterIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        rasterIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('1:50,000'),
            callback=self.load50kRasterIndex,
            parent=rasterIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        rasterIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('1:25,000'),
            callback=self.load25kRasterIndex,
            parent=rasterIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        rasterIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('1:250,000'),
            callback=self.load250kVectorIndex,
            parent=vectorIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        vectorIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('1:100,000'),
            callback=self.load100kVectorIndex,
            parent=vectorIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        vectorIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('1:50,000'),
            callback=self.load50kVectorIndex,
            parent=vectorIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        vectorIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('1:25,000'),
            callback=self.load25kVectorIndex,
            parent=vectorIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        vectorIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/server.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Configure Servers'),
            callback=self.viewServers,
            parent=server,
            add_to_menu=False,
            add_to_toolbar=False)
        server.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/server.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Manage Dbs from Server'),
            callback=self.batchDbManager,
            parent=server,
            add_to_menu=False,
            add_to_toolbar=False)
        server.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/histogram.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Image tools'),
            callback=self.showImageProcessor,
            parent=self.dsgTools,
            add_to_menu=False,
            add_to_toolbar=False)
        self.dsgTools.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/inventory.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Inventory tools'),
            callback=self.showInventoryTool,
            parent=self.dsgTools,
            add_to_menu=False,
            add_to_toolbar=False)
        self.dsgTools.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/install.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Models and Scripts Installer'),
            callback=self.installModelsAndScripts,
            parent=self.dsgTools,
            add_to_menu=False,
            add_to_toolbar=False)
        self.dsgTools.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/install.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Convert Database'),
            callback=self.showConvertDatabase,
            parent=self.dsgTools,
            add_to_menu=False,
            add_to_toolbar=False)
        self.dsgTools.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/dsg.png'
        action = self.add_action(
            icon_path,
            text=self.tr('About'),
            callback=self.showAbout,
            parent=self.dsgTools,
            add_to_menu=False,
            add_to_toolbar=False)
        self.dsgTools.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/help.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Help'),
            callback=self.showHelp,
            parent=self.dsgTools,
            add_to_menu=False,
            add_to_toolbar=False)
        self.dsgTools.addAction(action)

        #QToolButtons
        self.databaseButton = self.createToolButton(self.toolbar, u'DatabaseTools')
        self.layerButton = self.createToolButton(self.toolbar, u'LayerTools')
        self.productionButton = self.createToolButton(self.toolbar, u'ProductionTools')

        icon_path = ':/plugins/DsgTools/icons/postgis.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Create PostGIS'),
            callback=self.createPostGISDatabase,
            parent=dbcreation,
            add_to_menu=False,
            add_to_toolbar=False)
        dbcreation.addAction(action)
        self.databaseButton.addAction(action)
        self.databaseButton.setDefaultAction(action)

        icon_path = ':/plugins/DsgTools/icons/spatialite.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Create Spatialite'),
            callback=self.createSpatialiteDatabase,
            parent=dbcreation,
            add_to_menu=False,
            add_to_toolbar=False)
        dbcreation.addAction(action)
        self.databaseButton.addAction(action) 
        
        icon_path = ':/plugins/DsgTools/icons/batchDatabase.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Batch Database Creation'),
            callback=self.batchDatabaseCreation,
            parent=dbcreation,
            add_to_menu=False,
            add_to_toolbar=False)
        dbcreation.addAction(action)
        self.databaseButton.addAction(action) 

        icon_path = ':/plugins/DsgTools/icons/validationtools.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Perform database validation'),
            callback=self.showValidationToolbox,
            parent=validationtools,
            add_to_menu=False,
            add_to_toolbar=False)
        validationtools.addAction(action)
        self.productionButton.addAction(action)
        self.productionButton.setDefaultAction(action)

        icon_path = ':/plugins/DsgTools/icons/fieldToolbox.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Feature reclassification tool'),
            callback=self.showFieldToolbox,
            parent=productiontools,
            add_to_menu=False,
            add_to_toolbar=False)
        productiontools.addAction(action)
        self.productionButton.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/complex.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Build Complex Structures'),
            callback=self.showComplexDock,
            parent=productiontools,
            add_to_menu=False,
            add_to_toolbar=False)
        productiontools.addAction(action)
        self.productionButton.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/calccontour.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Assign Contour Values'),
            callback=self.showCalcContour,
            parent=productiontools,
            add_to_menu=False,
            add_to_toolbar=False)
        productiontools.addAction(action)
        self.productionButton.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/codelist.png'
        action = self.add_action(
            icon_path,
            text=self.tr('View Code List Codes and Values'),
            callback=self.showCodeList,
            parent=productiontools,
            add_to_menu=False,
            add_to_toolbar=False)
        productiontools.addAction(action)
        self.productionButton.addAction(action)
    
        icon_path = ':/plugins/DsgTools/icons/category.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Load Layers'),
            callback=self.loadLayersFromServer,
            parent=layers,
            add_to_menu=False,
            add_to_toolbar=False)
        layers.addAction(action)
        self.layerButton.addAction(action)
        self.layerButton.setDefaultAction(action)

        icon_path = ':/plugins/DsgTools/icons/centroid.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Load Auxiliar Structure'),
            callback=self.loadAuxStruct,
            parent=layers,
            add_to_menu=False,
            add_to_toolbar=False)
        layers.addAction(action)
        self.layerButton.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/frame.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Create Frame'),
            callback=self.createFrame,
            parent=layers,
            add_to_menu=False,
            add_to_toolbar=False)
        layers.addAction(action)
        self.layerButton.addAction(action)
        
        self.toolbar.addWidget(self.minimumAreaTool)
        self.toolbar.addWidget(self.inspectFeatures)

        self.createMilitaryMenu(self.dsgTools)
    
    def createMilitaryMenu(self, parentMenu):
        self.opInstaller = DsgToolsOpInstaller()
        if self.opInstaller.checkIfInstalled():
            icon_path = ':/plugins/DsgTools/icons/militarySimbology.png'
            dsgtoolsop = self.addMenu(parentMenu, u'dsgtoolsop', self.tr('Dsg Tools Military Tools'), icon_path)
            self.opInstaller.loadTools(dsgtoolsop, self, icon_path)

    def unload(self):
        """
        Removes the plugin menu item and icon from QGIS GUI
        """
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr('&DSG Tools'),
                action)
            self.iface.removeToolBarIcon(action)

        if self.dsgTools is not None:
            self.menuBar.removeAction(self.dsgTools.menuAction())


    def run(self):
        """
        Run method that performs all the real work
        """
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def showAbout(self):
        """
        Shows the about dialog
        """
        dlg = AboutDialog()
        dlg.exec_()

    def showHelp(self):
        """
        Shows the help
        """
        index = os.path.join(os.path.dirname(__file__), 'help', 'index')
        showPluginHelp('DsgTools', index)

    def showConvertDatabase(self):
        """
        Show sthe convert database dialog
        """
        dlg = ConvertDatabase()
        dlg.show()
        result = dlg.exec_()
        if result:
            pass
        
    def showImageProcessor(self):
        """
        Shows the processing tools dialog
        """
        dlg = ProcessingTools(self.iface)
        result = dlg.exec_()
        if result == 1:
            (filesList, rasterType, minOutValue, maxOutValue, outDir, percent, epsg) = dlg.getParameters()
            #creating the separate process
            self.processManager.createDpiProcess(filesList, rasterType, minOutValue, maxOutValue, outDir, percent, epsg)

    def showInventoryTool(self):
        """
        Shows the inventory tools dialog
        """
        dlg = InventoryTools(self.iface)
        result = dlg.exec_()
        if result == 1:
            (parentFolder, outputFile, makeCopy, destinationFolder, formatsList, isWhitelist, isOnlyGeo) = dlg.getParameters()
            #creating the separate process
            self.processManager.createInventoryProcess(parentFolder, outputFile, makeCopy, destinationFolder, formatsList, isWhitelist, isOnlyGeo)
            
    def showCalcContour(self):
        """
        Shows the countour dock
        """
        if self.contourDock:
            self.iface.removeDockWidget(self.contourDock)
        else:
            self.contourDock = CalcContour(self.iface)
        self.contourDock.activateTool()
        self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.contourDock)
    
    def showCodeList(self):
        """
        Shows the Code list Dock
        """
        if self.codeList:
            self.iface.removeDockWidget(self.codeList)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.codeList)

    def showFieldToolbox(self):
        """
        Shows the reclassification tool box dock
        """
        if self.fieldDock:
            self.iface.removeDockWidget(self.fieldToolbox)
        else:
            self.fieldToolbox = FieldToolbox(self.iface)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.fieldToolbox)
    
    def showValidationToolbox(self):
        """
        Shows the Validation Dock
        """
        if self.validationToolbox:
            self.iface.removeDockWidget(self.validationToolbox)
        else:
            self.validationToolbox = ValidationToolbox(self.iface)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.validationToolbox)

    def showComplexDock(self):
        """
        Shows the Manage Complex features Dock
        """
        if self.complexWindow:
            self.iface.removeDockWidget(self.complexWindow)
        else:
            self.complexWindow = ComplexWindow(self.iface)
        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.complexWindow)
            
    def installModelsAndScripts(self):
        """
        Shows the model and scripts installer dialog
        """
        dlg = ModelsAndScriptsInstaller()
        result = dlg.exec_()
        if result == 1:
            pass

    def createSpatialiteDatabase(self):
        """
        Shows the create spatialite dialog
        """
        try:
            self.databaseButton.setDefaultAction(self.toolbar.sender())
        except:
            pass
        dlg = CriaSpatialiteDialog()
        result = dlg.exec_()
        if result:
            pass
    
    def batchDatabaseCreation(self):
        """
        Shows the batch database creation dialog
        """
        try:
            self.databaseButton.setDefaultAction(self.toolbar.sender())
        except:
            pass
        dlg = BatchDbCreator()
        result = dlg.exec_()
        if result:
            pass

    def createPostGISDatabase(self):
        """
        Shows the create postgis dialog
        """
        try:
            self.databaseButton.setDefaultAction(self.toolbar.sender())
        except:
            pass
        dlg = PostgisDBTool(self.iface)
        result = dlg.exec_()
        if result == 1:
            (dbName, abstractDb , version, epsg) = dlg.getParameters()
            #creating the separate process
            self.processManager.createPostgisDatabaseProcess(dbName,abstractDb, version, epsg)


    def loadAuxStruct(self):
        """
        Shows the load line-centroid configuration dialog
        """
        try:
            self.layerButton.setDefaultAction(self.toolbar.sender())
        except:
            pass
        dlg = LoadAuxStruct(self.iface)
        dlg.show()
        result = dlg.exec_()
        if result:
            pass
    
    def loadLayersFromServer(self):
        """
        Shows the dialog that loads layers from server
        """
        try:
            self.layerButton.setDefaultAction(self.toolbar.sender())
        except:
            pass
        dlg = LoadLayersFromServer(self.iface)
        dlg.show()
        result = dlg.exec_()
        if result:
            pass

    def createFrame(self):
        """
        Shows the create frame dialog
        """
        try:
            self.layerButton.setDefaultAction(self.toolbar.sender())
        except:
            pass
        dlg = CreateInomDialog(self.iface)
        dlg.show()
        result = dlg.exec_()
        if result:
            pass

    def viewServers(self):
        """
        Shows the view servers dialog
        """
        dlg = ViewServers(self.iface)
        dlg.show()
        result = dlg.exec_()
        if result:
            pass
    
    def exploreDB(self):
        """
        Shows the explore database dialog
        """
        dlg = ExploreDb()
        dlg.show()
        result = dlg.exec_()
        if result:
            pass

    def batchDbManager(self):
        """
        Shows the database manager dialog
        """
        dlg = BatchDbManager()
        dlg.show()
        result = dlg.exec_()
        if result:
            pass

    def loadRapidEyeLayer(self):
        """
        Loads rapideye layer
        """
        urlWithParams = self.BDGExTools.getTileCache('RapidEye')
        if not urlWithParams:
            return
        print urlWithParams
        self.iface.addRasterLayer(urlWithParams, 'RapidEye','wms')

    def loadLandsatLayer(self):
        """
        Loads landsat layer
        """
        urlWithParams = self.BDGExTools.getTileCache('Landsat7')
        if not urlWithParams:
            return
        self.iface.addRasterLayer(urlWithParams, 'Landsat7', 'wms')

    def load250kLayer(self):
        """
        Loads landsat layer
        """
        urlWithParams = self.BDGExTools.getTileCache('1:250k')
        if not urlWithParams:
            return
        self.iface.addRasterLayer(urlWithParams, '1:250k', 'wms')
    
    def load100kLayer(self):
        """
        Loads 100k layer
        """
        urlWithParams = self.BDGExTools.getTileCache('1:100k')
        if not urlWithParams:
            return
        self.iface.addRasterLayer(urlWithParams, '1:100k', 'wms')

    def load50kLayer(self):
        """
        Loads 50k layer
        """
        urlWithParams = self.BDGExTools.getTileCache('1:50k')
        if not urlWithParams:
            return
        self.iface.addRasterLayer(urlWithParams, '1:50k', 'wms')

    def load25kLayer(self):
        """
        Loads 25k layer
        """
        urlWithParams = self.BDGExTools.getTileCache('1:25k')
        if not urlWithParams:
            return
        self.iface.addRasterLayer(urlWithParams, '1:25k', 'wms')

    def load250kRasterIndex(self):
        """
        Loads 250k raster index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F250_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:250k Available Raster Charts'), 'wms')

    def load100kRasterIndex(self):
        """
        Loads 100k raster index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F100_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:100k Available Raster Charts'), 'wms')

    def load50kRasterIndex(self):
        """
        Loads 50 raster index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F50_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:50k Available Raster Charts'), 'wms')

    def load25kRasterIndex(self):
        """
        Loads 25k raster index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F25_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:25k Available Raster Charts'), 'wms')

    def load250kVectorIndex(self):
        """
        Loads 250k vector index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F250_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:250k Available Vectorial Charts'), 'wms')

    def load100kVectorIndex(self):
        """
        Loads 100k vector index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F100_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:100k Available Vectorial Charts'), 'wms')

    def load50kVectorIndex(self):
        """
        Loads 50k vector index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F50_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:50k Available Vectorial Charts'), 'wms')

    def load25kVectorIndex(self):
        """
        Loads 25k vector index layer
        """
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F25_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:25k Available Vectorial Charts'),'wms')