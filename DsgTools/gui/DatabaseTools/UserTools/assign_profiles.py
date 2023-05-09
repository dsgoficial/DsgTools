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

# PyQt imports
from qgis.PyQt.QtWidgets import QApplication
from qgis.PyQt.QtGui import QCursor

# Qt imports
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, Qt

# DSGTools imports
from DsgTools.gui.DatabaseTools.UserTools.profile_editor import ProfileEditor

import json

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "assign_profiles.ui")
)


class AssignProfiles(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, serverIndex=None, index=None, parent=None):
        """
        Constructor
        """
        super(AssignProfiles, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.widget.tabWidget.setTabEnabled(1, False)
        if index and serverIndex:
            self.widget.serverWidget.serversCombo.setCurrentIndex(serverIndex)
            self.widget.comboBoxPostgis.setCurrentIndex(index)
        self.widget.serverWidget.superNeeded = True
        self.folder = os.path.join(os.path.dirname(__file__), "profiles")
        self.getModelProfiles()
        self.getInstalledProfiles()

        # Objects Connections
        QtCore.QObject.connect(
            self.widget,
            QtCore.SIGNAL(("connectionChanged()")),
            self.getInstalledProfiles,
        )

    def parseJson(self, filename):
        """
        Parses the profile file and creates a dictionary
        """
        try:
            file = open(filename, "r")
            data = file.read()
            profileDict = json.loads(data)
            file.close()
            return profileDict
        except:
            return None

    def getModelProfiles(self):
        """
        Scans the profile folder for files and make a list with them
        """
        self.possibleProfiles.clear()

        ret = []
        for root, dirs, files in os.walk(self.folder):
            for file in files:
                ext = file.split(".")[-1]
                if ext == "json":
                    ret.append(file.split(".")[0])

        ret.sort()
        self.possibleProfiles.addItems(ret)

    def getInstalledProfiles(self):
        """
        Gets the installed profiles from a database
        """
        self.assignedProfiles.clear()

        if not self.widget.abstractDb:
            return

        ret = []
        try:
            ret = self.widget.abstractDb.getRoles()
        except Exception as e:
            QMessageBox.critical(self, self.tr("Critical!"), ":".join(e.args))

        self.assignedProfiles.addItems(ret)

    @pyqtSlot(bool)
    def on_installButton_clicked(self):
        """
        Installs the selected profiles into the database selected
        """
        if len(self.possibleProfiles.selectedItems()) == 0:
            QMessageBox.warning(
                self,
                self.tr("Warning!"),
                self.tr("Select at least one profile and try again!"),
            )
            return

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        for item in self.possibleProfiles.selectedItems():
            role = item.text()
            profile = os.path.join(self.folder, role + ".json")
            dict = self.parseJson(profile)

            try:
                self.widget.abstractDb.createRole(role, dict)
            except Exception as e:
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self, self.tr("Critical!"), ":".join(e.args))
                return

        QApplication.restoreOverrideCursor()
        QMessageBox.warning(
            self, self.tr("Warning!"), self.tr("Profiles assigned successfully!")
        )

        self.getInstalledProfiles()

    @pyqtSlot(bool)
    def on_closeButton_clicked(self):
        """
        Closes the dialog
        """
        self.close()

    @pyqtSlot(bool)
    def on_openProfileEditor_clicked(self):
        """
        Opens the profile editor dialog
        """
        dlg = ProfileEditor()
        dlg.exec_()
        self.getModelProfiles()

    @pyqtSlot(bool)
    def on_removeButton_clicked(self):
        """
        Removes a installed profile from the database (i.e we execute a drop role sql query)
        """
        if len(self.assignedProfiles.selectedItems()) == 0:
            QMessageBox.warning(
                self,
                self.tr("Warning!"),
                self.tr("Select at least one profile and try again!"),
            )
            return

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        problem = False
        for item in self.assignedProfiles.selectedItems():
            role = item.text()

            try:
                self.widget.abstractDb.dropRole(role)
            except Exception as e:
                problem = True
                QApplication.restoreOverrideCursor()
                QMessageBox.critical(self, self.tr("Critical!"), ":".join(e.args))

        if not problem:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(
                self, self.tr("Warning!"), self.tr("Profiles removed successfully!")
            )

        self.getInstalledProfiles()

    @pyqtSlot(bool)
    def on_removeJson_clicked(self):
        """
        Deletes a profile file
        """
        if len(self.possibleProfiles.selectedItems()) == 0:
            QMessageBox.warning(
                self,
                self.tr("Warning!"),
                self.tr("Select at least one profile and try again!"),
            )
            return

        if (
            QMessageBox.question(
                self,
                self.tr("Question"),
                self.tr("Do you really want to remove selected profile models?"),
                QMessageBox.Ok | QMessageBox.Cancel,
            )
            == QMessageBox.Cancel
        ):
            return

        for item in self.possibleProfiles.selectedItems():
            json = item.text()
            file = json + ".json"
            path = os.path.join(self.folder, file)
            try:
                os.remove(path)
            except OSError as e:
                QMessageBox.critical(
                    self,
                    self.tr("Critical!"),
                    self.tr("Problem removing profile model: ")
                    + json
                    + "\n"
                    + e.strerror,
                )

        self.getModelProfiles()
