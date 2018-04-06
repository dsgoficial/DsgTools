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
import os
# Import the PyQt and QGIS libraries
from qgis.PyQt import uic
from qgis.PyQt.QtCore import QSettings
from PyQt4.QtGui import QMessageLog
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
from qgis.PyQt.QtWidgets import QDialog

#QGIS Imports
from qgis.core import QgsCoordinateReferenceSystem, QgsMessageLog, QgsCredentials
from qgis.gui import QgsGenericProjectionSelector

#DsgTools Imports
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.ServerTools.viewServers import ViewServers


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_postgisDBTool.ui'))

class PostgisDBTool(QDialog, FORM_CLASS):
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
        self.db = None
        self.abstractDb = None
        self.factory = SqlGeneratorFactory()
        #setting the sql generator
        self.gen = self.factory.createSqlGenerator(False)

        self.epsg = 4326

    def getParameters(self):
        """
        Gets database parameters
        """
        return (self.databaseEdit.text(), self.abstractDb, self.versionCombo.currentText(), self.epsg)

    @pyqtSlot(bool)
    def on_saveButton_clicked(self):
        """
        Creates a postgis database
        """
        if self.databaseEdit.text() == '':
            QgsMessageLog.logMessage('Enter database name!', "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        else:
            self.db = self.getDatabase()
            if self.db:
                self.storeConnectionConfiguration(self.serversCombo.currentText(), self.databaseEdit.text())
                self.done(1)


    @pyqtSlot(bool)
    def on_cancelButton_clicked(self):
        """
        Cancels everything
        """
        self.done(-1)

    @pyqtSlot(bool)
    def on_configureServerButton_clicked(self):
        """
        Opens the ViewServer dialog
        """
        dlg = ViewServers(self.iface)
        dlg.show()
        result = dlg.exec_()
        self.populateServersCombo()

    @pyqtSlot(bool)
    def on_srsButton_clicked(self):
        """
        Opens the CRS selector dialog
        """
        projSelector = QgsGenericProjectionSelector()
        message = 'Select the Spatial Reference System!'
        projSelector.setMessage(theMessage=message)
        projSelector.exec_()
        try:
            self.epsg = int(projSelector.selectedAuthId().split(':')[-1])
            srs = QgsCoordinateReferenceSystem(self.epsg, QgsCoordinateReferenceSystem.EpsgCrsId)
            if srs:
                self.srsEdit.setText(srs.description())
            else:
                self.epsg = 4326
        except:
            QMessageBox.warning(self, self.tr("Warning!"), message)


    def createDatabase(self, name):
        """
        Creates the database
        """
        sql = self.gen.getCreateDatabase(name)

        db = self.getDatabase()

        #creating the database
        query = QSqlQuery(db)
        if not query.exec_(sql):
            QMessageBox.warning(self, self.tr("Warning!"), query.lastError().text())
            db.close()
            return False
        db.close()
        return True

    def getDatabase(self, database = 'postgres'):
        """
        Gets a a QSqlDatabase 
        """
        (host, port, user, password) = self.getServerConfiguration(self.serversCombo.currentText())
        self.abstractDb = DbFactory().createDbFactory('QPSQL')

        if password == '':
            conInfo = 'host='+host+' port='+port+' dbname='+database
            self.setCredentials(self.abstractDb.db, conInfo, user)
        else:
            self.abstractDb.connectDatabaseWithParameters(host, port, database, user, password)

        if not self.abstractDb.db.open():
            QgsMessageLog.logMessage(self.abstractDb.db.lastError().text(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)

        return self.abstractDb

    def setCredentials(self, db, conInfo, user):
        """
        Sets connection credentials
        db: QSqlDatabase used
        conInfo: connection information
        user: user name
        """
        (success, user, password) = QgsCredentials.instance().get(conInfo, user, None)
        if not success:
            return
        else:
            db.setPassword(password)
            db.setUserName(user)
            if not db.open():
                self.setCredentials(db, conInfo, user)
            else:
                QgsCredentials.instance().put(conInfo, user, password)

    def updateConnectionName(self):
        """
        Updates connection name
        """
        server = self.serversCombo.currentText()
        database = self.databaseEdit.text()
        name = server+'_'+database
        self.connectionEdit.setText(name)

    def on_serversCombo_currentIndexChanged(self, index):
        """
        Slot to update the connection name
        """
        self.updateConnectionName()

    def on_databaseEdit_textEdited(self, text):
        """
        Adjusts the text before updating the connection name
        """
        self.updateConnectionName()

    def checkFields(self):
        """
        Check fields prior the next step
        """
        if self.serversCombo.currentText() == '' or self.databaseEdit.text() == '' or self.srsEdit.text() == '':
            return False
        return True

    def getServerConfiguration(self, name):
        """
        Gets server configuration from QSettings
        name: server name
        """
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers/'+name)
        host = settings.value('host')
        port = settings.value('port')
        user = settings.value('username')
        password = settings.value('password')
        settings.endGroup()
        return (host, port, user, password)

    def storeConnectionConfiguration(self, server, database):
        """
        Stores the new configuration
        server: server name
        database: database name
        """
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
        """
        Gets all servers from QSettings
        """
        settings = QSettings()
        settings.beginGroup('PostgreSQL/servers')
        currentConnections = settings.childGroups()
        settings.endGroup()
        return currentConnections

    def populateServersCombo(self):
        """
        Populates the server combo box
        """
        self.serversCombo.clear()
        currentConnections = self.getServers()
        for connection in currentConnections:
            self.serversCombo.addItem(connection)
