# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-01
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : borba@dsg.eb.mil.br
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

from qgis.core import QgsMessageLog
from qgis.gui import QgsCollapsibleGroupBox

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtGui import QFormLayout, QMessageBox, QFileDialog

# DSGTools imports
from DsgTools.CustomWidgets.CustomDbManagementWidgets.newClassWidget import NewClassWidget
from DsgTools.CustomWidgets.CustomDbManagementWidgets.newAttributeWidget import NewAttributeWidget
from DsgTools.CustomWidgets.CustomDbManagementWidgets.newDomainWidget import NewDomainWidget
from DsgTools.CustomWidgets.CustomDbManagementWidgets.newDomainValueWidget import NewDomainValueWidget
from DsgTools.CustomWidgets.CustomDbManagementWidgets.codeNameCustomizationWidget import CodeNameCustomizationWidget
from DsgTools.CustomWidgets.CustomDbManagementWidgets.changeNullityWidget import ChangeNullityWidget
from DsgTools.CustomWidgets.CustomDbManagementWidgets.changeFilterWidget import ChangeFilterWidget
from DsgTools.CustomWidgets.CustomDbManagementWidgets.alterDefaultWidget import AlterDefaultWidget
from DsgTools.CustomWidgets.selectFileWidget import SelectFileWidget
from DsgTools.PostgisCustomization.dbCustomizer import DbCustomizer
from DsgTools.Utils.utils import Utils

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'createDatabaseCustomization.ui'))

class CreateDatabaseCustomization(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.connectionWidget.tabWidget.setTabEnabled(1, False)
        self.connectionWidget.dbChanged.connect(self.minimizeConnectionWidget)
        self.contentsDict = dict()
        self.populateCustomizationCombo()
        self.selectFileWidget.filter = '*.json'
        self.selectFileWidget.filesSelected.connect(self.populateWidgetsFromSelectedFile)
        self.utils = Utils()
    
    def minimizeConnectionWidget(self):
        self.connectionWidget.mGroupBox.setCollapsed(True)
    
    def getStructDict(self):
        pass
    
    def populateCustomizationCombo(self):
        '''
        Populates the customization combo and also defines customDict.
        '''
        self.customDict = dict()
        self.customDict['attribute'] = self.tr('Attribute Customization')
        self.customDict['class'] = self.tr('Class Customization')
        self.customDict['codeName'] = self.tr('Code Name Customization')
        self.customDict['default'] = self.tr('Default Customization')
        self.customDict['domain'] = self.tr('Domain Customization')
        self.customDict['domainValue'] = self.tr('Domain Value Customization')
        self.customDict['nullity'] = self.tr('Attribute Nullity Customization')
        self.customDict['filter'] = self.tr('Attribute Filter Customization')
        rootNode = self.customizationTreeWidget.invisibleRootItem()
        for type in self.customDict.keys():
            if self.customDict[type] not in self.contentsDict.keys():
                self.contentsDict[self.customDict[type]] = dict()
            self.customizationSelectionComboBox.addItem(self.customDict[type])
            self.contentsDict[self.customDict[type]]['widgetList'] = []
            self.contentsDict[self.customDict[type]]['treeItem'] = self.createItem(rootNode, self.customDict[type], 0)
        self.customizationTreeWidget.expandAll()
    
    @pyqtSlot(bool)
    def on_addAttributePushButton_clicked(self):
        if self.customizationSelectionComboBox.currentText() == self.tr('Attribute Customization'):
            self.addAttributeWidget()
        elif self.customizationSelectionComboBox.currentText() == self.tr('Class Customization'):
            self.addClassWidget()
        elif self.customizationSelectionComboBox.currentText() == self.tr('Code Name Customization'):
            self.addCodeNameWidget()
        elif self.customizationSelectionComboBox.currentText() == self.tr('Default Customization'):
            self.addDefaultWidget()
        elif self.customizationSelectionComboBox.currentText() == self.tr('Domain Customization'):
            self.addDomainWidget()
        elif self.customizationSelectionComboBox.currentText() == self.tr('Domain Value Customization'):
            self.addDomainValueWidget()
        elif self.customizationSelectionComboBox.currentText() == self.tr('Attribute Nullity Customization'):
            self.addNullityWidget()
        elif self.customizationSelectionComboBox.currentText() == self.tr('Attribute Filter Customization'):
            self.addFilterWidget()
        else:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Select a custom operation!'))
    
    def addWidgetItem(self, contentsKey, widgetTitle, widget):
        widgetList = self.contentsDict[contentsKey]['widgetList']
        if len(widgetList) > 0:
            i = int(widgetList[-1].layout().itemAt(0).widget().getTitle().split('#')[-1])
        else:
            i = 0
        title = widgetTitle+' #{0}'.format(i+1) #add number
        widget.setTitle(title)
        self.contentsDict[contentsKey]['widgetList'].append(self.addWidget(widget, title))
        self.createItem(self.contentsDict[contentsKey]['treeItem'], title, 0)
    
    def addAttributeWidget(self,jsonTag=None):
        widget = NewAttributeWidget(self.connectionWidget.abstractDb,jsonTag = jsonTag)
        self.addWidgetItem(self.tr('Attribute Customization'), self.tr('New Custom Attribute'), widget)
    
    def addClassWidget(self,jsonTag=None):
        widget = NewClassWidget(self.connectionWidget.abstractDb,jsonTag = jsonTag)
        self.addWidgetItem(self.tr('Class Customization'), self.tr('New Custom Class'), widget)
    
    def addCodeNameWidget(self,jsonTag=None):
        widget = CodeNameCustomizationWidget(self.connectionWidget.abstractDb,jsonTag = jsonTag)
        self.addWidgetItem(self.tr('Code Name Customization'), self.tr('New Custom Code Name'), widget)

    def addDefaultWidget(self,jsonTag=None):
        widget = AlterDefaultWidget(self.connectionWidget.abstractDb,jsonTag = jsonTag)
        self.addWidgetItem(self.tr('Default Customization'), self.tr('New Custom Default'), widget) 

    def addDomainWidget(self,jsonTag=None):
        widget = NewDomainWidget(self.connectionWidget.abstractDb,jsonTag = jsonTag)
        self.addWidgetItem(self.tr('Domain Customization'), self.tr('New Custom Domain'), widget)

    def addDomainValueWidget(self,jsonTag=None):
        widget = NewDomainValueWidget(self.connectionWidget.abstractDb,jsonTag = jsonTag)
        self.addWidgetItem(self.tr('Domain Value Customization'), self.tr('New Domain Value'), widget)

    def addNullityWidget(self,jsonTag=None):
        widget = ChangeNullityWidget(self.connectionWidget.abstractDb,jsonTag = jsonTag)
        self.addWidgetItem(self.tr('Attribute Nullity Customization'), self.tr('New Custom Attribute Nullity'), widget)

    def addFilterWidget(self,jsonTag=None):
        widget = ChangeFilterWidget(self.connectionWidget.abstractDb,jsonTag = jsonTag)
        self.addWidgetItem(self.tr('Attribute Filter Customization'), self.tr('New Custom Attribute Filter'), widget)
    
    def addWidget(self, widget, title):
        layout = QtGui.QFormLayout()
        layout.addRow(widget)
        groupBox = QgsCollapsibleGroupBox(title)
        groupBox.setCollapsed(False)
        groupBox.setSaveCollapsedState(False)
        groupBox.setLayout(layout)
        self.scrollAreaLayout.addWidget(groupBox)
        return groupBox
    
    def createItem(self, parent, text, column):
        item = QtGui.QTreeWidgetItem(parent)
        item.setText(column, text)
        return item
    
    def getWidgetIndexFromTreeItem(self, treeItem):
        parent = treeItem.parent()
        widgetName = treeItem.text(0) 
        if not parent:
            return
        if parent == self.customizationTreeWidget.invisibleRootItem():
            return None
        childCount = parent.childCount()
        for i in range(childCount):
            child = parent.child(i)
            if child.text(0) == widgetName:
                return i
    
    @pyqtSlot(bool)
    def on_removeSelectedPushButton_clicked(self):
        treeItem = self.customizationTreeWidget.currentItem()
        parent = treeItem.parent()
        if parent == self.customizationTreeWidget.invisibleRootItem():
            return
        idx = self.getWidgetIndexFromTreeItem(treeItem)
        itemToRemove = self.contentsDict[parent.text(0)]['widgetList'].pop(idx)
        itemToRemove.setParent(None)
        self.contentsDict[parent.text(0)]['treeItem'].removeChild(treeItem)
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        exceptionList = []
        customJsonDict = dict()
        for i in self.customDict.keys():
            customJsonDict[i] = []
        correspondenceDict = {self.customDict[i]:i for i in self.customDict.keys()}
        for key in self.contentsDict.keys():
            jsonTagList = []
            for widget in self.contentsDict[key]['widgetList']:
                try:
                    jsonTagList = widget.layout().itemAt(0).widget().getJSONTag()
                except Exception as e:
                    exceptionList.append(e.args[0])
                if len(exceptionList) == 0:
                    for jsonItem in jsonTagList:
                        customJsonDict[correspondenceDict[key]].append(jsonItem)
        if self.validateJsonDict(customJsonDict):
            self.exportJson(customJsonDict)
    
    def validateJsonDict(self, customJsonDict):
        """
        Method to apply validation to customJsonDict
        """
        #TODO
        return True
    
    def exportJson(self, customJsonDict):
        try:
            fd = QFileDialog()
            filename = fd.getSaveFileName(caption=self.tr('Choose file to output'),filter=self.tr('json file (*.json)'))
            outputFile = os.path.join(filename+'.json')
            with open(outputFile, 'w') as outfile:
                json.dump(customJsonDict, outfile, sort_keys=True, indent=4)
            QMessageBox.warning(self, self.tr('Success!'), self.tr('Customization created on: ') +str(outputFile))
        except Exception as e:
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Error! Problem exporting customization: ') + e.args[0])
    
    def populateWidgetsFromSelectedFile(self):
        jsonFileName = self.selectFileWidget.fileNameList
        customJsonDict = self.utils.readJsonFile(jsonFileName)
        self.createWidgetsFromCustomJsonDict(customJsonDict)
    
    def createWidgetsFromCustomJsonDict(self, customJsonDict):
        for key in customJsonDict.keys():
            for jsonTag in customJsonDict[key]:
                self.createWidgetFromKey(key, jsonTag)
    
    def createWidgetFromKey(self, key, jsonTag):
        if key == 'attribute':
            self.addAttributeWidget(jsonTag=jsonTag)
        elif key == 'class':
            self.addClassWidget(jsonTag=jsonTag)
        elif key == 'codeName':
            self.addCodeNameWidget(jsonTag=jsonTag)
        elif key == 'default':
            self.addDefaultWidget(jsonTag=jsonTag)
        elif key == 'domain':
            self.addDomainWidget(jsonTag=jsonTag)
        elif key == 'domainValue':
            self.addDomainValueWidget(jsonTag=jsonTag)
        elif key == 'nullity':
            self.addNullityWidget(jsonTag=jsonTag)
        elif key == 'filter':
            self.addFilterWidget(jsonTag=jsonTag)
        else:
            pass
    

