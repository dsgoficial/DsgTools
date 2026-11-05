# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
from qgis.PyQt.QtCore import QSettings, pyqtSlot
from qgis.PyQt.QtWidgets import QMessageBox, QDialog, QLineEdit
from qgis.PyQt import uic
import os

from DsgTools.core.Utils import credentialStore

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "ui_serverConfigurator.ui")
)


class ServerConfigurator(QDialog, FORM_CLASS):
    def __init__(self, iface):
        """
        Constructor
        """
        super(ServerConfigurator, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.iface = iface
        self.isEdit = 0
        self.oldName = ""
        self.passwordStored = False
        self.passwordLoadFailed = False

        self.passwordEdit.setEchoMode(QLineEdit.EchoMode.Password)

    @pyqtSlot(bool)
    def on_saveButton_clicked(self):
        """
        Saves a new server
        """
        if self.checkFields():
            name = self.servEdit.text()
            host = self.hostEdit.text()
            port = self.portEdit.text()
            user = self.userEdit.text()
            password = self.passwordEdit.text()
            if not self.storeServerConfiguration(name, host, port, user, password):
                return
            if password and not self.passwordStored:
                QMessageBox.warning(
                    self,
                    self.tr("Warning!"),
                    self.tr(
                        "Server stored without the password: the QGIS authentication "
                        "database is not available (master password not set). "
                        "The password will be asked when connecting."
                    ),
                )
            QMessageBox.warning(self, self.tr("Info!"), self.tr("Server stored."))
            self.done(1)
        else:
            QMessageBox.warning(
                self, self.tr("Warning!"), self.tr("Fill all parameters.")
            )

    @pyqtSlot(bool)
    def on_cancelButton_clicked(self):
        """
        Cancel everything
        """
        self.done(0)

    def checkFields(self):
        """
        Checks if the fields are filled
        """
        if (
            self.hostEdit.text() == ""
            or self.portEdit.text() == ""
            or self.userEdit.text() == ""
        ):
            return False
        return True

    def storeServerConfiguration(
        self, name, host, port, user, password, isDefault=False
    ):
        """
        Stores server configuration in QSettings
        """
        if "_" in name:
            QMessageBox.warning(
                self,
                self.tr("Warning!"),
                self.tr('Server name cannot contain the character "_".'),
            )
            self.servEdit.setStyleSheet("background-color: rgb(255, 150, 150)")
            return 0

        settings = QSettings()
        if not self.isEdit:
            if settings.contains("PostgreSQL/servers/" + name + "/host"):
                QMessageBox.warning(
                    self,
                    self.tr("Warning!"),
                    self.tr("Already has a server with this name."),
                )
                self.servEdit.setStyleSheet("background-color: rgb(255, 150, 150)")
                return 0
        # the password goes to the QGIS authentication database and QSettings
        # keeps only the authcfg reference (CDCiber 4.2)
        _, self.passwordStored = credentialStore.saveServer(
            name,
            host,
            port,
            user,
            password,
            isDefault=isDefault,
            previousName=self.oldName if self.isEdit else None,
            keepCredentialWhenEmpty=self.passwordLoadFailed,
        )
        return 1

    def setServerConfiguration(self, name):
        """
        Sets server confogiration by its name
        """
        self.isEdit = 1
        self.oldName = name
        host, port, user, password = credentialStore.readServer(name)
        # a stored password that could not be read (master password refused)
        # must survive an edit that leaves the field empty
        self.passwordLoadFailed = not password and credentialStore.hasStoredPassword(
            "PostgreSQL/servers/" + name
        )

        self.servEdit.setText(name)
        self.hostEdit.setText(host)
        self.portEdit.setText(port)
        self.userEdit.setText(user)
        self.passwordEdit.setText(password)
