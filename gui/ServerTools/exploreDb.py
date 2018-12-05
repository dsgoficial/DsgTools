# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgManagementToolsDialog
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-08-12
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
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, Qt, QSettings
from qgis.PyQt.QtWidgets import QListWidgetItem, QMessageBox, QMenu, QApplication
from qgis.PyQt.QtGui import QCursor

# DSGTools imports
from DsgTools.core.Utils.utils import Utils
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.gui.DatabaseTools.UserTools.permission_properties import PermissionProperties
from DsgTools.gui.ServerTools.createView import CreateView
from DsgTools.gui.ServerTools.manageDBAuxiliarStructure import ManageDBAuxiliarStructure
from DsgTools.core.dsgEnums import DsgEnums

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'exploreDb.ui'))

class ExploreDb(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """
        Constructor
        """
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.utils = Utils()
        self.dbFactory = DbFactory()
        self.localDb = None
        self.serverWidget.populateServersCombo()
        #signal connections
        self.serverWidget.abstractDbLoaded.connect(self.checkSuperUser)
        self.serverWidget.clearWidgets.connect(self.clearAll)
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.createMenuAssigned)
        
    def populateListWithDatabasesFromServer(self):
        '''
        Populates databases list from server
        '''
        dbList = []
        try:
            dbList = self.serverWidget.abstractDb.getEDGVDbsFromServer()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), ':'.join(e.args))

        dbList.sort()
        for (dbname, dbversion) in dbList:
            item = QListWidgetItem(self.dbListWidget)
            item.setText(dbname+' (EDGV v. '+dbversion+')')
            item.setData(Qt.UserRole, dbname)
    
    @pyqtSlot(bool)
    def on_closePushButton_clicked(self):
        '''
        Closes the dialog
        '''
        self.done(0)
    
    def renewDb(self):
        '''
        Renews the database
        '''
        if self.localDb:
            del self.localDb
            self.localDb = None
    
    def clearAll(self):
        '''
        Clears the database list
        '''
        self.dbListWidget.clear()
        self.treeWidget.clear()
        self.renewDb()
    
    def checkSuperUser(self):
        '''
        Checks if the user is a super user
        '''
        try:
            if self.serverWidget.abstractDb.checkSuperUser():
                self.populateListWithDatabasesFromServer()
            else:
                QMessageBox.warning(self, self.tr('Info!'), self.tr('Connection refused. Connect with a super user to inspect server.'))
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), ':'.join(e.args))
    
    def createItem(self, parent, text, column):
        '''
        Creates a tree widget item
        '''
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        item.setText(column, text)
        return item
    
    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def on_dbListWidget_currentItemChanged(self, current, previous):
        '''
        Updates the information related with the database (e.g. users and roles for instance)
        '''
        self.treeWidget.clear()
        if not current:
            return
        self.localDb = self.dbFactory.createDbFactory(DsgEnums.DriverPostGIS)
        originalCon = self.serverWidget.abstractDb.makeOgrConn()
        self.localDb.connectDatabaseWithParameters(self.serverWidget.abstractDb.db.hostName(), self.serverWidget.abstractDb.db.port(), current.text().split(' ')[0], self.serverWidget.abstractDb.db.userName(), self.serverWidget.abstractDb.db.password())

        candidateUserList = []
        try:
            candidateUserList = self.localDb.getUsers()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), ':'.join(e.args))

        for candidate in candidateUserList:
            installed,assigned = self.localDb.getUserRelatedRoles(candidate)
            if len(assigned)>0:
                userItem = self.createItem(self.treeWidget.invisibleRootItem(), candidate,0)
                for perm in assigned:
                    self.createItem(userItem, perm,1)
    
    def createMenuAssigned(self, position):
        '''
        Creates a pop up menu
        '''
        menu = QMenu()
        item = self.treeWidget.itemAt(position)
        if item:
            menu.addAction(self.tr('Show properties'), self.showAssignedProperties)
        menu.exec_(self.treeWidget.viewport().mapToGlobal(position))
              
    def showAssignedProperties(self):
        '''
        Shows information about the selected permissions model 
        '''
        permission = self.treeWidget.currentItem().text(1)
        dbname = self.dbListWidget.currentItem().text().split(' ')[0]

        permissionsDict = dict()
        try:
            permissionsDict = self.localDb.getRolePrivileges(permission, dbname)
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), ':'.join(e.args))

        dlg = PermissionProperties(permissionsDict)
        dlg.exec_()
    
    @pyqtSlot(bool)
    def on_dropDatabasePushButton_clicked(self):
        '''
        Drops a database and updates QSettings
        '''
        currentItem = self.dbListWidget.currentItem()
        if not currentItem:
            return
        if QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to drop database: ')+currentItem.text().split(' ')[0], QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
            return
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        localDbName = self.localDb.getDatabaseName()
        self.renewDb()
        try:
            self.serverWidget.abstractDb.dropDatabase(localDbName)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Database ')+localDbName+self.tr(' dropped successfully!'))
            self.clearQSettings(localDbName)
        except Exception as e:
            QApplication.restoreOverrideCursor()            
            QMessageBox.critical(self, self.tr('Critical!'), ':'.join(e.args))
        self.clearAll()
        self.populateListWithDatabasesFromServer()

    @pyqtSlot(bool)
    def on_createViewsPushButton_clicked(self):
        '''
        Creates view button
        '''
        if not self.localDb:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Select a database to create view'))
            return
        dlg = CreateView(self.localDb,self.dbListWidget.currentItem().text())
        dlg.exec_()
        pass
    
    def clearQSettings(self,database):
        '''
        Clear the database from QSettings
        '''
        name = self.serverWidget.serversCombo.currentText()+'_'+database
        settings = QSettings()
        settings.beginGroup('PostgreSQL/connections/'+name)
        settings.remove('')
        settings.endGroup()
    
    @pyqtSlot(bool)
    def on_manageAuxStructPushButton_clicked(self):
        '''
        Opens the dialog to manage database auxiliar structure
        '''
        if not self.localDb:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Select a database to manage auxiliar structure'))
            return
        dlg = ManageDBAuxiliarStructure(self.localDb)
        dlg.exec_()
        pass    
