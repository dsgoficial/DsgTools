# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-01-09
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from PyQt4.QtGui import QApplication, QCursor
# DSGTools imports
from DsgTools.PostgisCustomization.CustomJSONTools.customJSONBuilder import CustomJSONBuilder

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'changeFilterWidget.ui'))

class ChangeFilterWidget(QtGui.QWidget, FORM_CLASS):
    populateSingleValue = pyqtSignal()
    populateListValue = pyqtSignal()
    populateInheritanceTree = pyqtSignal(list)
    def __init__(self, abstractDb, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.abstractDb = abstractDb
        self.setupUi(self)
        self.jsonBuilder = CustomJSONBuilder()
        self.populateSchemaCombo()
        self.hideWidgetList([self.singleValueLabel, self.singleValueComboBox, self.actionComboBox])
        self.singleAttribute = True
        self.filterCustomSelectorWidget.setTitle(self.tr('Select filter values'))
        self.populateSingleValue.connect(self.populateWidgetWithSingleValue)
        self.populateListValue.connect(self.populateWidgetWithListValue)
        geomTypeDict = self.abstractDb.getGeomTypeDict()
        geomDict = self.abstractDb.getGeomDict(geomTypeDict)
        self.domainDict = self.abstractDb.getDbDomainDict(geomDict)
    
    def populateSchemaCombo(self):
        self.schemaComboBox.clear()
        self.schemaComboBox.addItem(self.tr('Select a schema'))
        schemaList = self.abstractDb.getGeometricSchemaList()
        for schema in schemaList:
            if schema not in ['views', 'validation']:
                self.schemaComboBox.addItem(schema)
    
    def hideWidgetList(self, widgetList):
        for widget in widgetList:
            widget.hide()
    
    def showWidgetList(self, widgetList):
        for widget in widgetList:
            widget.show()
    
    @pyqtSlot(int)
    def on_schemaComboBox_currentIndexChanged(self, idx):
        if idx == 0:
            self.tableComboBox.clear()
            self.tableComboBox.setEnabled(False)
            self.attributeComboBox.clear()
            self.attributeComboBox.setEnabled(False)
        else:
            schema = self.schemaComboBox.currentText()
            self.tableComboBox.setEnabled(True)
            self.tableComboBox.clear()
            self.tableComboBox.addItem(self.tr('Select a table'))
            tableList = self.abstractDb.getGeometricTableListFromSchema(schema)
            for table in tableList:
                self.tableComboBox.addItem(table)
    
    @pyqtSlot(int)
    def on_tableComboBox_currentIndexChanged(self, idx):
        if idx == 0:
            self.attributeComboBox.clear()
            self.attributeComboBox.setEnabled(False)
        else:
            schema = self.schemaComboBox.currentText()
            tableName = self.tableComboBox.currentText()
            self.attributeComboBox.setEnabled(True)
            self.attributeComboBox.clear()
            self.attributeComboBox.addItem(self.tr('Select an attribute'))
            if tableName in self.domainDict.keys():
                attributeList = self.domainDict[tableName]['columns'].keys()
                for attribute in attributeList:
                    self.attributeComboBox.addItem(attribute)
    
    @pyqtSlot(int, name='on_tableComboBox_currentIndexChanged')
    @pyqtSlot(int, name='on_schemaComboBox_currentIndexChanged')
    @pyqtSlot(int, name='on_attributeComboBox_currentIndexChanged')
    def populateWidgetWithSingleValue(self):
        if self.schemaComboBox.currentIndex() <> 0 and self.tableComboBox.currentIndex() <> 0 and (self.allTablesCheckBox.checkState() == 2 or self.allAttributesCheckBox.checkState() == 2):
            self.attributeComboBox.clear()
            self.attributeComboBox.setEnabled(False)
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.singleValueComboBox.clear()
            self.singleValueComboBox.addItem(self.tr('Select a value to alter'))
            if self.allAttributesCheckBox.checkState() == 2:
                tableList = [self.tableComboBox.currentText()]
            else:
                tableList = self.domainDict.keys()
            allValueList = []
            idxList = []
            for tableName in tableList:
                for attrName in self.domainDict[tableName]['columns'].keys():
                    for code in self.domainDict[tableName]['columns'][attrName]['values']:
                        value = self.domainDict[tableName]['columns'][attrName]['values'][code]
                        if value not in allValueList:
                            allValueList.append(value)
            
            for value in allValueList:
                for tableName in tableList:
                    for attrName in self.domainDict[tableName]['columns'].keys():
                        if value not in self.domainDict[tableName]['columns'][attrName]['values'].values():
                            idx = allValueList.index(value)
                            if idx not in idxList:
                                idxList.append(idx)
            idxList.sort(reverse=True)
            for idx in idxList:
                allValueList.pop(idx)
            for value in allValueList:
                self.singleValueComboBox.addItem(value)
            QApplication.restoreOverrideCursor()
        
    
    @pyqtSlot(int, name='on_attributeComboBox_currentIndexChanged')
    def populateWidgetWithListValue(self):
        self.filterCustomSelectorWidget.clearAll()
        if self.allTablesCheckBox.checkState() == 2 or self.allAttributesCheckBox.checkState() == 2:
            return
        if self.schemaComboBox.currentIndex() == 0:
            self.schemaComboBox.currentIndexChanged.emit(0)
            return
        elif self.tableComboBox.currentIndex() == 0:
            self.tableComboBox.currentIndexChanged.emit(0)
            return
        elif self.attributeComboBox.currentIndex() == 0:
            return
        filterList = []
        tableName = self.tableComboBox.currentText()
        attributeName = self.attributeComboBox.currentText()
        tableFilter = []
        filterToList = []
        if tableName in self.domainDict.keys():
            if attributeName in self.domainDict[tableName]['columns'].keys():
                attrDomainDict = self.domainDict[tableName]['columns'][attributeName]['values']
                tableFilter = self.domainDict[tableName]['columns'][attributeName]['constraintList']
        filterToList = [attrDomainDict[i] for i in tableFilter]
        filterFromList = [i for i in attrDomainDict.values() if i not in filterToList]
        self.filterCustomSelectorWidget.setFromList(filterFromList, unique = True)
        self.filterCustomSelectorWidget.setToList(filterToList)
        
    
    @pyqtSlot(int)
    def on_allTablesCheckBox_stateChanged(self, state):
        self.hideOrShowWidgets()
        if state == 0:
            self.allAttributesCheckBox.setEnabled(True)
            self.schemaComboBox.setCurrentIndex(0)
            self.schemaComboBox.setEnabled(True)
        elif state == 2:
            self.allAttributesCheckBox.setEnabled(False)
            self.allAttributesCheckBox.setCheckState(0)
            self.schemaComboBox.setCurrentIndex(0)
            self.schemaComboBox.setEnabled(False)
            
    
    @pyqtSlot(int)
    def on_allAttributesCheckBox_stateChanged(self, state):
        if state == 2:
            self.allTablesCheckBox.setEnabled(False)
            self.allTablesCheckBox.setCheckState(0)
            self.attributeComboBox.setCurrentIndex(0)
            self.attributeComboBox.setEnabled(False)
        if state == 0:
            self.allTablesCheckBox.setEnabled(True)
            self.attributeComboBox.setEnabled(True)
        self.hideOrShowWidgets()
    
    def hideOrShowWidgets(self):
        if self.allAttributesCheckBox.checkState() == 2 or self.allTablesCheckBox.checkState() == 2:
            self.filterCustomSelectorWidget.hide()
            self.singleValueLabel.show()
            self.singleValueComboBox.show()
            self.actionComboBox.show()
            self.populateSingleValue.emit()
        else:
            self.filterCustomSelectorWidget.show()
            self.singleValueLabel.hide()
            self.singleValueComboBox.hide()
            self.actionComboBox.hide()
            self.tableComboBox.currentIndexChanged.emit(self.tableComboBox.currentIndex())
            self.populateListValue.emit()
    
    def getTitle(self):
        return self.title
    
    def setTitle(self, title):
        self.title = title
    
    def validate(self):
        if self.allAttributesCheckBox.checkState() == 2:
             pass
        if self.allTablesCheckBox.checkState() == 2:
            pass
        return True

    def validateDiagnosis(self):
        invalidatedReason = ''
        if self.schemaComboBox.currentIndex() == 0:
            invalidatedReason += self.tr('A schema must be chosen.\n')
        if self.tableComboBox.currentIndex() == 0:
            invalidatedReason += self.tr('A table must be chosen.\n')
        if self.actionComboBox.currentIndex() == 0:
            invalidatedReason += self.tr('An action be chosen.\n')
        if self.allAttributesCheckBox.checkState() <> 2 and self.attributeComboBox.currentIndex() == 0:
            invalidatedReason += self.tr('An attribute must be chosen.\n')
        return invalidatedReason
    
    def getJSONTag(self):
        if not self.validate():
            raise Exception(self.tr('Error in change nullity customization ')+ self.title + ' : ' + self.validateDiagnosis())
        if self.actionComboBox.currentIndex() == 1:
            notNull = True
        elif self.actionComboBox.currentIndex() == 2:
            notNull = False
        jsonList = []
        if self.allTablesCheckBox.checkState() == 2:
            attributeJsonList = self.abstractDb.getAttributeJsonFromDb()
            for attributeJson in attributeJsonList:
                schema = attributeJson['table_schema']
                table = attributeJson['table_name']
                for attrName in attributeJson['attributelist']:
                    jsonList.append(self.jsonBuilder.buildChangeNullityElement(schema, table, attrName, notNull))
        else:
            schema = self.schemaComboBox.currentText()
            table = self.tableComboBox.currentText()
            if self.allAttributesCheckBox.checkState() == 2:
                attrList = self.abstractDb.getAttributeListFromTable(schema, table)
                for attrName in attrList:
                    jsonList.append(self.jsonBuilder.buildChangeNullityElement(schema, table, attrName, notNull))
            else:
                attrName = self.attributeComboBox.currentText()
                jsonList.append(self.jsonBuilder.buildChangeNullityElement(schema, table, attrName, notNull))
        return jsonList