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
        
        self.db = None
        
        self.factory = SqlGeneratorFactory()
        self.gen = self.factory.createSqlGenerator(True)
        self.utils = Utils()

        self.folder = os.path.join(os.path.dirname(__file__), 'profiles')
        self.jsonCombo.addItems(self.getProfiles())
        self.setInitialState()
        
    def __del__(self):
        if self.db:
            self.db.close()
            self.db = None

    def getProfiles(self):
        ret = []
        for root, dirs, files in os.walk(self.folder):
            for file in files:
                ext = file.split('.')[-1]
                if ext == 'json':
                    ret.append(file.split('.')[0])
        return ret

    def setInitialState(self):
        self.treeWidget.clear()

        if self.jsonCombo.count() == 0:
            currentPath = os.path.dirname(__file__)
            if self.versionCombo.currentText() == '2.1.3':
                edgvPath = os.path.join(currentPath, '..', 'DbTools', 'SpatialiteTool', 'template', '213', 'seed_edgv213.sqlite')
            else:
                edgvPath = os.path.join(currentPath, '..', 'DbTools', 'SpatialiteTool', 'template', '30', 'seed_edgv30.sqlite')

            self.db = QSqlDatabase("QSQLITE")
            self.db.setDatabaseName(edgvPath)
            if not self.db.open():
                #QgsMessageLog.logMessage(self.db.lastError().text(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                print db.lastError().text()

            self.populateTreeWidget()

            self.db.close()
        else:
            profile = os.path.join(self.folder, self.jsonCombo.currentText()+'.json')
            self.readJsonFile(profile)
        
    def createItem(self, parent, text):
        item = QtGui.QTreeWidgetItem(parent)
        item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
        item.setCheckState(1, QtCore.Qt.Unchecked)
        item.setCheckState(2, QtCore.Qt.Unchecked)
        item.setCheckState(3, QtCore.Qt.Unchecked)
        item.setCheckState(4, QtCore.Qt.Unchecked)
        item.setCheckState(5, QtCore.Qt.Unchecked)
        item.setText(0, text)
        return item
            
    def populateTreeWidget(self):
        sql = self.gen.getTablesFromDatabase()
        query = QSqlQuery(sql, self.db)
        
        #invisible root item
        rootItem = self.treeWidget.invisibleRootItem()
        #database item
        dbItem = self.createItem(rootItem, 'database')
        
        self.categories = dict()
        while query.next():
            #table name
            tableName = query.value(0)
            
            #proceed only for edgv tables
            if tableName.split("_")[-1] == "p" or tableName.split("_")[-1] == "l" or tableName.split("_")[-1] == "a":
                layerName = tableName
                split = tableName.split('_')
                
                if len(split) < 2:
                    continue
                
                schema = split[0]
                category = split[1]
                if schema not in self.categories.keys():
                    self.categories[schema] = dict()
                    
                    #schema item
                    schemaItem = self.createItem(dbItem, schema)
                    
                if category not in self.categories[schema].keys():
                    self.categories[schema][category] = []
                    
                    #category item
                    categoryItem = self.createItem(schemaItem, category)

                if layerName not in self.categories[schema][category]:
                    self.categories[schema][category].append(layerName)
                    
                    #layer item
                    layerItem = self.createItem(categoryItem, layerName)
                    
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
                 
        profileDict['database'] = permissions   
        return profileDict
    
    def readJsonFile(self, filename):
        try:
            file = open(filename, 'r')
            data = file.read()
            profileDict = json.loads(data)
        except:
            profileDict = dict()
            
        #invisible root item
        rootItem = self.treeWidget.invisibleRootItem()
        #database item
        dbItem = self.createItem(rootItem, 'database')

        permissions = profileDict['database']
        self.createChildrenItems(dbItem, permissions)
                                        
    def createChildrenItems(self, parent, mydict):
        #permissions
        lista = ['read', 'write', 'create', 'drop', 'super']
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
        elif key == 'create':
            item.setCheckState(3, int(mydict[key]))
        elif key == 'drop':
            item.setCheckState(4, int(mydict[key]))
        elif key == 'super':
            item.setCheckState(5, int(mydict[key]))
    
    def getItemCheckState(self, item):
        ret = dict()
        ret['read'] = str(item.checkState(1))
        ret['write'] = str(item.checkState(2))
        ret['create'] = str(item.checkState(3))
        ret['drop'] = str(item.checkState(4))
        ret['super'] = str(item.checkState(5))
        return ret
        
    @pyqtSlot(int)
    def on_versionCombo_currentIndexChanged(self):
         self.setInitialState()

    @pyqtSlot(int)
    def on_jsonCombo_currentIndexChanged(self):
         self.setInitialState()

    @pyqtSlot(bool)
    def on_saveButton_clicked(self):
        if not self.jsonCombo.currentText():
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Fill the profile name!'))
            return
        else:
            profile = self.jsonCombo.currentText()
            
        path = os.path.join(self.folder, profile+'.json')
        
        with open(path, 'w') as outfile:
            json.dump(self.makeProfileDict(), outfile)
            if self.jsonCombo.findText(profile) == -1:
                self.jsonCombo.addItem(profile)
