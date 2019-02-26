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
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtSql import QSqlQuery

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'create_user.ui'))

class CreateUser(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, user = None, abstractDb = None, parent = None):
        """
        Constructor
        """
        super(CreateUser, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.abstractDb = abstractDb
        self.refreshScreen()
    
    def refreshScreen(self):
        """
        Restores the initial state
        """
        self.userLineEdit.setText('')
        self.passwordLineEdit.setText('')
        self.passwordLineEdit_2.setText('')
        self.superUserCheckBox.setCheckState(0)
    
    @pyqtSlot(bool)
    def on_createUserButton_clicked(self):
        """
        Creates the user in the database (i.e create user sql query)
        """
        user = self.userLineEdit.text()
        password = self.passwordLineEdit.text()
        password_2 = self.passwordLineEdit_2.text()
        if password != password_2:
            QtWidgets.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Password mismatch! User not created!'))
            self.refreshScreen()
            return
        
        
        if self.superUserCheckBox.checkState() == 2:
            isSuperUser = True
        else:
            isSuperUser = False

        try:
            self.abstractDb.createUser(user, password, isSuperUser)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, self.tr('Critical!'), ':'.join(e.args))
            self.refreshScreen()
            return

        QtWidgets.QMessageBox.warning(self, self.tr('Success!'), self.tr('User ') +user+self.tr(' created successfully on server ')+self.abstractDb.getHostName()+'!')
        self.refreshScreen()
        return

    @pyqtSlot(bool)
    def on_closeButton_clicked(self):
        """
        Closes the dialog
        """
        self.close()
