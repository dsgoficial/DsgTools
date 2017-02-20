# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-02-08
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

# Qt imports
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt4.QtGui import QMessageBox, QApplication, QCursor, QFileDialog

#DsgTools imports
from DsgTools.ServerManagementTools.customizationManager import CustomizationManager
from DsgTools.PostgisCustomization.createDatabaseCustomization import CreateDatabaseCustomization

from qgis.core import QgsMessageLog
import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customizationManagerWidget.ui'))

class CustomizationManagerWidget(QtGui.QWidget, FORM_CLASS):
    def __init__(self, customizationManager = None, parent = None):
        """
        Constructor
        """
        super(CustomizationManagerWidget, self).__init__(parent)
        self.setupUi(self)
        self.customizationManager = customizationManager
        self.versionDict = {'2.1.3':1, 'FTer_2a_Ed':2}
        self.customDict = None
        self.setComponentsEnabled(False)
    
    def setParameters(self, serverAbstractDb):
        if serverAbstractDb:
            self.setComponentsEnabled(True)
            self.serverAbstractDb = serverAbstractDb
            self.customizationManager = CustomizationManager(serverAbstractDb, {})
        else:
            self.setComponentsEnabled(False)
    
    def setComponentsEnabled(self, enabled):
        self.customizationTreeWidget.setEnabled(enabled)
        self.createPushButton.setEnabled(enabled)
        self.deleteCustomizationPushButton.setEnabled(enabled)
        self.importPushButton.setEnabled(enabled)
        self.batchImportPushButton.setEnabled(enabled)
        self.exportPushButton.setEnabled(enabled)
        self.batchExportPushButton.setEnabled(enabled)
        self.databasePerspectivePushButton.setEnabled(enabled)
        self.customizationPerspectivePushButton.setEnabled(enabled)
    
    def readJsonFromDatabase(self, customName, edgvVersion):
        '''
        Reads the profile file, gets a dictionary of it and builds the tree widget
        '''
        self.customDict = self.customizationManager.getCustomization(customName, edgvVersion)
    
    @pyqtSlot(bool)
    def on_createPushButton_clicked(self):
        '''
        Slot that opens the create profile dialog
        '''
        dlg = CreateDatabaseCustomization(self.serverAbstractDb, self.customizationManager)
        dlg.exec_()
    
    @pyqtSlot(bool)
    def on_deleteCustomizationPushButton_clicked(self):
        customizationName = self.customizationListWidget.currentItem().text()
        edgvVersion = self.versionSelectionComboBox.currentText()
        if QtGui.QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to delete customization ')+customizationName+'?', QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel) == QtGui.QMessageBox.Cancel:
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.customizationManager.deleteCustomization(customizationName, edgvVersion)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Customization ') + customizationName + self.tr(' successfully deleted.'))
            self.refreshProfileList()
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem deleting customization: ') + e.args[0])

    @pyqtSlot(bool)
    def on_importPushButton_clicked(self):
        fd = QFileDialog()
        filename = fd.getOpenFileName(caption=self.tr('Select a dsgtools profile'),filter=self.tr('json file (*.json)'))
        if filename == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Select a file to import!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.customizationManager.importProfile(filename)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Permission successfully imported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem importing permission: ') + e.args[0])
        self.refreshProfileList()
    
    @pyqtSlot(bool)
    def on_exportPushButton_clicked(self):
        if not self.profilesListWidget.currentItem():
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Select a profile to export!'))
            return
        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption = self.tr('Select a folder to output'))
        if folder == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Select a output!'))
            return
        profileName = self.customListWidget.currentItem().text()
        edgvVersion = self.versionSelectionComboBox.currentText()
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.customizationManager.exportProfile(profileName, edgvVersion, folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Permission successfully exported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem exporting permission: ') + e.args[0])
        
    @pyqtSlot(bool)
    def on_batchExportPushButton_clicked(self):
        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption = self.tr('Select a folder to output'))
        if folder == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Select a output!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.customizationManager.batchExportCustomizations(folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Customizations successfully exported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem exporting customization: ') + e.args[0])
    
    @pyqtSlot(bool)
    def on_batchImportPushButton_clicked(self):
        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption = self.tr('Select a folder with permissions: '))
        if folder == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Select a input folder!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.customizationManager.batchImportCustomizations(folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Customizations successfully imported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem importing customization: ') + e.args[0])

    @pyqtSlot(bool, name='on_databasePerspectivePushButton_clicked')
    @pyqtSlot(bool, name='on_customizationPerspectivePushButton_clicked')
    def refresh(self):
        '''
        Refreshes customization table according to selected view type.
        '''
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        viewType = self.getViewType()
        self.customizationTreeWidget.clear()
        if viewType == 'database':
            self.populateWithDatabasePerspective()
        if viewType == 'customization':
            self.populateWithCustomizationPerspective()
        QApplication.restoreOverrideCursor()    

    def getViewType(self):
        if self.databasePerspectivePushButton.isChecked():
            return 'database'
        else:
            return 'customization'

    def populateWithDatabasePerspective(self):
        #TODO
        self.customizationTreeWidget.setHeaderLabels([self.tr('Database'), self.tr('Customization')])
        dbPerspectiveDict = self.customizationManager.getDatabasePerspectiveDict()
        rootNode = self.customizationTreeWidget.invisibleRootItem()
        for dbName in dbPerspectiveDict.keys():
            parentDbItem = self.createItem(rootNode, dbName, 0)
            for customization in dbPerspectiveDict[dbName].keys():
                dbItem = self.createItem(parentDbItem, customization, 1)
                for user in dbPerspectiveDict[dbName][customization]:
                    userItem = self.createItem(dbItem, user, 2)
        self.customizationTreeWidget.sortItems(0, Qt.AscendingOrder)
        self.customizationTreeWidget.expandAll()

    def populateWithCustomizationPerspective(self):
        #TODO
        self.customizationTreeWidget.setHeaderLabels([self.tr('Customization'), self.tr('Database')])
        customizationPerspectiveDict = self.customizationManager.getcustomizationPerspectiveDict()
        rootNode = self.customizationTreeWidget.invisibleRootItem()
        for customizationName in customizationPerspectiveDict.keys():
            parentCustomItem = self.createItem(rootNode, customizationName, 0)
            for dbName in customizationPerspectiveDict[customizationName].keys():
                dbItem = self.createItem(parentCustomItem, dbName, 1)
                for customization in customizationPerspectiveDict[customizationName][dbName]:
                    customizationItem = self.createItem(dbItem, customization, 2)
        self.customizationTreeWidget.sortItems(0, Qt.AscendingOrder)
        self.customizationTreeWidget.expandAll()