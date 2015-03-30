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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
import os.path
import aboutdialog
import sys

currentPath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from DsgTools.LayerTools.load_by_class import LoadByClass
from DsgTools.LayerTools.load_by_category import LoadByCategory
from DsgTools.LayerTools.ui_create_inom_dialog import CreateInomDialog

from DsgTools.DbTools.SpatialiteTool.cria_spatialite_dialog import CriaSpatialiteDialog
from DsgTools.DbTools.PostGISTool.postgisDBTool import PostgisDBTool
from DsgTools.DbTools.PostGISTool.createPostGISDatabase import CreatePostGISDatabase

from DsgTools.ComplexTools.complexWindow import ComplexWindow

from DsgTools.ServerTools.serverConfigurator import ServerConfigurator

from DsgTools.ImageTools.processingTools import ProcessingTools

from DsgTools.ProcessingTools.processManager import ProcessManager

from qgis.utils import showPluginHelp

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

        self.complexWindow = ComplexWindow(iface)

        self.processManager = ProcessManager(iface)


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
        child = QMenu(parent)
        child.setObjectName(name)
        child.setTitle(self.tr(title))
        child.setIcon(QIcon(icon_path))
        parent.addMenu(child)
        return child

    def createToolButton(self, parent, text):
        button = QToolButton(parent)
        button.setObjectName(text)
        button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button.setPopupMode(QToolButton.MenuButtonPopup)
        parent.addWidget(button)
        return button

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.dsgTools = QMenu(self.iface.mainWindow())
        self.dsgTools.setObjectName(u'DsgTools')
        self.dsgTools.setTitle(self.tr('DSG Tools'))

        self.menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.dsgTools)

        #Sub menus
        server = self.addMenu(self.dsgTools, u'server', self.tr('Server Catalog'),':/plugins/DsgTools/icons/server.png')
        database = self.addMenu(self.dsgTools, u'database', self.tr('Database Tools'),':/plugins/DsgTools/icons/database.png')
        layers = self.addMenu(self.dsgTools, u'layers', self.tr('Layer Tools'),':/plugins/DsgTools/icons/layers.png')
        bdgex = self.addMenu(self.dsgTools, u'bdgex', self.tr('BDGEx'),':/plugins/DsgTools/icons/eb.png')
        topocharts = self.addMenu(bdgex, u'topocharts', self.tr('Topographic Charts'),':/plugins/DsgTools/icons/eb.png')
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
            parent=rasterIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        vectorIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('1:100,000'),
            callback=self.load100kVectorIndex,
            parent=rasterIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        vectorIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('1:50,000'),
            callback=self.load50kVectorIndex,
            parent=rasterIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        vectorIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/eb.png'
        action = self.add_action(
            icon_path,
            text=self.tr('1:25,000'),
            callback=self.load25kVectorIndex,
            parent=rasterIndex,
            add_to_menu=False,
            add_to_toolbar=False)
        vectorIndex.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/server.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Server Settings'),
            callback=self.configurateServers,
            parent=self.dsgTools,
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
#         self.dsgTools.addAction(action)

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

        icon_path = ':/plugins/DsgTools/icons/spatialite.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Create Spatialite'),
            callback=self.createSpatialiteDatabase,
            parent=database,
            add_to_menu=False,
            add_to_toolbar=False)
        database.addAction(action)
        self.databaseButton.addAction(action)
        self.databaseButton.setDefaultAction(action)

        icon_path = ':/plugins/DsgTools/icons/postgis.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Create PostGIS'),
            callback=self.createPostGISDatabase,
            parent=database,
            add_to_menu=False,
            add_to_toolbar=False)
        database.addAction(action)
        self.databaseButton.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/category.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Load by Category'),
            callback=self.loadByCategory,
            parent=database,
            add_to_menu=False,
            add_to_toolbar=False)
        layers.addAction(action)
        self.layerButton.addAction(action)
        self.layerButton.setDefaultAction(action)

        icon_path = ':/plugins/DsgTools/icons/class.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Load by Class'),
            callback=self.loadByClass,
            parent=database,
            add_to_menu=False,
            add_to_toolbar=False)
        layers.addAction(action)
        self.layerButton.addAction(action)

        icon_path = ':/plugins/DsgTools/icons/frame.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Create Frame'),
            callback=self.createFrame,
            parent=database,
            add_to_menu=False,
            add_to_toolbar=False)
        layers.addAction(action)
        self.layerButton.addAction(action)

        self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.complexWindow)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr('&DSG Tools'),
                action)
            self.iface.removeToolBarIcon(action)

        if self.dsgTools is not None:
            self.menuBar.removeAction(self.dsgTools.menuAction())

            self.iface.removeDockWidget(self.complexWindow)

    def run(self):
        """Run method that performs all the real work"""
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
        dlg = aboutdialog.AboutDialog()
        dlg.exec_()

    def showHelp(self):
        index = os.path.join(os.path.dirname(__file__), 'help', 'index')
        showPluginHelp('DsgTools', index)

    def showImageProcessor(self):
        dlg = ProcessingTools(self.iface)
        result = dlg.exec_()

    def createSpatialiteDatabase(self):
        try:
            self.databaseButton.setDefaultAction(self.toolbar.sender())
        except:
            pass
        self.dlg = CriaSpatialiteDialog()
        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            pass

    def createPostGISDatabase(self):
        try:
            self.databaseButton.setDefaultAction(self.toolbar.sender())
        except:
            pass
        self.dlg = PostgisDBTool(self.iface)
        self.dlg.show()
        result = self.dlg.exec_()
        if result == 1:
            (db, version, epsg) = self.dlg.getParameters()
            #creating the separeate process
            self.processManager.createPostgisDatabaseProcess(db, version, epsg)

    def loadByCategory(self):
        try:
            self.layerButton.setDefaultAction(self.toolbar.sender())
        except:
            pass
        self.dlg = LoadByCategory()
        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            pass

    def loadByClass(self):
        try:
            self.layerButton.setDefaultAction(self.toolbar.sender())
        except:
            pass
        self.dlg = LoadByClass()
        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            pass

    def createFrame(self):
        try:
            self.layerButton.setDefaultAction(self.toolbar.sender())
        except:
            pass
        self.dlg = CreateInomDialog()
        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            pass

    def configurateServers(self):
        self.dlg = ServerConfigurator(self.iface)
        self.dlg.show()
        result = self.dlg.exec_()
        if result:
            pass

    def load250kLayer(self):
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/gif&layers=ctm250&styles=&tileMatrixSet=ctm250-wmsc-4&url=http://www.geoportal.eb.mil.br/tiles'
        self.iface.addRasterLayer(urlWithParams, '1:250k','wms')

    def load250kRasterIndex(self):
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F250_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:250k Available Raster Charts'),'wms')

    def load100kRasterIndex(self):
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F100_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:100k Available Raster Charts'),'wms')

    def load50kRasterIndex(self):
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F50_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:50k Available Raster Charts'),'wms')

    def load25kRasterIndex(self):
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F25_WGS84_MATRICIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:25k Available Raster Charts'),'wms')

    def load250kVectorIndex(self):
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F250_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:250k Available Vectorial Charts'),'wms')

    def load100kVectorIndex(self):
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F100_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:100k Available Vectorial Charts'),'wms')

    def load50kVectorIndex(self):
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F50_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:50k Available Vectorial Charts'),'wms')

    def load25kVectorIndex(self):
        urlWithParams = 'crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/png&layers=F25_WGS84_VETORIAL&styles=&url=http://www.geoportal.eb.mil.br/teogc42/terraogcwms.cgi?version=1.1.0'
        self.iface.addRasterLayer(urlWithParams, self.tr('1:25k Available Vectorial Charts'),'wms')
