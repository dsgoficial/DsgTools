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
    
    def setParameters(self, abstractDb):
        if abstractDb:
            self.setComponentsEnabled(True)
            self.abstractDb = abstractDb
            self.customizationManager = CustomizationManager(abstractDb)
        else:
            self.setComponentsEnabled(False)
    
    def setComponentsEnabled(self, enabled):
        self.versionSelectionComboBox.setEnabled(enabled)
        self.createPushButton.setEnabled(enabled)
        self.customizationListWidget.setEnabled(enabled)
        self.deleteCustomizationPushButton.setEnabled(enabled)
        self.importPushButton.setEnabled(enabled)
        self.batchImportPushButton.setEnabled(enabled)
        self.exportPushButton.setEnabled(enabled)
        self.batchExportPushButton.setEnabled(enabled)
    
    def readJsonFromDatabase(self, customName, edgvVersion):
        '''
        Reads the profile file, gets a dictionary of it and builds the tree widget
        '''
        self.customDict = self.customizationManager.getCustomization(customName, edgvVersion)
    
    @pyqtSlot(int, name='on_versionSelectionComboBox_currentIndexChanged')
    def refreshProfileList(self):
        index = self.versionSelectionComboBox.currentIndex()
        self.customizationListWidget.clear()
        if index <> 0:
            edgvVersion = self.versionSelectionComboBox.currentText()
            customDict = self.customizationManager.getCustomizations()
            if edgvVersion in customDict.keys():
                self.customizationListWidget.addItems(customDict[edgvVersion])
    
    @pyqtSlot(bool)
    def on_createPushButton_clicked(self):
        '''
        Slot that opens the create profile dialog
        '''
        dlg = CreateDatabaseCustomization(self.abstractDb)
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
            self.permissionManager.importProfile(filename)
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
            self.permissionManager.exportProfile(profileName, edgvVersion, folder)
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