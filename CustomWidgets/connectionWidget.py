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
import os, sys

# QGIS imports
import qgis as qgis
from qgis.gui import QgsMessageBar
from qgis.core import QgsCoordinateReferenceSystem,QgsDataSourceURI,QgsVectorLayer,QgsMapLayerRegistry,QgsMessageLog

# Qt imports
from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtGui import QApplication, QCursor

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory

from DsgTools.ServerTools.serverDBExplorer import ServerDBExplorer

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
        if self.db:
            self.db.close()
            self.db = None

    def setInitialState(self):
        self.filename = ''
        self.dbLoaded = False
        self.epsg = 0
        self.crs = None
        
        self.db = None
        self.isSpatialite = True
        self.tabWidget.setCurrentIndex(0)
        self.factory = SqlGeneratorFactory()
        self.gen = self.factory.createSqlGenerator(self.isSpatialite)
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
        self.connectionChanged.emit()
        
    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self):
        self.filename = ''
        self.dbLoaded = False
        self.epsg = 0
        self.crs = None
        
        self.spatialiteFileEdit.setText(self.filename)
        self.postGISCrsEdit.setText('')
        self.postGISCrsEdit.setReadOnly(True)
        self.spatialiteCrsEdit.setText('')
        self.spatialiteCrsEdit.setReadOnly(True)        
    
        #Setting the database type
        if self.tabWidget.currentIndex() == 0:
            self.isSpatialite = True
        else:
            self.isSpatialite = False

        #getting the sql generator according to the database type
        self.gen = self.factory.createSqlGenerator(self.isSpatialite)

    def loadDatabase(self):
        self.closeDatabase()

        if self.isSpatialite:
            (self.filename, self.db) = self.utils.getSpatialiteDatabase()
            if self.filename:
                self.spatialiteFileEdit.setText(self.filename)
        else:
            self.db = self.utils.getPostGISDatabase(self.comboBoxPostgis.currentText())
        try:
            if not self.db.open():
                QgsMessageLog.logMessage(self.db.lastError().text(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            else:
                self.dbLoaded = True
                self.setCRS()
        except:
            pass    

    def setCRS(self):
        try:
            self.epsg = self.utils.findEPSG(self.db)
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
        self.comboBoxPostgis.addItems(self.utils.getPostGISConnections())
        
    def isDBConnected(self):
        return self.dbLoaded
        
    def getDBVersion(self):
        if self.isDBConnected():
            return self.utils.getDatabaseVersion(self.db)
    
    def getQmlPath(self):
        if self.isDBConnected():
            return self.utils.getQmlDir(self.db)
        
    @pyqtSlot(bool)
    def on_addConnectionButton_clicked(self):  
        newConnectionDialog =  ServerDBExplorer(self)
        retvalue = newConnectionDialog.exec_()
        self.populatePostGISConnectionsCombo()
        return retvalue