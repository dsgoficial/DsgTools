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

from qgis.core import QgsCoordinateReferenceSystem
from qgis.gui import QgsGenericProjectionSelector

from ui_postgisDBTool import Ui_Dialog

class PostgisDBTool(QDialog, Ui_Dialog):
    def __init__(self, iface):
        """Constructor."""
        super(PostgisDBTool, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        
        self.iface = iface
        
        self.populateServersCombo()
        
        self.srs = None
        
    @pyqtSlot(bool)    
    def on_saveButton_clicked(self):
        if self.checkFields():
            server = self.serversCombo.currentText()
            database = self.databaseEdit.text()
            name = server+'_'+database
            srs = self.srsEdit.text()
            self.storeConnectionConfiguration(server, database, srs)
            self.populateServersCombo()
        else:
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", "Fill all parameters.")
    
    @pyqtSlot(bool)    
    def on_cancelButton_clicked(self):
        self.done(0)

    @pyqtSlot(bool)    
    def on_srsButton_clicked(self):
        projSelector = QgsGenericProjectionSelector()
        message = 'Select the Spatial Reference System!'
        projSelector.setMessage(theMessage=message)
        projSelector.exec_()
        try:
            epsg = int(projSelector.selectedAuthId().split(':')[-1])
            self.srs = QgsCoordinateReferenceSystem(epsg, QgsCoordinateReferenceSystem.EpsgCrsId)
            if self.srs:
                self.srsEdit.setText(self.srs.description())
        except:
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", message)
    
    def updateConnectionName(self):
        server = self.serversCombo.currentText()
        database = self.databaseEdit.text()
        name = server+'_'+database
        self.connectionEdit.setText(name)
    
    def on_serversCombo_currentIndexChanged(self, index):
        self.updateConnectionName()
        
    def on_databaseEdit_textEdited(self, text):
        self.updateConnectionName()
    
    def checkFields(self):
        if self.serversCombo.currentText() == '' or self.databaseEdit.text() == '' \
            or self.srsEdit.text() == '':
            return False
        return True
    
    def getServerConfiguration(self, name):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers/'+name)
        host = settings.value('host')
        port = settings.value('port')
        user = settings.value('username')
        password = settings.value('password')
        settings.endGroup()
        return (host, port, user, password)
    
    def storeConnectionConfiguration(self, server, database, srs):
        name = self.connectionEdit.text()
        
        (host, port, user, password) = self.getServerConfiguration(server)
        
        settings = QSettings()
        settings.beginGroup('PostgreSQL/connections/'+name)
        settings.setValue('database', database)
        settings.setValue('host', host)
        settings.setValue('port', port)
        settings.setValue('username', user)
        settings.setValue('password', password)
        settings.endGroup()
        
    def getServers(self):
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers')
        currentConnections = settings.childGroups()
        settings.endGroup()
        return currentConnections
        
    def populateServersCombo(self):
        self.serversCombo.clear()
        currentConnections = self.getServers()
        for connection in currentConnections:
            self.serversCombo.addItem(connection)
            