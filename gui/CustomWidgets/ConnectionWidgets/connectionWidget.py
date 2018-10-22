# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgManagementToolsDialog
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-08-12
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Brazilian Army - Geographic Service Bureau
        email                : suporte.dsgtools@dsg.eb.mil.br
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
import os

from qgis.core import QgsCoordinateReferenceSystem,QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from qgis.PyQt.QtSql import QSqlDatabase
from qgis.PyQt.QtWidgets import QApplication, QMessageBox
from qgis.PyQt.QtGui import QCursor

# DSGTools imports
from ....core.Utils.utils import Utils
from ....core.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.core.dsgEnums import DsgEnums

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'connectionWidget.ui'))

class ConnectionWidget(QtWidgets.QWidget, FORM_CLASS):
    connectionChanged = pyqtSignal()
    problemOccurred = pyqtSignal(str)
    dbChanged = pyqtSignal(AbstractDb)
    styleChanged = pyqtSignal(dict)
    def __init__(self, parent = None):
        """Constructor."""
        super(ConnectionWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setInitialState()
        self.serverWidget.populateServersCombo()
        self.serverWidget.abstractDbLoaded.connect(self.getDatabasesFromServer)
        self.serverWidget.clearWidgets.connect(self.clearAll)
        
         
    def __del__(self):
        """
        Closes the database
        """
        self.closeDatabase()

    def closeDatabase(self):
        """
        Closes the current database
        """
        if self.abstractDb:
            del self.abstractDb
            self.abstractDb = None
                 
    def clearAll(self):
        """
        Resets the initial state
        """
        self.filename = ''
        self.dbLoaded = False
        self.epsg = 0
        self.crs = None
        
        self.abstractDb = None
        self.isSpatialite = False
        self.abstractDbFactory = DbFactory()
        self.utils = Utils()

        #populating the postgis combobox
        self.comboBoxPostgis.clear()
        self.spatialiteFileEdit.setReadOnly(True)   
        self.postGISCrsEdit.setReadOnly(True)
        self.spatialiteCrsEdit.setReadOnly(True)   
        self.edgvSpatialiteVersionEdit.setReadOnly(True)
        self.edgvPostgisVersionEdit.setReadOnly(True)      

    def setInitialState(self):
        """
        Sets the initial state
        """
        self.filename = ''
        self.dbLoaded = False
        self.epsg = 0
        self.crs = None
        
        self.abstractDb = None
        self.isSpatialite = False
        self.tabWidget.setCurrentIndex(0)
        self.abstractDbFactory = DbFactory()
        self.utils = Utils()
        self.serverWidget.serversCombo.setCurrentIndex(0)

        #populating the postgis combobox
        self.comboBoxPostgis.clear()
        self.spatialiteFileEdit.setReadOnly(True)   
        self.postGISCrsEdit.setReadOnly(True)
        self.spatialiteCrsEdit.setReadOnly(True)   
        self.edgvSpatialiteVersionEdit.setReadOnly(True)
        self.edgvPostgisVersionEdit.setReadOnly(True)      

    @pyqtSlot(int)
    def on_comboBoxPostgis_currentIndexChanged(self):
        """
        Updates database information when the combo box changes
        """
        if self.comboBoxPostgis.currentIndex() > 0:
            self.postGISCrsEdit.setText('')
            self.postGISCrsEdit.setReadOnly(True)
            self.edgvPostgisVersionEdit.setText('')
            self.edgvPostgisVersionEdit.setReadOnly(True)  
            self.loadDatabase()
            self.connectionChanged.emit()
        
    @pyqtSlot(bool)
    def on_pushButtonOpenFile_clicked(self):  
        """
        Loads a spatialite database
        """
        self.loadDatabase()
        if self.isDBConnected():
            self.connectionChanged.emit()
        
    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self):
        """
        Changes the tab to work with spatialite or postgis databases
        """
        self.filename = ''
        self.comboBoxPostgis.clear()
        self.dbLoaded = False
        self.epsg = 0
        self.crs = None
        self.dbVersion = ''
        self.serverWidget.serversCombo.setCurrentIndex(0)
        self.spatialiteFileEdit.setReadOnly(True)
        self.spatialiteFileEdit.setText(self.filename)
        self.postGISCrsEdit.setText('')
        self.postGISCrsEdit.setReadOnly(True)
        self.spatialiteCrsEdit.setText('')
        self.spatialiteCrsEdit.setReadOnly(True)   
        self.edgvSpatialiteVersionEdit.setText('')
        self.edgvSpatialiteVersionEdit.setReadOnly(True)
        self.edgvPostgisVersionEdit.setText('')
        self.edgvPostgisVersionEdit.setReadOnly(True)
        self.mGroupBox.setTitle(self.tr('Database connection'))
        
        #Setting the database type
        if self.tabWidget.currentIndex() == 1:
            self.isSpatialite = True
        else:
            self.isSpatialite = False

    def loadDatabase(self):
        """
        Loads the selected database
        """
        self.closeDatabase()
        try:
            if self.isSpatialite:
                self.abstractDb = self.abstractDbFactory.createDbFactory(DsgEnums.DriverSpatiaLite)
                self.abstractDb.connectDatabase()
                self.spatialiteFileEdit.setText(self.abstractDb.db.databaseName())
                self.edgvSpatialiteVersionEdit.setText(self.abstractDb.getDatabaseVersion())
                    
            else:
                self.abstractDb = self.abstractDbFactory.createDbFactory(DsgEnums.DriverPostGIS)
                (host, port, user, password) = self.serverWidget.getServerParameters()
                dbName = self.comboBoxPostgis.currentText()
                self.abstractDb.connectDatabaseWithParameters(host, port, dbName, user, password)
                self.edgvPostgisVersionEdit.setText(self.abstractDb.getDatabaseVersion())
                serverName = self.serverWidget.serversCombo.currentText()
                newText = dbName + self.tr(' on ') + serverName 
                self.mGroupBox.setToolTip(newText)
                # self.mGroupBox.setTitle(newText)

            self.abstractDb.checkAndOpenDb()
            self.dbLoaded = True
            self.dbVersion = self.abstractDb.getDatabaseVersion()
            self.abstractDb.checkAndCreateStyleTable()
            self.styles = self.abstractDb.getStyleDict(self.dbVersion)
            self.styleChanged.emit(self.styles)
            self.dbChanged.emit(self.abstractDb)
            if self.dbVersion == '-1':
                self.problemOccurred.emit(self.tr('This is not a valid DsgTools database!'))
            else:
                self.setCRS()
        except Exception as e:
            self.problemOccurred.emit(self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)   

    def setCRS(self):
        """
        Sets the CRS information
        """
        try:
            self.epsg = self.abstractDb.findEPSG()
            if self.epsg == -1:
                self.problemOccurred.emit(self.tr('Coordinate Reference System not set or invalid!'))
            else:
                self.crs = QgsCoordinateReferenceSystem(self.epsg, QgsCoordinateReferenceSystem.EpsgCrsId)
                if self.isSpatialite:
                    self.spatialiteCrsEdit.setText(self.crs.description())
                    self.spatialiteCrsEdit.setReadOnly(True)
                else:
                    self.postGISCrsEdit.setText(self.crs.description())
                    self.postGISCrsEdit.setReadOnly(True)
        except Exception as e:
            self.problemOccurred.emit(self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)

        
    def isDBConnected(self):
        """
        Checks if the database is already loaded
        """
        return self.dbLoaded
        
    def getDBVersion(self):
        """
        Gets the database version
        """
        ret = ''
        try:
            ret = self.abstractDb.getDatabaseVersion()
        except Exception as e:
            self.problemOccurred.emit(self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
        return ret
    
    def getQmlPath(self):
        """
        Gets the QML path
        """
        ret = ''
        try:
            ret = self.abstractDb.getQmlDir()
        except Exception as e:
            self.problemOccurred.emit(self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
        return ret
    
    def getDatabasesFromServer(self):
        """
        Gets databases from server
        """  
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            if self.serverWidget.abstractDb:
                dbList = self.serverWidget.abstractDb.getEDGVDbsFromServer(parentWidget = self)
                dbList.sort()
                self.comboBoxPostgis.clear()
                self.comboBoxPostgis.addItem(self.tr('Select Database'))
                for db, version in dbList:
                    self.comboBoxPostgis.addItem(db)
                
            else:
                self.setInitialState()
                return
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), ':'.join(e.args))
            self.setInitialState()
            self.setInitialState()
        QApplication.restoreOverrideCursor()