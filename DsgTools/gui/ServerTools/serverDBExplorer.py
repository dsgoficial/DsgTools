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
from builtins import range
import os

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt, QSettings
from qgis.PyQt.QtWidgets import QListWidgetItem, QMessageBox
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery

# DSGTools imports
from DsgTools.core.Utils.utils import Utils
from DsgTools.core.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.gui.ServerTools.viewServers import ViewServers
from DsgTools.core.dsgEnums import DsgEnums

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "ui_serverDBExplorer.ui")
)


class ServerDBExplorer(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.utils = Utils()
        self.factory = SqlGeneratorFactory()
        # setting the sql generator
        self.gen = self.factory.createSqlGenerator(driver=DsgEnums.DriverPostGIS)
        self.serverWidget.populateServersCombo()
        self.serverWidget.abstractDbLoaded.connect(
            self.populateListWithDatabasesFromServer
        )

    def storeConnection(self, server, database):
        """
        Stores database connection in the QSettings
        """
        (host, port, user, password) = self.getServerConfiguration(server)
        connection = server + "_" + database
        settings = QSettings()
        if not settings.contains("PostgreSQL/connections/" + connection + "/database"):
            settings.beginGroup("PostgreSQL/connections/" + connection)
            settings.setValue("database", database)
            settings.setValue("host", host)
            settings.setValue("port", port)
            settings.setValue("username", user)
            settings.setValue("password", password)
            settings.endGroup()
            return True
        return False

    def getServerConfiguration(self, name):
        """
        Gets server configuration from QSetting by its name
        """
        settings = QSettings()
        settings.beginGroup("PostgreSQL/servers/" + name)
        host = settings.value("host")
        port = settings.value("port")
        user = settings.value("username")
        password = settings.value("password")
        settings.endGroup()
        return (host, port, user, password)

    def storeConnectionConfiguration(self, server, database):
        """
        Stores connection configuration in thw QSettings
        server: server name
        database: database name
        """
        name = self.connectionEdit.text()

        (host, port, user, password) = self.getServerConfiguration(server)
        settings = QSettings()
        if not settings.contains("PostgreSQL/servers/" + name + "/host"):
            settings.beginGroup("PostgreSQL/connections/" + name)
            settings.setValue("database", database)
            settings.setValue("host", host)
            settings.setValue("port", port)
            settings.setValue("username", user)
            settings.setValue("password", password)
            settings.endGroup()

    def populateListWithDatabasesFromServer(self):
        """
        Populates databases from server
        """
        self.serverListWidget.clear()

        dbList = []
        try:
            dbList = self.serverWidget.abstractDb.getEDGVDbsFromServer()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Critical!"), ":".join(e.args))
        dbList.sort()

        for (dbname, dbversion) in dbList:
            item = QListWidgetItem(self.serverListWidget)
            item.setText(dbname + " (EDGV v. " + dbversion + ")")
            item.setData(Qt.UserRole, dbname)

    @pyqtSlot(bool)
    def on_createConnectionPushButton_clicked(self):
        """
        Creates a connection with the selected databases
        """
        items = self.serverListWidget.selectedItems()
        existentConnections = []
        newConnections = []
        for item in items:
            dbname = item.data(Qt.UserRole)
            ret = self.storeConnection(
                self.serverWidget.serversCombo.currentText(), dbname
            )
            if not ret:
                existentConnections.append(dbname)
            else:
                newConnections.append(dbname)

        msg = self.tr("Information:\n")
        if len(existentConnections) > 0:
            msg += self.tr("The following databases connections already exist:\n")
            for conn in existentConnections:
                msg += conn + ", "
        if len(newConnections) > 0:
            msg += self.tr(
                "\nThe following databases connections were created successfully:\n"
            )
            for conn in newConnections:
                msg += conn + ", "
        QMessageBox.warning(self, self.tr("Warning!"), msg)

    @pyqtSlot(bool)
    def on_selectAllPushButton_clicked(self):
        """
        Select all databases on server to create connection
        """
        count = self.serverListWidget.count()
        for row in range(count):
            item = self.serverListWidget.item(row)
            item.setSelected(True)

    @pyqtSlot(bool)
    def on_removeMissingPushButton_clicked(self):
        """
        Remove missing databases from QSetttings
        """
        servers = self.serverWidget.getServers()
        settings = QSettings()
        settings.beginGroup("PostgreSQL/connections")
        candidates = settings.childGroups()
        settings.endGroup()
        removedConn = []
        dbList = []
        try:
            dbList = self.serverWidget.abstractDb.getDbsFromServer()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Critical!"), ":".join(e.args))

        for candidate in candidates:
            candidateSettings = QSettings()
            candidateSettings.beginGroup("PostgreSQL/connections/" + candidate)
            candidateDb = candidateSettings.value("database")
            if candidateDb not in dbList:
                self.removeConnections(candidate, removedConn)
        if len(removedConn) > 0:
            msg = self.tr(
                "\nThe following databases connections were removed successfully:\n"
            ) + ", ".join(removedConn)
        else:
            msg = self.tr("No connections were removed.")
        QMessageBox.warning(self, self.tr("Warning!"), msg)

    def removeConnections(self, candidate, removedConn):
        """
        Remove a specific connection from QSettings
        """
        candidateSettings = QSettings()
        candidateSettings.beginGroup("PostgreSQL/connections/" + candidate)
        candidateSettings.remove("")
        removedConn.append(candidate)
        candidateSettings.endGroup()
