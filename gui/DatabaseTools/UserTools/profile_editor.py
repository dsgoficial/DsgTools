# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2015-09-10
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
from builtins import str
from builtins import range
import os

# Qt imports
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot

# DSGTools imports
from DsgTools.gui.DatabaseTools.UserTools.create_profile import CreateProfile

import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'profile_editor.ui'))

class ProfileEditor(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """
        Constructor
        """
        super(ProfileEditor, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.treeWidget.setColumnWidth(0, 400)
        
        self.folder = os.path.join(os.path.dirname(__file__), 'profiles')
        self.getProfiles()
        self.setInitialState()
        
    def getProfiles(self, profileName = None):
        """
        Get profile files and insert them in the combo box
        """
        ret = []
        for root, dirs, files in os.walk(self.folder):
            for file in files:
                ext = file.split('.')[-1]
                if ext == 'json':
                    ret.append(file.split('.')[0])

        ret.sort()
        self.jsonCombo.clear()
        self.jsonCombo.addItem(self.tr('Select a profile'))
        self.jsonCombo.addItems(ret)
        
        index = self.jsonCombo.findText(profileName)
        if index != -1:
            self.jsonCombo.setCurrentIndex(index)
        self.setInitialState()

    def setInitialState(self):
        """
        Gets the current selected profile in the combo box and builds the tree widget by reading the file
        """
        self.treeWidget.clear()
        self.treeWidget.setSortingEnabled(False)
        if self.jsonCombo.count() == 0 or self.jsonCombo.currentIndex() == 0:
            self.treeWidget.clear()
            return
        else:
            profile = os.path.join(self.folder, self.jsonCombo.currentText()+'.json')
            self.readJsonFile(profile)
        self.treeWidget.sortByColumn(0, QtCore.Qt.AscendingOrder)
        
    def createItem(self, parent, text):
        """
        Creates tree widget items
        """
        item = QtGui.QTreeWidgetItem(parent)
        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(1, QtCore.Qt.Unchecked)
        item.setCheckState(2, QtCore.Qt.Unchecked)
        item.setText(0, text)
        return item
    
    def makeProfileDict(self):
        """
        Makes a dictionary out of the tree widget items
        """
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
    
    def readJsonFile(self, filename):
        """
        Reads the profile file, gets a dictionary of it and builds the tree widget
        """
        try:
            file = open(filename, 'r')
            data = file.read()
            profileDict = json.loads(data)
            self.parent = list(profileDict.keys())[0]
            file.close()
        except:
            return
            
        #invisible root item
        rootItem = self.treeWidget.invisibleRootItem()
        #database item
        dbItem = self.createItem(rootItem, self.parent)

        permissions = profileDict[self.parent]
        self.createChildrenItems(dbItem, permissions)
                                        
    def createChildrenItems(self, parent, mydict):
        """
        Creates children item in the tree widget
        """
        #permissions
        lista = ['read', 'write']
        for key in list(mydict.keys()):
            if key in lista:
                self.setItemCheckState(parent, mydict, key)
            else:
                itemText = key
                item = self.createItem(parent, itemText)
                self.createChildrenItems(item, mydict[key])
                
    def setItemCheckState(self, item, mydict, key):
        """
        Sets the item check state
        """
        if key == 'read':
            item.setCheckState(1, int(mydict[key]))
        elif key == 'write':
            item.setCheckState(2, int(mydict[key]))
    
    def getItemCheckState(self, item):
        """
        Gets the item check state for READ and WRITE columns
        """
        ret = dict()
        ret['read'] = str(item.checkState(1))
        ret['write'] = str(item.checkState(2))
        return ret
        
    @pyqtSlot(int)
    def on_jsonCombo_currentIndexChanged(self):
        """
        Slot to update the initial state
        """
        self.setInitialState()
    
    @pyqtSlot(bool)
    def on_createButton_clicked(self):
        """
        Slot that opens the create profile dialog
        """
        dlg = CreateProfile()
        dlg.profileCreated.connect(self.getProfiles)
        dlg.exec_()
            
    @pyqtSlot(bool)
    def on_clearButton_clicked(self):
        """
        Clears the tree widget
        """
        #invisible root item
        rootItem = self.treeWidget.invisibleRootItem()
        #database item
        dbItem = rootItem.child(0)
        if dbItem:
            dbItem.setCheckState(1, 0)
            dbItem.setCheckState(2, 0)
        
    @pyqtSlot(bool)
    def on_saveButton_clicked(self):
        """
        Saves the profile file
        """
        if self.jsonCombo.currentIndex() == 0:
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Select a profile model!'))
            return
        else:
            profile = self.jsonCombo.currentText()
            
        path = os.path.join(self.folder, profile+'.json')
        
        try:
            with open(path, 'w') as outfile:
                json.dump(self.makeProfileDict(), outfile, sort_keys=True, indent=4)
        except Exception as e:
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Problem saving file! \n')+':'.join(e.args))
            return
            
        QMessageBox.warning(self, self.tr('Warning!'), self.tr('Profile saved successfully!'))
    
    @pyqtSlot(bool)
    def on_closeButton_clicked(self):
        """
        Closes the dialog
        """
        self.close()
    
    @pyqtSlot(bool)
    def on_deletePushButton_clicked(self):
        """
        Deletes the select profile
        :return:
        """
        if self.jsonCombo.currentIndex() != 0:
            profileName = self.jsonCombo.currentText()
            if QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to remove profile ')+profileName+'?', QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
                return
            try:
                os.remove(os.path.join(self.folder,profileName+'.json'))
            except Exception as e:
                QMessageBox.warning(self, self.tr('Warning!'), self.tr('Problem deleting profile! \n')+':'.join(e.args))
                return
            self.getProfiles()
            self.setInitialState()