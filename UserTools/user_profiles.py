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
from PyQt4.QtCore import pyqtSlot
from PyQt4.QtSql import QSqlQuery

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.UserTools.create_profile import CreateProfile
from DsgTools.UserTools.assign_profiles import AssignProfiles
from DsgTools.UserTools.create_user import CreateUser
from DsgTools.UserTools.alter_user_password import AlterUserPassword

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'user_profiles.ui'))

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
        
        #Objects Connections
        QtCore.QObject.connect(self.widget, QtCore.SIGNAL(("connectionChanged()")), self.populateUsers)
        
    def populateUsers(self):
        self.comboBox.clear()
        
        if not self.widget.abstractDb:
            return
        
        ret = self.widget.abstractDb.getUsers()
        
        self.comboBox.addItem(self.tr('Select a User'))
        self.comboBox.addItems(ret)
                
    def getProfiles(self, username):
        self.installedProfiles.clear()
        self.assignedProfiles.clear()

        if self.comboBox.currentIndex() == 0:
            return
        
        if not self.widget.abstractDb:
            return
        
        self.installed, self.assigned = self.widget.abstractDb.getUserRelatedRoles(username)

        self.installedProfiles.addItems(self.installed)
        self.assignedProfiles.addItems(self.assigned)
        
    @pyqtSlot(bool)
    def on_installProfile_clicked(self):
        dlg = AssignProfiles(self.widget.comboBoxPostgis.currentIndex())
        dlg.exec_()
        self.getProfiles(self.comboBox.currentText())        

    @pyqtSlot(bool)
    def on_createUserButton_clicked(self):
        if not self.widget.abstractDb:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('First select a database!'))
            return
        dlg = CreateUser(self.comboBox.currentText(),self.widget.abstractDb)
        dlg.exec_()
        self.populateUsers()
    
    @pyqtSlot(bool)    
    def on_removeUserButton_clicked(self):
        user = self.comboBox.currentText()
        if not self.widget.abstractDb:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('First select a database!'))
            return
        if self.comboBox.currentIndex() == 0:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('First select a user to remove!'))
            return

        try:
            self.widget.abstractDb.removeUser(user)
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), e.args[0])
            self.getProfiles(user)
            return

        self.getProfiles(user)
        QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('User removed successfully!'))
        self.populateUsers()               

    @pyqtSlot(bool)
    def on_alterPasswordButton_clicked(self):
        user = self.comboBox.currentText()
        if not self.widget.abstractDb:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('First select a database!'))
            return
        if self.comboBox.currentIndex() == 0:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('First select a user!'))
            return
        dlg = AlterUserPassword(user, self.widget.abstractDb)
        dlg.exec_()

    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self):
        self.getProfiles(self.comboBox.currentText())
        
    def saveUserState(self):
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
            try:
                self.widget.abstractDb.grantRole(user, role)
            except Exception as e:
                QtGui.QMessageBox.critical(self, self.tr('Critical!'), e.args[0])
                self.getProfiles(user)
                return

        for role in revoke:
            try:
                self.widget.abstractDb.revokeRole(user, role)
            except Exception as e:
                QtGui.QMessageBox.critical(self, self.tr('Critical!'), e.args[0])
                self.getProfiles(user)
                return

        self.getProfiles(user)
        QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('User updated successfully!'))
        
    @pyqtSlot(bool)
    def on_closeButton_clicked(self):
        self.close()
        
    @pyqtSlot(bool)
    def on_insertAllButton_clicked(self):
        tam = self.installedProfiles.__len__()
        for i in range(tam+1,1,-1):
            item = self.installedProfiles.takeItem(i-2)
            self.assignedProfiles.addItem(item)
        self.assignedProfiles.sortItems()
        
        self.saveUserState()

    @pyqtSlot(bool)
    def on_removeAllButton_clicked(self):
        tam = self.assignedProfiles.__len__()
        for i in range(tam+1,1,-1):
            item = self.assignedProfiles.takeItem(i-2)
            self.installedProfiles.addItem(item)
        self.installedProfiles.sortItems()

        self.saveUserState()

    @pyqtSlot(bool)
    def on_insertButton_clicked(self):
        listedItems = self.installedProfiles.selectedItems()
        for i in listedItems:
            item = self.installedProfiles.takeItem(self.installedProfiles.row(i))
            self.assignedProfiles.addItem(item)
        self.assignedProfiles.sortItems()

        self.saveUserState()

    @pyqtSlot(bool)
    def on_removeButton_clicked(self):
        listedItems = self.assignedProfiles.selectedItems()
        for i in listedItems:
            item = self.assignedProfiles.takeItem(self.assignedProfiles.row(i))
            self.installedProfiles.addItem(item)
        self.installedProfiles.sortItems()

        self.saveUserState()