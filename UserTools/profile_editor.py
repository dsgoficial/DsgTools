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
import os

# Qt imports
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtSql import QSqlDatabase, QSqlQuery

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.UserTools.create_profile import CreateProfile

import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'profile_editor.ui'))

class ProfileEditor(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(ProfileEditor, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.treeWidget.setColumnWidth(0, 400)
        
        self.db = None
        
        self.factory = SqlGeneratorFactory()
        self.gen = self.factory.createSqlGenerator(True)
        self.utils = Utils()

        self.folder = os.path.join(os.path.dirname(__file__), 'profiles')
        self.getProfiles()
        self.setInitialState()
        
    def getProfiles(self):
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

    def setInitialState(self):
        self.treeWidget.clear()
        self.treeWidget.setSortingEnabled(False)
        if self.jsonCombo.count() == 0 or self.jsonCombo.currentIndex() == 0:
            self.treeWidget.clear()
            return
        else:
            profile = os.path.join(self.folder, self.jsonCombo.currentText()+'.json')
            self.readJsonFile(profile)
#         self.treeWidget.setSortingEnabled(True)
        self.treeWidget.sortByColumn(0,QtCore.Qt.AscendingOrder)
        
    def createItem(self, parent, text):
        item = QtGui.QTreeWidgetItem(parent)
        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(1, QtCore.Qt.Unchecked)
        item.setCheckState(2, QtCore.Qt.Unchecked)
        item.setText(0, text)
        return item
    
    def makeProfileDict(self):
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
        try:
            file = open(filename, 'r')
            data = file.read()
            profileDict = json.loads(data)
            self.parent = profileDict.keys()[0]
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
        if key == 'read':
            item.setCheckState(1, int(mydict[key]))
        elif key == 'write':
            item.setCheckState(2, int(mydict[key]))
    
    def getItemCheckState(self, item):
        ret = dict()
        ret['read'] = str(item.checkState(1))
        ret['write'] = str(item.checkState(2))
        return ret
        
    @pyqtSlot(int)
    def on_jsonCombo_currentIndexChanged(self):
        self.setInitialState()
    
    @pyqtSlot(bool)
    def on_createButton_clicked(self):
        dlg = CreateProfile()
        result = dlg.exec_()
        if result:
            self.getProfiles()
            
    @pyqtSlot(bool)
    def on_clearButton_clicked(self):
        #invisible root item
        rootItem = self.treeWidget.invisibleRootItem()
        #database item
        dbItem = rootItem.child(0)
        if dbItem:
            dbItem.setCheckState(1, 0)
            dbItem.setCheckState(2, 0)
        
    @pyqtSlot(bool)
    def on_saveButton_clicked(self):
        if not self.jsonCombo.currentText():
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Fill the profile name!'))
            return
        else:
            profile = self.jsonCombo.currentText()
            
        path = os.path.join(self.folder, profile+'.json')
        
        try:
            with open(path, 'w') as outfile:
                json.dump(self.makeProfileDict(), outfile, sort_keys=True, indent=4)
        except:
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Problem saving file!'))
            
        QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Profile saved successfully!'))
    
    @pyqtSlot(bool)
    def on_closeButton_clicked(self):
        self.close()