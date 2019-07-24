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
from __future__ import absolute_import
from builtins import map
from builtins import str
from builtins import range
import os, json

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt
from qgis.PyQt.QtWidgets import QMessageBox, QCheckBox, QButtonGroup, QItemDelegate, \
                                QDialog, QMessageBox, QListWidget, QListWidgetItem, \
                                QAction
from qgis.PyQt.QtWidgets import QFileDialog, QTreeWidgetItem, QTableWidget, \
                                QTableWidgetItem, QStyledItemDelegate, QComboBox, \
                                QMenu, QLineEdit, QShortcut
from qgis.PyQt.QtGui import QKeySequence
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery

# QGIS imports
from qgis.core import QgsMapLayer, QgsGeometry, QgsMessageLog
from qgis.gui import QgsGui

#DsgTools imports
from .....core.Factories.DbFactory.dbFactory import DbFactory
from .....core.Misc.QmlTools.qmlParser import QmlParser
from ....CustomWidgets.BasicInterfaceWidgets.dsgCustomComboBox import DsgCustomComboBox
from . import acquisition_tools

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'field_setup.ui'))

class FieldSetup(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, abstractDb, returnDict = False, parent = None):
        """
        Constructor
        """
        super(self.__class__, self).__init__(parent)
        self.abstractDb = abstractDb
        self.edgvVersion = self.abstractDb.getDatabaseVersion()
        if self.abstractDb.db.driverName() == 'QPSQL':
            self.geomTypeDict = self.abstractDb.getGeomTypeDict()
            self.geomDict = self.abstractDb.getGeomDict(self.geomTypeDict)
            self.domainDict = self.abstractDb.getDbDomainDict(self.geomDict)
            self.geomStructDict = self.abstractDb.getGeomStructDict()
        self.returnDict = returnDict
        self.setupUi(self)
        self.tableComboBox.setCurrentIndex(-1)  
        self.populateClassList()
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.createMenu)        
        self.folder = os.path.join(os.path.dirname(__file__), 'FieldSetupConfigs') #re-do this
        self.optionalDict = {self.tr('Yes'):'1', self.tr('No'):'0'}
        self.buttonPropDict = dict()
        self.shortcutsManager = QgsGui.shortcutsManager()
        self.qgisShortcutList = self.getQGISShortcutList()
    
    def getQGISShortcutList(self):
        """
        Returns all shortcuts from qgis
        """
        shortcutList = []
        for shortcutItem in self.shortcutsManager.listAll():
            if isinstance(shortcutItem, QAction):
                for i in shortcutItem.shortcuts():
                    if i not in shortcutList:
                        shortcutList.append(i)
            if isinstance(shortcutItem, QShortcut):
                if shortcutItem not in shortcutList:
                    shortcutList.append(shortcutItem)
        return shortcutList
    
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
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('A problem occurred! Check log for details.'))
            QgsMessageLog.logMessage(':'.join(e.args), 'DSG Tools Plugin', Qgis.Critical)
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
        while next(query):
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
            if fullTableName in list(self.nullDict.keys()):
                for attr in self.nullDict[fullTableName]:
                    if attr in list(qmlDict.keys()):
                        if not isinstance(qmlDict[attr],tuple):
                            qmlDict[attr]['']=''
            return qmlDict
        elif self.abstractDb.db.driverName() == 'QPSQL':
            qmlDict = dict()
            schemaName, tableName = self.abstractDb.getTableSchema(fullTableName)
            if tableName in list(self.domainDict.keys()):
                for attrName in list(self.domainDict[tableName]['columns'].keys()):
                    if attrName not in list(qmlDict.keys()):
                        qmlDict[attrName] = dict()
                    valueDict = self.domainDict[tableName]['columns'][attrName]['values']
                    constraintList = self.domainDict[tableName]['columns'][attrName]['constraintList']
                    valueRelationDict = dict()
                    for key in list(valueDict.keys()):
                        if len(constraintList) > 0: 
                            if key in constraintList:
                                qmlDict[attrName][valueDict[key]] = str(key)
                        else:
                            qmlDict[attrName][valueDict[key]] = str(key)
                    if tableName in list(self.geomStructDict.keys()):
                        if attrName in list(self.geomStructDict[tableName].keys()):
                            if self.geomStructDict[tableName][attrName]:
                                qmlDict[attrName]['']=''
            return qmlDict
    
    def buildNullityDicts(self):
        nullDict = dict()
        notNullDict = dict()
        for tableName in list(self.geomStructDict.keys()):
            schema = self.geomDict['tablePerspective'][tableName]['schema']
            fullTableName = schema + '.' + tableName
            if fullTableName not in list(nullDict.keys()):
                nullDict[fullTableName] = []
            if fullTableName not in list(notNullDict.keys()):
                notNullDict[fullTableName] = []
            for attr in list(self.geomStructDict[tableName].keys()):
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
            sqlPath = os.path.join(currentPath, '..', '..', '..', '..', 'core', 'DbModels', 'PostGIS', '213', 'edgv213.sql')
        elif self.edgvVersion == 'FTer_2a_Ed':
            sqlPath = os.path.join(currentPath, '..', '..', '..', '..', 'core', 'DbModels', 'PostGIS', '213', 'edgvFter_2a_Ed.sql')
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
        if fullTableName in currentDict:
            for attr in currentDict[fullTableName]:
                self.attributeTableWidget.insertRow(count)
                item = QTableWidgetItem()
                item.setText(attr)
                if colour:
                    item.setBackground(colour)
                self.attributeTableWidget.setItem(count, 0, item)
                #creating the specific cell widget. It can be a QCombobox, a QLineEdit or a QListWidget
                self.createCellWidget(qmlDict, attr, count)
                count+=1
                        
    def createCellWidget(self, qmlDict, attr, count):
        """
        Creates specific widgets for each attribute, which can be a QCombobox, a QLineEdit or a QListWidget.
        """
        if attr in qmlDict:
            enableIgnoreOption = False
            #case the type is dict the cell widget must be a combobox
            if isinstance(qmlDict[attr],dict):
                comboItem = DsgCustomComboBox()
                comboItem.addItems(sorted(qmlDict[attr].keys()))
                self.attributeTableWidget.setCellWidget(count, 1, comboItem)
            #case the type is tuple the cell widget must be a listwidget
            if isinstance(qmlDict[attr],tuple):
                (table, filterKeys) = qmlDict[attr]
                #getting the value relation dictionary used to make the listwidget
                valueRelation = self.makeValueRelationDict(table, filterKeys)
                list = QListWidget()
                for key in list(valueRelation.keys()):
                    listItem = QListWidgetItem(key)
                    listItem.setCheckState(Qt.Unchecked)
                    list.addItem(listItem)
                self.attributeTableWidget.setCellWidget(count, 1, list)
        #this is the normal case, a simple lineedit
        else:
            textItem = QLineEdit()
            self.attributeTableWidget.setCellWidget(count, 1, textItem)
            enableIgnoreOption = True
        #insert here aditional parameters
        self.createAditionalParameters(count, enableIgnoreOption)
    
    def createAditionalParameters(self, count, enableIgnoreOption):
        """
        Creates aditional parameters upon creation of an attribute item
        """
        #editable item
        comboItem = QComboBox()
        comboItem.addItems([self.tr('Yes'), self.tr('No')])
        self.attributeTableWidget.setCellWidget(count, 2, comboItem)
        #ignored item
        comboItem = QComboBox()
        comboItem.addItems([self.tr('No'), self.tr('Yes')])
        comboItem.setEnabled(enableIgnoreOption)
        self.attributeTableWidget.setCellWidget(count, 3, comboItem)
    
    def validateShortcut(self, currentButtonName):
        currentShortcut = self.buttonPropWidget.shortcutWidget.getShortcut(asQKeySequence = True)
        if currentShortcut == 0:
            return True
        sList = []
        for tableName in list(self.buttonPropDict.keys()):
            for buttonName in list(self.buttonPropDict[tableName].keys()):
                if 'buttonShortcut' in list(self.buttonPropDict[tableName][buttonName].keys()) and buttonName != currentButtonName:
                    sList.append(QKeySequence(self.buttonPropDict[tableName][buttonName]['buttonShortcut']))
        if currentShortcut in self.qgisShortcutList or currentShortcut in sList:
            return False
        else:
            return True
    
    @pyqtSlot(bool)
    def on_addUpdatePushButton_clicked(self):
        """
        Creates a new reclassification button ready to be used
        """
        #checking if the button name is defined
        if self.buttonNameLineEdit.text() == '':
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Enter a button name!'))
            return

        if not self.validateShortcut(self.buttonNameLineEdit.text()):
            QMessageBox.critical(self, self.tr('Critical!'), self.tr('Shortcut already set to another tool!'))
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
        #add optional parameters to self.buttonPropDict
        if fullTableName not in list(self.buttonPropDict.keys()):
            self.buttonPropDict[fullTableName] = dict()
        #parameter dict from buttonPropWidget has the following format:
        #{'buttonColor':--color of the button--, 'buttonToolTip'--button toolTip--, 'buttonGroupTag':--group tag of the button--}
        self.buttonPropDict[fullTableName][self.buttonNameLineEdit.text()] = self.buttonPropWidget.getParameterDict()

        # accessing the attribute name and widget (QComboBox or QListWidget depending on data type)
        for i in range(self.attributeTableWidget.rowCount()):
            attribute = self.attributeTableWidget.item(i, 0).text()
            
            # this guy is a QComboBox or a QListWidget
            widgetItem = self.attributeTableWidget.cellWidget(i, 1)
            
            if attribute in list(qmlDict.keys()):
                if isinstance(qmlDict[attribute], dict):
                    if widgetItem.currentText() in list(qmlDict[attribute].keys()):
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
                if isinstance(widgetItem, DsgCustomComboBox):
                    value = widgetItem.currentText()
                else:
                    value = widgetItem.text()
            
            #sweep tree for attribute
            attrFound = False
            for k in range(buttonItem.childCount()):
                attrItem = buttonItem.child(k)
                if attribute == attrItem.text(0):
                    attrFound = True
                    attributeItem = attrItem
                    break
            if not attrFound:
                attributeItem = QTreeWidgetItem(buttonItem)
                attributeItem.setText(0, attribute)
            attributeItem.setText(1, value)
            for j in [2,3]:
                itemCell = self.attributeTableWidget.cellWidget(i, j)
                if itemCell:
                    if itemCell.isEnabled():
                        itemText = itemCell.currentText()
                        attributeItem.setText(j, self.optionalDict[itemText])
            
    def recreateAttributeTable(self, buttonItem):
        """
        Making the attribute table with the actual values present in the tree widget
        """
        # class row in the classListWidget
        classRow = self.tableComboBox.currentIndex()

        schemaName, tableName = self.abstractDb.getTableSchema(self.tableComboBox.currentText())

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
                if attribute != self.attributeTableWidget.item(i, 0).text():
                    continue
                
                # this guy is a QComboBox or a QListWidget
                widgetItem = self.attributeTableWidget.cellWidget(i, 1)
                
                # this guy is a QComboBox here
                if attribute in list(qmlDict.keys()):
                    if isinstance(qmlDict[attribute], dict):
                        for i in range(widgetItem.count()):
                            text = widgetItem.itemText(i)
                            if text in list(qmlDict[attribute].keys()):
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
                for j in [2,3]:
                    #populate the other properties of the attribute
                    widgetItem = self.attributeTableWidget.cellWidget(i, j)
                    if widgetItem:
                        textList = [key for key in list(self.optionalDict.keys()) if  self.optionalDict[key] == attrItem.text(j)]
                        if len(textList) > 0:
                            text = textList[0]
                            for idx in range(widgetItem.count()):
                                if widgetItem.itemText(idx) == text:
                                    widgetItem.setCurrentIndex(idx)
            
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
        Dictionary has the following format:
        {
            "category": {
                "schema.table_name":{
                    "buttonName":{
                        "attrName": {"value":value, "isEditable":isEditable, "isIgnored":isIgnored}
                        "buttonProp": {"buttonColor":buttonColor, "buttonToolTip":buttonToolTip, "buttonGroupTag":buttonGroupTag}
                    }
                },
            "uiParameterJsonDict": {
                "checkBox": bool, 
                "slider": size
                }, 
            "version": version
            }
        }
        old dict has the following format:
        {
            "category": {
                "schema.table_name":{
                    "buttonName":{
                        "attrName": value
                    }
                },
            "uiParameterJsonDict": {
                    "checkBox": bool, 
                    "slider": size
                }, 
            "version": version
            }
        }
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
                    #buttonItem.text(0) is the buttonName
                    reclassificationDict[categoryItem.text(0)][classItem.text(0)][buttonItem.text(0)] = dict()
                    for l in range(buttonItem.childCount()):
                        attributeItem = buttonItem.child(l)
                        if attributeItem.text(0) == '':
                            continue
                        dictItem = {"value":attributeItem.text(1), "isEditable":attributeItem.text(2), "isIgnored":attributeItem.text(3)}
                        reclassificationDict[categoryItem.text(0)][classItem.text(0)][buttonItem.text(0)][attributeItem.text(0)] = dictItem
                    if classItem.text(0) in list(self.buttonPropDict.keys()):
                        if buttonItem.text(0) in self.buttonPropDict[classItem.text(0)]:
                            reclassificationDict[categoryItem.text(0)][classItem.text(0)][buttonItem.text(0)]["buttonProp"] = self.buttonPropDict[classItem.text(0)][buttonItem.text(0)]
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
        self.qgisShortcutList = self.getQGISShortcutList() #resets lists
        
        #invisible root item
        rootItem = self.treeWidget.invisibleRootItem()
        
        for category in list(reclassificationDict.keys()):
            if category == 'version':
                continue
            if category == 'uiParameterJsonDict':
                self.populateFromUiParameterJsonDict(reclassificationDict[category])
                continue
            categoryItem = QTreeWidgetItem(rootItem)
            categoryItem.setText(0, category)
            for edgvClass in list(reclassificationDict[category].keys()):
                classItem = QTreeWidgetItem(categoryItem)
                classItem.setText(0, edgvClass)
                for button in list(reclassificationDict[category][edgvClass].keys()):
                    buttonItem = QTreeWidgetItem(classItem)
                    buttonItem.setText(0, button)
                    for attribute in list(reclassificationDict[category][edgvClass][button].keys()):
                        attributeItem = QTreeWidgetItem(buttonItem)
                        attrDict = reclassificationDict[category][edgvClass][button][attribute]
                        if attribute == 'buttonProp':
                            if edgvClass not in list(self.buttonPropDict.keys()):
                                self.buttonPropDict[edgvClass] = dict()
                            self.buttonPropDict[edgvClass][button] = attrDict
                        else:
                            attributeItem.setText(0, attribute)
                            if isinstance(attrDict, dict):
                                attributeItem.setText(1, attrDict['value'])
                                attributeItem.setText(2, attrDict['isEditable'])
                                attributeItem.setText(3, attrDict['isIgnored'])
                            else:
                                attributeItem.setText(1, attrDict)
                    
    def on_treeWidget_currentItemChanged(self, previous, current):
        """
        Adjusts the button visualization according to the selected item in the tree widget
        """
        depth = self.depth(previous)
        if depth == 1:
            self.buttonNameLineEdit.setText('')
        elif depth == 2:
            idx = self.tableComboBox.findData(previous.text(0), Qt.MatchExactly)
            self.tableComboBox.setCurrentIndex(idx)
            self.buttonNameLineEdit.setText('')
        elif depth == 3:
            idx = self.tableComboBox.findData(previous.parent().text(0), Qt.MatchExactly)
            if idx != -1:
                self.tableComboBox.setCurrentIndex(idx)
            self.buttonNameLineEdit.setText(previous.text(0))
            self.recreateAttributeTable(previous)
            self.populateOptionalParametersWidget(previous.text(0))
        elif depth == 4:
            idx = self.tableComboBox.findData(previous.parent().parent().text(0), Qt.MatchExactly)
            if idx != -1:
                self.tableComboBox.setCurrentIndex(idx)
            self.buttonNameLineEdit.setText(previous.parent().text(0))
            self.recreateAttributeTable(previous.parent())
    
    def populateOptionalParametersWidget(self, buttonName):
        """
        Takes values from self.buttonPropDict and populates butonPropWidget
        """
        schemaName, tableName = self.abstractDb.getTableSchema(self.tableComboBox.currentText())
        fullTableName = '.'.join([schemaName, tableName])
        if fullTableName in list(self.buttonPropDict.keys()):
            if buttonName in list(self.buttonPropDict[fullTableName].keys()):
                self.buttonPropWidget.setInterface(self.buttonPropDict[fullTableName][buttonName])

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
        self.treeWidget.invisibleRootItem().removeChild(item)
        del item

    @pyqtSlot(bool)
    def on_loadButton_clicked(self):
        """
        Loads a configuration file
        """
        self.loadedFileEdit.setText('')
        
        filename, __ = QFileDialog.getOpenFileName(self, self.tr('Open reclassification setup file'), self.folder, self.tr('Reclassification Setup Files (*.reclas)'))
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
                
            filename, __ = QFileDialog.getSaveFileName(self, self.tr('Save reclassification setup file'), self.folder, self.tr('Reclassification Setup Files (*.reclas)'))
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

        