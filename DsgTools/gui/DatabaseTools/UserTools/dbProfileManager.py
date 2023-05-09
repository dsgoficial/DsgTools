# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-12-07
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
from builtins import str
import os

from qgis.core import QgsMessageLog, Qgis

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt
from qgis.PyQt.QtWidgets import (
    QListWidgetItem,
    QMessageBox,
    QMenu,
    QApplication,
    QFileDialog,
)
from qgis.PyQt.QtGui import QCursor


FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "dbProfileManager.ui")
)


class DbProfileManager(QtWidgets.QDialog, FORM_CLASS):
    def __init__(
        self,
        grantedProfileList,
        notGrantedProfileList,
        permissionManager,
        userName,
        dbName,
        edgvVersion,
        parent=None,
    ):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.grantedProfileList = grantedProfileList
        self.notGrantedProfileList = notGrantedProfileList
        self.permissionManager = permissionManager
        self.userName = userName
        self.dbName = dbName
        self.edgvVersion = edgvVersion
        self.profileCustomSelector.setTitle(
            self.tr("Manage permissions to user ")
            + userName
            + self.tr(" on database ")
            + dbName
        )
        self.profileCustomSelector.setFromList(
            list(notGrantedProfileList), unique=True
        )  # passes a copy using list(<list object>)
        self.profileCustomSelector.setToList(list(grantedProfileList))

    @pyqtSlot(bool)
    def on_applyPushButton_clicked(self):
        permissionsToGrant = [
            i
            for i in self.profileCustomSelector.toLs
            if i not in self.grantedProfileList
        ]
        profilesToRevoke = [
            i
            for i in self.profileCustomSelector.fromLs
            if i not in self.notGrantedProfileList
        ]
        # grant operation
        header = self.tr("Grant / Revoke operation complete: ")
        successList = []
        errorDict = dict()
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        for profileName in permissionsToGrant:
            try:
                self.permissionManager.grantPermission(
                    self.dbName, profileName, self.edgvVersion, self.userName
                )  # TODO: add error treatment
                successList.append(profileName)
            except Exception as e:
                errorDict[profileName] = str(e.args[0])
        for profileName in profilesToRevoke:
            try:
                self.permissionManager.revokePermission(
                    self.dbName, profileName, self.userName
                )  # TODO: add error treatment
                successList.append(profileName)
            except Exception as e:
                errorDict[profileName] = ":".join(e.args)
        QApplication.restoreOverrideCursor()
        self.outputMessage(header, successList, errorDict)
        self.close()

    @pyqtSlot(bool)
    def on_cancelPushButton_clicked(self):
        self.close()

    def outputMessage(self, header, successList, exceptionDict):
        msg = header
        if len(successList) > 0:
            msg += self.tr("\nSuccessful profiles: ")
            msg += ", ".join(successList)
        msg += self.logInternalError(exceptionDict)
        QMessageBox.warning(self, self.tr("Operation Complete!"), msg)

    def logInternalError(self, exceptionDict):
        msg = ""
        errorDbList = list(exceptionDict.keys())
        if len(errorDbList) > 0:
            msg += self.tr("\Profiles with error:")
            msg += ", ".join(errorDbList)
            msg += self.tr("\nError messages for each profile were output in qgis log.")
            for errorDb in errorDbList:
                QgsMessageLog.logMessage(
                    self.tr("Error for profile ")
                    + errorDb
                    + ": "
                    + exceptionDict[errorDb],
                    "DSGTools Plugin",
                    Qgis.Critical,
                )
        return msg
