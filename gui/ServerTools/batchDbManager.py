# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-07-16
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
from builtins import str
from builtins import range
import os
from os.path import expanduser

from qgis.core import QgsMessageLog, Qgis

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt, QSettings, pyqtSignal
from qgis.PyQt.QtWidgets import QListWidgetItem, QMessageBox, QMenu, QApplication, QFileDialog
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery

# DSGTools imports
from DsgTools.core.Utils.utils import Utils
from DsgTools.core.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.gui.ServerTools.viewServers import ViewServers
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory

from DsgTools.gui.DatabaseTools.UserTools.profile_editor import ProfileEditor
from DsgTools.gui.ServerTools.createView import CreateView
from DsgTools.gui.ServerTools.manageDBAuxiliarStructure import ManageDBAuxiliarStructure
from DsgTools.gui.ServerTools.selectStyles import SelectStyles
from DsgTools.core.dsgEnums import DsgEnums

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'batchDbManager.ui'))

class BatchDbManager(QtWidgets.QDialog, FORM_CLASS):
    EDGV213, EDGV_FTer_2a_Ed, Non_EDGV = list(range(3))
    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.utils = Utils()
        self.dbFactory = DbFactory()
        self.factory = SqlGeneratorFactory()
        self.showTabs(show = False)
        #setting the sql generator
        self.serverWidget.populateServersCombo()
        self.serverWidget.abstractDbLoaded.connect(self.checkSuperUser)
        self.serverWidget.abstractDbLoaded.connect(self.populateOtherInterfaces)
        self.dbsCustomSelector.setTitle(self.tr('Server Databases'))
        self.dbsCustomSelector.selectionChanged.connect(self.showTabs)
        self.dbsCustomSelector.selectionChanged.connect(self.populateStylesInterface)
        self.dbsCustomSelector.selectionChanged.connect(self.populateOtherInterfaces)
        self.previousTab = 0
        self.dbDict = {'2.1.3':[], '2.1.3 Pro':[], 'FTer_2a_Ed':[],'Non_EDGV':[], '3.0':[], '3.0 Pro':[]}
        self.correspondenceDict = {
            self.tr('Load Database Model EDGV Version 2.1.3'):'2.1.3',
            self.tr('Load Database Model EDGV Version 2.1.3 Pro'):'2.1.3 Pro',
            self.tr('Load Database Model EDGV Version 3.0'):'3.0',
            self.tr('Load Database Model EDGV Version 3.0 Pro'):'3.0 Pro',
            self.tr('Load Database Model EDGV Version FTer_2a_Ed'):'FTer_2a_Ed',
            self.tr('Load Other Database Models'):'Non_EDGV'
        }

    @pyqtSlot(bool)
    def on_closePushButton_clicked(self):
        self.done(0)
    
    def showTabs(self, show = True):
        if show:
            self.tabWidget.show()
        else:
            self.tabWidget.hide()

    def populateListWithDatabasesFromServer(self):
        try:
            dbList = self.serverWidget.abstractDb.getEDGVDbsFromServer(parentWidget = self)
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), ':'.join(e.args))

        dbList.sort()
        for (dbname, dbversion) in dbList:
            if dbversion not in list(self.dbDict.keys()):
                dbversion = 'Non_EDGV'
            if dbname not in self.dbDict[dbversion]:
                self.dbDict[dbversion].append(dbname)

    def setDatabases(self):
        self.populateListWithDatabasesFromServer()
    
    @pyqtSlot(int)
    def on_edgvComboFilter_currentIndexChanged(self, idx):
        if idx != -1 and idx != 0:
            self.dbsCustomSelector.setInitialState(self.dbDict[self.correspondenceDict[self.edgvComboFilter.currentText()]])

    def checkSuperUser(self):
        try:
            if self.serverWidget.abstractDb.checkSuperUser():
                self.setDatabases()
            else:
                QMessageBox.warning(self, self.tr('Info!'), self.tr('Connection refused. Connect with a super user to inspect server.'))
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), ':'.join(e.args))

    def getSelectedDbList(self):
        return self.dbsCustomSelector.toLs
    
    def instantiateAbstractDbs(self, instantiateTemplates = False):
        dbsDict = dict()
        selectedDbNameList = self.getSelectedDbList()
        selectedDbNameList = list(set(selectedDbNameList + ['template_edgv_213', 'template_edgv_fter_2a_ed', 'template_edgv_3', 'dsgtools_admindb'])) if instantiateTemplates else selectedDbNameList
        for dbName in selectedDbNameList:
            localDb = self.dbFactory.createDbFactory(DsgEnums.DriverPostGIS)
            localDb.connectDatabaseWithParameters(self.serverWidget.abstractDb.db.hostName(), self.serverWidget.abstractDb.db.port(), dbName, self.serverWidget.abstractDb.db.userName(), self.serverWidget.abstractDb.db.password())
            dbsDict[dbName] = localDb
        return dbsDict

    def closeAbstractDbs(self, dbsDict):
        exceptionDict = dict()
        for dbName in list(dbsDict.keys()):
            try:
                dbsDict[dbName].db.close()
            except Exception as e:
                exceptionDict[dbName] =  ':'.join(e.args)
        return exceptionDict

    def outputMessage(self, header, successList, exceptionDict):
        msg = header
        if len(successList) > 0:
            msg += self.tr('\nSuccessful databases: ')
            msg +=', '.join(successList)
        if exceptionDict != []:
            msg += self.logInternalError(exceptionDict)
        if successList != [] and exceptionDict != []:
            QMessageBox.warning(self, self.tr('Operation Complete!'), msg)
    
    def logInternalError(self, exceptionDict):
        msg = ''
        errorDbList = list(exceptionDict.keys())
        if len(errorDbList)> 0:
            msg += self.tr('\nDatabases with error:')
            msg+= ', '.join(errorDbList)
            msg+= self.tr('\nError messages for each database were output in qgis log.')
            for errorDb in errorDbList:
                msg = self.tr("Error for database {0}: ").format(errorDb, exceptionDict[errorDb])
                QgsMessageLog.logMessage(msg, "DSG Tools Plugin", Qgis.Critical)
        return msg 

    @pyqtSlot(bool)
    def on_dropDatabasePushButton_clicked(self):
        selectedDbNameList = self.getSelectedDbList()
        if len(selectedDbNameList) == 0:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Please select one or more databases to drop!'))
            return
        if QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to drop databases: ')+', '.join(selectedDbNameList), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
            return
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        successList, exceptionDict = self.batchDropDbs(selectedDbNameList)
        QApplication.restoreOverrideCursor()
        self.setDatabases()
        header = self.tr('Drop operation complete. \n')
        self.outputMessage(header, successList, exceptionDict)
        self.dbsCustomSelector.setInitialState(self.dbsCustomSelector.fromLs)

    @pyqtSlot(bool)
    def on_upgradePostgisPushButton_clicked(self):
        selectedDbNameList = self.getSelectedDbList()
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        successList, exceptionDict = self.batchUpgradePostgis(selectedDbNameList)
        QApplication.restoreOverrideCursor()
        self.setDatabases()
        header = self.tr('Upgrade Posgtis operation complete. \n')
        self.outputMessage(header, successList, exceptionDict)

    def batchUpgradePostgis(self, dbList):
        exceptionDict = dict()
        successList = []
        if QMessageBox.question(self, self.tr('Question'), self.tr('This operation will upgrade PostGIS version for templates databases as well as the selected databases. Would you like to continue?'), QMessageBox.Ok|QMessageBox.Cancel) == QMessageBox.Cancel:
            return successList, exceptionDict
        dbsDict = self.instantiateAbstractDbs(instantiateTemplates = True)
        self.closeAbstractDbs(dbsDict)
        for dbName in dbsDict:
            try:
                if self.serverWidget.abstractDb.checkIfTemplate(dbName):
                    self.serverWidget.abstractDb.setDbAsTemplate(dbName = dbName, setTemplate = False)
                    dbsDict[dbName].upgradePostgis()
                    self.serverWidget.abstractDb.setDbAsTemplate(dbName = dbName, setTemplate = True)
                    successList.append(dbName)
                else:
                    dbsDict[dbName].upgradePostgis()
                    successList.append(dbName)
            except Exception as e:
                exceptionDict[dbName] =  ':'.join(e.args)
        return successList, exceptionDict

    def batchDropDbs(self, dbList):
        exceptionDict = dict()
        successList = []
        dbsDict = self.instantiateAbstractDbs()
        self.closeAbstractDbs(dbsDict)
        for dbName in dbList:
            try:
                self.serverWidget.abstractDb.dropDatabase(dbName)
                successList.append(dbName)
            except Exception as e:
                exceptionDict[dbName] =  ':'.join(e.args)
        return successList, exceptionDict
    
    @pyqtSlot(bool)
    def on_importStylesPushButton_clicked(self):
        dbsDict = self.instantiateAbstractDbs()
        exceptionDict = dict()
        versionList = []
        if dbsDict != {}:
            for dbName in list(dbsDict.keys()):
                try:
                    version = dbsDict[dbName].getDatabaseVersion()
                    if version not in versionList:
                        versionList.append(version)
                except Exception as e:
                    exceptionDict[dbName] = ':'.join(e.args)
            if len(list(exceptionDict.keys()))>0:
                self.logInternalError(exceptionDict)
            if len(versionList) > 1:
                QMessageBox.warning(self, self.tr('Warning'), self.tr('Multiple edgv versions are not allowed!'))
                return
            styleDir = self.getStyleDir(versionList)
            styleList = self.getStyleList(styleDir)
            dlg = SelectStyles(styleList)
            dlg.exec_()
            selectedStyles = dlg.selectedStyles
            if len(selectedStyles) == 0:
                return
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            successList, exceptionDict = self.batchImportStyles(dbsDict, styleDir, selectedStyles, versionList[0])
            QApplication.restoreOverrideCursor()
            header = self.tr('Import operation complete. \n')
            self.outputMessage(header, successList, exceptionDict)
            self.populateStylesInterface()
            closeExceptionDict = self.closeAbstractDbs(dbsDict)
            self.logInternalError(closeExceptionDict)            
            
    
    def getStyleList(self, styleDir):
        #TODO: Reimplement
        styleList = []
        version = None
        if os.path.basename(styleDir) in ['edgv_213','edgv_FTer_2a_Ed', 'edgv_3']:
            version = os.path.basename(styleDir)
        else:
            parentFolder = os.path.dirname(styleDir)
            version = os.path.basename(parentFolder)
        for style in next(os.walk(styleDir))[1]:
            styleList.append('/'.join([version,style]))
        if len(styleList) == 0:
            styleList = [version+'/'+os.path.basename(styleDir)]
        return styleList
    
    def batchImportStyles(self, dbsDict, styleDir, styleList, version):
        exceptionDict = dict()
        successList = []
        for dbName in list(dbsDict.keys()):
            for style in styleList:
                try:
                    dbsDict[dbName].importStylesIntoDb(style)
                    successList.append(dbName)
                except Exception as e:
                    errors = []
                    for arg in e.args:
                        if isinstance(arg, str):
                            s = '{}'.format(arg.encode('utf-8'))
                        else:
                            s = str(arg)
                        errors.append(s)
                    exceptionDict[dbName] =  ':'.join(errors)
        return successList, exceptionDict
    
    def getStyleDir(self, versionList):
        if versionList != []:
            return os.path.join(os.path.dirname(__file__),'..', '..', 'core', 'Styles', self.serverWidget.abstractDb.versionFolderDict[versionList[0]])
        return ""
    
    def getStylesFromDbs(self, perspective = 'style'):
        '''
        Returns a dict of styles in a form acording to perspective:
            if perspective = 'style'    : [styleName][dbName][tableName] = timestamp
            if perspective = 'database' : [dbName][styleName][tableName] = timestamp 
        '''
        dbsDict = self.instantiateAbstractDbs()
        allStylesDict = dict()
        exceptionDict = dict()
        for dbName in list(dbsDict.keys()):
            try:
                newDict =dbsDict[dbName].getAllStylesDict(perspective)
                allStylesDict = self.utils.mergeDict(newDict, allStylesDict)
            except Exception as e:
                exceptionDict[dbName] = ':'.join(e.args)
        if len(list(exceptionDict.keys()))>0:
            self.logInternalError(exceptionDict)
        return allStylesDict

    def createItem(self, parent, text, column):
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setText(column, text)
        return item

    def populateStylesInterface(self):
        self.stylesTreeWidget.clear()
        allStylesDict = self.getStylesFromDbs()
        rootNode = self.stylesTreeWidget.invisibleRootItem()
        for styleName in list(allStylesDict.keys()):
            parentStyleItem = self.createItem(rootNode, styleName, 0)
            dbList = list(allStylesDict[styleName].keys())
            parentTimeList = []
            for dbName in dbList:
                dbItem = self.createItem(parentStyleItem, dbName, 1)
                tableList = list(allStylesDict[styleName][dbName].keys())
                tableList.sort()
                timeList = []
                for table in tableList:
                    tableItem = self.createItem(dbItem, table, 2)
                    timeStamp = allStylesDict[styleName][dbName][table].toString()
                    timeList.append(timeStamp)
                    tableItem.setText(3,allStylesDict[styleName][dbName][table].toString())
                parentTimeList.append(max(timeList))
                dbItem.setText(3,max(timeList))
    
    @pyqtSlot(bool)
    def on_deleteStyles_clicked(self):
        dbsDict = self.instantiateAbstractDbs()
        styleDict = self.getStylesFromDbs()
        styleList = list(styleDict.keys())
        dlg = SelectStyles(styleList)
        execStatus = dlg.exec_()
        selectedStyles = dlg.selectedStyles
        if execStatus != 0 and selectedStyles != []:
            selectedStyleDict = { k : styleDict[k] for k in selectedStyles }
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            successList, exceptionDict = self.batchDeleteStyles(dbsDict, selectedStyleDict)
            QApplication.restoreOverrideCursor()
            header = self.tr('Delete operation complete. \n')
            self.outputMessage(header, successList, exceptionDict)
            self.populateStylesInterface()
            closeExceptionDict = self.closeAbstractDbs(dbsDict)
            self.logInternalError(closeExceptionDict)       
    
    def batchDeleteStyles(self, dbsDict, styleDict):
        exceptionDict = dict()
        successList = []
        for style in list(styleDict.keys()):
            for dbName in list(styleDict[style].keys()):
                try:
                    dbsDict[dbName].deleteStyle(style)
                    successList.append(dbName)
                except Exception as e:
                    exceptionDict[dbName] =  ':'.join(e.args)
        return successList, exceptionDict
    
    def getSQLFile(self):
        fd = QFileDialog()
        filename = fd.getOpenFileName(caption=self.tr('Select a SQL file'),filter=self.tr('sql file (*.sql)'))
        return filename
    
    @pyqtSlot(bool)
    def on_customizeFromSQLFilePushButton_clicked(self):
        dbsDict = self.instantiateAbstractDbs()
        sqlFilePath = self.getSQLFile()
        if sqlFilePath == '':
            return
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        successList, exceptionDict = self.batchCustomizeFromSQLFile(dbsDict, sqlFilePath)
        QApplication.restoreOverrideCursor()
        header = self.tr('Customize from SQL file operation complete. \n')
        self.outputMessage(header, successList, exceptionDict)
        closeExceptionDict = self.closeAbstractDbs(dbsDict)
        self.logInternalError(closeExceptionDict)
    
    def batchCustomizeFromSQLFile(self, dbsDict, sqlFilePath):
        exceptionDict = dict()
        successList = []
        for dbName in list(dbsDict.keys()):
            try:
                dbsDict[dbName].runSqlFromFile(sqlFilePath)
                successList.append(dbName)
            except Exception as e:
                exceptionDict[dbName] =  ':'.join(e.args)
        return successList, exceptionDict

    def populateOtherInterfaces(self):
        dbsDict = self.instantiateAbstractDbs()
        if self.edgvComboFilter.currentIndex() != 0:
            edgvVersion = self.correspondenceDict[self.edgvComboFilter.currentText()]
            self.permissionWidget.setParameters(self.serverWidget.abstractDb, dbsDict, edgvVersion)
            # self.customizationManagerWidget.setParameters(self.serverWidget.abstractDb, edgvVersion, dbsDict = dbsDict)
            self.fieldToolBoxConfigManagerWidget.setParameters(self.serverWidget.abstractDb, edgvVersion, dbsDict = dbsDict)
            self.earthCoverageManagerWidget.setParameters(self.serverWidget.abstractDb, edgvVersion, dbsDict = dbsDict)
