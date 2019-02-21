# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-05-15
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba.philipe@eb.mil.br
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

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, Qt
from qgis.PyQt.QtWidgets import QApplication, QMessageBox
from qgis.PyQt.QtGui import QCursor
from qgis.core import QgsMessageLog, Qgis

from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.dsgCustomComboBox import DsgCustomComboBox
from DsgTools.gui.ServerTools.viewServers import ViewServers
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.gui.CustomWidgets.DatabaseConversionWidgets.datasourceInfoTable import DatasourceInfoTable
from DsgTools.core.dsgEnums import DsgEnums

import os

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'connectionComboBox.ui'))
class ConnectionComboBox(QtWidgets.QWidget, FORM_CLASS):
    connectionChanged = pyqtSignal()
    dbChanged = pyqtSignal(AbstractDb)
    problemOccurred = pyqtSignal(str)
    def __init__(self, parent=None):
        super(ConnectionComboBox, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.abstractDb = None
        self.abstractDbFactory = DbFactory()
        self.serverAbstractDb = None
        self.displayDict = {'2.1.3':'EDGV 2.1.3', '2.1.3 Pro':'EDGV 2.1.3 Pro','FTer_2a_Ed':'EDGV FTer 2a Ed', 'Non_EDGV':self.tr('Other database model'), '3.0':'EDGV 3.0'}
        self.instantiateAbstractDb = False
        self.viewServers = ViewServers()
        self.viewServers.defaultChanged.connect(self.loadServerAbstractDb)
        self.connectionSelectorComboBox.addItem(self.tr('Select database'))
        self.loadServerAbstractDb()
    
    def __del__(self):
        """
        Destructor
        """
        if self.serverAbstractDb is not None:
            self.serverAbstractDb.closeDatabase()
        super(ConnectionComboBox, self).__del__()
    
    def loadServerAbstractDb(self):
        """
        Checks if there is a default db in self.viewServers . If there isn't one, disables connection combo
        """
        if self.viewServers.defaultConnectionDict == dict():
            self.connectionSelectorComboBox.setEnabled(False)
        else:
            self.connectionSelectorComboBox.setEnabled(True)
            (_, host, port, user, password) = self.viewServers.getDefaultConnectionParameters()
            serverAbstractDb = self.abstractDbFactory.createDbFactory(DsgEnums.DriverPostGIS)
            serverAbstractDb.connectDatabaseWithParameters(host, port, 'postgres', user, password)
            self.setServerDb(serverAbstractDb)
            serverAbstractDb.closeDatabase()
    
    def closeDatabase(self):
        if self.abstractDb is not None:
            self.abstractDb.closeDatabase()

    def clear(self):
        self.connectionSelectorComboBox.clear()
        self.closeDatabase()
    
    def setServerDb(self, serverAbstractDb):
        self.serverAbstractDb = serverAbstractDb
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            if self.serverAbstractDb:
                dbList = self.serverAbstractDb.getEDGVDbsFromServer(parentWidget = self.parent, getDatabaseVersions = False)
                dbList.sort()
                self.clear()
                self.connectionSelectorComboBox.addItem(self.tr('Select Database'))
                self.addItems(dbList)
            else:
                self.clear()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), ':'.join(e.args))
        QApplication.restoreOverrideCursor()
    
    def addItems(self, items):
        itemList = []
        if items == []:
            return
        elif isinstance(items[0], tuple) and len(items[0]) == 2:
            for item in items:
                if item[1] not in list(self.displayDict.keys()):
                    version = item[1]
                else:
                    version = self.displayDict[item[1]]
                newText = item[0] + ' ({0})'.format(version)
                itemList.append(newText)
        if itemList == []:
            itemList = items
        self.connectionSelectorComboBox.addItems(itemList)
    
    def currentDb(self):
        if self.connectionSelectorComboBox.currentIndex() == 0:
            return ''
        else:
            return self.connectionSelectorComboBox.currentText().split(' (')[0]
    
    @pyqtSlot(int, name = 'on_connectionSelectorComboBox_currentIndexChanged')
    def loadDatabase(self, idx):
        """
        Loads the selected database
        """
        try:
            if self.abstractDb is not None:
                self.closeDatabase()
            if self.serverAbstractDb is not None and idx > 0:
                if not self.instantiateAbstractDb:
                    self.abstractDb = self.abstractDbFactory.createDbFactory(DsgEnums.DriverPostGIS)
                    (host, port, user, password) = self.serverAbstractDb.getDatabaseParameters()
                    dbName = self.connectionSelectorComboBox.currentText().split(' (')[0]
                    self.abstractDb.connectDatabaseWithParameters(host, port, dbName, user, password)
                    self.abstractDb.checkAndOpenDb()
                    self.dbChanged.emit(self.abstractDb)
                    self.connectionChanged.emit()
        except Exception as e:
            self.closeDatabase()
            self.problemOccurred.emit(self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), "DSG Tools Plugin", Qgis.Critical)
    
    @pyqtSlot(bool)
    def on_serverPushButton_clicked(self):
        self.viewServers.exec_()

    def serverIsValid(self):
        """
        Checks if connection to server is valid.
        """
        # for files, server check is not necessary
        h = self.viewServers.getDefaultConnectionParameters()[1]
        return self.viewServers.testServer(h)

    def databaseExists(self):
        """
        Checks if database exists.
        """
        # for files, it is only necessary to check if file exists and is not empty.
        if self.abstractDb:
            _, host, port, user, password = self.viewServers.getDefaultConnectionParameters()
            database = self.currentDb()
            return self.abstractDb.testCredentials(host, port, database, user, password)
        return False

    def validate(self):
        """
        Validates current widget. To be validated, it is necessary:
        - a valid datasource selection; and
        - a valid database structure.
        :return: (str) invalidation reason.
        """
        # check a valid server name
        # check if datasource is a valid name and if it already exists into selected server
        if not self.currentDb() or not self.abstractDb:
            return self.tr('Invalid datasource.')
        else:
            # check if the connection is a valid connection
            if not self.serverIsValid():
                return self.tr('Invalid connection to server.')
            # check if it exists
            if not self.databaseExists():
                return self.tr('Database {0} does not exist.').format(self.currentDb())
        # if all tests were positive, widget has a valid selection
        return ''

    def isValid(self):
        """
        Validates selection.
        :return: (bool) validation status.
        """
        return self.validate() == ''
        # msg = self.validate()
        # if msg:
        #     # if an invalidation reason was given, warn user and nothing else.
        #     iface.messageBar().pushMessage(self.tr('Warning!'), msg, level=Qgis.Warning, duration=5)
        # return msg == ''

    @pyqtSlot(bool)
    def on_infoPushButton_clicked(self):
        """
        Exhibits information about selected database.
        """
        contents = self.abstractDb.databaseInfo() if self.abstractDb else []
        DatasourceInfoTable(contents=contents).exec_()
