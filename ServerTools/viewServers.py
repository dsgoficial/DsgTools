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
from PyQt4.QtCore import *
from PyQt4.QtGui import QHeaderView, QTableWidgetItem, QMessageBox, QApplication, QCursor
from PyQt4.QtSql import QSqlDatabase
from serverConfigurator import ServerConfigurator

from qgis.core import QgsMessageLog

from DsgTools.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.Factories.DbFactory.dbFactory import DbFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_viewServers.ui'))

class ViewServers(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        '''Constructor.'''
        super(ViewServers, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface
        self.abstractDbFactory = DbFactory()
        self.initGui()
    
    def initGui(self):
        header = self.tableWidget.horizontalHeader()
        header.setResizeMode(QHeaderView.Stretch)
        self.populateTable()
        
    def populateTable(self):
        currentConnections = self.getServers()
        self.tableWidget.setRowCount(len(currentConnections))
        for i, connection in enumerate(currentConnections):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(connection))
            (host, port, user, password) = self.getServerConfiguration(connection)
            self.tableWidget.setItem(i, 1, QTableWidgetItem(host))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(port))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(user))
            if not password or len(password) == 0:
                self.tableWidget.setItem(i, 4, QTableWidgetItem(self.tr('Not Saved')))
            else:
                self.tableWidget.setItem(i, 4, QTableWidgetItem(self.tr('Saved')))
        
    @pyqtSlot(bool)
    def on_cancelButton_clicked(self):
        self.done(0)
        
    @pyqtSlot(bool)
    def on_addButton_clicked(self):
        dlg = ServerConfigurator(self)
        result = dlg.exec_()
        if result:
            self.populateTable()
            
    @pyqtSlot(bool)
    def on_editButton_clicked(self):
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
        selectedItem = self.returnSelectedName()
        if not selectedItem:
            return
        self.removeServerConfiguration(selectedItem.text())
        self.tableWidget.removeRow(selectedItem.row())
        QMessageBox.warning(self, self.tr('Info!'), self.tr('Server removed.'))
        
    @pyqtSlot(bool)
    def on_testButton_clicked(self):
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
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers')
        currentConnections = settings.childGroups()
        settings.endGroup()
        return currentConnections
    
    def getServerConfiguration(self, name):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers/'+name)
        host = settings.value('host')
        port = settings.value('port')
        user = settings.value('username')
        password = settings.value('password')
        settings.endGroup()
        
        return (host, port, user, password)
    
    def removeServerConfiguration(self, name):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers/'+name)
        settings.remove('')
        settings.endGroup()
        
    def testServer(self, name):
        abstractDb = self.abstractDbFactory.createDbFactory('QPSQL')
        if not abstractDb:
            return False
        (host, port, user, password) = abstractDb.getServerConfiguration(name)
        abstractDb.connectDatabaseWithParameters(host, port, 'postgres', user, password)
        try:
            abstractDb.checkAndOpenDb()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(e.args[0], 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
            return False
        return True
    
    def returnSelectedName(self):
        if len(self.tableWidget.selectedItems()) == 0:
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Select one server.'))
            return
        return self.tableWidget.selectedItems()[0]