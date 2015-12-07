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
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'alter_user_password.ui'))

class AlterUserPassword(QtGui.QDialog, FORM_CLASS):
    def __init__(self, user = None, abstractDb = None, parent = None):
        """Constructor."""
        super(AlterUserPassword, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.abstractDb = abstractDb
        self.user = user
        self.newPasswordLineEdit.setFocus()
    
    @pyqtSlot(bool)
    def on_alterPasswordButton_clicked(self):
        newpassword = self.newPasswordLineEdit.text()
        newpassword_2 = self.newPasswordLineEdit_2.text()
        if newpassword <> newpassword_2:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Password mismatch! Password not altered!'))
            return

        try:
            self.abstracDb.alterUserPass(self.user, newpassword)
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), e.args[0])
            return

        QtGui.QMessageBox.warning(self, self.tr('Success!'), self.tr('User ') +self.user+self.tr(' password successfully updated on database ')+self.abstractDb.getDatabaseName()+'!')
        self.close()

    @pyqtSlot(bool)
    def on_cancelButton_clicked(self):
        self.close()