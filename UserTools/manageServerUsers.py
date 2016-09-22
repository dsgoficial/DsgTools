# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-09-22
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
from os.path import expanduser

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, Qt, QSettings
from PyQt4.QtGui import QListWidgetItem, QMessageBox, QMenu, QApplication, QCursor, QFileDialog
from PyQt4.QtSql import QSqlDatabase,QSqlQuery

# DSGTools imports
from DsgTools.UserTools.create_user import CreateUser
from DsgTools.UserTools.alter_user_password import AlterUserPassword
from DsgTools.UserTools.permission_properties import PermissionProperties


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'manageServerUsers.ui'))

class ManageServerUsers(QtGui.QDialog, FORM_CLASS):
    
    def __init__(self, abstractDb, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.abstractDb = abstractDb
        self.userTypeDict = {True:self.tr('Super User'), False:self.tr('User')}
        self.populateUsers()
    
    def populateUsers(self):
        rootNode = self.serverUserTable.invisibleRootItem()
        if not self.abstractDb:
            return
        ret = []
        try:
            ret = self.abstractDb.getUsersFromServer()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), e.args[0])
        for user, type in ret:
            userNameItem = self.createItem(rootNode, user, 0)
            userNameItem.setText(1,self.userTypeDict[type])
    
    def createItem(self, parent, text, column):
        item = QtGui.QTreeWidgetItem(parent)
        item.setText(column, text)
        return item