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

import sys, os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QHeaderView, QTableWidgetItem
from serverConfigurator import ServerConfigurator

from qgis.core import *

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
            (host, port, user) = self.getServerConfiguration(connection)
            self.tableWidget.setItem(i,1,QTableWidgetItem(host))
            self.tableWidget.setItem(i,2,QTableWidgetItem(port))
            self.tableWidget.setItem(i,3,QTableWidgetItem(user))

    
        
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
    def on_removeButton_clicked(self):
        selectedItem = self.tableWidget.selectedItems()[0]
        self.removeServerConfiguration(selectedItem.text())
        self.tableWidget.removeRow(selectedItem.row())
        
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
        
        return (host, port, user)
    
    
    def removeServerConfiguration(self, name):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers/'+name)
        settings.remove('')
        settings.endGroup()