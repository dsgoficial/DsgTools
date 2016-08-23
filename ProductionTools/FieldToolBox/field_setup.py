# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                             -------------------
        begin                : 2016-05-07
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Brazilian Army - Geographic Service Bureau
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
import os, json

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, Qt
from PyQt4.QtGui import QMessageBox, QCheckBox, QButtonGroup, QItemDelegate, QDialog, QMessageBox, QListWidget, QListWidgetItem
from PyQt4.QtGui import QFileDialog, QTreeWidgetItem, QTableWidget, QTableWidgetItem, QStyledItemDelegate, QComboBox, QMenu, QLineEdit
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from PyQt4.QtSql import QSqlDatabase, QSqlQuery

# QGIS imports
from qgis.core import QgsMapLayer, QgsGeometry, QgsMapLayerRegistry

#DsgTools imports
from DsgTools.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.QmlTools.qmlParser import QmlParser
import acquisition_tools

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'field_setup.ui'))

class FieldSetup(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """
        Constructor
        """
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.abstractDb = None
        self.abstractDbFactory = DbFactory()
        self.setupUi(self)
        
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.createMenu)        
        
        self.geomClasses = []
        
        self.folder = os.path.join(os.path.dirname(__file__), 'FieldSetupConfigs')
    
    def __del__(self):
        if self.abstractDb:
            del self.abstractDb
            self.abstractDb = None
        
    def getDbInfo(self):
        '''
        Gather information about the database and QML's used
        '''
        currentPath = os.path.dirname(__file__)
        if self.versionCombo.currentText() == '2.1.3':
            edgvPath = os.path.join(currentPath, '..', '..', 'DbTools', 'SpatialiteTool', 'template', '213', 'seed_edgv213.sqlite')
            sqlPath = os.path.join(currentPath, '..', '..', 'DbTools', 'PostGISTool', 'sqls', '213', 'edgv213.sql')
        elif self.versionCombo.currentText() == 'FTer_2a_Ed':
            edgvPath = os.path.join(currentPath, '..', '..', 'DbTools', 'SpatialiteTool', 'template', 'FTer_2a_Ed', 'seed_edgvfter_2a_ed.sqlite')
            sqlPath = os.path.join(currentPath, '..', '..', 'DbTools', 'PostGISTool', 'sqls', 'FTer_2a_Ed', 'edgvFter_2a_Ed.sql')
            
        self.notNullDict = acquisition_tools.sqlParser(sqlPath, True)

        self.abstractDb = self.abstractDbFactory.createDbFactory('QSQLITE')
        if not self.abstractDb:
            QtGui.QMessageBox.warning(self, self.tr('Warning!'), self.tr('A problem occurred! Check log for details.'))
            return
        self.abstractDb.connectDatabase(edgvPath)

        try:
            self.abstractDb.checkAndOpenDb()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(e.args[0], 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
        self.qmlDir = self.abstractDb.getQmlDir()
    
    def populateClassList(self):
        '''
        Populates the class list with all geometric classes from database
        '''
        self.classListWidget.clear()
        self.geomClasses = []
        try:
            self.geomClasses = self.abstractDb.listGeomClassesFromDatabase()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(e.args[0], 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
        self.classListWidget.addItems(self.geomClasses)
        
    def on_filterEdit_textChanged(self, text):
        '''
        Sets a filter to only show desired classes
        '''
        classes = [edgvClass for edgvClass in self.geomClasses if text in edgvClass]
        self.classListWidget.clear()
        self.classListWidget.addItems(classes)
        self.classListWidget.sortItems()        
    
    @pyqtSlot(int)
    def on_versionCombo_currentIndexChanged(self, clear=True):
        '''
        Updates the class list when EDGV version is changed
        '''
        if self.versionCombo.currentIndex() <> 0:
            self.getDbInfo()
            self.populateClassList()
            if clear:
                self.treeWidget.invisibleRootItem().takeChildren()
        else:
            self.classListWidget.clear()
    
    def clearAttributeTableWidget(self):
        '''
        Clears the attribute table widget. 
        '''
        for i in range(self.attributeTableWidget.rowCount(),-1,-1):
            self.attributeTableWidget.removeRow(i)
    
    def makeValueRelationDict(self, table, codes):
        '''
        Makes a query to obtain a dictionary with code names and related codes 
        '''
        ret = dict()

        in_clause = '(%s)' % ",".join(map(str, codes))
        if self.abstractDb.db.driverName() == 'QPSQL':
            sql = 'select code, code_name from dominios.%s where code in %s' % (table, in_clause)
        elif self.abstractDb.db.driverName() == 'QSQLITE':
            sql = 'select code, code_name from dominios_%s where code in %s' % (table, in_clause)

        query = QSqlQuery(sql, self.abstractDb.db)
        while query.next():
            code = query.value(0)
            code_name = query.value(1)
            ret[code_name] = code

        return ret    
    
    @pyqtSlot(int)
    def on_classListWidget_currentRowChanged(self,row):
        '''
        Creates the attribute table according to the QML file.
        Creates specific widgets for each attribute, which can be a QCombobox, a QLineEdit or a QListWidget.
        All mandatory attributes are shown in RED.
        '''
        #reset the button name
        self.buttonNameLineEdit.setText('')
        #clear the attribute table
        self.clearAttributeTableWidget()
        
        if not self.classListWidget.item(row):
            return
        
        fullTableName = self.classListWidget.item(row).text()
        #getting schema name and table name
        schemaName, tableName = self.abstractDb.getTableSchema(fullTableName)
        #getting the QML path
        qmlPath = os.path.join(self.qmlDir,tableName+'.qml')
        
        qml = QmlParser(qmlPath)
        qmlDict = qml.getDomainDict()
        count = 0
        #creating the items in the attribute table, not null attributes must be in red
        if fullTableName in self.notNullDict.keys():
            for attr in self.notNullDict[fullTableName]:
                self.attributeTableWidget.insertRow(count)
                item = QTableWidgetItem()
                item.setText(attr)
                item.setBackgroundColor(Qt.red)
                self.attributeTableWidget.setItem(count, 0, item)
                #creating the specific cell widget. It can be a QCombobox, a QLineEdit or a QListWidget
                self.createCellWidget(qmlDict, attr, count)
                count+=1
            
        for attr in qmlDict.keys():
            #analyzing attributes not yet created in the table
            if fullTableName in self.notNullDict.keys() and attr in self.notNullDict[fullTableName]:
                continue

            self.attributeTableWidget.insertRow(count)
            item = QTableWidgetItem()
            item.setText(attr)
            self.attributeTableWidget.setItem(count, 0, item)
            #creating the specific cell widget. It can be a QCombobox, a QLineEdit or a QListWidget
            self.createCellWidget(qmlDict, attr, count)
            count+=1
                        
    def createCellWidget(self, qmlDict, attr, count):
        '''
        Creates specific widgets for each attribute, which can be a QCombobox, a QLineEdit or a QListWidget.
        '''
        if attr in qmlDict.keys():
            #case the type is dict the cell widget must be a combobox
            if isinstance(qmlDict[attr],dict):
                comboItem = QComboBox()
                comboItem.addItems(qmlDict[attr].keys())
                self.attributeTableWidget.setCellWidget(count, 1, comboItem)
            #case the type is tuple the cell widget must be a listwidget
            if isinstance(qmlDict[attr],tuple):
                (table, filterKeys) = qmlDict[attr]
                #getting the value relation dictionary used to make the listwidget
                valueRelation = self.makeValueRelationDict(table, filterKeys)
                list = QListWidget()
                for key in valueRelation.keys():
                    listItem = QListWidgetItem(key)
                    listItem.setCheckState(Qt.Unchecked)
                    list.addItem(listItem)
                self.attributeTableWidget.setCellWidget(count, 1, list)
        #this is the normal case, a simple lineedit
        else:
            textItem = QLineEdit()
            self.attributeTableWidget.setCellWidget(count, 1, textItem)
    
    @pyqtSlot(bool)
    def on_addUpdatePushButton_clicked(self):
        '''
        Creates a new reclassification button ready to be used
        '''
        #checking if the button name is defined
        if self.buttonNameLineEdit.text() == '':
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Enter a button name!'))
            return
        
        # invisible root item
        rootItem = self.treeWidget.invisibleRootItem()

        # class row in the classListWidget
        classRow = self.classListWidget.currentRow()

        schemaName, tableName = self.abstractDb.getTableSchema(self.classListWidget.item(classRow).text())
        category = schemaName + '_' + tableName.split('_')[0]

        # creating items in tree
        buttonInTree = False
        leafChildInTree = False
        leafInTree = False
        for i in range(rootItem.childCount()):
            leaf = rootItem.child(i)
            if leaf.text(0) == category:
                leafInTree = True
                item = leaf
                for j in range(leaf.childCount()):
                    leafChild = leaf.child(j)
                    if leafChild.text(0) == self.classListWidget.item(classRow).text():
                        leafChildInTree = True
                        item = leafChild
                        for k in range(leafChild.childCount()):
                            leafGrandson = leafChild.child(k)
                            if leafGrandson.text(0) == self.buttonNameLineEdit.text():
                                buttonItem = leafGrandson
                                buttonItem.setText(0, self.buttonNameLineEdit.text())
                                buttonInTree = True
                                break
        if not leafInTree:
            item = QTreeWidgetItem(rootItem)
            item.setText(0, category)
        if not leafChildInTree:
            item = QTreeWidgetItem(item)
            item.setText(0, self.classListWidget.item(classRow).text())
        if not buttonInTree:        
            # item that will be used to create the button
            buttonItem = QTreeWidgetItem(item)
            buttonItem.setText(0, self.buttonNameLineEdit.text())

        qmlPath = os.path.join(self.qmlDir, tableName+'.qml')
        qml = QmlParser(qmlPath)
        # qml dict for this class (tableName)
        qmlDict = qml.getDomainDict()
        
        # accessing the attribute name and widget (QComboBox or QListWidget depending on data type)
        for i in range(self.attributeTableWidget.rowCount()):
            attribute = self.attributeTableWidget.item(i, 0).text()
            
            # this guy is a QComboBox or a QListWidget
            widgetItem = self.attributeTableWidget.cellWidget(i, 1)
            
            if attribute in qmlDict.keys():
                if isinstance(qmlDict[attribute], dict):
                    value = qmlDict[attribute][widgetItem.currentText()]
                elif isinstance(qmlDict[attribute], tuple):
                    (table, filterKeys) = qmlDict[attribute]
                    valueRelation = self.makeValueRelationDict(table, filterKeys)
                    values = []
                    for i in range(widgetItem.count()):
                        if widgetItem.item(i).checkState() == Qt.Checked:
                            key = widgetItem.item(i).text()
                            values.append(valueRelation[key])
                    value = '{%s}' % ','.join(map(str, values))
            else:
                value = widgetItem.text() 
            
            #sweep tree for attribute
            attrFound = False
            for i in range(buttonItem.childCount()):
                attrItem = buttonItem.child(i)
                if attribute == attrItem.text(0):
                    attrFound = True
                    attributeItem = attrItem
                    break
            if not attrFound:
                attributeItem = QTreeWidgetItem(buttonItem)
                attributeItem.setText(0, attribute)
            attributeItem.setText(1, value)
            
    def recreateAttributeTable(self, buttonItem):
        '''
        Making the attribute table with the actual values present in the tree widget
        '''
        # class row in the classListWidget
        classRow = self.classListWidget.currentRow()

        schemaName, tableName = self.abstractDb.getTableSchema(self.classListWidget.item(classRow).text())

        qmlPath = os.path.join(self.qmlDir, tableName+'.qml')
        qml = QmlParser(qmlPath)
        # qml dict for this class (tableName)
        qmlDict = qml.getDomainDict()

        for i in range(buttonItem.childCount()):
            attrItem = buttonItem.child(i)
            attribute = attrItem.text(0)
            value = attrItem.text(1)
            # accessing the attribute name and widget (QComboBox or QListWidget depending on data type)
            for i in range(self.attributeTableWidget.rowCount()):
                if attribute <> self.attributeTableWidget.item(i, 0).text():
                    continue
                
                # this guy is a QComboBox or a QListWidget
                widgetItem = self.attributeTableWidget.cellWidget(i, 1)
    
                if attribute in qmlDict.keys():
                    # this guy is a QComboBox here
                    if isinstance(qmlDict[attribute], dict):
                        for i in range(widgetItem.count()):
                            text = widgetItem.itemText(i)
                            if qmlDict[attribute][text] == value:
                                widgetItem.setCurrentIndex(i)
                    # this guy is a QListWidget here
                    if isinstance(qmlDict[attribute], tuple):
                        #getting just the values
                        multivalues = value.replace('{', '').replace('}', '').split(',')
                        (table, filterKeys) = qmlDict[attribute]
                        valueRelation = self.makeValueRelationDict(table, filterKeys)
                        #marking just the correct values
                        for i in range(widgetItem.count()):
                            text = widgetItem.item(i).text()
                            if str(valueRelation[text]) in multivalues:
                                widgetItem.item(i).setCheckState(Qt.Checked)
                else:
                    widgetItem.setText(value)
            
    def makeReclassificationDict(self):
        '''
        Makes the reclassification dictionary used to perform the actual reclassification
        '''
        reclassificationDict = dict()
        
        reclassificationDict['version'] = self.versionCombo.currentText()
        
        #invisible root item
        rootItem = self.treeWidget.invisibleRootItem()

        #class item
        for i in range(rootItem.childCount()):
            categoryItem = rootItem.child(i)
            reclassificationDict[categoryItem.text(0)] = dict()
            for j in range(categoryItem.childCount()):
                classItem = categoryItem.child(j)
                reclassificationDict[categoryItem.text(0)][classItem.text(0)] = dict()
                for k in range(classItem.childCount()):
                    buttonItem = classItem.child(k)
                    reclassificationDict[categoryItem.text(0)][classItem.text(0)][buttonItem.text(0)] = dict()
                    for l in range(buttonItem.childCount()):
                        attributeItem = buttonItem.child(l)
                        reclassificationDict[categoryItem.text(0)][classItem.text(0)][buttonItem.text(0)][attributeItem.text(0)] = attributeItem.text(1)
        return reclassificationDict
    
    def readJsonFile(self, filename):
        '''
        Reads the json configuration file
        '''
        try:
            file = open(filename, 'r')
            data = file.read()
            reclassificationDict = json.loads(data)
            file.close()
            return reclassificationDict
        except:
            return dict()    
    
    def loadReclassificationConf(self, reclassificationDict):
        '''
        Makes the treewidget using the reclassification dictionary obtained from the configuration file
        '''
        index = self.versionCombo.findText(reclassificationDict['version'])
        self.versionCombo.setCurrentIndex(index)
        
        self.treeWidget.clear()
        
        #invisible root item
        rootItem = self.treeWidget.invisibleRootItem()
        
        for category in reclassificationDict.keys():
            if category == 'version':
                continue
            categoryItem = QTreeWidgetItem(rootItem)
            categoryItem.setText(0, category)
            for edgvClass in reclassificationDict[category].keys():
                classItem = QTreeWidgetItem(categoryItem)
                classItem.setText(0, edgvClass)
                for button in reclassificationDict[category][edgvClass].keys():
                    buttonItem = QTreeWidgetItem(classItem)
                    buttonItem.setText(0, button)
                    for attribute in reclassificationDict[category][edgvClass][button].keys():
                        attributeItem = QTreeWidgetItem(buttonItem)
                        attributeItem.setText(0, attribute)
                        attributeItem.setText(1, reclassificationDict[category][edgvClass][button][attribute])
                    
    def on_treeWidget_currentItemChanged(self, previous, current):
        '''
        Adjusts the button visualization according to the selected item in the tree widget
        '''
        self.filterEdit.setText('')
        depth = self.depth(previous)
        if depth == 1:
            self.buttonNameLineEdit.setText('')
        elif depth == 2:
            classItems = self.classListWidget.findItems(previous.text(0), Qt.MatchExactly)
            self.classListWidget.setCurrentItem(classItems[0])
            self.buttonNameLineEdit.setText('')
        elif depth == 3:
            classItems = self.classListWidget.findItems(previous.parent().text(0), Qt.MatchExactly)
            self.classListWidget.setCurrentItem(classItems[0])
            self.buttonNameLineEdit.setText(previous.text(0))
            self.recreateAttributeTable(previous)
        elif depth == 4:
            classItems = self.classListWidget.findItems(previous.parent().parent().text(0), Qt.MatchExactly)
            self.classListWidget.setCurrentItem(classItems[0])
            self.buttonNameLineEdit.setText(previous.parent().text(0))
            self.recreateAttributeTable(previous.parent())
        
    def depth(self, item):
        '''
        Calculates the item depth in the tree widget
        '''
        #calculates the depth of the item
        depth = 0
        while item is not None:
            item = item.parent()
            depth += 1
        return depth   
    
    def createMenu(self, position):
        '''
        Creates a menu that allows button removal by the user
        '''
        menu = QMenu()
        
        item = self.treeWidget.itemAt(position)

        if item and self.depth(item) < 4:
            menu.addAction(self.tr('Remove child node'), self.removeChildNode)
        menu.exec_(self.treeWidget.viewport().mapToGlobal(position))

    def removeChildNode(self):
        '''
        Removes a tree widget item and all its children
        '''
        item = self.treeWidget.currentItem()
        item.parent().removeChild(item)     
        
    @pyqtSlot(bool)
    def on_loadButton_clicked(self):
        '''
        Loads a configuration file
        '''
        self.loadedFileEdit.setText('')
        
        filename = QFileDialog.getOpenFileName(self, self.tr('Open reclassification setup file'), self.folder, self.tr('Reclassification Setup Files (*.reclas)'))
        if not filename:
            return
        #makes the dictionary used to create the tree widget
        reclassificationDict = self.readJsonFile(filename)
        #assembles the tree widget based on the dictionary
        self.loadReclassificationConf(reclassificationDict)
        
        self.loadedFileEdit.setText(filename)
        
    @pyqtSlot()    
    def on_buttonBox_accepted(self):
        '''
        Saves the configuration work done so far.
        '''
        if QMessageBox.question(self, self.tr('Question'), self.tr('Do you want to save this reclassification setup?'), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
            return
            
        filename = QFileDialog.getSaveFileName(self, self.tr('Save reclassification setup file'), self.folder, self.tr('Reclassification Setup Files (*.reclas)'))
        if not filename:
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Define a name for the reclassification setup file!'))
            return
        
        if '.reclas' not in filename:
            filename = filename + '.reclas'

        reclassificationDict = self.makeReclassificationDict()
        with open(filename, 'w') as outfile:
            json.dump(reclassificationDict, outfile, sort_keys=True, indent=4)
            
        QMessageBox.information(self, self.tr('Information!'), self.tr('Reclassification setup file saved successfully!'))
