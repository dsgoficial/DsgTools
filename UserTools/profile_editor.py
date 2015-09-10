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
        
        self.factory = SqlGeneratorFactory()
        self.gen = self.factory.createSqlGenerator(True)
        self.utils = Utils()
        
        self.db = None
        
        self.setInitialState()      
        
    def setInitialState(self):
        if self.db:
            self.db.close()
        
        currentPath = os.path.dirname(__file__)
        if self.comboBox.currentText() == '2.1.3':
            edgvPath = os.path.join(currentPath, '..', 'DbTools', 'SpatialiteTool', 'template', '213', 'seed_edgv213.sqlite')
        else:
            edgvPath = os.path.join(currentPath, '..', 'DbTools', 'SpatialiteTool', 'template', '30', 'seed_edgv30.sqlite')

        self.db = QSqlDatabase("QSQLITE")
        self.db.setDatabaseName(edgvPath)
        if not self.db.open():
            #QgsMessageLog.logMessage(self.db.lastError().text(), "DSG Tools Plugin", QgsMessageLog.CRITICAL)
            print self.db.lastError().text()
            
        self.populateTreeWidget()
        
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
        dbItem = self.createItem(rootItem, self.tr('Database'))
        
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
        permissions = self.getItemCheckState(dbItem)
        
        schema_count = dbItem.childCount()
        for i in range(schema_count):
            schemaItem = dbItem.child(i)
            permissions[schemaItem.text(0)] = self.getItemCheckState(schemaItem)
            category_count = schemaItem.childCount()
            for j in range(category_count):
                categoryItem = schemaItem.child(j)
                permissions[schemaItem.text(0)][categoryItem.text(0)] = self.getItemCheckState(categoryItem)
                layer_count = categoryItem.childCount()
                for k in range(layer_count):
                    layerItem = categoryItem.child(k)
                    permissions[schemaItem.text(0)][categoryItem.text(0)][layerItem.text(0)] = self.getItemCheckState(layerItem)
                 
        profileDict['database'] = permissions   
        return profileDict
    
    def getItemCheckState(self, item):
        ret = dict()
        ret['read'] = str(item.checkState(1))
        ret['write'] = str(item.checkState(2))
        ret['create'] = str(item.checkState(3))
        ret['drop'] = str(item.checkState(4))
        ret['super'] = str(item.checkState(5))
        return ret
        
    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self):
         self.setInitialState()
         
    @pyqtSlot(bool)
    def on_saveButton_clicked(self):
        if not self.profileEdit.text():
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('Fill the profile name!'))
            return
        else:
            profile = self.profileEdit.text()
            
        path = os.path.join(os.path.dirname(__file__), profile+'.json')
        
        with open(path, 'w') as outfile:
            json.dump(self.makeProfileDict(), outfile)
