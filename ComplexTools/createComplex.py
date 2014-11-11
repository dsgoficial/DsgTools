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

from PyQt4.QtSql import QSqlQueryModel,QSqlDatabase,QSqlQuery

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
        
        self.selectedFeaturesTreeWidget.setDragDropMode(QAbstractItemView.DragDrop)
        self.selectedFeaturesTreeWidget.setDefaultDropAction(Qt.MoveAction)
        self.componentFeaturesTreeWidget.setDragDropMode(QAbstractItemView.DragDrop)
        self.componentFeaturesTreeWidget.setDefaultDropAction(Qt.MoveAction)
        
        self.populateSelectedFeaturesWidget()
        
    def setFile(self):
        fd = QFileDialog()
        self.filename = fd.getOpenFileName(filter='*.sqlite')
        if self.filename <> "":
            self.fileLineEdit.setText(self.filename)
            
        self.loadDb()

    def loadDb(self):
        self.filename = self.fileLineEdit.text()
        
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.filename)
        self.db.open()
        
        self.populateComboBox()
        
    def updateTableView(self):
        table = self.comboBox.currentText()
        
        projectModel = QSqlQueryModel()
        projectModel.setQuery("select * from "+table,self.db)
        
        self.tableView.setModel(projectModel)
        self.tableView.show()
        
    def populateComboBox(self):
        self.comboBox.clear()
        
        query = QSqlQuery("SELECT name FROM sqlite_master WHERE type='table'", self.db)
        while query.next():
            name = query.value(0)
            if 'Complexo' in name:
                self.comboBox.addItem(query.value(0))

    def populateSelectedFeaturesWidget(self):
        self.layers = self.iface.mapCanvas().layers()
        for layer in self.layers:
            selectedFeatures = layer.selectedFeatures()
            if len(selectedFeatures) == 0:
                continue
            item = QTreeWidgetItem(self.selectedFeaturesTreeWidget)
            item.setText(0,layer.name())
            for feature in selectedFeatures:
                featureItem = QTreeWidgetItem(item)
                featureItem.setText(0,str(feature.id()))
                
    def selectAllFeatures(self):
        root = self.selectedFeaturesTreeWidget.invisibleRootItem()
        children = root.takeChildren()
        if len(children) > 0:
            for child in children:
                self.componentFeaturesTreeWidget.addTopLevelItem(child)
    
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
                    
                if item.parent().childCount() == 0:
                    layerIndex = root.indexOfChild(item.parent())
                    root.takeChild(layerIndex)
            else:#layer selected
                layerIndex = root.indexOfChild(item)
                layerItem = root.takeChild(layerIndex)

    def deselectOneFeature(self):
        items = self.componentFeaturesTreeWidget.selectedItems()
        for i in range(len(items)):
            item = self.componentFeaturesTreeWidget.takeTopLevelItem(i)
            self.selectedFeaturesTreeWidget.addTopLevelItem(item)

    def deselectAllFeatures(self):
        self.selectedFeaturesTreeWidget.clear()
        self.componentFeaturesTreeWidget.clear()
        self.populateSelectedFeaturesWidget()
    
