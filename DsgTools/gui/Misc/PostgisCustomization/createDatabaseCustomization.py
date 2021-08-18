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
from builtins import range
import os, json

from qgis.core import QgsMessageLog
from qgis.gui import QgsCollapsibleGroupBox

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from qgis.PyQt.QtSql import QSqlQuery
from qgis.PyQt.QtWidgets import QFormLayout, QMessageBox, QFileDialog, QApplication
from qgis.PyQt.QtGui import QCursor

# DSGTools imports
from DsgTools.gui.CustomWidgets.CustomDbManagementWidgets.newClassWidget import NewClassWidget
from DsgTools.gui.CustomWidgets.CustomDbManagementWidgets.newAttributeWidget import NewAttributeWidget
from DsgTools.gui.CustomWidgets.CustomDbManagementWidgets.newDomainWidget import NewDomainWidget
from DsgTools.gui.CustomWidgets.CustomDbManagementWidgets.newDomainValueWidget import NewDomainValueWidget
from DsgTools.gui.CustomWidgets.CustomDbManagementWidgets.codeNameCustomizationWidget import CodeNameCustomizationWidget
from DsgTools.gui.CustomWidgets.CustomDbManagementWidgets.changeNullityWidget import ChangeNullityWidget
from DsgTools.gui.CustomWidgets.CustomDbManagementWidgets.changeFilterWidget import ChangeFilterWidget
from DsgTools.gui.CustomWidgets.CustomDbManagementWidgets.alterDefaultWidget import AlterDefaultWidget
from DsgTools.gui.CustomWidgets.SelectionWidgets.selectFileWidget import SelectFileWidget
from DsgTools.gui.Misc.PostgisCustomization.dbCustomizer import DbCustomizer
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.Utils.utils import Utils

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'createDatabaseCustomization.ui'))

class CreateDatabaseCustomization(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, customizationName, abstractDb, edgvVersion, customizationManager, customJsonDict = None, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.customizationManager = customizationManager
        self.abstractDb = abstractDb
        self.edgvVersion = edgvVersion
        self.customizationName = customizationName
        self.contentsDict = dict()
        self.populateCustomizationCombo()
        self.setWidgetsEnabled(True)
        self.utils = Utils()
        if customJsonDict:
            self.createWidgetsFromCustomJsonDict(customJsonDict)

    def clearWidgets(self):
        rootItem = self.customizationTreeWidget.invisibleRootItem()
        childNodeCount = rootItem.childCount()
        #remove widgets
        for i in range(childNodeCount):
            typeChild = rootItem.child(i)
            childCount = typeChild.childCount()
            childTextList = []
            for j in range(childCount):
                childTextList.append(typeChild.child(i).text(0))
            for childText in childTextList:
                self.removeWidget(widgetText = childText)
    
    def setWidgetsEnabled(self, enabled):
        self.customizationSelectionComboBox.setEnabled(enabled)
        self.addAttributePushButton.setEnabled(enabled)
        self.customizationTreeWidget.setEnabled(enabled)
        self.removeSelectedPushButton.setEnabled(enabled)
    
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
        for type in list(self.customDict.keys()):
            if self.customDict[type] not in list(self.contentsDict.keys()):
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
        widget = NewAttributeWidget(self.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
        self.addWidgetItem(self.tr('Attribute Customization'), self.tr('New Custom Attribute'), widget)
    
    def addClassWidget(self,uiParameterJsonDict=None):
        widget = NewClassWidget(self.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
        self.addWidgetItem(self.tr('Class Customization'), self.tr('New Custom Class'), widget)
    
    def addCodeNameWidget(self,uiParameterJsonDict=None):
        widget = CodeNameCustomizationWidget(self.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
        self.addWidgetItem(self.tr('Code Name Customization'), self.tr('New Custom Code Name'), widget)

    def addDefaultWidget(self,uiParameterJsonDict=None):
        widget = AlterDefaultWidget(self.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
        self.addWidgetItem(self.tr('Default Customization'), self.tr('New Custom Default'), widget) 

    def addDomainWidget(self,uiParameterJsonDict=None):
        widget = NewDomainWidget(self.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
        self.addWidgetItem(self.tr('Domain Customization'), self.tr('New Custom Domain'), widget)

    def addDomainValueWidget(self,uiParameterJsonDict=None):
        widget = NewDomainValueWidget(self.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
        self.addWidgetItem(self.tr('Domain Value Customization'), self.tr('New Domain Value'), widget)

    def addNullityWidget(self,uiParameterJsonDict=None):
        widget = ChangeNullityWidget(self.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
        self.addWidgetItem(self.tr('Attribute Nullity Customization'), self.tr('New Custom Attribute Nullity'), widget)

    def addFilterWidget(self,uiParameterJsonDict=None):
        widget = ChangeFilterWidget(self.abstractDb,uiParameterJsonDict = uiParameterJsonDict)
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
        item = QtWidgets.QTreeWidgetItem(parent)
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
    
    @pyqtSlot(bool, name='on_removeSelectedPushButton_clicked')
    def removeWidget(self, widgetText = None):
        if not widgetText:
            treeItemList = [self.customizationTreeWidget.currentItem()]
        else:
            treeItemList = self.customizationTreeWidget.findItems(widgetText, flags = Qt.MatchExactly)
        if len(treeItemList)>0:
            for treeItem in treeItemList:
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
        for i in list(self.customDict.keys()):
            customJsonDict[i] = []
        correspondenceDict = {self.customDict[i]:i for i in list(self.customDict.keys())}
        nCustom = 0
        for key in list(self.contentsDict.keys()):
            for widgetItem in self.contentsDict[key]['widgetList']:
                nCustom += 1
        progress = ProgressWidget(1,nCustom,self.tr('Preparing to export customizations... '), parent = self)
        progress.initBar()
        for key in list(self.contentsDict.keys()):
            jsonTagList = []
            for widget in self.contentsDict[key]['widgetList']:
                currJsonItem = {'jsonUi':None, 'dbJsonTagList':[]}
                currentWidget = widget.layout().itemAt(0).widget()
                try:
                    jsonTagList = currentWidget.getJSONTag()
                    jsonUi = currentWidget.getUiParameterJsonDict()
                except Exception as e:
                    exceptionList.append(':'.join(e.args))
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
            versionText = 'database_'+self.edgvVersion
            finalJsonDict = {versionText:customJsonDict}
            self.customizationManager.createSetting(self.customizationName, self.edgvVersion, finalJsonDict)
            QMessageBox.information(self, self.tr('Success!'), self.tr('Database Customization ') + self.customizationName + self.tr(' created successfuly!'))
            #EMIT to reload?
            self.close()
        else:
            msg = ''
            if len(exceptionList)> 0:
                msg += self.tr('\Errors occured while trying to export customs built. Check qgis log for further details.')
                for error in exceptionList:
                    QgsMessageLog.logMessage(self.tr('Customization error: ') + error, "DSGTools Plugin", Qgis.Critical)
                QMessageBox.warning(self, self.tr('Error!'), msg)
    
    def validateJsonDict(self, customJsonDict):
        """
        Method to apply validation to customJsonDict
        """
        #TODO
        return True

    def populateWidgetsFromSelectedFile(self):
        jsonFileName = self.selectFileWidget.fileNameList
        customJsonDict = self.utils.readJsonFile(jsonFileName)
        self.createWidgetsFromCustomJsonDict(customJsonDict)
    
    def createWidgetsFromCustomJsonDict(self, customJsonDict):
        for key in list(customJsonDict.keys()):
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
