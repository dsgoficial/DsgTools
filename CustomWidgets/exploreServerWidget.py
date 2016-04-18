# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ExploreServerWidget
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

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings
from PyQt4.QtSql import QSqlQuery

# DSGTools imports
from DsgTools.ServerTools.viewServers import ViewServers
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.Factories.DbFactory.dbFactory import DbFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'exploreServerWidget.ui'))

class ExploreServerWidget(QtGui.QWidget, FORM_CLASS):
    abstractDbLoaded = pyqtSignal()
    clearWidgets = pyqtSignal()
    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.dbFactory = DbFactory()

    #TODO
    def getServers(self):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers')
        currentConnections = settings.childGroups()
        settings.endGroup()
        return currentConnections
    
    #TODO
    def browseServer(self,dbList,host,port,user,password):
        gen = self.factory.createSqlGenerator(False)
        edvgDbList = []
        for database in dbList:
            db = self.getPostGISDatabaseWithParams(database, host, port, user, password)
            if not db.open():
                qgis.utils.iface.messageBar().pushMessage('DB :'+database+'| msg: '+db.lastError().databaseText(), level=QgsMessageBar.CRITICAL)

            query = QSqlQuery(db)
            if query.exec_(gen.getEDGVVersion()):
                while query.next():
                    version = query.value(0)
                    if version:
                        edvgDbList.append((database, version))
        return edvgDbList
    
    #TODO
    def getDbsFromServer(self,name):
        gen = self.factory.createSqlGenerator(False)
        
        (host, port, user, password) = self.getServerConfiguration(name)
        database = 'postgres'
        
        db = self.getPostGISDatabaseWithParams(database, host, port, user, password)
        if not db.open():
            QgsMessageLog.logMessage(db.lastError().text(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            QMessageBox.critical(self.iface.mainWindow(), self.tr('Critical'), self.tr('A problem occurred! Check log for details.'))
        
        query = QSqlQuery(gen.getDatabasesFromServer(), db)
        if not query.isActive():
            QMessageBox.critical(self.iface.mainWindow(), self.tr('Critical'), self.tr("Problem executing query: ")+query.lastError().text())
            
        dbList = []
        while query.next():
            dbList.append(query.value(0))
        return self.browseServer(dbList, host, port, user, password)
    
    @pyqtSlot(bool)
    def on_createNewServerPushButton_clicked(self):  
        createNewServer = ViewServers(self)
        createNewServer.exec_()
        self.populateServersCombo()

    def populateServersCombo(self):
        self.serversCombo.clear()
        self.serversCombo.addItem(self.tr('Select Server'))
        currentConnections = self.getServers()
        for connection in currentConnections:
            self.serversCombo.addItem(connection)
    
    @pyqtSlot(int)
    def on_serversCombo_currentIndexChanged(self):
        self.clearWidgets.emit()
        if self.serversCombo.currentIndex() != 0:
            self.abstractDb = self.dbFactory.createDbFactory('QPSQL')
            if not self.abstractDb:
                QMessageBox.critical(self.iface.mainWindow(), self.tr('Critical'), self.tr('A problem occurred! Check log for details.'))
                return
            (host, port, user, password) = self.abstractDb.getServerConfiguration(self.serversCombo.currentText())
            self.abstractDb.connectDatabaseWithParameters(host, port, 'postgres', user, password)
            self.abstractDbLoaded.emit()