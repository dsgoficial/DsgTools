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
import os
from os.path import expanduser

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, Qt, QSettings
from PyQt4.QtGui import QListWidgetItem, QMessageBox, QMenu, QApplication, QCursor, QFileDialog
from PyQt4.QtSql import QSqlDatabase,QSqlQuery

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.ServerTools.viewServers import ViewServers
from DsgTools.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.UserTools.permission_properties import PermissionProperties
from DsgTools.ServerTools.createView import CreateView
from DsgTools.ServerTools.manageDBAuxiliarStructure import ManageDBAuxiliarStructure
from DsgTools.ServerTools.selectStyles import SelectStyles



FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'batchDbManager.ui'))

class BatchDbManager(QtGui.QDialog, FORM_CLASS):
    
    def __init__(self, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.utils = Utils()
        self.dbFactory = DbFactory()
        self.factory = SqlGeneratorFactory()
        #setting the sql generator
        self.serverWidget.populateServersCombo()
        self.serverWidget.abstractDbLoaded.connect(self.checkSuperUser)
        self.dbsCustomSelector.setTitle(self.tr('Server Databases'))

    @pyqtSlot(bool)
    def on_closePushButton_clicked(self):
        self.done(0)

    def populateListWithDatabasesFromServer(self):
        dbList = []
        try:
            dbList = self.serverWidget.abstractDb.getEDGVDbsFromServer()
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), e.args[0])

        dbList.sort()
        dbTextList = []
        for (dbname, dbversion) in dbList:
            dbTextList.append(dbname+' (EDGV v. '+dbversion+')')
        return dbTextList

    def setDatabases(self):
        dbList = self.populateListWithDatabasesFromServer()
        self.dbsCustomSelector.setInitialState(dbList)        

    def checkSuperUser(self):
        try:
            if self.serverWidget.abstractDb.checkSuperUser():
                self.setDatabases()
            else:
                QMessageBox.warning(self, self.tr('Info!'), self.tr('Connection refused. Connect with a super user to inspect server.'))
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), e.args[0])

    def getSelectedDbList(self):
        return [i.split(' ')[0] for i in self.dbsCustomSelector.toLs]
    
    def instantiateAbstractDbs(self):
        dbsDict = dict()
        selectedDbNameList = self.getSelectedDbList()
        for dbName in selectedDbNameList:
            localDb = self.dbFactory.createDbFactory('QPSQL')
            localDb.connectDatabaseWithParameters(self.serverWidget.abstractDb.db.hostName(), self.serverWidget.abstractDb.db.port(), dbName, self.serverWidget.abstractDb.db.userName(), self.serverWidget.abstractDb.db.password())
            dbsDict[dbName] = localDb
        return dbsDict

    def closeAbstractDbs(self, dbsDict):
        dbsDict = dict()
        selectedDbNameList = self.getSelectedDbList()
        exceptionDict = dict()
        for dbName in dbsDict.keys():
            try:
                dbsDict[dbName].db.close()
            except Exception as e:
                exceptionDict[dbName] =  str(e.args[0])
        return exceptionDict

    def outputMessage(self, header, successList, exceptionDict):
        msg = header
        if len(successList) > 0:
            msg += self.tr('\nSuccessful databases: ')
            msg +=', '.join(successList)
        msg += self.logInternalError(exceptionDict)
        QMessageBox.warning(self, self.tr('Operation Complete!'), msg)
    
    def logInternalError(self, exceptionDict):
        msg = ''
        errorDbList = exceptionDict.keys()
        if len(errorDbList)> 0:
            msg += self.tr('\nDatabases with error:')
            msg+= ', '.join(errorDbList)
            msg+= self.tr('\nError messages for each database were output in qgis log.')
            for errorDb in errorDbList:
                QgsMessageLog.logMessage(self.tr('Error for database ')+ errorDb + ': ' +exceptionDict[errorDb], "DSG Tools Plugin", QgsMessageLog.CRITICAL)
        return msg 

    @pyqtSlot(bool)
    def on_dropDatabasePushButton_clicked(self):
        selectedDbNameList = self.getSelectedDbList()
        if len(selectedDbNameList) == 0:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Please select one or more databases to drop!'))
        if QtGui.QMessageBox.question(self, self.tr('Question'), self.tr('Do you really want to drop databases: ')+', '.join(selectedDbNameList), QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel) == QtGui.QMessageBox.Cancel:
            return
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        successList, exceptionDict = self.batchDropDbs(selectedDbNameList)
        QApplication.restoreOverrideCursor()
        self.setDatabases()
        header = self.tr('Drop operation complete. \n')
        self.outputMessage(header, successList, exceptionDict)

    def batchDropDbs(self, dbList):
        exceptionDict = dict()
        successList = []
        for dbName in dbList:
            try:
                self.serverWidget.abstractDb.dropDatabase(dbName)
                successList.append(dbName)
            except Exception as e:
                exceptionDict[dbName] =  str(e.args[0])
        return successList, exceptionDict
    
    @pyqtSlot(bool)
    def on_importStylesPushButton_clicked(self):
        dbsDict = self.instantiateAbstractDbs()
        exceptionDict = dict()
        versionList = []
        
        for dbName in dbsDict.keys():
            try:
                version = dbsDict[dbName].getDatabaseVersion()
                if version not in versionList:
                    versionList.append(version)
            except Exception as e:
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
        closeExceptionDict = self.closeAbstractDbs(dbsDict)
        self.logInternalError(closeExceptionDict)            
            
    
    def getStyleList(self, styleDir):
        #TODO: Reimplement
        styleList = []
        version = None
        if os.path.basename(styleDir) in ['edgv_213','edgv_FTer_2a_Ed']:
            version = os.path.basename(styleDir)
        else:
            parentFolder = os.path.dirname(styleDir)
            version = os.path.basename(parentFolder)
        for style in os.walk(styleDir).next()[1]:
            styleList.append('/'.join([version,style]))
        if len(styleList) == 0:
            styleList = [version+'/'+os.path.basename(styleDir)]
        return styleList
    
    def batchImportStyles(self, dbsDict, styleDir, styleList, version):
        exceptionDict = dict()
        successList = []
        for dbName in dbsDict.keys():
            for style in styleList:
                try:
                    dbsDict[dbName].importStylesIntoDb(style)
                    successList.append(dbName)
                except Exception as e:
                    exceptionDict[dbName] =  str(e.args[0])
        return successList, exceptionDict
    
    def getStyleDir(self, versionList):
        currentPath = os.path.join(os.path.dirname(__file__),'..','Styles', self.serverWidget.abstractDb.versionFolderDict[versionList[0]])
        return currentPath
                