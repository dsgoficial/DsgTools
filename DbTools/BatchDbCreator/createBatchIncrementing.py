# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-25
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
import os, sqlite3
import json

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt4.QtGui import QMessageBox, QFileDialog, QApplication, QCursor
from fileinput import filename
from DsgTools.Utils.utils import Utils
from DsgTools.CustomWidgets.progressWidget import ProgressWidget

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'createBatchIncrementing.ui'))

class CreateBatchIncrementing(QtGui.QWizardPage, FORM_CLASS):
    parametersSet = pyqtSignal(dict)
    def __init__(self, parent=None):
        '''Constructor.'''
        super(self.__class__, self).__init__()
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
    
    def getParameters(self):
        #Get outputDir, outputList, refSys
        parameterDict = dict()
        parameterDict['driverName'] = 'QSQLITE'
        parameterDict['output'] = self.outputDirSelector.fileNameList[0]
        parameterDict['outputList'] = self.getOutputDbNameList()
        parameterDict['crs'] = self.databaseParameterWidget.mQgsProjectionSelectionWidget.crs()
        parameterDict['version'] = self.databaseParameterWidget.getVersion()
        return parameterDict
    
    def getOutputDbNameList(self):
        prefix = None
        sufix = None
        dbBaseName = self.databaseParameterWidget.dbNameLineEdit.text()
        outputPath = self.outputDirSelector.fileNameList[0]
        outputDbNameList = []
        if self.databaseParameterWidget.prefixLineEdit.text() <> '':
            prefix = self.databaseParameterWidget.prefixLineEdit.text()
        if self.databaseParameterWidget.sufixLineEdit.text() <> '':
            sufix = self.databaseParameterWidget.sufixLineEdit.text()
        for i in range(self.spinBox.value()):
            attrNameList = []
            if prefix:
                attrNameList.append(prefix)
            attrNameList.append(dbBaseName+str(i+1))
            if sufix:
                attrNameList.append(sufix)
            dbName = '_'.join(attrNameList)
            fullPath = os.path.join(outputPath,dbName+'.sqlite')
            outputDbNameList.append(fullPath)
        return outputDbNameList

    def validatePage(self):
        #insert validation messages
        validated = self.databaseParameterWidget.validate()
        if not validated:
            return False
        parameterDict = self.getParameters()
        self.loadDatabases(parameterDict)
        return True
    
    def loadDatabases(self,parameterDict):
        creator = SpatialiteCreator(parameterDict['version'])
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        for dbName in parameterDict['outputList']:
            try:
                creator.createDatabase(dbName,int(parameterDict['crs'].authid().split(':')[-1]))
            except Exception as e:
                QApplication.restoreOverrideCursor()
                raise e
        QApplication.restoreOverrideCursor()
    