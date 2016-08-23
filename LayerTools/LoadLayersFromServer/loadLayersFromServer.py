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
from PyQt4.QtGui import QListWidgetItem, QMessageBox, QMenu, QApplication, QCursor, QFileDialog, QProgressBar
from PyQt4.QtSql import QSqlDatabase,QSqlQuery

# DSGTools imports
from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.ServerTools.viewServers import ViewServers
from DsgTools.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.Factories.LayerFactoryV2.layerFactoryV2 import LayerFactory
from DsgTools.ServerTools.createView import CreateView
from DsgTools.ServerTools.manageDBAuxiliarStructure import ManageDBAuxiliarStructure
from DsgTools.ServerTools.selectStyles import SelectStyles
from DsgTools.CustomWidgets.progressWidget import ProgressWidget


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'loadLayersFromServer.ui'))

class LoadLayersFromServer(QtGui.QDialog, FORM_CLASS):
    def __init__(self, iface, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.iface = iface
        self.utils = Utils()
        self.setupUi(self)
        self.layerFactory = LayerFactory()
        self.customServerConnectionWidget.postgisCustomSelector.setTitle(self.tr('Select Databases'))
        self.customServerConnectionWidget.spatialiteCustomSelector.setTitle(self.tr('Selected Spatialites'))
        self.layersCustomSelector.setTitle(self.tr('Select layers to be loaded'))
        self.customServerConnectionWidget.dbDictChanged.connect(self.updateLayersFromDbs)
        self.customServerConnectionWidget.resetAll.connect(self.resetInterface)
        self.customServerConnectionWidget.styleChanged.connect(self.populateStyleCombo)
        self.lyrDict = dict()
    
    def resetInterface(self):
        self.layersCustomSelector.clearAll()
        self.styleComboBox.clear()
        #TODO: refresh optional parameters
        self.checkBoxOnlyWithElements.setCheckState(0)
        self.onlyParentsCheckBox.setCheckState(0)
        pass
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        self.close()
    
    def updateLayersFromDbs(self, type, dbList):
        errorDict = dict()
        if type == 'added':
            progress = ProgressWidget(1,len(dbList),self.tr('Reading selected databases... '), parent = self)
            for dbName in dbList:
                try:
                    geomDict = self.customServerConnectionWidget.selectedDbsDict[dbName].getGeomColumnDict()
                    for geom in geomDict.keys():
                        for lyr in geomDict[geom]:
                            schema, lyrName = lyr.split('.')
                            if lyrName not in self.lyrDict.keys():
                                self.lyrDict[lyrName] = dict()
                                self.lyrDict[lyrName]['dbList'] = []
                            self.lyrDict[lyrName]['schema'] = schema
                            self.lyrDict[lyrName]['cat'] = lyrName.split('_')[0]
                            if dbName not in self.lyrDict[lyrName]['dbList']:
                                self.lyrDict[lyrName]['dbList'].append(dbName)
                except Exception as e:
                    errorDict[dbName] = str(e.args[0])
                progress.step()
                
        elif type == 'removed':
            for lyr in self.lyrDict.keys():
                popList = []
                for i in range(len(self.lyrDict[lyr]['dbList'])):
                    if len(self.lyrDict[lyr]['dbList']) > 0:
                        if self.lyrDict[lyr]['dbList'][i] in dbList:
                            popList.append(i)
                popList.sort(reverse=True)
                for i in popList:
                    self.lyrDict[lyr]['dbList'].pop(i)
                if len(self.lyrDict[lyr]['dbList']) == 0:
                    self.lyrDict.pop(lyr)
        self.layersCustomSelector.setInitialState(self.lyrDict.keys(),unique = True)
    
    
    @pyqtSlot(bool)
    def on_showCategoriesRadioButton_toggled(self):
        if self.lyrDict <> dict():
            cats = []
            for lyr in self.lyrDict.keys():
                 if self.lyrDict[lyr]['cat'] not in cats:
                     cats.append(self.lyrDict[lyr]['cat'])
            self.layersCustomSelector.setInitialState(cats,unique = True)
    
    @pyqtSlot(bool)
    def on_showClassesRadioButton_toggled(self):
        if self.lyrDict <> dict():
            self.layersCustomSelector.setInitialState(self.lyrDict.keys(),unique = True)
            
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        #1- filter classes if categories is checked and build list.
        selected = self.layersCustomSelector.toLs
        selectedClasses = []
        if self.showCategoriesRadioButton.isChecked():
            for lyr in self.lyrDict.keys():
                if self.lyrDict[lyr]['cat'] in selected and lyr not in selectedClasses:
                    selectedClasses.append(lyr)
        else:
            selectedClasses = self.layersCustomSelector.toLs
        #2- get parameters
        withElements = self.checkBoxOnlyWithElements.isChecked()
        selectedStyle = None
        if self.styleComboBox.currentIndex() <> 0:
            selectedStyle = self.customServerConnectionWidget.stylesDict[self.styleComboBox.currentText()]
        onlyParents = self.onlyParentsCheckBox.isChecked()
        #3- Build factory dict
        factoryDict = dict()
        dbList = self.customServerConnectionWidget.selectedDbsDict.keys()
        for dbName in dbList:
            factoryDict[dbName] = self.layerFactory.makeFactory(self.iface, self.customServerConnectionWidget.selectedDbsDict[dbName])
        #4- load for each db
        exceptionDict = dict()
        progress = ProgressWidget(1,len(dbList),self.tr('Loading layers from selected databases... '), parent = self)
        for dbName in factoryDict.keys():
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            try:
                factoryDict[dbName].load(selectedClasses,onlyWithElements=withElements, stylePath = selectedStyle, useInheritance = onlyParents)
                progress.step()
            except Exception as e:
                exceptionDict[dbName] = str(e.args[0])
                progress.step()
        QApplication.restoreOverrideCursor()
        self.logInternalError(exceptionDict)
        self.close()
    
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

    def populateStyleCombo(self, styleDict):
        self.styleComboBox.clear()
        styleList = styleDict.keys()
        numberOfStyles = len(styleList)
        if numberOfStyles > 0:
            self.styleComboBox.addItem(self.tr('Select Style'))
            for i in range(numberOfStyles):
                self.styleComboBox.addItem(styleList[i])
        else:
            self.styleComboBox.addItem(self.tr('No available styles'))