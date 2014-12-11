# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_serverConfigurator import Ui_Dialog

class ServerConfigurator(QDialog, Ui_Dialog):
    def __init__(self, iface):
        """Constructor."""
        super(ServerConfigurator, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        self.iface = iface
        
        self.populateServersCombo()
        
    @pyqtSlot(bool)    
    def on_saveButton_clicked(self):
        if self.checkFields():
            name = self.serversCombo.currentText()
            host = self.hostEdit.text()
            port = self.portEdit.text()
            user = self.userEdit.text()
            password = self.passwordEdit.text()
            self.storeServerConfiguration(name, host, port, user, password)
            self.populateServersCombo()
        else:
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", "Fill all parameters.")
    
    @pyqtSlot(bool)    
    def on_cancelButton_clicked(self):
        self.done(0)
    
    def on_serversCombo_currentIndexChanged(self, index):
        self.getServerConfiguration(self.serversCombo.currentText())
    
    def checkFields(self):
        if self.hostEdit.text() == '' or self.portEdit.text() == '' \
            or self.userEdit.text() == '' or self.passwordEdit.text() == '':
            return False
        return True
    
    def storeServerConfiguration(self, name, host, port, user, password):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/connections/'+name)
        settings.setValue('database', 'postgres')
        settings.setValue('host', host)
        settings.setValue('port', port)
        settings.setValue('username', user)
        settings.setValue('password', password)
        settings.endGroup()
        
    def getServerConfiguration(self, name):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/connections/'+name)
        database = settings.value('database')
        host = settings.value('host')
        port = settings.value('port')
        user = settings.value('username')
        password = settings.value('password')
        settings.endGroup()
        
        self.hostEdit.setText(host)
        self.portEdit.setText(port)
        self.userEdit.setText(user)
        self.passwordEdit.setText(password)
        
    def getServers(self):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/connections')
        currentConnections = settings.childGroups()
        settings.endGroup()
        return currentConnections
        
    def populateServersCombo(self):
        self.serversCombo.clear()
        currentConnections = self.getServers()
        for connection in currentConnections:
            self.serversCombo.addItem(connection)
        