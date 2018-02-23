# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-07-16
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from os.path import expanduser

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, Qt, QSettings, pyqtSignal
from PyQt4.QtGui import QListWidgetItem, QMessageBox, QMenu, QApplication, QCursor, QFileDialog
from PyQt4.QtSql import QSqlDatabase,QSqlQuery

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.ServerTools.viewServers import ViewServers
from DsgTools.Factories.DbFactory.dbFactory import DbFactory

from DsgTools.UserTools.profile_editor import ProfileEditor
from DsgTools.ServerTools.createView import CreateView
from DsgTools.ServerTools.manageDBAuxiliarStructure import ManageDBAuxiliarStructure
from DsgTools.ServerTools.selectStyles import SelectStyles

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'options.ui'))

class Options(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot(bool)
    def on_addPushButton_clicked(self):
        newValue = self.addParameterLineEdit.text()
        valueList = [self.blackListWidget.itemAt(i,0).text() for i in range(self.blackListView.count())]
        if newValue == '':
            QMessageBox.warning(self, self.tr('Fill in a value before adding!'))
            return
        if newValue in valueList:
            QMessageBox.warning(self, self.tr('Value already in black list!'))
            return
        self.blackListWidget.addItem(newValue)
        self.blackListView.sortItems(order = Qt.AscendingOrder)
    
    def validateParameters(self):
        if self.geogigPathLineEdit.text() == '':
            return False
        if self.serverIPLineEdit.text() == '':
            return False
        if self.portLineEdit.text() == '':
            return False
        if self.userLineEdit.text() == '':
            return False
        if self.passwordLineEdit.text() == '':
            return False
        if self.schemaLineEdit.text() == '':
            return False
        if self.repositoryNameLineEdit.text() == '':
            return False
        if self.localDbNameLineEdit.text() == '':
            return False
        if self.branchNameLineEdit.text() == '':
            return False
        return True

    def invalidatedReason(self):
        msg = ''
        if self.geogigPathLineEdit.text() == '':
            msg += self.tr('Enter Geogig path!\n')
        if self.serverIPLineEdit.text() == '':
            msg += self.tr('Enter server IP!\n')
        if self.portLineEdit.text() == '':
            msg += self.tr('Enter server port!\n')
        if self.userLineEdit.text() == '':
            msg += self.tr('Enter server user!\n')
        if self.passwordLineEdit.text() == '':
            msg += self.tr('Enter server password!\n')
        if self.schemaLineEdit.text() == '':
            msg += self.tr('Enter server schema!\n')
        if self.repositoryNameLineEdit.text() == '':
            msg += self.tr('Enter repository name!\n')
        if self.localDbNameLineEdit.text() == '':
            msg += self.tr('Enter database name!\n')
        if self.branchNameLineEdit.text() == '':
            msg += self.tr('Enter a branch name!\n')
        return msg
    
    def getParameters(self):
        geogigPath = self.geogigPathLineEdit.text()
        serverIP =  self.serverIPLineEdit.text()
        port = self.portLineEdit.text()
        user = self.userLineEdit.text()
        password = self.passwordLineEdit.text()
        schema = self.schemaLineEdit.text()
        repo = self.repositoryNameLineEdit.text()
        dbName = self.localDbNameLineEdit.text()
        branchName = self.branchNameLineEdit.text()
        return (geogigPath, serverIP, port, user, password, schema, repo, dbName, branchName)

    def loadParametersFromConfig(self):
        settings = QSettings()
        settings.beginGroup('Geogig_PG')
        geogigPath = settings.value('geogigPath')
        serverIP = settings.value('serverIP')
        port = settings.value('port')
        user = settings.value('username')
        password = settings.value('password')
        schema = settings.value('schema')
        repo = settings.value('repo')
        dbName = settings.value('dbName')
        branchName = settings.value('branchName')
        settings.endGroup()
        return (geogigPath, serverIP, port, user, password, schema, repo, dbName, branchName)
    
    def setInterfaceWithParametersFromConfig(self):
        (geogigPath, serverIP, port, user, password, schema, repo, dbName, branchName) = self.loadParametersFromConfig()
        if geogigPath != '':
            self.geogigPathLineEdit.setText(geogigPath)
        if serverIP != '':
            self.serverIPLineEdit.setText(serverIP)
        if port != '':
            self.portLineEdit.setText(port)
        if user != '':
            self.userLineEdit.setText(user)
        if password != '':
            self.passwordLineEdit.setText(password)
        if schema != '':
            self.schemaLineEdit.setText(schema)
        if repo != '':
            self.repoLineEdit.setText(repo)
        if dbName != '':
            self.dbNameLineEdit.setText(dbName)
        if branchName != '':
            self.branchNameLineEdit.setText(branchName)
    
    def storeParametersInConfig(self):
        (geogigPath, serverIP, port, user, password, schema, repo, dbName, branchName) = self.getParameters()
        settings = QSettings()
        settings.beginGroup('Geogig_PG')
        settings.setValue('geogigPath', geogigPath)
        settings.setValue('serverIP', serverIP)
        settings.setValue('port', port)
        settings.setValue('user', user)
        settings.setValue('password', password)
        settings.setValue('schema', schema)
        settings.setValue('repo', repo)
        settings.setValue('dbName', dbName)
        settings.setValue('branchName', branchName)
        settings.endGroup()
    
    @pyqtSlot(bool)
    def on_okPushButton_clicked(self):
        if not self.validateParameters():
            msg = self.invalidatedReason()
            QMessageBox.warning(self, msg)
            return
        self.storeParametersInConfig()
        self.done(1)
        self.close