# -*- coding: utf-8 -*-
"""
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
"""
import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QHeaderView, QTableWidgetItem, QMessageBox, QApplication, QCursor
from PyQt4.QtSql import QSqlDatabase
from serverConfigurator import ServerConfigurator
from numpy.lib._iotools import NameValidator

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_viewServers.ui'))

class ViewServers(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        super(ViewServers, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface
        
        self.initGui()
    
    def initGui(self):
        header = self.tableWidget.horizontalHeader()
        header.setResizeMode(QHeaderView.Stretch)
        self.populateTable()
            
        
        
    def populateTable(self):
        currentConnections = self.getServers()
        self.tableWidget.setRowCount(len(currentConnections))
        for i, connection in enumerate(currentConnections):
            self.tableWidget.setItem(i,0,QTableWidgetItem(connection))
            (host, port, user, password) = self.getServerConfiguration(connection)
            self.tableWidget.setItem(i,1,QTableWidgetItem(host))
            self.tableWidget.setItem(i,2,QTableWidgetItem(port))
            self.tableWidget.setItem(i,3,QTableWidgetItem(user))
            if len(password)==0:
                self.tableWidget.setItem(i,4,QTableWidgetItem(self.tr('Clear')))
            else:
                self.tableWidget.setItem(i,4,QTableWidgetItem(self.tr('Saved')))
    
        
    @pyqtSlot(bool)
    def on_cancelButton_clicked(self):
        self.done(0)
        
    @pyqtSlot(bool)
    def on_addButton_clicked(self):
        dlg = ServerConfigurator(self)
        #dlg.show()
        result = dlg.exec_()
        if result:
            self.populateTable()
            
    @pyqtSlot(bool)
    def on_editButton_clicked(self):
        selectedItem = self.returnSelectedName()
        dlg = ServerConfigurator(self)
        dlg.setServerConfiguration(selectedItem.text())
        #dlg.show()
        result = dlg.exec_()
        if result:
            self.populateTable()
        
        
    @pyqtSlot(bool)
    def on_removeButton_clicked(self):
        selectedItem = self.returnSelectedName()
        self.removeServerConfiguration(selectedItem.text())
        self.tableWidget.removeRow(selectedItem.row())
        QMessageBox.warning(self, self.tr("Info!"), self.tr("Server removed."))
        
    @pyqtSlot(bool)
    def on_testButton_clicked(self):
        name = self.returnSelectedName().text()
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        test = self.testServer(name)
        QApplication.restoreOverrideCursor()
        if test:
            QMessageBox.warning(self, self.tr("Info!"), self.tr("Server Online."))
        else:
            QMessageBox.warning(self, self.tr("Info!"), self.tr("Server Offline."))
        
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
        (host, port, user, password) = self.getServerConfiguration(name)
        db = None
        db = QSqlDatabase("QPSQL")
        db.setConnectOptions("connect_timeout=50")
        #db.setDatabaseName("")
        db.setHostName(host)
        db.setPort(int(port))
        db.setUserName(user)
        db.setPassword(password)
        open = db.open()
        db.close()
        return open
    
    def returnSelectedName(self):
        if len(self.tableWidget.selectedItems())==0:
            QMessageBox.warning(self, self.tr("Warning!"), self.tr("Select one server."))
            return
        return self.tableWidget.selectedItems()[0]