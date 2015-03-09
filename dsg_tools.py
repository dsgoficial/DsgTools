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

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/DbTools/PostGISTool'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/DbTools/SpatialiteTool'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/LayerTools'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/ComplexTools'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/ServerTools'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/MosaicTools'))

from load_by_class import LoadByClass
from load_by_category import LoadByCategory
from cria_spatialite_dialog import CriaSpatialiteDialog
from complexWindow import ComplexWindow
from serverConfigurator import ServerConfigurator
from postgisDBTool import PostgisDBTool
from createPostGISDatabase import CreatePostGISDatabase
from ui_create_inom_dialog import CreateInomDialog
from mosaicTools import MosaicTools

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

        icon_path = ':/plugins/DsgTools/icons/server.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Server Settings'),
            callback=self.configurateServers,
            parent=self.dsgTools,
            add_to_menu=False,
            add_to_toolbar=False)
        server.addAction(action)

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

        icon_path = ':/plugins/DsgTools/icons/help.png'
        action = self.add_action(
            icon_path,
            text=self.tr('Mosaic tools'),
            callback=self.showMosaic,
            parent=self.dsgTools,
            add_to_menu=False,
            add_to_toolbar=False)
        self.dsgTools.addAction(action)

        #QToolButtons
        self.databaseButton = self.createToolButton(self.toolbar, u'DatabaseTools')
        self.layerButton = self.createToolButton(self.toolbar, u'LayerTools')
        #self.complexButton = self.createToolButton(self.toolbar, u'ComplexTools')

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
    
    def showMosaic(self):
        dlg = MosaicTools(self.iface)
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
            # Setting the progress bar
            self.progressMessageBar = self.iface.messageBar().createMessage(self.tr("Creating database structure..."))
            self.progressBar = QProgressBar()
            self.progressBar.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
            self.progressMessageBar.layout().addWidget(self.progressBar)
            self.iface.messageBar().pushWidget(self.progressMessageBar, self.iface.messageBar().INFO)

            (db, version, epsg) = self.dlg.getParameters()
            self.thread = CreatePostGISDatabase(db, version, epsg)
            #Thread signals
            QObject.connect( self.thread, SIGNAL( "rangeCalculated( PyQt_PyObject )" ), self.setProgressRange )
            QObject.connect( self.thread, SIGNAL( "queryProcessed()" ), self.queryProcessed )
            QObject.connect( self.thread, SIGNAL( "processingFinished(PyQt_PyObject)" ), self.processFinished )

            QObject.connect( self.progressMessageBar, SIGNAL( "destroyed()" ), self.progressCanceled )

            # Startin the processing
            self.thread.start()
        elif result == 0:
            QMessageBox.information(self.iface.mainWindow(), 'DSG Tools',self.tr('Problem creating the Database!'))

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

    def setProgressRange( self, maximum ):
        if self.progressMessageBar:
            self.progressBar.setRange( 0, maximum )
    
    def queryProcessed( self):
        if self.progressMessageBar:
            self.progressBar.setValue( self.progressBar.value() + 1 )

    def userCanceled( self ):
        QMessageBox.information(self.iface.mainWindow(), 'DSG Tools',self.tr('Database structure creation canceled!'))

    def processFinished( self, feedback):
        if self.thread != None:
            self.thread.stop()
            self.thread = None
            
        if feedback == 1:
            self.progressBar.setValue( self.progressBar.maximum())
            QMessageBox.information(self.iface.mainWindow(), 'DSG Tools',self.tr('Database structure successfully created!'))
        elif feedback == 0:
            QMessageBox.information(self.iface.mainWindow(), 'DSG Tools',self.tr('Problem creating the database structure!\n Check the Log terminal for details.'))
        elif feedback == -1:
            QMessageBox.information(self.iface.mainWindow(), 'DSG Tools',self.tr('User canceled the database structure creation!'))
            
    def progressCanceled(self):
        self.progressMessageBar = None
        self.progressBar = None
            
        if self.thread:
            self.thread.stop()
            self.thread = None
