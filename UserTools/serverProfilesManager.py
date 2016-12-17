# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-12-07
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

from qgis.core import QgsMessageLog

# DSGTools imports
from DsgTools.UserTools.createProfileWithProfileManager import CreateProfileWithProfileManager

import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'serverProfilesManager.ui'))

class ServerProfilesManager(QtGui.QDialog, FORM_CLASS):
    profilesChanged = pyqtSignal()
    def __init__(self, permissionManager, parent = None):
        """
        Constructor
        """
        super(ServerProfilesManager, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.permissionManager = permissionManager
        self.versionDict = {'2.1.3':0, 'FTer_2a_Ed':1}

        
    def createItem(self, parent, text):
        '''
        Creates tree widget items
        '''
        item = QtGui.QTreeWidgetItem(parent)
        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(1, QtCore.Qt.Unchecked)
        item.setCheckState(2, QtCore.Qt.Unchecked)
        item.setText(0, text)
        return item
    
    def makeProfileDict(self):
        '''
        Makes a dictionary out of the tree widget items
        '''
        profileDict = dict()
        
        #invisible root item
        rootItem = self.treeWidget.invisibleRootItem()
        #database item
        dbItem = rootItem.child(0)
        permissions = dict()
        
        schema_count = dbItem.childCount()
        for i in range(schema_count):
            schemaItem = dbItem.child(i)
            permissions[schemaItem.text(0)] = dict()
            category_count = schemaItem.childCount()
            for j in range(category_count):
                categoryItem = schemaItem.child(j)
                permissions[schemaItem.text(0)][categoryItem.text(0)] = dict()
                layer_count = categoryItem.childCount()
                for k in range(layer_count):
                    layerItem = categoryItem.child(k)
                    permissions[schemaItem.text(0)][categoryItem.text(0)][layerItem.text(0)] = self.getItemCheckState(layerItem)
                 
        profileDict[self.parent] = permissions   
        return profileDict
    
    def readJsonFromDatabase(self, profileName, edgvVersion):
        '''
        Reads the profile file, gets a dictionary of it and builds the tree widget
        '''

        profileDict = self.permissionManager.getProfile(profileName, edgvVersion)
        self.parent = profileDict.keys()[0]
        #invisible root item
        rootItem = self.treeWidget.invisibleRootItem()
        #database item
        dbItem = self.createItem(rootItem, self.parent)

        permissions = profileDict[self.parent]
        self.createChildrenItems(dbItem, permissions)
        self.treeWidget.sortItems(0, Qt.AscendingOrder)
                                        
    def createChildrenItems(self, parent, mydict):
        '''
        Creates children item in the tree widget
        '''
        #permissions
        lista = ['read', 'write']
        for key in mydict.keys():
            if key in lista:
                self.setItemCheckState(parent, mydict, key)
            else:
                itemText = key
                item = self.createItem(parent, itemText)
                self.createChildrenItems(item, mydict[key])
                
    def setItemCheckState(self, item, mydict, key):
        '''
        Sets the item check state
        '''
        if key == 'read':
            item.setCheckState(1, int(mydict[key]))
        elif key == 'write':
            item.setCheckState(2, int(mydict[key]))
    
    def getItemCheckState(self, item):
        '''
        Gets the item check state for READ and WRITE columns
        '''
        ret = dict()
        ret['read'] = str(item.checkState(1))
        ret['write'] = str(item.checkState(2))
        return ret
    
    @pyqtSlot(bool)
    def on_createButton_clicked(self):
        '''
        Slot that opens the create profile dialog
        '''
        dlg = CreateProfile()
        dlg.profileCreated.connect(self.updateInterface)
        dlg.exec_()
        
    @pyqtSlot(bool)
    def on_clearButton_clicked(self):
        '''
        Clears the tree widget
        '''
        #invisible root item
        rootItem = self.treeWidget.invisibleRootItem()
        #database item
        dbItem = rootItem.child(0)
        if dbItem:
            dbItem.setCheckState(1, 0)
            dbItem.setCheckState(2, 0)
        
    @pyqtSlot(bool)
    def on_saveButton_clicked(self):
        '''
        Saves the profile file
        '''
        #REDO
        if self.jsonCombo.currentIndex() == 0:
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Select a profile model!'))
            return
        else:
            profile = self.jsonCombo.currentText()
            
        path = os.path.join(self.folder, profile+'.json')
        
        try:
            with open(path, 'w') as outfile:
                json.dump(self.makeProfileDict(), outfile, sort_keys=True, indent=4)
        except Exception as e:
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Problem saving file! \n')+e.args[0])
            return
            
        QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Profile saved successfully!'))
    
    @pyqtSlot(bool)
    def on_closeButton_clicked(self):
        '''
        Closes the dialog
        '''
        self.close()
    
    @pyqtSlot(int)
    def on_versionSelectionComboBox_currentIndexChanged(self):
        self.refreshProfileList()
    
    def refreshProfileList(self):
        index = self.versionSelectionComboBox.currentIndex()
        self.profilesListWidget.clear()
        self.treeWidget.clear()
        self.setEnabled(False)
        if index <> 0:
            edgvVersion = self.versionSelectionComboBox.currentText()
            profilesDict = self.permissionManager.getProfiles()
            if edgvVersion in profilesDict.keys():
                self.profilesListWidget.addItems(profilesDict[edgvVersion])
    
    @pyqtSlot(bool)
    def on_createPermissionPushButton_clicked(self):
        '''
        Slot that opens the create profile dialog
        '''
        dlg = CreateProfileWithProfileManager(self.permissionManager)
        dlg.profileCreated.connect(self.updateInterface)
        dlg.exec_()
    
    
    def setEnabled(self, enabled):
        self.treeWidget.setEnabled(enabled)
        self.saveButton.setEnabled(enabled)
        self.clearButton.setEnabled(enabled)
    
    @pyqtSlot()
    def on_profilesListWidget_itemSelectionChanged(self):
        profileName = self.profilesListWidget.currentItem().text()
        try:
            self.setEnabled(True)
            edgvVersion = self.versionSelectionComboBox.currentText()
            self.treeWidget.clear()
            self.readJsonFromDatabase(profileName, edgvVersion)
        except:
            pass
    
    def updateInterface(self, profileName, edgvVersion):
        self.refreshProfileList()
        idx = self.versionSelectionComboBox.findText(edgvVersion, flags = Qt.MatchExactly)
        self.versionSelectionComboBox.setCurrentIndex(idx)
        profileItem = self.profilesListWidget.findItems(profileName, Qt.MatchExactly)[0]
        self.profilesListWidget.setCurrentItem(profileItem)
    
    @pyqtSlot(bool)
    def on_deletePermissionPushButton_clicked(self):
        profileName = self.profilesListWidget.currentItem().text()
        edgvVersion = self.versionSelectionComboBox.currentText()
        if QtGui.QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to delete profile ')+profileName+'?', QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel) == QtGui.QMessageBox.Cancel:
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.permissionManager.deletePermission(profileName, edgvVersion)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Permission ') + profileName + self.tr(' successfully deleted.'))
            self.refreshProfileList()
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem deleting permission: ') + e.args[0])
    
    @pyqtSlot(bool)
    def on_saveButton_clicked(self):
        profileName = self.profilesListWidget.currentItem().text()
        edgvVersion = self.versionSelectionComboBox.currentText()
        newProfileDict = self.makeProfileDict()
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.permissionManager.updatePermissionProfile(profileName, edgvVersion, newProfileDict)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Permission ') + profileName + self.tr(' successfully updated.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem updating permission: ') + e.args[0])
    
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
        profileName = self.profilesListWidget.currentItem().text()
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
            self.permissionManager.batchExportProfiles(folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Permissions successfully exported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem exporting permission: ') + e.args[0])
    
    @pyqtSlot(bool)
    def on_batchImportPushButton_clicked(self):
        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption = self.tr('Select a folder with permissions: '))
        if folder == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Select a input folder!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.permissionManager.batchImportProfiles(folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Permissions successfully imported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem importing permission: ') + e.args[0])
