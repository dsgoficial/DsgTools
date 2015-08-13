 
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
from PyQt4.QtCore import pyqtSlot, pyqtSignal, Qt, QSettings
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtGui import QApplication, QCursor, QListWidgetItem, QMessageBox

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.ServerTools.viewServers import ViewServers
from PyQt4.Qt import QVariant
from OpenGL.raw.GL.APPLE import row_bytes

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_serverDBExplorer.ui'))

class ServerDBExplorer(QtGui.QDialog, FORM_CLASS):
    
    def __init__(self, parent = None):
        """Constructor."""
        super(ServerDBExplorer, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.utils = Utils()
        
        self.factory = SqlGeneratorFactory()
        #setting the sql generator
        self.gen = self.factory.createSqlGenerator(False)
        
        self.populateServersCombo()
        
    def getServers(self):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers')
        currentConnections = settings.childGroups()
        settings.endGroup()
        return currentConnections
    
    def storeConnectionConfiguration(self, server, database):
        name = self.connectionEdit.text()
        
        (host, port, user, password) = self.getServerConfiguration(server)
        
        settings = QSettings()
        if not settings.contains('PostgreSQL/servers/'+name+'/host'):
            settings.beginGroup('PostgreSQL/connections/'+name)
            settings.setValue('database', database)
            settings.setValue('host', host)
            settings.setValue('port', port)
            settings.setValue('username', user)
            settings.setValue('password', password)
            settings.endGroup()
    
    @pyqtSlot(bool)
    def on_createNewServerPushButton_clicked(self):  
        createNewServer = ViewServers(self)
        createNewServer.exec_()
        self.populateServersCombo()

    def populateServersCombo(self):
        self.serversCombo.clear()
        self.serversCombo.addItem("Select Server")
        currentConnections = self.getServers()
        for connection in currentConnections:
            self.serversCombo.addItem(connection)
    
    @pyqtSlot(int)
    def on_serversCombo_currentIndexChanged(self):
        self.serverListWidget.clear()
        if not self.serversCombo.currentIndex() > 0:
            return
        
        dbList = self.utils.getDbsFromServer(self.serversCombo.currentText())
        for (dbname, dbversion) in dbList:
            item =  QListWidgetItem(self.serverListWidget)
            item.setText(dbname+' (EDGV v. '+dbversion+')')
            item.setData(Qt.UserRole, dbname)
            
    @pyqtSlot(bool)
    def on_createConnectionPushButton_clicked(self):
        items = self.serverListWidget.selectedItems()
        existentConnections = []
        for item in items:
            dbname = item.data(Qt.UserRole)
            ret = self.utils.storeConnection(self.serversCombo.currentText(), dbname)
            if not ret:
                existentConnections.append(dbname)
        
        if len(existentConnections) > 0:
            msg = self.tr('The following databases connections already exist:\n')  
            for conn in existentConnections:
                msg += conn+'\n'
            QMessageBox.warning(self, self.tr("Warning!"), msg)
        else:
            QMessageBox.warning(self, self.tr("Warning!"), self.tr('Connections created successfully!'))
            
    @pyqtSlot(bool)
    def on_selectAllPushButton_clicked(self):
        count = self.serverListWidget.count()
        for row in range(count):
            item = self.serverListWidget.item(row)
            item.setSelected(True)        