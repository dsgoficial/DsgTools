# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-02-25
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
    os.path.dirname(__file__), 'createBatchIncrementingSpatialite.ui'))

class CreateBatchIncrementingSpatialite(QtGui.QWizardPage, FORM_CLASS):
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
        self.outputDirSelector.setCaption(self.tr('Select the output dir'))
        self.outputDirSelector.setFilter(self.tr('Comma Separated Values File (*.csv)'))
        self.outputDirSelector.setType('dir')
        self.outputDirSelector.setTitle(self.tr('Output Directory'))
    
    def getParameters(self):
        #Get outputDir, outputList, refSys
        parameterDict = dict()
        parameterDict['driverName'] = 'QSQLITE'
        parameterDict['output'] = self.outputDirSelector.fileNameList[0]
        parameterDict['outputList'] = self.getOutputDbNameList()
        parameterDict['crs'] = self.mQgsProjectionSelectionWidget.crs()
        return parameterDict
    
    def getOutputDbNameList(self):
        prefix = None
        sufix = None
        dbBaseName = self.dbNameLineEdit.text()
        outputPath = self.outputDirSelector.fileNameList[0]
        outputDbNameList = []
        if self.prefixLineEdit.text() <> '':
            prefix = self.prefixLineEdit.text()
        if self.sufixLineEdit.text() <> '':
            sufix = self.sufixLineEdit.text()
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
        if self.dbNameLineEdit.text() == '':
            return False
        if self.outputDirSelector.fileNameList == []:
            return False
        if self.mQgsProjectionSelectionWidget.crs().authid() == '':
            return False
        parameterDict = self.getParameters()
        self.loadDatabases(parameterDict)
        return True
    
    def loadDatabases(self,parameterDict):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        for dbName in parameterDict['outputList']:
            try:
                self.createDatabase(dbName,int(parameterDict['crs'].authid().split(':')[-1]))
            except Exception as e:
                QApplication.restoreOverrideCursor()
                raise e
        QApplication.restoreOverrideCursor()
    
    def getTemplateLocation(self):
        currentPath = os.path.dirname(__file__)
        if self.versionComboBox.currentText() == '2.1.3':
            edgvPath = os.path.join(currentPath, '..', 'SpatialiteTool','template', '213', 'seed_edgv213.sqlite')
        elif self.versionComboBox.currentText() == 'FTer_2a_Ed':
            edgvPath = os.path.join(currentPath, '..', 'SpatialiteTool', 'template', 'FTer_2a_Ed', 'seed_edgvfter_2a_ed.sqlite')
        return edgvPath
    
    def createDatabase(self,destino,srid):
        f = open(self.getTemplateLocation(),'rb')
        g = open(destino,'wb')
        x = f.readline()
        while x:
            g.write(x)
            x = f.readline()

        g.close()

        con = sqlite3.connect(destino)
        cursor = con.cursor()
        srid_sql = (srid,)
        cursor.execute("UPDATE geometry_columns SET srid=?",srid_sql)
        con.commit()
        con.close()