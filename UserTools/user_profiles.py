# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-09-14
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

# Qt imports
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtSql import QSqlDatabase, QSqlQuery

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.UserTools.create_profile import CreateProfile

import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'user_profiles.ui'))

from DsgTools.UserTools.assign_profiles import AssignProfiles

class ManageUserProfiles(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(ManageUserProfiles, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.widget.tabWidget.setTabEnabled(0, False)
        
        self.factory = SqlGeneratorFactory()
        self.gen = self.factory.createSqlGenerator(False)
        self.utils = Utils()
        
        #Objects Connections
        QtCore.QObject.connect(self.widget, QtCore.SIGNAL(("connectionChanged()")), self.populateUsers)
        
    def populateUsers(self):
        self.comboBox.clear()
        
        if not self.widget.db:
            return
        
        ret = []
        
        sql = self.gen.getUsers()
        query = QSqlQuery(sql, self.widget.db)

        while query.next():
            ret.append(query.value(0))
            
        ret.sort()
        self.comboBox.addItem(self.tr('Select a User'))
        self.comboBox.addItems(ret)
                
    def getProfiles(self, username):
        self.installedProfiles.clear()
        self.assignedProfiles.clear()

        if self.comboBox.currentIndex() == 0:
            return
        
        if not self.widget.db:
            return
        
        self.installed = []
        self.assigned = []

        sql = self.gen.getUserRelatedRoles(username)
        query = QSqlQuery(sql, self.widget.db)

        while query.next():
            rolname = query.value(0)
            usename = query.value(1)
            if not usename:
                self.installed.append(rolname)
            else:
                self.assigned.append(rolname)

        self.installed.sort()
        self.assigned.sort()
        self.installedProfiles.addItems(self.installed)
        self.assignedProfiles.addItems(self.assigned)
        
    @pyqtSlot(bool)
    def on_assignProfile_clicked(self):
        dlg = AssignProfiles(self.widget.comboBoxPostgis.currentIndex())
        dlg.exec_()
        self.getProfiles(self.comboBox.currentText())        
        
    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self):
        self.getProfiles(self.comboBox.currentText())
        
    @pyqtSlot(bool)
    def on_saveButton_clicked(self):
        if self.comboBox.currentIndex() == 0:
            return

        user = self.comboBox.currentText()
        grant = []
        revoke = []
        profiles1 = []
        for i in range(self.assignedProfiles.__len__()):
            role = self.assignedProfiles.item(i).text()
            profiles1.append(role)
            
        for role in profiles1:
            if role not in self.assigned:
                grant.append(role)

        profiles2 = []
        for i in range(self.installedProfiles.__len__()):
            role = self.installedProfiles.item(i).text()
            profiles2.append(role)
            
        for role in profiles2:
            if role not in self.installed:
                revoke.append(role)
            
        for role in grant:
            sql = self.gen.grantRole(user, role)
            query = QSqlQuery(self.widget.db)

            if not query.exec_(sql):
                QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Problem granting profile: ') +role+'\n'+query.lastError().text())
                self.getProfiles(user)
                return

        for role in revoke:
            sql = self.gen.revokeRole(user, role)
            query = QSqlQuery(self.widget.db)

            if not query.exec_(sql):
                QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Problem revoking profile: ') +role+'\n'+query.lastError().text())
                self.getProfiles(user)
                return
                
        self.getProfiles(user)
        
        QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('User updated successfully!'))
        
    @pyqtSlot(bool)
    def on_cancelButton_clicked(self):
        self.close()
        
    @pyqtSlot(bool)
    def on_insertAllButton_clicked(self):
        tam = self.installedProfiles.__len__()
        for i in range(tam+1,1,-1):
            item = self.installedProfiles.takeItem(i-2)
            self.assignedProfiles.addItem(item)
        self.assignedProfiles.sortItems()

    @pyqtSlot(bool)
    def on_removeAllButton_clicked(self):
        tam = self.assignedProfiles.__len__()
        for i in range(tam+1,1,-1):
            item = self.assignedProfiles.takeItem(i-2)
            self.installedProfiles.addItem(item)
        self.installedProfiles.sortItems()

    @pyqtSlot(bool)
    def on_insertButton_clicked(self):
        listedItems = self.installedProfiles.selectedItems()
        for i in listedItems:
            item = self.installedProfiles.takeItem(self.installedProfiles.row(i))
            self.assignedProfiles.addItem(item)
        self.assignedProfiles.sortItems()

    @pyqtSlot(bool)
    def on_removeButton_clicked(self):
        listedItems = self.assignedProfiles.selectedItems()
        for i in listedItems:
            item = self.assignedProfiles.takeItem(self.assignedProfiles.row(i))
            self.installedProfiles.addItem(item)
        self.installedProfiles.sortItems()
        