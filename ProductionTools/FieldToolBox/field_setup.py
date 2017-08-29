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
from qgis.core import QgsMapLayer, QgsGeometry, QgsMapLayerRegistry, QgsMessageLog

#DsgTools imports
from DsgTools.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.QmlTools.qmlParser import QmlParser
import acquisition_tools

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'field_setup.ui'))

class FieldSetup(QtGui.QDialog, FORM_CLASS):
    def __init__(self, abstractDb, returnDict = False, parent = None):
        """
        Constructor
        """
        super(self.__class__, self).__init__(parent)
        self.abstractDb = abstractDb

        self.setupUi(self)
        self.tableComboBox.setCurrentIndex(-1)  
        self.populateClassList()
        # self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.treeWidget.customContextMenuRequested.connect(self.createMenu)        
        self.edgvVersion = self.abstractDb.getDatabaseVersion()
        if self.abstractDb.db.driverName() == 'QPSQL':
            self.geomTypeDict = self.abstractDb.getGeomTypeDict()
            self.geomDict = self.abstractDb.getGeomDict(self.geomTypeDict)
            self.domainDict = self.abstractDb.getDbDomainDict(self.geomDict)
            self.geomStructDict = self.abstractDb.getGeomStructDict()
        self.returnDict = returnDict
        
        self.folder = os.path.join(os.path.dirname(__file__), 'FieldSetupConfigs') #re-do this
    
    def __del__(self):
        if self.abstractDb:
            del self.abstractDb
            self.abstractDb = None
    
    def populateClassList(self):
        """
        Populates the class list with all geometric classes from database
        """
        self.tableComboBox.clear()
        self.geomClasses = []
        try:
            self.geomClasses = self.abstractDb.listGeomClassesFromDatabase()
        except Exception as e:
            QtGui.QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), 'DSG Tools Plugin', QgsMessageLog.CRITICAL)
        self.geomClasses.sort()
        self.tableComboBox.addItems(self.geomClasses)
        self.tableComboBox.setCurrentIndex(-1)  
    
    def clearAttributeTableWidget(self):
        """
        Clears the attribute table widget. 
        """
        for i in range(self.attributeTableWidget.rowCount(),-1,-1):
            self.attributeTableWidget.removeRow(i)
    
    def makeValueRelationDict(self, table, codes):
        """
        Makes a query to obtain a dictionary with code names and related codes 
        """
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
    def on_tableComboBox_currentIndexChanged(self,row):
        """
        Creates the attribute table according to database.
        Creates specific widgets for each attribute, which can be a QCombobox, a QLineEdit or a QListWidget.
        All mandatory attributes are shown in RED.
        """
        if self.abstractDb.db.driverName() == 'QSQLITE':
            self.populateAttributeFormFromSpatialite(row)
        elif self.abstractDb.db.driverName() == 'QPSQL':
            self.populateAttributeFormFromPostgis(row)
            
    def buildQmlDict(self, fullTableName):
        if self.abstractDb.db.driverName() == 'QSQLITE':
            qml = QmlParser(self.qmlPath)
            qmlDict = qml.getDomainDict()
            if fullTableName in self.nullDict.keys():
                for attr in self.nullDict[fullTableName]:
                    if attr in qmlDict.keys():
                        if not isinstance(qmlDict[attr],tuple):
                            qmlDict[attr]['']=''
            return qmlDict
        elif self.abstractDb.db.driverName() == 'QPSQL':
            qmlDict = dict()
            schemaName, tableName = self.abstractDb.getTableSchema(fullTableName)
            if tableName in self.domainDict.keys():
                for attrName in self.domainDict[tableName]['columns'].keys():
                    if attrName not in qmlDict.keys():
                        qmlDict[attrName] = dict()
                    valueDict = self.domainDict[tableName]['columns'][attrName]['values']
                    constraintList = self.domainDict[tableName]['columns'][attrName]['constraintList']
                    valueRelationDict = dict()
                    for key in valueDict.keys():
                        if len(constraintList) > 0: 
                            if key in constraintList:
                                qmlDict[attrName][valueDict[key]] = str(key)
                        else:
                            qmlDict[attrName][valueDict[key]] = str(key)
                    if tableName in self.geomStructDict.keys():
                        if attrName in self.geomStructDict[tableName].keys():
                            if self.geomStructDict[tableName][attrName]:
                                qmlDict[attrName]['']=''
            return qmlDict
    
    def buildNullityDicts(self):
        nullDict = dict()
        notNullDict = dict()
        for tableName in self.geomStructDict.keys():
            schema = self.geomDict['tablePerspective'][tableName]['schema']
            fullTableName = schema + '.' + tableName
            if fullTableName not in nullDict.keys():
                nullDict[fullTableName] = []
            if fullTableName not in notNullDict.keys():
                notNullDict[fullTableName] = []
            for attr in self.geomStructDict[tableName].keys():
                if self.geomStructDict[tableName][attr]:
                    nullDict[fullTableName].append(attr)
                else:
                    notNullDict[fullTableName].append(attr)
        return nullDict, notNullDict
    
    def populateAttributeFormFromSpatialite(self, row):
        """
        Creates the attribute table according to the QML file to spatialite
        Creates specific widgets for each attribute, which can be a QCombobox, a QLineEdit or a QListWidget.
        All mandatory attributes are shown in RED.
        """
        #reset the button name
        self.buttonNameLineEdit.setText('')
        #clear the attribute table
        self.clearAttributeTableWidget()
        
        if row == -1:
            return
        
        fullTableName = self.tableComboBox.currentText()
        #getting schema name and table name
        schemaName, tableName = self.abstractDb.getTableSchema(fullTableName)
        #getting the QML path
        self.qmlDir = self.abstractDb.getQmlDir()
        self.qmlPath = os.path.join(self.qmlDir,tableName+'.qml')
        
        currentPath = os.path.dirname(__file__)
        
        if self.edgvVersion == '2.1.3':
            sqlPath = os.path.join(currentPath, '..', '..', 'DbTools', 'PostGISTool', 'sqls', '213', 'edgv213.sql')
        elif self.edgvVersion == 'FTer_2a_Ed':
            sqlPath = os.path.join(currentPath, '..', '..', 'DbTools', 'PostGISTool', 'sqls', 'FTer_2a_Ed', 'edgvFter_2a_Ed.sql')
        self.notNullDict, self.nullDict = acquisition_tools.sqlParser(sqlPath, True)
        qmlDict = self.buildQmlDict(fullTableName)
        count = 0
        #creating the items in the attribute table, not null attributes must be in red
        self.createAttributeItems(fullTableName, self.notNullDict, qmlDict, count, colour = Qt.red)
            
        self.createAttributeItems(fullTableName, self.nullDict, qmlDict, count)
    
    def populateAttributeFormFromPostgis(self, row):
        """
        Creates the attribute table according to the postgis dict
        Creates specific widgets for each attribute, which can be a QCombobox, a QLineEdit or a QListWidget.
        All mandatory attributes are shown in RED.
        """
        #reset the button name
        self.buttonNameLineEdit.setText('')
        #clear the attribute table
        self.clearAttributeTableWidget()
        
        if row == -1:
            return
        
        fullTableName = self.tableComboBox.currentText()
        #getting schema name and table name
        qmlDict = self.buildQmlDict(fullTableName)
        count = 0
        #creating the items in the attribute table, not null attributes must be in red
        
        self.nullDict, self.notNullDict = self.buildNullityDicts()
        
        self.createAttributeItems(fullTableName, self.notNullDict, qmlDict, count, colour = Qt.red)
            
        self.createAttributeItems(fullTableName, self.nullDict, qmlDict, count)

    def createAttributeItems(self, fullTableName, currentDict, qmlDict, count, colour = None):
        """
        Creates a QTableWidgetItem for each attribute.
        The cell can have different types according to the data type used (i.e QCombobox, QLineEdit or QListWidget)
        """
        if fullTableName in currentDict.keys():
            for attr in currentDict[fullTableName]:
                self.attributeTableWidget.insertRow(count)
                item = QTableWidgetItem()
                item.setText(attr)
                if colour:
                    item.setBackgroundColor(colour)
                self.attributeTableWidget.setItem(count, 0, item)
                #creating the specific cell widget. It can be a QCombobox, a QLineEdit or a QListWidget
                self.createCellWidget(qmlDict, attr, count)
                count+=1
                        
    def createCellWidget(self, qmlDict, attr, count):
        """
        Creates specific widgets for each attribute, which can be a QCombobox, a QLineEdit or a QListWidget.
        """
        if attr in qmlDict.keys():
            #case the type is dict the cell widget must be a combobox
            if isinstance(qmlDict[attr],dict):
                comboItem = QComboBox()
                comboItem.addItems(sorted(qmlDict[attr].keys()))
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
        """
        Creates a new reclassification button ready to be used
        """
        #checking if the button name is defined
        if self.buttonNameLineEdit.text() == '':
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Enter a button name!'))
            return
        
        # invisible root item
        rootItem = self.treeWidget.invisibleRootItem()

        # class row in the classListWidget
        classRow = self.tableComboBox.currentText()

        schemaName, tableName = self.abstractDb.getTableSchema(classRow)
        if self.abstractDb.db.driverName() == 'QSQLITE':
            category = schemaName + '_' + tableName.split('_')[0]
        else:
            if self.edgvVersion == 'Non_EDGV':
                category = schemaName
            else:
                category = schemaName + '.' + tableName.split('_')[0]

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
                    if leafChild.text(0) == self.tableComboBox.currentText():
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
            item.setText(0, classRow)
        if not buttonInTree:        
            # item that will be used to create the button
            buttonItem = QTreeWidgetItem(item)
            buttonItem.setText(0, self.buttonNameLineEdit.text())

        if self.abstractDb.db.driverName() == 'QSQLITE':
            self.qmlPath = os.path.join(self.qmlDir, tableName+'.qml')
            fullTableName = schemaName+'_'+tableName
        else:
            fullTableName = schemaName+'.'+tableName
        qmlDict = self.buildQmlDict(fullTableName)
        
        # accessing the attribute name and widget (QComboBox or QListWidget depending on data type)
        for i in range(self.attributeTableWidget.rowCount()):
            attribute = self.attributeTableWidget.item(i, 0).text()
            
            # this guy is a QComboBox or a QListWidget
            widgetItem = self.attributeTableWidget.cellWidget(i, 1)
            
            if attribute in qmlDict.keys():
                if isinstance(qmlDict[attribute], dict):
                    if widgetItem.currentText() in qmlDict[attribute].keys():
                        value = qmlDict[attribute][widgetItem.currentText()]
                if isinstance(qmlDict[attribute], tuple):
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
        #test
        paramDict = self.buttonPropWidget.getParameterDict()
            
    def recreateAttributeTable(self, buttonItem):
        """
        Making the attribute table with the actual values present in the tree widget
        """
        # class row in the classListWidget
        classRow = self.classListWidget.currentRow()

        schemaName, tableName = self.abstractDb.getTableSchema(self.classListWidget.item(classRow).text())

        # qml dict for this class (tableName)
        if self.abstractDb.db.driverName() == 'QSQLITE':
            fullTableName = schemaName + '_' + tableName
        elif self.abstractDb.db.driverName() == 'QPSQL':
            fullTableName = schemaName + '.' + tableName

        qmlDict = self.buildQmlDict(fullTableName)

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
                
                # this guy is a QComboBox here
                if attribute in qmlDict.keys():
                    if isinstance(qmlDict[attribute], dict):
                        for i in range(widgetItem.count()):
                            text = widgetItem.itemText(i)
                            if text in qmlDict[attribute].keys():
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
                    value = widgetItem.setText(value)
            
    def getUiParameterJsonDict(self):
        """
        builds a dict with the following format:
        {
            'slider': --slider value --
            'checkBox': --check state of checkBox --
        }
        """
        uiParameterJsonDict = dict()
        uiParameterJsonDict['slider'] = self.slider.value()
        uiParameterJsonDict['checkBox'] = self.checkBox.isChecked()
        return uiParameterJsonDict
    
    def makeReclassificationDict(self):
        """
        Makes the reclassification dictionary used to perform the actual reclassification
        """
        reclassificationDict = dict()
        
        reclassificationDict['version'] = self.edgvVersion
        reclassificationDict['uiParameterJsonDict'] = self.getUiParameterJsonDict()
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
        """
        Reads the json configuration file
        """
        try:
            file = open(filename, 'r')
            data = file.read()
            reclassificationDict = json.loads(data)
            file.close()
            return reclassificationDict
        except:
            return dict()
    
    def populateFromUiParameterJsonDict(self, uiParameterJsonDict):
        """
        populates ui from  uiParameterJsonDict with the following keys:
        {
            'slider': --slider value --
            'checkBox': --check state of checkBox --
        }
        """
        if uiParameterJsonDict:
            self.slider.setValue(uiParameterJsonDict['slider'])
            if uiParameterJsonDict['checkBox']:
                self.checkBox.setCheckState(2)
    
    def loadReclassificationConf(self, reclassificationDict):
        """
        Makes the treewidget using the reclassification dictionary obtained from the configuration file
        """
        index = self.edgvVersion
        
        self.treeWidget.clear()
        
        #invisible root item
        rootItem = self.treeWidget.invisibleRootItem()
        
        for category in reclassificationDict.keys():
            if category == 'version':
                continue
            if category == 'uiParameterJsonDict':
                self.populateFromUiParameterJsonDict(reclassificationDict[category])
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
        """
        Adjusts the button visualization according to the selected item in the tree widget
        """
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
        """
        Calculates the item depth in the tree widget
        """
        #calculates the depth of the item
        depth = 0
        while item is not None:
            item = item.parent()
            depth += 1
        return depth   
    
    def createMenu(self, position):
        """
        Creates a menu that allows button removal by the user
        """
        menu = QMenu()
        
        item = self.treeWidget.itemAt(position)

        if item and self.depth(item) < 4:
            menu.addAction(self.tr('Remove child node'), self.removeChildNode)
        menu.exec_(self.treeWidget.viewport().mapToGlobal(position))

    def removeChildNode(self):
        """
        Removes a tree widget item and all its children
        """
        item = self.treeWidget.currentItem()
        item.parent().removeChild(item)     
        
    @pyqtSlot(bool)
    def on_loadButton_clicked(self):
        """
        Loads a configuration file
        """
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
        """
        Saves the configuration work done so far.
        """
        if not self.returnDict:
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
        else:
            return self.makeReclassificationDict()

        