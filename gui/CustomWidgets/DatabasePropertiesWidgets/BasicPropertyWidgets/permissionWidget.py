# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-12-01
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
from builtins import range
import os

from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, Qt
from qgis.PyQt.QtWidgets import QTreeWidgetItem, QMessageBox, QMenu, QApplication, QFileDialog
from qgis.PyQt.QtGui import QCursor

from qgis.core import QgsMessageLog

from DsgTools.core.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.gui.DatabaseTools.UserTools.permission_properties import PermissionProperties
from DsgTools.gui.DatabaseTools.UserTools.manageServerUsers import ManageServerUsers
from DsgTools.gui.DatabaseTools.UserTools.PermissionManagerWizard.permissionWizard import PermissionWizard
from DsgTools.gui.DatabaseTools.UserTools.profileUserManager import ProfileUserManager
from DsgTools.gui.DatabaseTools.UserTools.dbProfileManager import DbProfileManager
from DsgTools.core.ServerManagementTools.permissionManager import PermissionManager
from DsgTools.gui.DatabaseTools.UserTools.serverProfilesManager import ServerProfilesManager


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'permissionWidget.ui'))

class PermissionWidget(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.serverAbstractDb = None
        self.dbDict = dict()
        self.permissionManager = None
        self.permissionTreeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.permissionTreeWidget.customContextMenuRequested.connect(self.createMenuAssigned)

    # @pyqtSlot(bool, name='on_manageProfilesPushButton_clicked')
    @pyqtSlot(bool, name='on_databasePerspectivePushButton_clicked')
    @pyqtSlot(bool, name='on_userPerspectivePushButton_clicked')
    def refresh(self):
        """
        Refreshes permission table according to selected view type.
        """
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        viewType = self.getViewType()
        self.permissionTreeWidget.clear()
        if viewType == 'database':
            self.populateWithDatabasePerspective()
        if viewType == 'user':
            self.populateWithUserPerspective()
        QApplication.restoreOverrideCursor()
    
    def populateWithDatabasePerspective(self):
        self.permissionTreeWidget.setHeaderLabels([self.tr('Database'), self.tr('Permission'), self.tr('User')])
        dbPerspectiveDict = self.permissionManager.getDatabasePerspectiveDict()
        rootNode = self.permissionTreeWidget.invisibleRootItem()
        for dbName in list(dbPerspectiveDict.keys()):
            parentDbItem = self.createItem(rootNode, dbName, 0)
            for permission in list(dbPerspectiveDict[dbName].keys()):
                dbItem = self.createItem(parentDbItem, permission, 1)
                for user in dbPerspectiveDict[dbName][permission]:
                    userItem = self.createItem(dbItem, user, 2)
        self.permissionTreeWidget.sortItems(0, Qt.AscendingOrder)
        self.permissionTreeWidget.expandAll()

    def populateWithUserPerspective(self):
        self.permissionTreeWidget.setHeaderLabels([self.tr('User'), self.tr('Database'), self.tr('Permission')])
        userPerspectiveDict = self.permissionManager.getUserPerspectiveDict()
        rootNode = self.permissionTreeWidget.invisibleRootItem()
        for userName in list(userPerspectiveDict.keys()):
            parentUserItem = self.createItem(rootNode, userName, 0)
            for dbName in list(userPerspectiveDict[userName].keys()):
                dbItem = self.createItem(parentUserItem, dbName, 1)
                for permission in userPerspectiveDict[userName][dbName]:
                    permissionItem = self.createItem(dbItem, permission, 2)
        self.permissionTreeWidget.sortItems(0, Qt.AscendingOrder)
        self.permissionTreeWidget.expandAll()
    
    def createItem(self, parent, text, column):
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setText(column, text)
        return item
    
    def getViewType(self):
        if self.databasePerspectivePushButton.isChecked():
            return 'database'
        else:
            return 'user'
    
    def setParameters(self, serverAbstractDb, dbDict, edgvVersion):
        self.serverAbstractDb = serverAbstractDb
        self.dbDict = dbDict
        self.permissionManager = PermissionManager(self.serverAbstractDb, self.dbDict, edgvVersion)
        self.refresh()

    @pyqtSlot(bool)
    def on_manageUsersPushButton_clicked(self):
        try:
            dlg = ManageServerUsers(self.serverAbstractDb)
            dlg.exec_()
        except:
            QMessageBox.warning(self, self.tr('Error!'), self.tr('Select a server!'))
        self.refresh()
    
    @pyqtSlot(bool)
    def on_manageProfilesPushButton_clicked(self):
        try:
            dlg = ServerProfilesManager(self.permissionManager)
            # dlg.profilesChanged.connect(self.refresh)
            dlg.exec_()
        except Exception as e:
            QMessageBox.warning(self, self.tr('Error!'), ':'.join(e.args))
        self.refresh()
    
    def createMenuAssigned(self, position):
        """
        Creates a pop up menu
        """
        viewType = self.getViewType()
        if viewType == 'database':
            self.createDbPerspectiveContextMenu(position)
        if viewType == 'user':
            self.createUserPerspectiveContextMenu(position)
        
    
    def createDbPerspectiveContextMenu(self, position):
        menu = QMenu()
        item = self.permissionTreeWidget.itemAt(position)
        if item:
            if item.text(0) != '':
                menu.addAction(self.tr('Revoke all permissions'), self.revokeAll)
            elif item.text(1) != '':
                menu.addAction(self.tr('Manage User Permissions'), self.manageUserPermissions)
            elif item.text(2) != '':
                menu.addAction(self.tr('Revoke User'), self.revokeSelectedUser)
        menu.exec_(self.permissionTreeWidget.viewport().mapToGlobal(position))
    
    def createUserPerspectiveContextMenu(self, position):
        menu = QMenu()
        item = self.permissionTreeWidget.itemAt(position)
        if item:
            if item.text(0) != '':
                menu.addAction(self.tr('Revoke permissions on all granted databases'), self.revokeAllDbs)
            elif item.text(1) != '':
                menu.addAction(self.tr('Manage Permissions on database'), self.managePermissionsOnDb)
            elif item.text(2) != '':
                menu.addAction(self.tr('Revoke Permission'), self.revokeSelectedPermission)
        menu.exec_(self.permissionTreeWidget.viewport().mapToGlobal(position))
    
    def manageUserPermissions(self):
        currItem = self.permissionTreeWidget.currentItem()
        profileName = currItem.text(1)
        dbName = currItem.parent().text(0)
        childCount = currItem.childCount()
        grantedUserList = []
        for i in range(childCount):
            grantedUserList.append(currItem.child(i).text(2))
        userList = self.serverAbstractDb.getUsersFromServer()
        notGrantedUserList = [i[0] for i in userList if i[0] not in grantedUserList]
        edgvVersion = self.dbDict[dbName].getDatabaseVersion()
        try:
            dlg = ProfileUserManager(grantedUserList, notGrantedUserList, self.permissionManager, profileName, dbName, edgvVersion)
            dlg.exec_()
        except:
            pass
        self.refresh()
    
    def revokeSelectedUser(self):
        userName = self.permissionTreeWidget.currentItem().text(2)
        permissionName = self.permissionTreeWidget.currentItem().parent().text(1)
        dbName = self.permissionTreeWidget.currentItem().parent().parent().text(0)
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.permissionManager.revokePermission(dbName, permissionName, userName)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Revoke Complete!'), self.tr('Revoke for user ') + userName + self.tr(' on profile ') + permissionName + self.tr(' of database ') + dbName + self.tr(' complete.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Error!'), ':'.join(e.args))
        self.refresh()

    def revokeAll(self):
        currItem = self.permissionTreeWidget.currentItem()
        dbName = currItem.text(0)
        dbChildCount = currItem.childCount()
        for i in range(dbChildCount):
            permissionNode = currItem.child(i)
            permissionName = permissionNode.text(1)
            userCount = permissionNode.childCount()
            for j in range(userCount):
                userName = permissionNode.child(j).text(2)
                self.permissionManager.revokePermission(dbName, permissionName, userName)
        self.refresh()
    
    def revokeAllDbs(self):
        currItem = self.permissionTreeWidget.currentItem()
        userName = currItem.text(0)
        userChildCount = currItem.childCount()
        for i in range(userChildCount):
            dbNode = currItem.child(i)
            dbName = dbNode.text(1)
            permissionCount = dbNode.childCount()
            for j in range(permissionCount):
                permissionName = dbNode.child(j).text(2)
                self.permissionManager.revokePermission(dbName, permissionName, userName)
        self.refresh()
    
    def managePermissionsOnDb(self):
        currItem = self.permissionTreeWidget.currentItem()
        dbName = currItem.text(1)
        userName = currItem.parent().text(0)
        childCount = currItem.childCount()
        grantedProfileList = []
        for i in range(childCount):
            grantedProfileList.append(currItem.child(i).text(2))
        profileDict = self.permissionManager.getSettings()
        edgvVersion = self.dbDict[dbName].getDatabaseVersion()
        notGrantedProfileList = [i for i in profileDict[edgvVersion] if i not in grantedProfileList]
        try:
            dlg = DbProfileManager(grantedProfileList, notGrantedProfileList, self.permissionManager, userName, dbName, edgvVersion)
            dlg.exec_()
        except:
            pass
        self.refresh()
    
    def revokeSelectedPermission(self):
        permissionName = self.permissionTreeWidget.currentItem().text(2)
        dbName = self.permissionTreeWidget.currentItem().parent().text(1)
        userName = self.permissionTreeWidget.currentItem().parent().parent().text(0)
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.permissionManager.revokePermission(dbName, permissionName, userName)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Revoke Complete!'), self.tr('Revoke for user ') + userName + self.tr(' on profile ') + permissionName + self.tr(' of database ') + dbName + self.tr(' complete.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Error!'), ':'.join(e.args))
        self.refresh()

    @pyqtSlot(bool)
    def on_importPushButton_clicked(self):
        fd = QFileDialog()
        filename = fd.getOpenFileName(caption=self.tr('Select a dsgtools profile'),filter=self.tr('json file (*.json)'))
        filename = filename[0] if isinstance(filename, tuple) else filename
        if filename == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Select a file to import!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.permissionManager.importSetting(filename)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Permission successfully imported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem importing permission: ') + ':'.join(e.args))
        # self.refreshProfileList()
    
    @pyqtSlot(bool)
    def on_exportPushButton_clicked(self):
        if not self.permissionTreeWidget.currentItem() or (self.permissionTreeWidget.currentItem().text(0) != '' or self.permissionTreeWidget.currentItem().text(2) != ''):
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Select a profile to export!'))
            return

        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption = self.tr('Select a folder to output'))
        if folder == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Select a output!'))
            return
        profileName = self.permissionTreeWidget.currentItem().text(1)
        dbName = self.permissionTreeWidget.currentItem().parent().text(0)
        edgvVersion = self.dbDict[dbName].getDatabaseVersion()
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.permissionManager.exportSetting(profileName, edgvVersion, folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Permission successfully exported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem exporting permission: ') + ':'.join(e.args))
        
    @pyqtSlot(bool)
    def on_batchExportPushButton_clicked(self):
        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption = self.tr('Select a folder to output'))
        if folder == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Select a output!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.permissionManager.batchExportSettings(folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Permissions successfully exported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem exporting permission: ') + ':'.join(e.args))
    
    @pyqtSlot(bool)
    def on_batchImportPushButton_clicked(self):
        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption = self.tr('Select a folder with permissions: '))
        if folder == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Select a input folder!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.permissionManager.batchImportSettings(folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Permissions successfully imported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem importing permission: ') + ':'.join(e.args))
