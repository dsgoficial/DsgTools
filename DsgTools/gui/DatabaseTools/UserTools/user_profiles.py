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
from builtins import range
import os

# Qt imports
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, Qt
from qgis.PyQt.QtSql import QSqlQuery
from qgis.PyQt.QtWidgets import QMenu, QMessageBox

# DSGTools imports
from DsgTools.core.Utils.utils import Utils
from DsgTools.core.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.gui.DatabaseTools.UserTools.create_profile import CreateProfile
from DsgTools.gui.DatabaseTools.UserTools.assign_profiles import AssignProfiles
from DsgTools.gui.DatabaseTools.UserTools.create_user import CreateUser
from DsgTools.gui.DatabaseTools.UserTools.alter_user_password import AlterUserPassword
from DsgTools.gui.DatabaseTools.UserTools.permission_properties import (
    PermissionProperties,
)

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "user_profiles.ui")
)


class ManageUserProfiles(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """
        Constructor
        """
        super(ManageUserProfiles, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.widget.tabWidget.setTabEnabled(1, False)
        self.widget.serverWidget.superNeeded = True
        # Objects Connections
        QtCore.QObject.connect(
            self.widget, QtCore.SIGNAL(("connectionChanged()")), self.populateUsers
        )

        self.installedProfiles.setContextMenuPolicy(Qt.CustomContextMenu)
        self.installedProfiles.customContextMenuRequested.connect(
            self.createMenuInstalled
        )
        self.assignedProfiles.setContextMenuPolicy(Qt.CustomContextMenu)
        self.assignedProfiles.customContextMenuRequested.connect(
            self.createMenuAssigned
        )

    def createMenuInstalled(self, position):
        """
        Creates a pop up menu to show permission properties
        """
        menu = QMenu()

        item = self.installedProfiles.itemAt(position)

        if item:
            menu.addAction(self.tr("Show properties"), self.showInstalledProperties)

        menu.exec_(self.installedProfiles.viewport().mapToGlobal(position))

    def showInstalledProperties(self):
        """
        Shows the installed permission's properties dialog
        """
        listedItems = self.installedProfiles.selectedItems()
        permission = listedItems[0].text()
        dbname = self.widget.abstractDb.getDatabaseName()

        permissionsDict = dict()
        try:
            permissionsDict = self.widget.abstractDb.getRolePrivileges(
                permission, dbname
            )
        except Exception as e:
            QMessageBox.critical(self, self.tr("Critical!"), ":".join(e.args))

        dlg = PermissionProperties(permissionsDict)
        dlg.exec_()

    def createMenuAssigned(self, position):
        """
        Creates a pop up menu to show properties of a permission assigned to a user
        """
        menu = QMenu()

        item = self.assignedProfiles.itemAt(position)

        if item:
            menu.addAction(self.tr("Show properties"), self.showAssignedProperties)

        menu.exec_(self.assignedProfiles.viewport().mapToGlobal(position))

    def showAssignedProperties(self):
        """
        Shows the assigned properties dialog
        """
        listedItems = self.assignedProfiles.selectedItems()
        permission = listedItems[0].text()
        dbname = self.widget.abstractDb.getDatabaseName()

        permissionsDict = dict()
        try:
            permissionsDict = self.widget.abstractDb.getRolePrivileges(
                permission, dbname
            )
        except Exception as e:
            QMessageBox.critical(self, self.tr("Critical!"), ":".join(e.args))

        dlg = PermissionProperties(permissionsDict)
        dlg.exec_()

    def populateUsers(self):
        """
        Populates postgresql users list
        """
        self.comboBox.clear()

        if not self.widget.abstractDb:
            return

        ret = []
        try:
            ret = self.widget.abstractDb.getUsers()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Critical!"), ":".join(e.args))

        self.comboBox.addItem(self.tr("Select a User"))
        self.comboBox.addItems(ret)

    def getProfiles(self, username):
        """
        Gets the installed and assigned profiles related to a user
        user: user name
        """
        self.installedProfiles.clear()
        self.assignedProfiles.clear()

        if self.comboBox.currentIndex() == 0:
            return

        if not self.widget.abstractDb:
            return

        self.installed, self.assigned = [], []
        try:
            self.installed, self.assigned = self.widget.abstractDb.getUserRelatedRoles(
                username
            )
        except Exception as e:
            QMessageBox.critical(self, self.tr("Critical!"), ":".join(e.args))

        self.installedProfiles.addItems(self.installed)
        self.assignedProfiles.addItems(self.assigned)

    @pyqtSlot(bool)
    def on_installProfile_clicked(self):
        """
        Slot to install profile
        """
        dlg = AssignProfiles(
            self.widget.serverWidget.serversCombo.currentIndex(),
            self.widget.comboBoxPostgis.currentIndex(),
        )
        dlg.exec_()
        self.getProfiles(self.comboBox.currentText())

    @pyqtSlot(bool)
    def on_createUserButton_clicked(self):
        """
        Slot to open create user dialog
        """
        if not self.widget.abstractDb:
            QMessageBox.critical(
                self, self.tr("Critical!"), self.tr("First select a database!")
            )
            return
        dlg = CreateUser(self.comboBox.currentText(), self.widget.abstractDb)
        dlg.exec_()
        self.populateUsers()

    @pyqtSlot(bool)
    def on_removeUserButton_clicked(self):
        """
        Slot to remove user
        """
        user = self.comboBox.currentText()
        if not self.widget.abstractDb:
            QMessageBox.critical(
                self, self.tr("Critical!"), self.tr("First select a database!")
            )
            return
        if self.comboBox.currentIndex() == 0:
            QMessageBox.critical(
                self, self.tr("Critical!"), self.tr("First select a user to remove!")
            )
            return

        try:
            self.widget.abstractDb.removeUser(user)
        except Exception as e:
            QMessageBox.critical(self, self.tr("Critical!"), ":".join(e.args))
            self.getProfiles(user)
            return

        self.getProfiles(user)
        QMessageBox.warning(
            self, self.tr("Warning!"), self.tr("User removed successfully!")
        )
        self.populateUsers()

    @pyqtSlot(bool)
    def on_alterPasswordButton_clicked(self):
        """
        Slot to alter user password
        """
        user = self.comboBox.currentText()
        if not self.widget.abstractDb:
            QMessageBox.critical(
                self, self.tr("Critical!"), self.tr("First select a database!")
            )
            return
        if self.comboBox.currentIndex() == 0:
            QMessageBox.critical(
                self, self.tr("Critical!"), self.tr("First select a user!")
            )
            return
        dlg = AlterUserPassword(user, self.widget.abstractDb)
        dlg.exec_()

    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self):
        """
        Slot to update assigned and installed profiles
        """
        self.getProfiles(self.comboBox.currentText())

    def saveUserState(self):
        """
        Saves the user state.
        The assigned and installed profiles are updated for the current selected user
        """
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
                QMessageBox.critical(self, self.tr("Critical!"), e.args[0])
                self.getProfiles(user)
                return

        for role in revoke:
            try:
                self.widget.abstractDb.revokeRole(user, role)
            except Exception as e:
                QMessageBox.critical(self, self.tr("Critical!"), ":".join(e.args))
                self.getProfiles(user)
                return

        self.getProfiles(user)
        QMessageBox.warning(
            self, self.tr("Warning!"), self.tr("User updated successfully!")
        )

    @pyqtSlot(bool)
    def on_closeButton_clicked(self):
        """
        Closes the dialog
        """
        self.close()

    @pyqtSlot(bool)
    def on_insertAllButton_clicked(self):
        """
        Slot to assign all profiles
        """
        tam = self.installedProfiles.__len__()
        if tam == 0:
            QMessageBox.warning(
                self,
                self.tr("Warning!"),
                self.tr("No profiles installed! Install at least one and try again."),
            )
            return

        for i in range(tam + 1, 1, -1):
            item = self.installedProfiles.takeItem(i - 2)
            self.assignedProfiles.addItem(item)
        self.assignedProfiles.sortItems()

        self.saveUserState()

    @pyqtSlot(bool)
    def on_removeAllButton_clicked(self):
        """
        Slot to remove all assigned profiles
        """
        tam = self.assignedProfiles.__len__()
        if tam == 0:
            QMessageBox.warning(
                self,
                self.tr("Warning!"),
                self.tr("No profiles assigned! Assign at least one and try again."),
            )
            return

        for i in range(tam + 1, 1, -1):
            item = self.assignedProfiles.takeItem(i - 2)
            self.installedProfiles.addItem(item)
        self.installedProfiles.sortItems()

        self.saveUserState()

    @pyqtSlot(bool)
    def on_insertButton_clicked(self):
        """
        Slot to assign a profile
        """
        listedItems = self.installedProfiles.selectedItems()
        if len(listedItems) == 0:
            QMessageBox.warning(
                self, self.tr("Warning!"), self.tr("Select a profile first!")
            )
            return

        for i in listedItems:
            item = self.installedProfiles.takeItem(self.installedProfiles.row(i))
            self.assignedProfiles.addItem(item)
        self.assignedProfiles.sortItems()

        self.saveUserState()

    @pyqtSlot(bool)
    def on_removeButton_clicked(self):
        """
        Slot to remove a assigned profile
        """
        listedItems = self.assignedProfiles.selectedItems()
        if len(listedItems) == 0:
            QMessageBox.warning(
                self, self.tr("Warning!"), self.tr("Select a profile first!")
            )
            return

        for i in listedItems:
            item = self.assignedProfiles.takeItem(self.assignedProfiles.row(i))
            self.installedProfiles.addItem(item)
        self.installedProfiles.sortItems()

        self.saveUserState()
