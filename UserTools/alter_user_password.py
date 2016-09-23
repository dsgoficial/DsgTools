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
from PyQt4.QtGui import QMessageBox

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'alter_user_password.ui'))

class AlterUserPassword(QtGui.QDialog, FORM_CLASS):
    def __init__(self, user = None, abstractDb = None, userList = None, parent = None):
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
        self.userList = userList
    
    @pyqtSlot(bool)
    def on_alterPasswordButton_clicked(self):
        newpassword = self.newPasswordLineEdit.text()
        newpassword_2 = self.newPasswordLineEdit_2.text()
        if newpassword <> newpassword_2:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Password mismatch! Password not altered!'))
            return
        if self.user:
            self.alterDatabasePassword(self.user, newpassword)
        if self.userList:
            self.alterServerPassword(self.userList, newpassword)
        self.close()

    @pyqtSlot(bool)
    def on_cancelButton_clicked(self):
        self.close()
    
    def alterDatabasePassword(self, user, newpassword):
        try:
            self.abstractDb.alterUserPass(self.user, newpassword)
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), e.args[0])
            return
        QtGui.QMessageBox.warning(self, self.tr('Success!'), self.tr('User ') +self.user+self.tr(' password successfully updated on database ')+self.abstractDb.getDatabaseName()+'!')
    
    def alterServerPassword(self, userList, newpassword):
        successList = []
        exceptionDict = dict()
        for user in userList:
            try:
                self.abstractDb.alterUserPass(user, newpassword)
                successList.append(user)
            except Exception as e:
                exceptionDict[user] = str(e.args[0])
        header = self.tr('Alter operation on server ')+self.abstractDb.getHostName()+self.tr(' complete!\n')
        self.outputMessage(header, successList, exceptionDict)
    
    def outputMessage(self, header, successList, exceptionDict):
        msg = header
        if len(successList) > 0:
            msg += self.tr('\nSuccessful users: ')
            msg +=', '.join(successList)
        msg += self.logInternalError(exceptionDict)
        QMessageBox.warning(self, self.tr('Operation Complete!'), msg)

    def logInternalError(self, exceptionDict):
        msg = ''
        errorDbList = exceptionDict.keys()
        if len(errorDbList)> 0:
            msg += self.tr('\Users with error:')
            msg+= ', '.join(errorDbList)
            msg+= self.tr('\nError messages for each user were output in qgis log.')
            for errorDb in errorDbList:
                QgsMessageLog.logMessage(self.tr('Error for user ')+ errorDb + ': ' +exceptionDict[errorDb], "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        return msg 