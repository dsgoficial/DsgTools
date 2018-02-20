# -*- coding: utf-8 -*-
'''
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2015-04-02
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Felipe Ferrari - Cartographic Engineer @ Brazilian Army
        email                : ferrari@dsg.eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
'''
import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, QSettings, pyqtSignal
from PyQt4.QtGui import QHeaderView, QTableWidgetItem, QMessageBox, QApplication, QCursor, QRadioButton
from PyQt4.QtSql import QSqlDatabase
from serverConfigurator import ServerConfigurator

from qgis.core import QgsMessageLog

from DsgTools.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.Factories.DbFactory.dbFactory import DbFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_viewServers.ui'))

class ViewServers(QtGui.QDialog, FORM_CLASS):
    defaultChanged = pyqtSignal()
    def __init__(self, iface = None, parent=None):
        '''Constructor.'''
        super(ViewServers, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.abstractDbFactory = DbFactory()
        self.initGui()
        host, port, user, password = self.getDefaultConnectionParameters()
        self.defaultConnectionDict = self.setDefaultConnectionParameters(host, port, user, password)
    
    def initGui(self):
        '''
        Initiates the dialog
        '''
        header = self.tableWidget.horizontalHeader()
        header.setResizeMode(QHeaderView.Stretch)
        self.populateTable()
        
    def populateTable(self):
        '''
        Populates the servers table
        '''
        currentConnections = self.getServers()
        self.tableWidget.setRowCount(len(currentConnections))
        for i, connection in enumerate(currentConnections):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(connection))
            (host, port, user, password, isDefault) = self.getServerConfiguration(connection)
            self.tableWidget.setItem(i, 1, QTableWidgetItem(host))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(port))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(user))
            if not password or len(password) == 0:
                self.tableWidget.setItem(i, 4, QTableWidgetItem(self.tr('Not Saved')))
            else:
                self.tableWidget.setItem(i, 4, QTableWidgetItem(self.tr('Saved')))
            radio = QRadioButton()
            if isDefault:
                radio.setChecked(True)
            self.tableWidget.setCellWidget(i, 5, radio)
    
    def setDefaultConnectionParameters(self, host, port, user, password):
        defaultConnectionDict = dict()
        if host and port and user and password:
            defaultConnectionDict['host'] = host
            defaultConnectionDict['port'] = port
            defaultConnectionDict['user'] = user
            defaultConnectionDict['password'] = password
        else:
            defaultConnectionDict = dict()
        return defaultConnectionDict
    
    def getDefaultConnectionParameters(self):
        currentConnections = self.getServers()
        for i, connection in enumerate(currentConnections):
            (host, port, user, password, isDefault) = self.getServerConfiguration(connection)
            if isDefault == True:
                return (host, port, user, password)
        return (None, None, None, None)

        
    @pyqtSlot(bool)
    def on_closeButton_clicked(self):
        '''
        Closes the dialog if default connection is set
        '''
        currentConnections = self.getServers()
        self.tableWidget.setRowCount(len(currentConnections))
        for i, connection in enumerate(currentConnections):
            if self.tableWidget.cellWidget(i, 5).isChecked():
                (host, port, user, password, isDefault) = self.getServerConfiguration(connection)
                dlg = ServerConfigurator(self)
                dlg.setServerConfiguration(connection)
                dlg.storeServerConfiguration(connection, host, port, user, password, isDefault = True)
                self.setDefaultConnectionParameters(host, port, user, password)
                self.defaultChanged.emit()
                self.done(0)
                return
        QMessageBox.warning(self, self.tr('Info!'), self.tr('Set default connection before closing!'))
        
    @pyqtSlot(bool)
    def on_addButton_clicked(self):
        '''
        Adds a new server
        '''
        dlg = ServerConfigurator(self)
        result = dlg.exec_()
        if result:
            self.populateTable()
            
    @pyqtSlot(bool)
    def on_editButton_clicked(self):
        '''
        Edits an existing server
        '''
        selectedItem = self.returnSelectedName()
        if not selectedItem:
            return
        dlg = ServerConfigurator(self)
        dlg.setServerConfiguration(selectedItem.text())
        result = dlg.exec_()
        if result:
            self.populateTable()
        
    @pyqtSlot(bool)
    def on_removeButton_clicked(self):
        '''
        Removes an existing server
        '''
        selectedItem = self.returnSelectedName()
        if not selectedItem:
            return
        self.removeServerConfiguration(selectedItem.text())
        self.tableWidget.removeRow(selectedItem.row())
        QMessageBox.warning(self, self.tr('Info!'), self.tr('Server removed.'))
        
    @pyqtSlot(bool)
    def on_testButton_clicked(self):
        '''
        Tests server connection
        '''
        selectedItem = self.returnSelectedName()
        if not selectedItem:
            return
        name = selectedItem.text()
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            test = self.testServer(name)
            QApplication.restoreOverrideCursor()
        except:
            QApplication.restoreOverrideCursor()
        if test:
            QMessageBox.warning(self, self.tr('Info!'), self.tr('Connection online.'))
        else:
            QMessageBox.warning(self, self.tr('Info!'), self.tr('Connection was not successful. Check log for details.'))
        
    def getServers(self):
        '''
        Gets all server from QSettings
        '''
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers')
        currentConnections = settings.childGroups()
        settings.endGroup()
        return currentConnections
    
    def getServerConfiguration(self, name):
        '''
        Gets server configuration
        name: server name 
        '''
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers/'+name)
        host = settings.value('host')
        port = settings.value('port')
        user = settings.value('username')
        password = settings.value('password')
        isDefault = settings.value('isDefault')
        settings.endGroup()
        
        return (host, port, user, password, isDefault)
    
    def removeServerConfiguration(self, name):
        '''
        Removes a server from QSettings
        '''
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers/'+name)
        settings.remove('')
        settings.endGroup()
        
    def testServer(self, name):
        '''
        Tests if the server is online
        '''
        abstractDb = self.abstractDbFactory.createDbFactory('QPSQL')
        if not abstractDb:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            return False
        (host, port, user, password) = abstractDb.getServerConfiguration(name)
        abstractDb.connectDatabaseWithParameters(host, port, 'postgres', user, password)
        try:
            abstractDb.checkAndOpenDb()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
            return False
        return True
    
    def returnSelectedName(self):
        '''
        Gets the selected server name 
        '''
        if len(self.tableWidget.selectedItems()) == 0:
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Select one server.'))
            return
        return self.tableWidget.selectedItems()[0]