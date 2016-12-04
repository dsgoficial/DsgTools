# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-18
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba@dsg.eb.mil.br
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
import json

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtGui import QTreeWidgetItem, QMessageBox

from qgis.core import QgsMessageLog

from DsgTools.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.UserTools.permission_properties import PermissionProperties
from DsgTools.UserTools.manageServerUsers import ManageServerUsers
from DsgTools.UserTools.PermissionManagerWizard.permissionWizard import PermissionWizard


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'permissionWidget.ui'))

class PermissionWidget(QtGui.QWidget, FORM_CLASS):
    def __init__(self, parent=None):
        '''Constructor.'''
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.serverAbstractDb = None
        self.dbDict = dict()
        self.permissionManager = None

    @pyqtSlot(bool, name='on_databasePerspectivePushButton_clicked')
    @pyqtSlot(bool, name='on_userPerspectivePushButton_clicked')
    def refresh(self):
        '''
        Refreshes permission table according to selected view type.
        '''
        viewType = self.getViewType()
        self.permissionTreeWidget.clear()
        if viewType == 'database':
            self.populateWithDatabasePerspective()
        if viewType == 'user':
            self.populateWithUserPerspective()
        print 'lalalala'
    
    def populateWithDatabasePerspective(self):
        pass
    
    def populateWithUserPerspective(self):
        pass
    
    
    def getViewType(self):
        if self.databasePerspectivePushButton.isChecked():
            return 'database'
        else:
            return 'user'
            
    
    def setParameters(self, serverAbstractDb, dbDict):
        self.serverAbstractDb = serverAbstractDb
        self.dbDict = dbDict
        self.permissionManager = PermissionManager(self.serverAbstractDb, self.dbDict)

    @pyqtSlot(bool)
    def on_manageUsersPushButton_clicked(self):
        try:
            dlg = ManageServerUsers(self.serverAbstractDb)
            dlg.exec_()
        except:
            QMessageBox.warning(self, self.tr('Error!'), self.tr('Select a server!'))
    
    @pyqtSlot(bool)
    def on_manageProfilesPushButton_clicked(self):
        try:
            dlg = ProfileEditor()
            dlg.exec_()
        except:
            pass
    
    @pyqtSlot(bool)
    def on_managePermissionsPushButton_clicked(self):
        #REDO
        dbsDict = self.parent.instantiateAbstractDbs()
        try:
            dlg = PermissionWizard(self.serverAbstractDb, dbsDict, parent = self) #REDO
            dlg.exec_()
        except:
            pass