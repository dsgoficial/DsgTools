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

from qgis.core import QgsMessageLog, Qgis

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings
from qgis.PyQt.QtSql import QSqlQuery
from qgis.PyQt.QtWidgets import QMessageBox

# DSGTools imports
from ....ServerTools.viewServers import ViewServers
from .....core.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from .....core.Factories.DbFactory.abstractDb import AbstractDb
from .....core.Factories.DbFactory.dbFactory import DbFactory
from ....CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget
from DsgTools.core.dsgEnums import DsgEnums

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "exploreServerWidget.ui")
)


class ExploreServerWidget(QtWidgets.QWidget, FORM_CLASS):
    abstractDbLoaded = pyqtSignal()
    serverAbstractDbLoaded = pyqtSignal(AbstractDb)
    clearWidgets = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(ExploreServerWidget, self).__init__(parent)
        self.setupUi(self)
        self.superNeeded = False
        self.dbFactory = DbFactory()
        self.factory = SqlGeneratorFactory()
        self.abstractDb = None
        self.populateServersCombo()

    def getServers(self):
        """
        Gets server from QSettings
        """
        settings = QSettings()
        settings.beginGroup("PostgreSQL/servers")
        currentConnections = settings.childGroups()
        settings.endGroup()
        return currentConnections

    def getServerConfiguration(self, name):
        """
        Gets server configuration
        name: server name
        """
        settings = QSettings()
        settings.beginGroup("PostgreSQL/servers/" + name)
        host = settings.value("host")
        port = settings.value("port")
        user = settings.value("username")
        password = settings.value("password")
        settings.endGroup()

        return (host, port, user, password)

    def browseServer(self, dbList, host, port, user, password):
        """
        Browses server for EDGV databases
        dbList: databases list
        host: server host ip address
        port: server port
        user: user name
        password: password
        """
        canLoad = True
        if self.superNeeded:
            canLoad = False
            try:
                if self.serverWidget.abstractDb.checkSuperUser():
                    canLoad = True
                else:
                    QMessageBox.warning(
                        self,
                        self.tr("Info!"),
                        self.tr(
                            "Connection refused. Connect with a super user to inspect server."
                        ),
                    )
                    return []
            except Exception as e:
                QMessageBox.critical(self, self.tr("Critical!"), ":".join(e.args))
        if canLoad:
            progress = ProgressWidget(
                1,
                len(dbList),
                self.tr("Loading databases from server... "),
                parent=self,
            )
            progress.initBar()
            gen = self.factory.createSqlGenerator(driver=DsgEnums.DriverPostGIS)
            edvgDbList = []
            for database in dbList:
                postgisDb = self.dbFactory.createDbFactory(DsgEnums.DriverPostGIS)
                postgisDb.connectDatabaseWithParameters(
                    host, port, database, user, password
                )
                if not postgisDb.db.open():
                    qgis.utils.iface.messageBar().pushMessage(
                        "DB :"
                        + database
                        + "| msg: "
                        + postgisDb.db.lastError().databaseText(),
                        level=Qgis.Critical,
                    )

                query = QSqlQuery(postgisDb.db)
                if query.exec_(gen.getEDGVVersion()):
                    while query.next():
                        version = query.value(0)
                        if version:
                            edvgDbList.append((database, version))
                progress.step()
            return edvgDbList

    def getDbsFromServer(self, name):
        """
        Gets server databases
        name: server name
        """
        gen = self.factory.createSqlGenerator(driver=DsgEnums.DriverPostGIS)

        (host, port, user, password) = self.getServerConfiguration(name)
        database = "postgres"
        postgisDb = self.dbFactory.createDbFactory(DsgEnums.DriverPostGIS)
        postgisDb.connectDatabaseWithParameters(host, port, database, user, password)
        if not postgisDb.db.open():
            QgsMessageLog.logMessage(
                db.lastError().text(), "DSGTools Plugin", Qgis.Critical
            )
            QMessageBox.critical(
                self.iface.mainWindow(),
                self.tr("Critical"),
                self.tr("A problem occurred! Check log for details."),
            )

        query = QSqlQuery(gen.getDatabasesFromServer(), postgisDb.db)
        if not query.isActive():
            QMessageBox.critical(
                self.iface.mainWindow(),
                self.tr("Critical"),
                self.tr("Problem executing query: ") + query.lastError().text(),
            )

        dbList = []
        while query.next():
            dbList.append(query.value(0))
        postgisDb.closeDatabase()
        return self.browseServer(dbList, host, port, user, password)

    @pyqtSlot(bool)
    def on_createNewServerPushButton_clicked(self):
        """
        Opens the View Server dialog
        """
        createNewServer = ViewServers(self)
        result = createNewServer.exec_()
        self.populateServersCombo()

    def populateServersCombo(self):
        """
        Populates the server name combo box
        """
        self.serversCombo.clear()
        self.serversCombo.addItem(self.tr("Select Server"))
        currentConnections = self.getServers()
        for connection in currentConnections:
            (host, port, user, password) = self.getServerConfiguration(connection)
            self.serversCombo.addItem(
                "{3} ({0}@{1}:{2})".format(user, host, port, connection)
            )

    @pyqtSlot(int)
    def on_serversCombo_currentIndexChanged(self):
        """
        Updates the server databases
        """
        self.clearWidgets.emit()
        if self.serversCombo.currentIndex() > 0:
            self.abstractDb = self.dbFactory.createDbFactory(DsgEnums.DriverPostGIS)
            if not self.abstractDb:
                QMessageBox.critical(
                    self.iface.mainWindow(),
                    self.tr("Critical"),
                    self.tr("A problem occurred! Check log for details."),
                )
                return
            (host, port, user, password) = self.abstractDb.getServerConfiguration(
                self.serversCombo.currentText().split("(")[0][0:-1]
            )
            if host or port or user:
                self.abstractDb.connectDatabaseWithParameters(
                    host, port, "postgres", user, password
                )
                if self.superNeeded:
                    try:
                        if not self.abstractDb.checkSuperUser():
                            QMessageBox.warning(
                                self,
                                self.tr("Info!"),
                                self.tr(
                                    "Connection refused. Connect with a super user to inspect server."
                                ),
                            )
                            self.serversCombo.setCurrentIndex(0)
                            return
                    except Exception as e:
                        QMessageBox.critical(
                            self, self.tr("Critical!"), ":".join(e.args)
                        )
                self.abstractDbLoaded.emit()
        else:
            try:
                if self.abstractDb:
                    self.abstractDb.__del__()
                    self.abstractDb = None
            except:
                pass
        self.serverAbstractDbLoaded.emit(self.abstractDb)

    def getServerParameters(self):
        """
        Gets postgis server parameters
        """
        if self.serversCombo.currentIndex() != 0:
            return self.abstractDb.getServerConfiguration(
                self.serversCombo.currentText().split("(")[0][0:-1]
            )
        else:
            return (None, None, None, None)

    def clearAll(self):
        """
        Resets the widget
        """
        try:
            if self.abstractDb:
                self.abstractDb.__del__()
                self.abstractDb = None
        except:
            pass
        self.serversCombo.setCurrentIndex(0)
