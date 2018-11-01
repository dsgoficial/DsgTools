# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-25
        git sha              : $Format:%H$
        copyright            : (C) 2018 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
                               (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
                               borba.philipe@eb.mil.br
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
import os, sqlite3
import json

from qgis.core import QgsMessageLog, Qgis
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, Qt
from qgis.PyQt.QtWidgets import QMessageBox, QFileDialog, QApplication
from qgis.PyQt.QtGui import QCursor
from DsgTools.core.Utils.utils import Utils
from DsgTools.gui.CustomWidgets.BasicInterfaceWidgets.progressWidget import ProgressWidget
from DsgTools.gui.CustomWidgets.SelectionWidgets.tabDbSelectorWidget import TabDbSelectorWidget
from DsgTools.core.Factories.DbCreatorFactory.dbCreatorFactory import DbCreatorFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'singleDbCreator.ui'))

class CreateSingleDatabase(QtWidgets.QDialog, FORM_CLASS):
    parametersSet = pyqtSignal(dict)
    def __init__(self, manager, parentButton, parentMenu, parent=None):
        """Constructor."""
        super(CreateSingleDatabase, self).__init__()
        self.manager = manager
        self.parentButton = parentButton
        self.parentMenu = parentMenu
        self.parent = parent
        self.setupUi(self)
        # hide unnecessary parts from reused interface
        self.databaseParameterWidget.prefixLineEdit.hide()
        self.databaseParameterWidget.sufixLineEdit.hide()
        self.databaseParameterWidget.prefixLabel.hide()
        self.databaseParameterWidget.sufixLabel.hide()
        self.databaseParameterWidget.groupBox.setTitle('')
        self.databaseParameterWidget.setDbNameVisible(False)
        self.tabDbSelectorWidget.serverWidget.serverAbstractDbLoaded.connect(self.databaseParameterWidget.setServerDb)
        self.databaseParameterWidget.comboBoxPostgis.parent = self
        self.databaseParameterWidget.useFrame = False
        self.databaseParameterWidget.setDbNameVisible(True)
        self.tabDbSelectorWidget.outputDirSelector.label.setText(self.tr('Select Database Path'))
        self.okPushButton.clicked.connect(self.validateParameters)
        self.cancelPushButton.clicked.connect(self.close_)
    
    def getParameters(self):
        #Get outputDir, outputList, refSys
        parameterDict = dict()
        parameterDict['srid'] = self.databaseParameterWidget.mQgsProjectionSelectionWidget.crs().authid().split(':')[-1]
        parameterDict['version'] = self.databaseParameterWidget.getVersion()
        parameterDict['nonDefaultTemplate'] = self.databaseParameterWidget.getTemplateName()
        parameterDict['dbBaseName'] = self.databaseParameterWidget.dbNameLineEdit.text()
        parameterDict['driverName'] = self.tabDbSelectorWidget.getType()
        parameterDict['factoryParam'] = self.tabDbSelectorWidget.getFactoryCreationParam()
        parameterDict['templateInfo'] = self.databaseParameterWidget.getTemplateParameters()
        return parameterDict

    def validateParameters(self):
        #insert validation messages
        validatedDbParams = self.databaseParameterWidget.validate()
        if not validatedDbParams:
            return False
        validated = self.tabDbSelectorWidget.validate()
        if not validated:
            return False
        parameterDict = self.getParameters()
        dbDict, errorDict = self.createDatabases(parameterDict)
        creationMsg = ''
        if len(dbDict):
            creationMsg = self.tr('Database {0} successfully created.').format(', '.join(list(dbDict.keys())))
        errorMsg = ''
        if len(errorDict):
            frameList = []
            errorList = []
            for key in list(errorDict.keys()):
                errorList.append(key)
                QgsMessageLog.logMessage(self.tr('Error on {0}: ').format(key)+errorDict[key], "DSG Tools Plugin", Qgis.Critical)
            if len(errorList) > 0:
                errorMsg += self.tr('Some errors occurred while trying to create database(s) {0}').format(', '.join(errorList))
        logMsg = ''
        if errorMsg != '':
            logMsg += self.tr('Check log for more details.')
        msg = [i for i in (creationMsg, errorMsg, logMsg) if i != '']
        QMessageBox.warning(self, self.tr('Info!'), self.tr('Process finished.')+'\n'+'\n'.join(msg))
        self.close()
        return True
    
    def createDatabases(self, parameterDict):
        dbCreator = DbCreatorFactory().createDbCreatorFactory(parameterDict['driverName'], parameterDict['factoryParam'], parentWidget=self)
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        dbDict, errorDict = dict(), dict()
        try:
            newDb = dbCreator.createDb(dbName=parameterDict['dbBaseName'], srid=parameterDict['srid'],\
                                                paramDict=parameterDict['templateInfo'], parentWidget=self)
            dbDict[parameterDict['dbBaseName']] = newDb
        except Exception as e:
            errorDict[parameterDict['dbBaseName']] = ':'.join(map(str, e.args))
        QApplication.restoreOverrideCursor()        
        return dbDict, errorDict

    def initGui(self):
        """
        Instantiates user interface and prepare it to be called whenever tool button is activated. 
        """
        callback = lambda : self.manager.createDatabase(isBatchCreation=False)
        self.manager.addTool(
            text=self.tr('Create a PostGIS or a SpatiaLite Database'),
            callback=callback,
            parentMenu=self.parentMenu,
            icon='database.png',
            parentButton=self.parentButton,
            defaultButton=True
        )

    def close_(self):
        """
        Closes interface.
        """
        self.close()

    def unload(self):
        pass