# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-02-24
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from DsgTools.Utils.utils import Utils

from qgis.core import QgsMessageLog
import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'genericManagerWidget.ui'))

class GenericManagerWidget(QtGui.QWidget, FORM_CLASS):
    def __init__(self, genericDbManager = None, parent = None):
        """
        Constructor
        """
        super(GenericManagerWidget, self).__init__(parent)
        self.setupUi(self)
        self.genericDbManager = genericDbManager
        self.versionDict = {'2.1.3':1, 'FTer_2a_Ed':2}
        self.textDict = {'EarthCoverage':self.tr('Earth Coverage'), 
                            'Customization':self.tr('Customization'), 
                            'Style':self.tr('Style'), 
                            'ValidationConfig':self.tr('Validation'), 
                            'FieldToolBoxConfig':self.tr('Field Toolbox Configuration')}
        self.widgetName = self.textDict[self.getWhoAmI()]
        self.genericDict = None
        self.setComponentsEnabled(False)
        self.utils = Utils()
        self.setHeaders()
    
    def setHeaders(self):
        viewType = self.getViewType()
        if viewType == 'database':
            self.treeWidget.setHeaderLabels([self.tr('Database'), self.widgetName])
        else:
            self.treeWidget.setHeaderLabels([self.widgetName, self.tr('Database')])
        return viewType
    
    def getWhoAmI(self):
        return str(self.__class__).split('.')[-1].replace('\'>', '').replace('ManagerWidget','')
    
    def setChildParameter(self):
        """
        Reimplement in each child
        """
        pass
    
    def setComponentsEnabled(self, enabled):
        self.treeWidget.setEnabled(enabled)
        self.importPushButton.setEnabled(enabled)
        self.batchImportPushButton.setEnabled(enabled)
        self.exportPushButton.setEnabled(enabled)
        self.batchExportPushButton.setEnabled(enabled)
        self.databasePerspectivePushButton.setEnabled(enabled)
        self.propertyPerspectivePushButton.setEnabled(enabled)
    
    def readJsonFromDatabase(self, propertyName, edgvVersion):
        '''
        Reads the profile file, gets a dictionary of it and builds the tree widget
        '''
        self.genericDict = self.genericDbManager.getCustomization(propertyName, edgvVersion)

    @pyqtSlot(bool)
    def on_importPushButton_clicked(self):
        fd = QFileDialog()
        filename = fd.getOpenFileName(caption=self.tr('Select a dsgtools profile'),filter=self.tr('json file (*.json)'))
        if filename == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Select a file to import!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.genericDbManager.importProfile(filename)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.widgetName + self.tr(' successfully imported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem importing ') +self.widgetName + ': '  + e.args[0])
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
            self.genericDbManager.exportProfile(profileName, edgvVersion, folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.widgetName + self.tr(' successfully exported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem exporting ') + self.widgetName + ': ' + e.args[0])
        
    @pyqtSlot(bool)
    def on_batchExportPushButton_clicked(self):
        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption = self.tr('Select a folder to output'))
        if folder == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Select a output!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.genericDbManager.batchExportCustomizations(folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), + self.widgetName + self.tr(' successfully exported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem exporting ') + self.widgetName + ': ' + e.args[0])
    
    @pyqtSlot(bool)
    def on_batchImportPushButton_clicked(self):
        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption = self.tr('Select a folder with json files: '))
        if folder == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Select a input folder!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.genericDbManager.batchImportCustomizations(folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), + self.widgetName + self.tr(' successfully imported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem importing ') + self.widgetName + ': ' + e.args[0])

    def getViewType(self):
        if self.databasePerspectivePushButton.isChecked():
            return 'database'
        else:
            return 'property'

    @pyqtSlot(bool, name='on_databasePerspectivePushButton_clicked')
    @pyqtSlot(bool, name='on_propertyPerspectivePushButton_clicked')
    def refresh(self):
        viewType = self.setHeaders()
        propertyPerspectiveDict = self.genericDbManager.getPropertyPerspectiveDict(viewType)
        self.treeWidget.clear()
        rootNode = self.treeWidget.invisibleRootItem()
        for key in propertyPerspectiveDict.keys():
            parentCustomItem = self.utils.createWidgetItem(rootNode, key, 0)
            for item in propertyPerspectiveDict[key]:
                dbItem = self.utils.createWidgetItem(parentCustomItem, item, 1)
        self.treeWidget.sortItems(0, Qt.AscendingOrder)
        self.treeWidget.expandAll()
