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
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings
from PyQt4.QtSql import QSqlDatabase

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.ServerTools.serverDBExplorer import ServerDBExplorer
from DsgTools.Factories.DbFactory.dbFactory import DbFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'connectionWidget.ui'))

class ConnectionWidget(QtGui.QWidget, FORM_CLASS):
    connectionChanged = pyqtSignal()
    problemOccurred = pyqtSignal(str)
    
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
         
    def __del__(self):
        self.closeDatabase()

    def closeDatabase(self):
        if self.abstractDb:
            del self.abstractDb
            self.abstractDb = None

    def setInitialState(self):
        self.filename = ''
        self.dbLoaded = False
        self.epsg = 0
        self.crs = None
        
        self.abstractDb = None
        self.isSpatialite = True
        self.tabWidget.setCurrentIndex(0)
        self.abstractDbFactory = DbFactory()
        self.utils = Utils()

        #populating the postgis combobox
        self.comboBoxPostgis.setCurrentIndex(0)
        self.populatePostGISConnectionsCombo()        

    @pyqtSlot(int)
    def on_comboBoxPostgis_currentIndexChanged(self):
        if self.comboBoxPostgis.currentIndex() > 0:
            self.loadDatabase()
            self.connectionChanged.emit()
        
    @pyqtSlot(bool)
    def on_pushButtonOpenFile_clicked(self):  
        self.loadDatabase()
        if self.isDBConnected():
            self.connectionChanged.emit()
        
    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self):
        self.filename = ''
        self.dbLoaded = False
        self.epsg = 0
        self.crs = None
        self.dbVersion = ''
        
        self.spatialiteFileEdit.setText(self.filename)
        self.postGISCrsEdit.setText('')
        self.postGISCrsEdit.setReadOnly(True)
        self.spatialiteCrsEdit.setText('')
        self.spatialiteCrsEdit.setReadOnly(True)   
        self.edgvSpatialiteVersionEdit.setText('')
        self.edgvPostgisVersionEdit.setText('')     
    
        #Setting the database type
        if self.tabWidget.currentIndex() == 0:
            self.isSpatialite = True
        else:
            self.isSpatialite = False

    def loadDatabase(self):
        self.closeDatabase()
        if self.isSpatialite:
            self.abstractDb = self.abstractDbFactory.createDbFactory('QSQLITE')
            self.abstractDb.connectDatabase()
            self.spatialiteFileEdit.setText(self.abstractDb.db.databaseName())
            self.edgvSpatialiteVersionEdit.setText(self.abstractDb.getDatabaseVersion())
                
        else:
            self.abstractDb = self.abstractDbFactory.createDbFactory('QPSQL')
            self.abstractDb.connectDatabase(self.comboBoxPostgis.currentText())
            self.edgvPostgisVersionEdit.setText(self.abstractDb.getDatabaseVersion())
        try:
            self.abstractDb.checkAndOpenDb()
            self.dbLoaded = True
            self.setCRS()
            self.dbVersion = self.abstractDb.getDatabaseVersion()
        except Exception as e:
            QgsMessageLog.logMessage(e.args[0], "DSG Tools Plugin", QgsMessageLog.CRITICAL)    

    def setCRS(self):
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
        except:
            pass

    def populatePostGISConnectionsCombo(self):
        self.comboBoxPostgis.clear()
        self.comboBoxPostgis.addItem(self.tr('Select Database'))
        self.comboBoxPostgis.addItems(self.getPostGISConnections())
        
    def isDBConnected(self):
        return self.dbLoaded
        
    def getDBVersion(self):
        return self.abstractDb.getDatabaseVersion()
    
    def getQmlPath(self):
        return self.abstractDb.getQmlDir()
        
    @pyqtSlot(bool)
    def on_addConnectionButton_clicked(self):  
        newConnectionDialog =  ServerDBExplorer(self)
        retvalue = newConnectionDialog.exec_()
        self.populatePostGISConnectionsCombo()
        return retvalue
    
    def getPostGISConnections(self):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/connections')
        currentConnections = settings.childGroups()
        settings.endGroup()
        return currentConnections