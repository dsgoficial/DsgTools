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
import os
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from qgis.PyQt.QtSql import QSqlDatabase
from qgis.PyQt.QtWidgets import QApplication, QMessageBox
from qgis.PyQt.QtGui import QCursor

from qgis.core import QgsMessageLog

from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.dsgCustomComboBox import DsgCustomComboBox
from DsgTools.gui.ServerTools.viewServers import ViewServers
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.Factories.DbFactory.abstractDb import AbstractDb

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
    
    def loadServerAbstractDb(self):
        """
        Checks if there is a default db in self.viewServers . If there isn't one, disables connection combo
        """
        if self.viewServers.defaultConnectionDict == dict():
            self.connectionSelectorComboBox.setEnabled(False)
        else:
            self.connectionSelectorComboBox.setEnabled(True)
            (host, port, user, password) = self.viewServers.getDefaultConnectionParameters()
            serverAbstractDb = self.abstractDbFactory.createDbFactory('QPSQL')
            serverAbstractDb.connectDatabaseWithParameters(host, port, 'postgres', user, password)
            self.setServerDb(serverAbstractDb)

    
    def closeDatabase(self):
        try:
            self.abstractDb.db.close()
            del self.abstractDb
            self.abstractDb = None
        except:
            self.abstractDb = None

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
                self.abstractDb = None
                return
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
        if self.currentIndex() == 0:
            return None
        else:
            return self.currentText().split(' (')[0]
    
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
                    self.abstractDb = self.abstractDbFactory.createDbFactory('QPSQL')
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