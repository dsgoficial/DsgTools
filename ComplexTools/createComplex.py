# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2014-11-08
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Luiz Andrade - Cartographic Engineer @ Brazilian Army
        email                : luiz.claudio@dsg.eb.mil.br
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from PyQt4.QtXml import *

from PyQt4.QtSql import QSqlQueryModel, QSqlTableModel,QSqlDatabase,QSqlQuery

from ui_createComplex import Ui_Dialog

class CreateComplexDialog(QDialog, Ui_Dialog):
    def __init__(self, iface):
        """Constructor.
        """
        QDialog.__init__( self )
        self.setupUi( self )
        
        self.iface = iface
        
        QObject.connect(self.filePushButton, SIGNAL(("clicked()")), self.setFile)
        QObject.connect(self.fileLineEdit, SIGNAL(("editingFinished()")), self.loadDb)
        QObject.connect(self.comboBox, SIGNAL("currentIndexChanged (int)"), self.updateTableView)
        
        QObject.connect(self.selectAllButton, SIGNAL(("clicked()")), self.selectAllFeatures)
        QObject.connect(self.selectOneButton, SIGNAL(("clicked()")), self.selectOneFeature)
        QObject.connect(self.deselectOneButton, SIGNAL(("clicked()")), self.deselectOneFeature)
        QObject.connect(self.deselectAllButton, SIGNAL(("clicked()")), self.deselectAllFeatures)
        QObject.connect(self.addRow, SIGNAL(("clicked()")), self.addComplex)
        QObject.connect(self.removeRow, SIGNAL(("clicked()")), self.removeComplex)
        
        QObject.connect(self.okButton, SIGNAL(("clicked()")), self.accept)
        QObject.connect(self.cancelButton, SIGNAL(("clicked()")), self.reject)
        
        self.populateSelectedFeaturesWidget()
        
        self.db = None

    def reject(self):
        if self.db:
            self.db.close()
        self.done(0)
             
    def accept(self): 
        #getting the selected rows           
        selectionModel = self.tableView.selectionModel()
        #getting the index of the column named OGC_FID
        selectedRows = selectionModel.selectedRows(self.projectModel.fieldIndex("OGC_FID"))
        # Just one row each time
        if len(selectedRows) != 1:
            QMessageBox.warning(self.iface.mainWindow(), "Warning!", "Please, select only one row.")
            return
        
        #complex index entered by the user or calculated using uuid4
        complexId = int(selectedRows[0].data())

        #iterating over the component features tree            
        root = self.componentFeaturesTreeWidget.invisibleRootItem()
        for i in range(root.childCount()):
            #getting the layer tree item
            layerItem = root.child(i)
            for layer in self.iface.mapCanvas().layers():
                #checking the layer name
                if layer.name() == layerItem.text(0):
                    #getting the foreign column index that will be updated
                    fieldIndex = [i for i in range(len(layer.dataProvider().fields())) if "id_complexo" in layer.dataProvider().fields()[i].name()]
                    for j in range(layerItem.childCount()):
                        #getting the feature tree item
                        featureItem = layerItem.child(j)
                        #feature id that will be updated
                        id = featureItem.text(0)
                        #attribute pair that will be changed
                        attrs = {fieldIndex[0]:complexId}
                        #actual update in the database
                        layer.dataProvider().changeAttributeValues({int(id):attrs})
            
        #commmiting all pending changes
        if not self.projectModel.submitAll():
            print self.projectModel.lastError().text()

    def setFile(self):
        #obtaining the database file name
        fd = QFileDialog()
        self.filename = fd.getOpenFileName(filter='*.sqlite')
        if self.filename <> "":
            self.fileLineEdit.setText(self.filename)
            
        self.loadDb()

    def loadDb(self):
        #opening the database
        self.filename = self.fileLineEdit.text()
        
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.filename)
        self.db.open()
        
        self.populateComboBox()
        
    def updateTableView(self):
        #table name
        table = self.comboBox.currentText()
        
        ##setting the model in the view
        self.projectModel = QSqlTableModel(None, self.db)
        self.projectModel.setTable(table)
        #manual commit rule
        self.projectModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.projectModel.select()
        
        self.tableView.setModel(self.projectModel)
        self.tableView.show()
        
    def addComplex(self):
        self.projectModel.insertRow(self.projectModel.rowCount())
        
    def removeComplex(self):
        selectionModel = self.tableView.selectionModel()
        selectedRows = selectionModel.selectedRows()
        for row in selectedRows:
            self.projectModel.removeRow(row.row())
        
    def populateComboBox(self):
        #getting all complex tables
        self.comboBox.clear()
        
        query = QSqlQuery("SELECT name FROM sqlite_master WHERE type='table'", self.db)
        while query.next():
            name = query.value(0)
            if 'Complexo' in name:
                self.comboBox.addItem(query.value(0))

    def populateSelectedFeaturesWidget(self):
        #getting the selected features
        self.layers = self.iface.mapCanvas().layers()
        for layer in self.layers:
            selectedFeatures = layer.selectedFeatures()
            if len(selectedFeatures) == 0:
                continue
            #create a layer tree item
            item = QTreeWidgetItem(self.selectedFeaturesTreeWidget)
            item.setText(0,layer.name())
            for feature in selectedFeatures:
                #create a feature item for each feature selected
                featureItem = QTreeWidgetItem(item)
                featureItem.setText(0,str(feature.id()))
                
        self.selectedFeaturesTreeWidget.sortItems(0, Qt.AscendingOrder)
                
    def selectAllFeatures(self):
        #clear both trees
        self.selectedFeaturesTreeWidget.clear()
        self.componentFeaturesTreeWidget.clear()
        self.populateSelectedFeaturesWidget()

        #copying all tree items to the component features tree
        sRoot = self.selectedFeaturesTreeWidget.invisibleRootItem()
        children = sRoot.takeChildren()
        cRoot = self.componentFeaturesTreeWidget.invisibleRootItem()
        cRoot.addChildren(children)
    
        #sorting
        self.componentFeaturesTreeWidget.sortItems(0, Qt.AscendingOrder)

    def selectOneFeature(self):
        root = self.selectedFeaturesTreeWidget.invisibleRootItem()
        items = self.selectedFeaturesTreeWidget.selectedItems()
        for item in items:
            if item.childCount() == 0:#feature selected
                parentItem = item.parent().clone()
                parentItem.takeChildren()
                featureIndex = item.parent().indexOfChild(item)
                featureItem = item.parent().takeChild(featureIndex)
                #insert item in the component tree                
                foundItems = self.componentFeaturesTreeWidget.findItems(parentItem.text(0), Qt.MatchExactly)
                if len(foundItems) == 0:
                    parentItem.addChild(featureItem)
                    self.componentFeaturesTreeWidget.addTopLevelItem(parentItem)
                else:
                    foundItems[0].addChild(featureItem)
                    
            else:#layer selected
                layerIndex = root.indexOfChild(item)
                layerItem = root.takeChild(layerIndex)
                foundItems = self.componentFeaturesTreeWidget.findItems(layerItem.text(0), Qt.MatchExactly)
                if len(foundItems) == 0:
                    self.componentFeaturesTreeWidget.addTopLevelItem(layerItem)
                else:
                    children = layerItem.takeChildren()
                    foundItems[0].addChildren(children)
             
        #cleaning the tree. Item should have at least one child   
        count = root.childCount()
        for i in range(count):
            child = root.child(i)
            if child.childCount() == 0:
                root.removeChild(child)
                
        self.componentFeaturesTreeWidget.sortItems(0, Qt.AscendingOrder)

    def deselectOneFeature(self):
        root = self.componentFeaturesTreeWidget.invisibleRootItem()
        items = self.componentFeaturesTreeWidget.selectedItems()
        for item in items:
            if item.childCount() == 0:#feature selected
                parentItem = item.parent().clone()
                parentItem.takeChildren()
                featureIndex = item.parent().indexOfChild(item)
                featureItem = item.parent().takeChild(featureIndex)
                #insert item in the component tree                
                foundItems = self.selectedFeaturesTreeWidget.findItems(parentItem.text(0), Qt.MatchExactly)
                if len(foundItems) == 0:
                    parentItem.addChild(featureItem)
                    self.selectedFeaturesTreeWidget.addTopLevelItem(parentItem)
                else:
                    foundItems[0].addChild(featureItem)
                    
            else:#layer selected
                layerIndex = root.indexOfChild(item)
                layerItem = root.takeChild(layerIndex)
                foundItems = self.selectedFeaturesTreeWidget.findItems(layerItem.text(0), Qt.MatchExactly)
                if len(foundItems) == 0:
                    self.selectedFeaturesTreeWidget.addTopLevelItem(layerItem)
                else:
                    children = layerItem.takeChildren()
                    foundItems[0].addChildren(children)
          
        #cleaning the tree. Item should have at least one child      
        count = root.childCount()
        for i in range(count):
            child = root.child(i)
            if child.childCount() == 0:
                root.removeChild(child)
                
        self.selectedFeaturesTreeWidget.sortItems(0, Qt.AscendingOrder)

    def deselectAllFeatures(self):
        #clear the component features tree and repopulate the selected features tree
        self.selectedFeaturesTreeWidget.clear()
        self.componentFeaturesTreeWidget.clear()
        self.populateSelectedFeaturesWidget()
    
