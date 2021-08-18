# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-12-06
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

from qgis.core import QgsMessageLog, Qgis

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt
from qgis.PyQt.QtWidgets import QListWidgetItem, QMessageBox, QMenu, QApplication, QFileDialog
from qgis.PyQt.QtGui import QCursor


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'profileUserManager.ui'))

class ProfileUserManager(QtWidgets.QDialog, FORM_CLASS):
    
    def __init__(self, grantedUserList, notGrantedUserList, permissionManager, profileName, dbName, edgvVersion, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.grantedUserList = grantedUserList
        self.notGrantedUserList = notGrantedUserList
        self.permissionManager = permissionManager
        self.profileName = profileName
        self.dbName = dbName
        self.edgvVersion = edgvVersion
        self.userCustomSelector.setTitle(self.tr('Manage user permissions to profile ') + profileName + self.tr(' on database ') + dbName)
        self.userCustomSelector.setFromList(list(notGrantedUserList), unique = True) #passes a copy using list(<list object>)
        self.userCustomSelector.setToList(list(grantedUserList))
    
    @pyqtSlot(bool)
    def on_applyPushButton_clicked(self):
        usersToGrant = [i for i in self.userCustomSelector.toLs if i not in self.grantedUserList]
        usersToRevoke = [i for i in self.userCustomSelector.fromLs if i not in self.notGrantedUserList]
        #grant operation
        header = self.tr('Grant / Revoke operation complete: ')
        successList = []
        errorDict = dict()
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        for userName in usersToGrant:
            try:
                self.permissionManager.grantPermission(self.dbName, self.profileName, self.edgvVersion, userName)
                successList.append(userName)
            except Exception as e:
                errorDict[userName] = ':'.join(e.args)
        for userName in usersToRevoke:
            try:
                self.permissionManager.revokePermission(self.dbName, self.profileName, userName)
                successList.append(userName)
            except Exception as e:
                errorDict[userName] = ':'.join(e.args)
        QApplication.restoreOverrideCursor()
        self.outputMessage(header, successList, errorDict)
        self.close()
    
    @pyqtSlot(bool)
    def on_cancelPushButton_clicked(self):
        self.close()    
    
    def outputMessage(self, header, successList, exceptionDict):
        msg = header
        if len(successList) > 0:
            msg += self.tr('\nSuccessful users: ')
            msg +=', '.join(successList)
        msg += self.logInternalError(exceptionDict)
        QMessageBox.warning(self, self.tr('Operation Complete!'), msg)
    
    def logInternalError(self, exceptionDict):
        msg = ''
        errorDbList = list(exceptionDict.keys())
        if len(errorDbList)> 0:
            msg += self.tr('\nUsers with error:')
            msg+= ', '.join(errorDbList)
            msg+= self.tr('\nError messages for each user were output in qgis log.')
            for errorDb in errorDbList:
                QgsMessageLog.logMessage(self.tr('Error for user ')+ errorDb + ': ' +exceptionDict[errorDb], "DSGTools Plugin", Qgis.Critical)
        return msg 