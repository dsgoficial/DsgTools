# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-02-24
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
from builtins import str
from builtins import range
import os

# Qt imports
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, Qt, pyqtSignal
from qgis.PyQt.QtWidgets import QMessageBox, QApplication, QFileDialog, QMenu, QHeaderView
from qgis.PyQt.QtGui import QCursor

#DsgTools imports
from DsgTools.gui.CustomWidgets.SelectionWidgets.listSelector import ListSelector
from DsgTools.core.Utils.utils import Utils
from DsgTools.core.dsgEnums import DsgEnums

from qgis.core import QgsMessageLog
import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'genericManagerWidget.ui'))

class GenericManagerWidget(QtWidgets.QWidget, FORM_CLASS):
    Install, Delete, Uninstall, Update, Create = list(range(5))
    def __init__(self, genericDbManager = None, parent = None):
        """
        Constructor
        """
        super(GenericManagerWidget, self).__init__(parent)
        self.setupUi(self)
        self.genericDbManager = genericDbManager
        self.textDict = {'EarthCoverage':self.tr('Earth Coverage'), 
                            'Customization':self.tr('Customization'), 
                            'Style':self.tr('Style'), 
                            'ValidationConfig':self.tr('Validation'), 
                            'FieldToolBoxConfig':self.tr('Field Toolbox Configuration'),
                            'Permission':self.tr('Permissions'),
                            'AttributeRules':self.tr('Attribute Rule Configuration'),
                            'SpatialRuleConfig':self.tr('Spatial Rule Configuration')}
        self.captionDict = {'EarthCoverage':self.tr('Earth Coverage'), 
                            'Customization':self.tr('Customization'), 
                            'Style':self.tr('Style'), 
                            'ValidationConfig':self.tr('Validation'), 
                            'FieldToolBoxConfig':self.tr('Reclassification Setup Files'),
                            'Permission':self.tr('Select a dsgtools permission profile'),
                            'AttributeRules':self.tr('Attribute Rule Configuration file'),
                            'SpatialRuleConfig':self.tr('Spatial Rule Configuration file')}
        self.filterDict = {'EarthCoverage':self.tr('Earth Coverage Setup File (*.dsgearthcov)'), 
                            'Customization':self.tr('DsgTools Customization File (*.dsgcustom)'), 
                            'Style':self.tr('DsgTools Styles File (*.dsgstyle)'), 
                            'ValidationConfig':self.tr('DsgTools Validation Configuration File (*.dsgvalidcfg)'), 
                            'FieldToolBoxConfig':self.tr('Reclassification Setup Files (*.reclas)'),
                            'Permission':self.tr('DsgTools Permission Profile File (*.dsgperm)'),
                            'AttributeRules':self.tr('Attribute Rule Configuration file (*.dsgattrrul)'),
                            'SpatialRuleConfig':self.tr('Spatial Rule Configuration file (*.dsgspatrul)')}
        self.widgetName = self.textDict[self.getWhoAmI()]
        self.genericDict = None
        self.setComponentsEnabled(False)
        self.utils = Utils()
        self.setHeaders()
        self.setButtons()
        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.createMenuAssigned)
       
    def setButtons(self):
        createText = self.createPushButton.text()
        self.createPushButton.setText(createText.replace(self.tr('Setting'),self.widgetName))
        deleteText = self.deletePushButton.text()
        self.deletePushButton.setText(deleteText.replace(self.tr('Setting'),self.widgetName))
    
    def setHeaders(self):
        viewType = self.getViewType()
        if viewType == DsgEnums.Database:
            self.treeWidget.setHeaderLabels([self.tr('Database'), self.widgetName])
        else:
            self.treeWidget.setHeaderLabels([self.widgetName, self.tr('Database')])
        return viewType
    
    def getWhoAmI(self):
        return str(self.__class__).split('.')[-1].replace('\'>', '').replace('ManagerWidget','')
    
    def setChildParameter(self):
        """
        Reimplement in each child
        """
        pass
    
    def setComponentsEnabled(self, enabled):
        """
        Changes states of all components of the widget, according to the boolean parameter enabled.
        """
        self.treeWidget.setEnabled(enabled)
        self.importPushButton.setEnabled(enabled)
        self.batchImportPushButton.setEnabled(enabled)
        self.exportPushButton.setEnabled(enabled)
        self.batchExportPushButton.setEnabled(enabled)
        self.databasePerspectivePushButton.setEnabled(enabled)
        self.propertyPerspectivePushButton.setEnabled(enabled)

    def populateConfigInterface(self, templateDb, jsonDict = None):
        """
        Must be reimplemented in each child
        """
        pass    

    def readJsonFromDatabase(self, propertyName, edgvVersion):
        """
        Reads the profile file, gets a dictionary of it and builds the tree widget
        """
        self.genericDict = self.genericDbManager.getCustomization(propertyName, edgvVersion)

    @pyqtSlot(bool)
    def on_importPushButton_clicked(self):
        """
        Imports a property file into dsgtools_admindb
        """
        fd = QFileDialog()
        widgetType = self.getWhoAmI()
        filename = fd.getOpenFileName(caption=self.captionDict[widgetType],filter=self.filterDict[widgetType])[0]
        if filename == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Select a file to import!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.genericDbManager.importSetting(filename)
            QApplication.restoreOverrideCursor()
            QMessageBox.information(self, self.tr('Success!'), self.widgetName + self.tr(' successfully imported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, self.tr('Error!'), self.tr('Error! Problem importing ') +self.widgetName + ': '  + ':'.join(e.args))
        self.refresh()
    
    @pyqtSlot(bool)
    def on_exportPushButton_clicked(self):
        """
        Export selected properties.
        """
        exportPropertyList = self.selectConfig()
        if exportPropertyList is None:
            # user cancelled
            return
        if exportPropertyList == []:
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Select a profile to export!'))
            return
        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption = self.tr('Select a folder to output'))
        if folder == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Select a output!'))
            return
        edgvVersion = self.genericDbManager.edgvVersion
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            for exportProperty in exportPropertyList:
                self.genericDbManager.exportSetting(exportProperty, edgvVersion, folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.information(self, self.tr('Success!'), self.widgetName + self.tr(' successfully exported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, self.tr('Error!'), self.tr('Error! Problem exporting ') + self.widgetName + ': ' + ':'.join(e.args))
        
    @pyqtSlot(bool)
    def on_batchExportPushButton_clicked(self):
        """
        Exports all configs from dsgtools_admindb.
        """
        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption = self.tr('Select a folder to output'))
        if folder == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Select a output!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.genericDbManager.batchExportSettings(folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.information(self, self.tr('Success!'), self.widgetName + self.tr(' successfully exported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, self.tr('Error!'), self.tr('Error! Problem exporting ') + self.widgetName + ': ' + ':'.join(e.args))
    
    @pyqtSlot(bool)
    def on_batchImportPushButton_clicked(self):
        """
        Imports all config files from a folder into dsgtools_admindb. It only works for a single type of config per time.
        """
        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption = self.tr('Select a folder with json files: '))
        if folder == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Select a input folder!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.genericDbManager.batchImportSettings(folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.information(self, self.tr('Success!'), self.widgetName + self.tr(' successfully imported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, self.tr('Error!'), self.tr('Error! Problem importing ') + self.widgetName + ': ' + ':'.join(e.args))

    @pyqtSlot(bool)
    def on_applyPushButton_clicked(self):
        dbList = list(self.genericDbManager.dbDict.keys())
        successDict, exceptionDict = self.manageSettings(GenericManagerWidget.Install, dbList = dbList)
        if successDict == {} and  exceptionDict == {}:
            return
        header, operation = self.getApplyHeader()
        self.outputMessage(operation, header, successDict, exceptionDict)

    @pyqtSlot(bool)
    def on_deletePushButton_clicked(self):
        successDict, exceptionDict = self.manageSettings(GenericManagerWidget.Delete)
        if successDict == {} and  exceptionDict == {}:
            return
        header, operation = self.getDeleteHeader()
        self.outputMessage(operation, header, successDict, exceptionDict)

    @pyqtSlot(bool)
    def on_uninstallFromSelectedPushButton_clicked(self):
        dbList = []
        successDict, exceptionDict = self.manageSettings(GenericManagerWidget.Uninstall, dbList)
        if successDict == {} and  exceptionDict == {}:
            return
        header, operation = self.getUninstallFromSelected()
        self.outputMessage(operation, header, successDict, exceptionDict)

    def getViewType(self):
        if self.databasePerspectivePushButton.isChecked():
            return DsgEnums.Database
        else:
            return DsgEnums.Property

    @pyqtSlot(bool, name='on_databasePerspectivePushButton_clicked')
    @pyqtSlot(bool, name='on_propertyPerspectivePushButton_clicked')
    def refresh(self):
        viewType = self.setHeaders()
        propertyPerspectiveDict = self.genericDbManager.getPropertyPerspectiveDict(viewType)
        self.treeWidget.clear()
        rootNode = self.treeWidget.invisibleRootItem()
        if viewType == DsgEnums.Database:
            propertyList = list(self.genericDbManager.dbDict.keys())
        else:
            propertyList = list(propertyPerspectiveDict.keys())
        for key in propertyList:
            parentCustomItem = self.utils.createWidgetItem(rootNode, key, 0)
            if key in list(propertyPerspectiveDict.keys()):
                for item in propertyPerspectiveDict[key]:
                    if item and item != '':
                        dbItem = self.utils.createWidgetItem(parentCustomItem, item, 1)
        self.treeWidget.sortItems(0, Qt.AscendingOrder)
        self.treeWidget.expandAll()
        self.treeWidget.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.treeWidget.header().setStretchLastSection(False)
    
    def outputMessage(self, operation, header, successDict, exceptionDict):
        """
        successDict = {configName: [--list of successful databases--]}
        exceptionDict = {configName: {dbName: errorText}}
        """
        viewType = self.getViewType()
        msg = header
        for setting in list(successDict.keys()):
            successList = successDict[setting]
            if len(successDict[setting]) > 0:
                msg += self.tr('\nSuccessful ')
                msg += operation + ' : '
                msg += setting
                if successList:
                    if len(successList) > 0:
                        try:
                            msg += self.tr(' on databases ') + ', '.join(successList)
                        except: #none type case, just add .
                            msg += '.'
        msg += self.logInternalError(exceptionDict)
        QMessageBox.warning(self, self.tr('Operation Complete!'), msg)
    
    def logInternalError(self, exceptionDict):
        """
        exceptionDict = {configName: {dbName: errorText}}
        """
        msg = ''
        configList = list(exceptionDict.keys())
        if len(configList) > 0:
            msg += self.tr('\nConfig with error:') + ','.join(configList)
            msg+= self.tr('\nError messages for each config and database were output in qgis log.')
            for config in configList:
                for dbName in list(exceptionDict[config].keys()):
                    if exceptionDict[config][dbName] != dict():
                        QgsMessageLog.logMessage(self.tr('Error for config ')+ config + ' in database ' +dbName+' : '+exceptionDict[config][dbName], "DSG Tools Plugin", Qgis.Critical)
        return msg 

    def manageSetting(self, config, manageType, dbList = [], parameterDict = dict()):
        if manageType == GenericManagerWidget.Install:
            return self.genericDbManager.installSetting(config, dbNameList = dbList)
        elif manageType == GenericManagerWidget.Delete:
            return self.genericDbManager.deleteSetting(config)
        elif manageType == GenericManagerWidget.Uninstall:
            return self.genericDbManager.uninstallSetting(config, dbNameList = dbList)
        elif manageType == GenericManagerWidget.Update:
            return self.genericDbManager.updateSetting(config, parameterDict['newJsonDict'])
        elif manageType == GenericManagerWidget.Create:
            return self.genericDbManager.createSetting(config, parameterDict['newJsonDict'])
    
    def selectConfig(self):
        availableConfig = list(self.genericDbManager.getPropertyPerspectiveDict().keys())
        dlg = ListSelector(availableConfig,[])
        res = dlg.exec_()
        if res == 0:
            # to identify when user presses Cancel
            return None
        selectedConfig = dlg.getSelected()
        return selectedConfig

    def manageSettings(self, manageType, dbList=None, selectedConfig=None, parameterDict = dict()):
        """
        Executes the setting work according to manageType
        successDict = {configName: [--list of successful databases--]}
        exceptionDict = {configName: {dbName: errorText}}
        """

        if selectedConfig is None:
            selectedConfig = self.selectConfig()
            if selectedConfig is None:
                # user cancelled
                return dict(), dict()
            if selectedConfig == []:
                QMessageBox.warning(self, self.tr('Warning!'), self.tr('Select at least one configuration!'))
                return (dict(),dict())
        successDict = dict()
        exceptionDict = dict()
        dbList = [] if dbList is None else dbList
        if self.lookAndPromptForStructuralChanges(dbList = dbList):
            for config in selectedConfig:
                QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                sucessList, errorDict = self.manageSetting(config, manageType, dbList = dbList, parameterDict = parameterDict)
                QApplication.restoreOverrideCursor()
                successDict[config] = sucessList
                if errorDict != dict():
                    exceptionDict[config] = errorDict
            self.refresh()
            return successDict, exceptionDict
        else:
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Operation canceled by user!'))
            return (dict(),dict())
    
    def createMenuAssigned(self, position):
        """
        Creates a pop up menu
        """
        viewType = self.getViewType()
        if viewType == DsgEnums.Database:
            self.createDbPerspectiveContextMenu(position)
        if viewType == DsgEnums.Property:
            self.createPropertyPerspectiveContextMenu(position)

    def createDbPerspectiveContextMenu(self, position):
        menu = QMenu()
        item = self.treeWidget.itemAt(position)
        if item:
            if item.text(0) != '':
                menu.addAction(self.tr('Uninstall all settings from selected database'), self.uninstallSettings)
                menu.addAction(self.tr('Manage settings from selected database'), self.manageDbSettings)
            elif item.text(1) != '':
                menu.addAction(self.tr('Update selected setting'), self.updateSelectedSetting)
                menu.addAction(self.tr('Clone selected setting'), self.cloneSelectedSetting)
                menu.addAction(self.tr('Uninstall selected setting'), self.uninstallSettings)
                menu.addAction(self.tr('Delete selected setting'), self.deleteSelectedSetting)
        menu.exec_(self.treeWidget.viewport().mapToGlobal(position))
    
    def createPropertyPerspectiveContextMenu(self, position):
        menu = QMenu()
        item = self.treeWidget.itemAt(position)
        if item:
            if item.text(0) != '':
                menu.addAction(self.tr('Update selected setting'), self.updateSelectedSetting)
                menu.addAction(self.tr('Clone selected setting'), self.cloneSelectedSetting)
                menu.addAction(self.tr('Manage selected setting'), self.manageSelectedSetting)
                menu.addAction(self.tr('Uninstall selected setting on all databases'), self.uninstallSettings)
                menu.addAction(self.tr('Delete selected setting'), self.deleteSelectedSetting)                
            elif item.text(1) != '':
                menu.addAction(self.tr('Manage Settings on database'), self.manageDbSettings)
                menu.addAction(self.tr('Uninstall selected setting on selected database'), self.uninstallSettings)
        menu.exec_(self.treeWidget.viewport().mapToGlobal(position))
    
    def manageDbSettings(self):
        """
        1. get installed profiles and available profiles
        2. populate selection with items from #1
        3. get final lists and uninstall items and them install items
        """
        uiParameterDict = self.getParametersFromInterface()
        propertyPerspectiveDict = self.genericDbManager.getPropertyPerspectiveDict()
        availableConfig = [i for i in list(propertyPerspectiveDict.keys()) if i not in uiParameterDict['parameterList']]
        dlg = ListSelector(availableConfig,uiParameterDict['parameterList'])
        dlg.exec_()
        fromLs, toLs = dlg.getInputAndOutputLists()
        #build install list: elements from toLs that were not in uiParameterDict['parameterList']
        installList = [i for i in toLs if i not in uiParameterDict['parameterList']]
        #build uninstall list: : elements fromLs that were not in availableConfig
        uninstallList = [i for i in fromLs if i in uiParameterDict['parameterList']]
        if (installList == [] and uninstallList == []):
            QMessageBox.warning(self, self.tr('Error!'), self.tr('Select at least one configuration to manage!'))
            return
        if installList != []:
            #install:
            successDict, exceptionDict = self.manageSettings(GenericManagerWidget.Install, selectedConfig = installList, dbList = uiParameterDict['databaseList'])
            header, operation = self.getApplyHeader()
            self.outputMessage(operation, header, successDict, exceptionDict)
        if uninstallList != []:
            #uninstall:
            successDict, exceptionDict = self.manageSettings(GenericManagerWidget.Uninstall, selectedConfig = uninstallList, dbList = uiParameterDict['databaseList'])
            header, operation = self.getUninstallSelectedSettingHeader()
            self.outputMessage(operation, header, successDict, exceptionDict)

    def manageSelectedSetting(self):
        """
        1. get installed profiles and available profiles
        2. populate selection with items from #1
        3. get final lists and uninstall items and them install items
        """
        uiParameterDict = self.getParametersFromInterface()
        propertyPerspectiveDict = self.genericDbManager.getPropertyPerspectiveDict(viewType = DsgEnums.Database)
        availableDb = [i for i in list(propertyPerspectiveDict.keys()) if i not in uiParameterDict['databaseList']]
        dlg = ListSelector(availableDb,uiParameterDict['databaseList'])
        dlg.exec_()
        fromLs, toLs = dlg.getInputAndOutputLists()
        #build install list: elements from toLs that were not in uiParameterDict['parameterList']
        installList = [i for i in toLs if i not in uiParameterDict['databaseList']]
        #build uninstall list: : elements fromLs that were not in availableConfig
        uninstallList = [i for i in fromLs if i in uiParameterDict['databaseList']]
        if (installList == [] and uninstallList == []):
            QMessageBox.warning(self, self.tr('Error!'), self.tr('Select at least one configuration database to manage!'))
            return
        if installList != []:
            #install:
            successDict, exceptionDict = self.manageSettings(GenericManagerWidget.Install, selectedConfig = uiParameterDict['parameterList'], dbList = installList)
            header, operation = self.getApplyHeader()
            self.outputMessage(operation, header, successDict, exceptionDict)
        if uninstallList != []:
            #uninstall:
            successDict, exceptionDict = self.manageSettings(GenericManagerWidget.Uninstall, selectedConfig = uiParameterDict['parameterList'], dbList = uninstallList)
            header, operation = self.getUninstallSelectedSettingHeader()
            self.outputMessage(operation, header, successDict, exceptionDict)

    def updateSelectedSetting(self):
        """
        1. get setting dict
        2. populate setting interface
        3. from new dict, update setting
        """
        currItem = self.treeWidget.currentItem()
        if self.getViewType() == DsgEnums.Database:
            settingName = currItem.text(1)
        else:
            settingName = currItem.text(0)
        edgvVersion = self.genericDbManager.edgvVersion
        templateDb = self.genericDbManager.instantiateTemplateDb(edgvVersion)
        originalDict = self.genericDbManager.getSetting(settingName, edgvVersion)
        newDict = self.populateConfigInterface(templateDb, jsonDict = originalDict)
        if newDict:
            successDict, exceptionDict = self.manageSettings(GenericManagerWidget.Update, selectedConfig = [settingName], parameterDict = {'newJsonDict':newDict})
            header, operation = self.getUpdateSelectedSettingHeader()
            self.outputMessage(operation, header, successDict, exceptionDict)
    
    def cloneSelectedSetting(self):
        currItem = self.treeWidget.currentItem()
        if self.getViewType() == DsgEnums.Database:
            settingName = currItem.text(1)
        else:
            settingName = currItem.text(0)
        edgvVersion = self.genericDbManager.edgvVersion
        templateDb = self.genericDbManager.instantiateTemplateDb(edgvVersion)
        originalDict = self.genericDbManager.getSetting(settingName, edgvVersion)
        newDict = self.populateConfigInterface(templateDb, jsonDict = originalDict)
        if newDict:
            successDict, exceptionDict = self.manageSettings(GenericManagerWidget.Create, selectedConfig = [settingName], parameterDict = {'newJsonDict':newDict})
            header, operation = self.getUpdateSelectedSettingHeader()
            self.outputMessage(operation, header, successDict, exceptionDict)

    def getParametersFromInterface(self):
        """
        Gets selected database and selected property. 
        Returns {'databaseList':dbList, 'parameterList':parameterList}
        """
        currItem = self.treeWidget.currentItem()
        if self.getViewType() == DsgEnums.Database:
            #2 possibilities: leaf (if first column is '') or parent (if first column != '')
            if currItem.text(0) == '':
                #leaf -> must get 
                parentNode = currItem.parent()
                dbName = parentNode.text(0)
                parameter = currItem.text(1)
                return {'databaseList':[dbName], 'parameterList':[parameter]}
            else:
                #parent
                dbName = currItem.text(0)
                childCount = currItem.childCount()
                parameterList = []
                for i in range(childCount):
                    childNode = currItem.child(i)
                    parameterName = childNode.text(1)
                    if parameterName not in parameterList:
                        parameterList.append(parameterName)
                return {'databaseList':[dbName], 'parameterList':parameterList}
        else:
            if currItem.text(0) == '':
                #leaf
                parentNode = currItem.parent()
                parameter = parentNode.text(0)
                dbName = currItem.text(1)
                return {'databaseList':[dbName], 'parameterList':[parameter]}
            else:
                #parent
                parameter = currItem.text(0)
                childCount = currItem.childCount()
                dbList = []
                for i in range(childCount):
                    childNode = currItem.child(i)
                    dbName = childNode.text(1)
                    if dbName not in dbList:
                        dbList.append(dbName)
                return {'databaseList':dbList, 'parameterList':[parameter]}

    def uninstallSettings(self):
        edgvVersion = self.genericDbManager.edgvVersion
        uiParameterDict = self.getParametersFromInterface()
        successDict, exceptionDict = self.manageSettings(GenericManagerWidget.Uninstall, dbList = uiParameterDict['databaseList'], selectedConfig = uiParameterDict['parameterList'])
        header, operation = self.getUninstallSelectedSettingHeader()
        self.outputMessage(operation, header, successDict, exceptionDict)
    
    def deleteSelectedSetting(self):
        edgvVersion = self.genericDbManager.edgvVersion
        uiParameterDict = self.getParametersFromInterface()
        settingTextList = ', '.join(uiParameterDict['parameterList'])
        if QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to delete ')+settingTextList+'?', QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
            return
        successDict, exceptionDict = self.manageSettings(GenericManagerWidget.Delete, selectedConfig = uiParameterDict['parameterList'])
        header, operation = self.getDeleteHeader()
        self.outputMessage(operation, header, successDict, exceptionDict)
    
    def lookAndPromptForStructuralChanges(self, dbList = []):
        '''
        Returns True if user accepts the process
        '''
        structuralChanges = self.genericDbManager.hasStructuralChanges(dbList)
        if structuralChanges != []:
            dbChangeList = ', '.join(structuralChanges)
            if QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to apply selected operation on ')+dbChangeList+'?'+self.tr(' (Data may be lost in the process)'), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
                return False
            else:
                return True
        else:
            return True
