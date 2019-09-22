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
from qgis.PyQt.QtWidgets import QMessageBox

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'alter_user_password.ui'))

class AlterUserPassword(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, user = None, abstractDb = None, userList = None, parent = None):
        """
        Constructor
        """
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
        """
        Slot to alter user's password
        """
        newpassword = self.newPasswordLineEdit.text()
        newpassword_2 = self.newPasswordLineEdit_2.text()
        if newpassword != newpassword_2:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Password mismatch! Password not altered!'))
            return
        if self.user:
            self.alterDatabasePassword(self.user, newpassword)
        if self.userList:
            self.alterServerPassword(self.userList, newpassword)
        self.close()
    
    def alterDatabasePassword(self, user, newpassword):
        """
        Alters the password of a specific user
        """
        try:
            self.abstractDb.alterUserPass(self.user, newpassword)
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), e.args[0])
            return
        QMessageBox.warning(self, self.tr('Success!'), self.tr('User ') +self.user+self.tr(' password successfully updated on database ')+self.abstractDb.getDatabaseName()+'!')
    
    def alterServerPassword(self, userList, newpassword):
        """
        Alters the password of a list of database users
        """
        successList = []
        exceptionDict = dict()
        for user in userList:
            try:
                self.abstractDb.alterUserPass(user, newpassword)
                successList.append(user)
            except Exception as e:
                exceptionDict[user] = ':'.join(e.args)
        header = self.tr('Alter operation on server ')+self.abstractDb.getHostName()+self.tr(' complete!\n')
        self.outputMessage(header, successList, exceptionDict)
    
    def outputMessage(self, header, successList, exceptionDict):
        """
        Makes the output message
        """
        msg = header
        if len(successList) > 0:
            msg += self.tr('\nSuccessful users: ')
            msg +=', '.join(successList)
        msg += self.logInternalError(exceptionDict)
        QMessageBox.warning(self, self.tr('Operation Complete!'), msg)

    def logInternalError(self, exceptionDict):
        """
        Logs all internal errors into QGIS' log
        """
        msg = ''
        errorDbList = list(exceptionDict.keys())
        if len(errorDbList)> 0:
            msg += self.tr('\nUsers with error:')
            msg+= ', '.join(errorDbList)
            msg+= self.tr('\nError messages for each user were output in qgis log.')
            for errorDb in errorDbList:
                QgsMessageLog.logMessage(self.tr('Error for user ')+ errorDb + ': ' +exceptionDict[errorDb], "DSGTools Plugin", Qgis.Critical)
        return msg 

    @pyqtSlot(bool)
    def on_cancelButton_clicked(self):
        """
        Cancels everything
        """
        self.close()