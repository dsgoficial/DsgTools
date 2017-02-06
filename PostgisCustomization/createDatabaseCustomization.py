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
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from PyQt4.QtSql import QSqlQuery
from PyQt4.QtGui import QFormLayout, QMessageBox, QFileDialog, QApplication, QCursor

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
from DsgTools.CustomWidgets.progressWidget import ProgressWidget
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
        self.selectFileWidget.filter = '*.dsgtoolscustom'
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
    
    def addAttributeWidget(self,uiParameterJsonDict=None):
        widget = NewAttributeWidget(self.connectionWidget.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
        self.addWidgetItem(self.tr('Attribute Customization'), self.tr('New Custom Attribute'), widget)
    
    def addClassWidget(self,uiParameterJsonDict=None):
        widget = NewClassWidget(self.connectionWidget.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
        self.addWidgetItem(self.tr('Class Customization'), self.tr('New Custom Class'), widget)
    
    def addCodeNameWidget(self,uiParameterJsonDict=None):
        widget = CodeNameCustomizationWidget(self.connectionWidget.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
        self.addWidgetItem(self.tr('Code Name Customization'), self.tr('New Custom Code Name'), widget)

    def addDefaultWidget(self,uiParameterJsonDict=None):
        widget = AlterDefaultWidget(self.connectionWidget.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
        self.addWidgetItem(self.tr('Default Customization'), self.tr('New Custom Default'), widget) 

    def addDomainWidget(self,uiParameterJsonDict=None):
        widget = NewDomainWidget(self.connectionWidget.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
        self.addWidgetItem(self.tr('Domain Customization'), self.tr('New Custom Domain'), widget)

    def addDomainValueWidget(self,uiParameterJsonDict=None):
        widget = NewDomainValueWidget(self.connectionWidget.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
        self.addWidgetItem(self.tr('Domain Value Customization'), self.tr('New Domain Value'), widget)

    def addNullityWidget(self,uiParameterJsonDict=None):
        widget = ChangeNullityWidget(self.connectionWidget.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
        self.addWidgetItem(self.tr('Attribute Nullity Customization'), self.tr('New Custom Attribute Nullity'), widget)

    def addFilterWidget(self,uiParameterJsonDict=None):
        widget = ChangeFilterWidget(self.connectionWidget.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
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
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        exceptionList = []
        customJsonDict = dict()
        for i in self.customDict.keys():
            customJsonDict[i] = []
        correspondenceDict = {self.customDict[i]:i for i in self.customDict.keys()}
        nCustom = 0
        for key in self.contentsDict.keys():
            for widgetItem in self.contentsDict[key]['widgetList']:
                nCustom += 1
        progress = ProgressWidget(1,nCustom,self.tr('Preparing to export customizations... '), parent = self)
        progress.initBar()
        for key in self.contentsDict.keys():
            jsonTagList = []
            for widget in self.contentsDict[key]['widgetList']:
                currJsonItem = {'jsonUi':None, 'dbJsonTagList':[]}
                currentWidget = widget.layout().itemAt(0).widget()
                try:
                    jsonTagList = currentWidget.getJSONTag()
                    jsonUi = currentWidget.getUiParameterJsonDict()
                except Exception as e:
                    exceptionList.append(e.args[0])
                if len(exceptionList) == 0:
                    currJsonItem['jsonUi'] = jsonUi
                    for jsonItem in jsonTagList:
                        if jsonItem not in currJsonItem['dbJsonTagList']:
                            currJsonItem['dbJsonTagList'].append(jsonItem)
                    if currJsonItem not in customJsonDict[correspondenceDict[key]]:
                        customJsonDict[correspondenceDict[key]].append(currJsonItem)
                progress.step()
        QApplication.restoreOverrideCursor()
        if self.validateJsonDict(customJsonDict) and len(exceptionList) == 0:
            self.exportJson(customJsonDict)
        else:
            msg = ''
            if len(exceptionList)> 0:
                msg += self.tr('\Errors occured while trying to export customs built. Check qgis log for further details.')
                for error in exceptionList:
                    QgsMessageLog.logMessage(self.tr('Customization error: ') + error, "DSG Tools Plugin", QgsMessageLog.CRITICAL)
                QMessageBox.warning(self, self.tr('Error!'), msg)
    
    def validateJsonDict(self, customJsonDict):
        """
        Method to apply validation to customJsonDict
        """
        #TODO
        return True
    
    def exportJson(self, customJsonDict):
        try:
            fd = QFileDialog()
            filename = fd.getSaveFileName(caption=self.tr('Choose file to output'),filter=self.tr('DSGTools Customization File (*.dsgtoolscustom)'))
            if '.dsgtoolscustom' not in filename:
                outputFile = os.path.join(filename+'.dsgtoolscustom')
            else:
                outputFile = filename
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
                self.createWidgetFromKey(key, jsonTag['jsonUi'])
    
    def createWidgetFromKey(self, key, uiParameterJsonDict):
        if key == 'attribute':
            self.addAttributeWidget(uiParameterJsonDict=uiParameterJsonDict)
        elif key == 'class':
            self.addClassWidget(uiParameterJsonDict=uiParameterJsonDict)
        elif key == 'codeName':
            self.addCodeNameWidget(uiParameterJsonDict=uiParameterJsonDict)
        elif key == 'default':
            self.addDefaultWidget(uiParameterJsonDict=uiParameterJsonDict)
        elif key == 'domain':
            self.addDomainWidget(uiParameterJsonDict=uiParameterJsonDict)
        elif key == 'domainValue':
            self.addDomainValueWidget(uiParameterJsonDict=uiParameterJsonDict)
        elif key == 'nullity':
            self.addNullityWidget(uiParameterJsonDict=uiParameterJsonDict)
        elif key == 'filter':
            self.addFilterWidget(uiParameterJsonDict=uiParameterJsonDict)
        else:
            pass
    

