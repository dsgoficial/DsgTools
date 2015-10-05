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
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtSql import QSqlDatabase, QSqlQuery

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.UserTools.profile_editor import ProfileEditor

import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'create_user.ui'))

class CreateUser(QtGui.QDialog, FORM_CLASS):
    def __init__(self, user = None, db = None, parent = None):
        """Constructor."""
        super(CreateUser, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.db = db
        self.factory = SqlGeneratorFactory()
        self.gen = self.factory.createSqlGenerator(False)
        
        
        self.utils = Utils()   
        self.refreshScreen()     
    
    def refreshScreen(self):
        self.userLineEdit.setText('')
        self.passwordLineEdit.setText('')
    
    @pyqtSlot(bool)
    def on_createUserButton_clicked(self):
        user = self.userLineEdit.text()
        password = self.passwordLineEdit.text()
        sql = self.gen.createUser(user,password)
        query = QSqlQuery(self.db)

        if not query.exec_(sql):
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('Problem creating user: ') +user+'\n'+query.lastError().text())
            self.refreshScreen()
            return
        else:
            QtGui.QMessageBox.warning(self, self.tr('Success!'), self.tr('User ') +user+' created successfully!')
            self.refreshScreen()
            return

    @pyqtSlot(bool)
    def on_closeButton_clicked(self):
        self.close()