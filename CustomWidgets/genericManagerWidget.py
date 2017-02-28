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
import os

# Qt imports
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt4.QtGui import QMessageBox, QApplication, QCursor, QFileDialog, QMenu

#DsgTools imports
from DsgTools.CustomWidgets.listSelector import ListSelector
from DsgTools.Utils.utils import Utils

from qgis.core import QgsMessageLog
import json

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'genericManagerWidget.ui'))

class GenericManagerWidget(QtGui.QWidget, FORM_CLASS):
    def __init__(self, genericDbManager = None, parent = None):
        """
        Constructor
        """
        super(GenericManagerWidget, self).__init__(parent)
        self.setupUi(self)
        self.genericDbManager = genericDbManager
        self.versionDict = {'2.1.3':1, 'FTer_2a_Ed':2}
        self.textDict = {'EarthCoverage':self.tr('Earth Coverage'), 
                            'Customization':self.tr('Customization'), 
                            'Style':self.tr('Style'), 
                            'ValidationConfig':self.tr('Validation'), 
                            'FieldToolBoxConfig':self.tr('Field Toolbox Configuration'),
                            'Permission':self.tr('Permissions')}
        self.captionDict = {'EarthCoverage':self.tr('Earth Coverage'), 
                            'Customization':self.tr('Customization'), 
                            'Style':self.tr('Style'), 
                            'ValidationConfig':self.tr('Validation'), 
                            'FieldToolBoxConfig':self.tr('Reclassification Setup Files'),
                            'Permission':self.tr('Select a dsgtools permission profile')}
        self.filterDict = {'EarthCoverage':'.dsgearthcov', 
                            'Customization':'.dsgcustom', 
                            'Style':'.dsgstyle', 
                            'ValidationConfig':'.dsgvalidcfg', 
                            'FieldToolBoxConfig':'.reclas',
                            'Permission':'.dsgperm'}
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
        if viewType == 'database':
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
        self.treeWidget.setEnabled(enabled)
        self.importPushButton.setEnabled(enabled)
        self.batchImportPushButton.setEnabled(enabled)
        self.exportPushButton.setEnabled(enabled)
        self.batchExportPushButton.setEnabled(enabled)
        self.databasePerspectivePushButton.setEnabled(enabled)
        self.propertyPerspectivePushButton.setEnabled(enabled)

    def populateConfigInterface(self, templateDb, jsonDict = None):
        '''
        Must be reimplemented in each child
        '''
        pass    

    def readJsonFromDatabase(self, propertyName, edgvVersion):
        '''
        Reads the profile file, gets a dictionary of it and builds the tree widget
        '''
        self.genericDict = self.genericDbManager.getCustomization(propertyName, edgvVersion)

    @pyqtSlot(bool)
    def on_importPushButton_clicked(self):
        fd = QFileDialog()
        widgetType = self.getWhoAmI()
        filename = fd.getOpenFileName(caption=self.captionDict[widgetType],filter=self.filterDict[widgetType])
        if filename == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Select a file to import!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.genericDbManager.importProfile(filename)
            QApplication.restoreOverrideCursor()
            QMessageBox.information(self, self.tr('Success!'), self.widgetName + self.tr(' successfully imported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, self.tr('Error!'), self.tr('Error! Problem importing ') +self.widgetName + ': '  + e.args[0])
        self.refreshProfileList()
    
    @pyqtSlot(bool)
    def on_exportPushButton_clicked(self):
        #TODO
        if not self.profilesListWidget.currentItem():
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Select a profile to export!'))
            return
        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption = self.tr('Select a folder to output'))
        if folder == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Select a output!'))
            return
        profileName = self.customListWidget.currentItem().text()
        edgvVersion = self.versionSelectionComboBox.currentText()
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.genericDbManager.exportProfile(profileName, edgvVersion, folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.information(self, self.tr('Success!'), self.widgetName + self.tr(' successfully exported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, self.tr('Error!'), self.tr('Error! Problem exporting ') + self.widgetName + ': ' + e.args[0])
        
    @pyqtSlot(bool)
    def on_batchExportPushButton_clicked(self):
        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption = self.tr('Select a folder to output'))
        if folder == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Select a output!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.genericDbManager.batchExportCustomizations(folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.information(self, self.tr('Success!'), + self.widgetName + self.tr(' successfully exported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, self.tr('Error!'), self.tr('Error! Problem exporting ') + self.widgetName + ': ' + e.args[0])
    
    @pyqtSlot(bool)
    def on_batchImportPushButton_clicked(self):
        fd = QFileDialog()
        folder = fd.getExistingDirectory(caption = self.tr('Select a folder with json files: '))
        if folder == '':
            QMessageBox.warning(self, self.tr('Warning!'), self.tr('Warning! Select a input folder!'))
            return
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            self.genericDbManager.batchImportCustomizations(folder)
            QApplication.restoreOverrideCursor()
            QMessageBox.information(self, self.tr('Success!'), + self.widgetName + self.tr(' successfully imported.'))
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(self, self.tr('Error!'), self.tr('Error! Problem importing ') + self.widgetName + ': ' + e.args[0])

    def getViewType(self):
        if self.databasePerspectivePushButton.isChecked():
            return 'database'
        else:
            return 'property'

    @pyqtSlot(bool, name='on_databasePerspectivePushButton_clicked')
    @pyqtSlot(bool, name='on_propertyPerspectivePushButton_clicked')
    def refresh(self):
        viewType = self.setHeaders()
        propertyPerspectiveDict = self.genericDbManager.getPropertyPerspectiveDict(viewType)
        self.treeWidget.clear()
        rootNode = self.treeWidget.invisibleRootItem()
        if viewType == 'database':
            propertyList = self.genericDbManager.dbDict.keys()
        else:
            propertyList = propertyPerspectiveDict.keys()
        for key in propertyList:
            parentCustomItem = self.utils.createWidgetItem(rootNode, key, 0)
            if key in propertyPerspectiveDict.keys():
                for item in propertyPerspectiveDict[key]:
                    dbItem = self.utils.createWidgetItem(parentCustomItem, item, 1)
        self.treeWidget.sortItems(0, Qt.AscendingOrder)
        self.treeWidget.expandAll()
    
    def outputMessage(self, operation, header, successDict, exceptionDict):
        '''
        successDict = {configName: [--list of successful databases--]}
        exceptionDict = {configName: {dbName: errorText}}
        '''
        viewType = self.getViewType()
        msg = header
        for setting in successDict.keys():
            successList = successDict[setting]
            if len(successDict[setting]) > 0:
                msg += self.tr('\nSuccessful ')
                msg += operation + ' : '
                msg += setting
                if len(successList) > 0:
                    msg += self.tr(' on databases ') + ', '.join(successList)
        msg += self.logInternalError(exceptionDict)
        QMessageBox.warning(self, self.tr('Operation Complete!'), msg)
    
    def logInternalError(self, exceptionDict):
        '''
        exceptionDict = {configName: {dbName: errorText}}
        '''
        msg = ''
        configList = exceptionDict.keys()
        if len(configList) > 0:
            msg += self.tr('\nConfig with error:') + ','.join(configList)
            msg+= self.tr('\nError messages for each config and database were output in qgis log.')
            for config in configList:
                for dbName in exceptionDict[config].keys():
                    if exceptionDict[config][dbName] != dict():
                        QgsMessageLog.logMessage(self.tr('Error for config ')+ config + ' in database ' +dbName+' : '+exceptionDict[config][dbName], "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        return msg 

    def manageSetting(self, config, manageType, dbList = [], parameterDict = dict()):
        if manageType == 'install':
            return self.genericDbManager.installSetting(config, dbNameList = dbList)
        elif manageType == 'delete':
            return self.genericDbManager.deleteSetting(config)
        elif manageType == 'uninstall':
            return self.genericDbManager.uninstallSetting(config)
        elif manageType == 'update':
            return self.genericDbManager.updateSetting(config, parameterDict['newJsonDict'])
        elif manageType == 'create':
            return self.genericDbManager.createSetting(config, parameterDict['newJsonDict'])

    def manageSettings(self, manageType, dbList = [], selectedConfig = [], parameterDict = dict()):
        '''
        Executes the setting work according to manageType
        successDict = {configName: [--list of successful databases--]}
        exceptionDict = {configName: {dbName: errorText}}
        '''
        if selectedConfig == []:
            availableConfig = self.genericDbManager.getPropertyPerspectiveDict().keys()
            dlg = ListSelector(availableConfig,[])
            dlg.exec_()
            selectedConfig = dlg.getSelected()
            if selectedConfig == []:
                QMessageBox.warning(self, self.tr('Warning!'), self.tr('Select at least one configuration!'))
                return (dict(),dict())
        successDict = dict()
        exceptionDict = dict()
        for config in selectedConfig:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            sucessList, errorDict = self.manageSetting(config, manageType, dbList = dbList, parameterDict = parameterDict)
            QApplication.restoreOverrideCursor()
            successDict[config] = sucessList
            if errorDict != dict():
                exceptionDict[config] = errorDict
        self.refresh()
        return successDict, exceptionDict
    
    def createMenuAssigned(self, position):
        """
        Creates a pop up menu
        """
        viewType = self.getViewType()
        if viewType == 'database':
            self.createDbPerspectiveContextMenu(position)
        if viewType == 'property':
            self.createPropertyPerspectiveContextMenu(position)

    def createDbPerspectiveContextMenu(self, position):
        menu = QMenu()
        item = self.treeWidget.itemAt(position)
        if item:
            if item.text(0) != '':
                menu.addAction(self.tr('Uninstall all settings from selected database'), self.uninstallAllSettingsFromDb)
                menu.addAction(self.tr('Manage settings from selected database'), self.manageDbSettings)
            elif item.text(1) != '':
                menu.addAction(self.tr('Update selected setting'), self.updateSelectedSetting)
                menu.addAction(self.tr('Clone selected setting'), self.cloneSelectedSetting)
                menu.addAction(self.tr('Uninstall selected setting'), self.uninstallSelectedSetting)
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
                menu.addAction(self.tr('Uninstall selected setting on all databases'), self.uninstallSelectedSettingAllDb)
                menu.addAction(self.tr('Delete selected setting'), self.deleteSelectedSetting)                
            elif item.text(1) != '':
                menu.addAction(self.tr('Manage Permissions on database'), self.managePermissionsOnDb)
                menu.addAction(self.tr('Uninstall selected setting on selected database'), self.uninstallSelectedSetting)
        menu.exec_(self.treeWidget.viewport().mapToGlobal(position))
    
    def uninstallAllSettingsFromDb(self):
        pass
    
    def manageDbSettings(self):
        pass

    def manageSelectedSetting(self):
        pass

    def updateSelectedSetting(self):
        '''
        1. get setting dict
        2. populate setting interface
        3. from new dict, update setting
        '''
        currItem = self.treeWidget.currentItem()
        if self.getViewType() == 'database':
            settingName = currItem.text(1)
        else:
            settingName = currItem.text(0)
        edgvVersion = self.genericDbManager.edgvVersion
        templateDb = self.genericDbManager.instantiateTemplateDb(edgvVersion)
        originalDict = self.genericDbManager.getSetting(settingName, edgvVersion)
        newDict = self.populateConfigInterface(templateDb, jsonDict = originalDict)
        if newDict:
            successDict, exceptionDict = self.manageSettings('update', selectedConfig = [settingName], parameterDict = {'newJsonDict':newDict})
            header, operation = self.getUpdateSelectedSettingHeader()
            self.outputMessage(operation, header, successDict, exceptionDict)
    
    def cloneSelectedSetting(self):
        currItem = self.treeWidget.currentItem()
        if self.getViewType() == 'database':
            settingName = currItem.text(1)
        else:
            settingName = currItem.text(0)
        edgvVersion = self.genericDbManager.edgvVersion
        templateDb = self.genericDbManager.instantiateTemplateDb(edgvVersion)
        originalDict = self.genericDbManager.getSetting(settingName, edgvVersion)
        newDict = self.populateConfigInterface(templateDb, jsonDict = originalDict)
        if newDict:
            successDict, exceptionDict = self.manageSettings('create', selectedConfig = [settingName], parameterDict = {'newJsonDict':newDict})
            header, operation = self.getUpdateSelectedSettingHeader()
            self.outputMessage(operation, header, successDict, exceptionDict)

    def uninstallSelectedSetting(self):
        pass
    
    def deleteSelectedSetting(self):
        pass

    def uninstallSelectedSettingAllDb(self):
        pass