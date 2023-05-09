# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-09-22
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

from qgis.core import QgsMessageLog, Qgis

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt, QSettings
from qgis.PyQt.QtWidgets import (
    QListWidgetItem,
    QMessageBox,
    QMenu,
    QApplication,
    QFileDialog,
)
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery

# DSGTools imports
from DsgTools.gui.DatabaseTools.UserTools.create_user import CreateUser
from DsgTools.gui.DatabaseTools.UserTools.alter_user_password import AlterUserPassword
from DsgTools.gui.DatabaseTools.UserTools.permission_properties import (
    PermissionProperties,
)


FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "manageServerUsers.ui")
)


class ManageServerUsers(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, abstractDb, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.abstractDb = abstractDb
        self.userTypeDict = {True: self.tr("Super User"), False: self.tr("User")}
        self.populateUsers()

    def populateUsers(self):
        self.serverUserTable.clear()
        rootNode = self.serverUserTable.invisibleRootItem()
        if not self.abstractDb:
            return
        ret = []
        try:
            ret = self.abstractDb.getUsersFromServer()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Critical!"), ":".join(e.args))
        for user, type in ret:
            userNameItem = self.createItem(rootNode, user, 0)
            userNameItem.setText(1, self.userTypeDict[type])

    def createItem(self, parent, text, column):
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setText(column, text)
        return item

    @pyqtSlot(bool)
    def on_createUserButton_clicked(self):
        if not self.abstractDb:
            QMessageBox.critical(
                self, self.tr("Critical!"), self.tr("First select a database!")
            )
            return
        dlg = CreateUser(abstractDb=self.abstractDb)
        dlg.exec_()
        self.populateUsers()

    @pyqtSlot(bool)
    def on_removeUserButton_clicked(self):
        selectedUsers = self.serverUserTable.selectedItems()
        if not self.abstractDb:
            QMessageBox.critical(
                self, self.tr("Critical!"), self.tr("First select a database!")
            )
            return
        if len(selectedUsers) == 0:
            QMessageBox.critical(
                self, self.tr("Critical!"), self.tr("First select a user to remove!")
            )
            return
        selectedUserNames = [i.text(0) for i in selectedUsers]
        if (
            QMessageBox.question(
                self,
                self.tr("Question"),
                self.tr("Do you really want to remove users: ")
                + ", ".join(selectedUserNames),
                QMessageBox.Ok | QMessageBox.Cancel,
            )
            == QMessageBox.Cancel
        ):
            return
        exceptionDict = dict()
        successList = []
        for user in selectedUserNames:
            try:
                self.abstractDb.reassignAndDropUser(user)
                successList.append(user)
            except Exception as e:
                exceptionDict[user] = ":".join(e.args)
        header = self.tr("Drop user(s) operation complete!\n")
        self.outputMessage(header, successList, exceptionDict)
        self.populateUsers()

    @pyqtSlot(bool)
    def on_alterPasswordButton_clicked(self):
        selectedUsers = self.serverUserTable.selectedItems()
        selectedUserNames = [i.text(0) for i in selectedUsers]
        if not self.abstractDb:
            QMessageBox.critical(
                self, self.tr("Critical!"), self.tr("First select a database!")
            )
            return
        if len(selectedUsers) == 0:
            QMessageBox.critical(
                self, self.tr("Critical!"), self.tr("First select a user to remove!")
            )
            return
        dlg = AlterUserPassword(userList=selectedUserNames, abstractDb=self.abstractDb)
        dlg.exec_()

    @pyqtSlot(bool)
    def on_closeButton_clicked(self):
        self.done(0)

    def outputMessage(self, header, successList, exceptionDict):
        msg = header
        if len(successList) > 0:
            msg += self.tr("\nSuccessful users: ")
            msg += ", ".join(successList)
        msg += self.logInternalError(exceptionDict)
        QMessageBox.warning(self, self.tr("Operation Complete!"), msg)

    def logInternalError(self, exceptionDict):
        msg = ""
        errorDbList = list(exceptionDict.keys())
        if len(errorDbList) > 0:
            msg += self.tr("\nUsers with error:")
            msg += ", ".join(errorDbList)
            msg += self.tr("\nError messages for each user were output in qgis log.")
            for errorDb in errorDbList:
                QgsMessageLog.logMessage(
                    self.tr("Error for user {user}: {exception}").format(
                        user=errorDb, exception=exceptionDict[errorDb]
                    ),
                    "DSGTools Plugin",
                    Qgis.Critical,
                )
        return msg
