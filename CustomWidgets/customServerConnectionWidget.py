# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-04
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
import os

# Qt imports
from PyQt4 import QtGui, uic
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import pyqtSlot, pyqtSignal

from DsgTools.Utils.utils import Utils
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.ServerTools.viewServers import ViewServers
from DsgTools.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.ServerTools.createView import CreateView
from DsgTools.ServerTools.manageDBAuxiliarStructure import ManageDBAuxiliarStructure
from DsgTools.ServerTools.selectStyles import SelectStyles


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customServerConnectionWidget.ui'))

class CustomServerConnectionWidget(QtGui.QWidget, FORM_CLASS):
    selectionChanged = pyqtSignal()
    resetAll = pyqtSignal()
    dbDictChanged = pyqtSignal(str,list)
    styleChanged = pyqtSignal(dict)
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
        self.serverWidget.populateServersCombo()
        self.serverWidget.abstractDbLoaded.connect(self.populatePostgisSelector)
        self.customFileSelector.filesSelected.connect(self.populateSpatialiteSelector)
        self.comboDict = {self.tr('Load EDGV v. 2.1.3'):'2.1.3', self.tr('Load EDGV v. FTer_2a_Ed'):'FTer_2a_Ed',self.tr('Load Non EDGV'):'Non_EDGV'}
        self.dbDict = {'2.1.3':[], 'FTer_2a_Ed':[]}
        self.selectedDbsDict = dict()
        self.stylesDict = dict()
        self.postgisCustomSelector.selectionChanged.connect(self.selectedDatabases)
        self.spatialiteCustomSelector.selectionChanged.connect(self.selectedFiles)
        self.path = None
        self.customFileSelector.setCaption(self.tr('Select a DSGTools Spatialite file'))
        self.customFileSelector.setFilter(self.tr('Spatialite file databases (*.sqlite)'))
        self.customFileSelector.setType('multi')
    
    def selectedDatabases(self,dbList,type):
        '''
        selectedDbsDict = { 'dbName' : 'abstractDb' }
        '''
        #TODO: build selectedDbsDict and emit dbDictChanged()
        #1- Iterate over dbList and check if all layers on dbList are on dict. If not, add it.
        if type == 'added':
            (host, port, user, password) = self.serverWidget.abstractDb.getParamsFromConectedDb()
            for dbName in dbList:
                if dbName not in self.selectedDbsDict.keys():
                    if host and port and user:
                        localDb = self.dbFactory.createDbFactory('QPSQL')
                        localDb.connectDatabaseWithParameters(host, port, dbName, user, password)
                        self.selectedDbsDict[dbName] = localDb
                        #do get dicts
                        localDict = localDb.getStyleDict(localDb.getDatabaseVersion())
                        for key in localDict.keys():
                            if key not in self.stylesDict.keys():
                                self.stylesDict[key] = dict()
                                self.stylesDict[key]['dbList'] = []
                            self.stylesDict[key]['style'] = localDict[key]
                            if dbName not in self.stylesDict[key]['dbList']:
                                self.stylesDict[key]['dbList'].append(dbName)
            self.dbDictChanged.emit('added', dbList)
            self.styleChanged.emit(self.stylesDict)
        #2- Iterate over selectedDbsDict and if there is a key not in dbList, close db and pop item
        if type == 'removed':
            for dbName in self.selectedDbsDict.keys():
                if dbName in dbList:
                    self.selectedDbsDict.pop(dbName)
            self.dbDictChanged.emit('removed', dbList)
            for key in self.stylesDict.keys():
                for db in self.stylesDict[key]['dbList']:
                    if db in dbList:
                        idx = self.stylesDict[key]['dbList'].index(db)
                        self.stylesDict[key]['dbList'].pop(idx)
                if len(self.stylesDict[key]['dbList']) == 0:
                    self.stylesDict.pop(key)
            self.styleChanged.emit(self.stylesDict)
    
    def selectedFiles(self,dbList,type):
        '''
        selectedDbsDict = { 'dbName' : 'abstractDb' }
        '''
        #TODO: build selectedDbsDict and emit dbDictChanged()
        #1- Iterate over dbList and check if all layers on dbList are on dict. If not, add it.
        if type == 'added':
            for dbName in dbList:
                if dbName not in self.selectedDbsDict.keys():
                    localDb = self.dbFactory.createDbFactory('QSQLITE')
                    localDb.connectDatabase(conn = self.spatialiteDict[dbName])
                    self.selectedDbsDict[dbName] = localDb
                    #do get dicts
                    localDict = localDb.getStyleDict(localDb.getDatabaseVersion())
                    for key in localDict.keys():
                        if key not in self.stylesDict.keys():
                            self.stylesDict[key] = dict()
                            self.stylesDict[key]['dbList'] = []
                        self.stylesDict[key]['style'] = localDict[key]
                        if dbName not in self.stylesDict[key]['dbList']:
                            self.stylesDict[key]['dbList'].append(dbName)
            self.dbDictChanged.emit('added', dbList)
            self.styleChanged.emit(self.stylesDict)
        #2- Iterate over selectedDbsDict and if there is a key not in dbList, close db and pop item
        if type == 'removed':
            for dbName in self.selectedDbsDict.keys():
                if dbName in dbList:
                    self.selectedDbsDict.pop(dbName)
            self.dbDictChanged.emit('removed', dbList)
            for key in self.stylesDict.keys():
                for db in self.stylesDict[key]['dbList']:
                    if db in dbList:
                        idx = self.stylesDict[key]['dbList'].index(db)
                        self.stylesDict[key]['dbList'].pop(idx)
                if len(self.stylesDict[key]['dbList']) == 0:
                    self.stylesDict.pop(key)
            self.styleChanged.emit(self.stylesDict)
    
    @pyqtSlot(int)
    def on_serverConnectionTab_currentChanged(self, currentTab):
        if currentTab == 0:
            self.clearSpatialiteTab()
            self.populatePostgisSelector()
        elif currentTab == 1:
            self.clearPostgisTab()
            self.populateSpatialiteSelector()
        pass
    
    def populatePostgisSelector(self):
        self.dbDict = {'2.1.3':[], 'FTer_2a_Ed':[],'Non_EDGV':[]}
        dbList = []
        try:
            if self.serverWidget.abstractDb:
                dbList = self.serverWidget.abstractDb.getEDGVDbsFromServer(parentWidget = self)
            else:
                self.clearPostgisTab()
                return
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), e.args[0])
            self.clearPostgisTab()
        dbList.sort()
        for (dbname, dbversion) in dbList:
            if dbversion in self.dbDict.keys():
                self.dbDict[dbversion].append(dbname)
            else:
                self.dbDict['Non_EDGV'].append(dbname)
#         if len(self.dbDict['2.1.3']) == 0:
#             self.postgisEdgvComboFilter.setCurrentIndex(1)
        comboText = self.postgisEdgvComboFilter.currentText()
        self.postgisCustomSelector.setInitialState(self.dbDict[self.comboDict[comboText]]) 
    
    def populateSpatialiteSelector(self):
        self.dbDict = {'2.1.3':[], 'FTer_2a_Ed':[],'Non_EDGV':[]}
        self.spatialiteDict = dict()
        dbList = []
        try:
            for dbPath in self.customFileSelector.fileNameList:
                auxAbstractDb = self.dbFactory.createDbFactory('QSQLITE')
                dbName = os.path.basename(dbPath).split('.')[0]
                self.path = os.path.dirname(dbPath)
                auxAbstractDb.connectDatabase(conn = dbPath)
                version = auxAbstractDb.getDatabaseVersion()
                dbList.append((dbName,version))
                self.spatialiteDict[dbName] = dbPath
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), e.args[0])
            self.clearSpatialiteTab()
        dbList.sort()
        for (dbname, dbversion) in dbList:
            if dbversion in self.dbDict.keys():
                self.dbDict[dbversion].append(dbname)        
#         if len(self.dbDict['2.1.3']) == 0:
#             self.spatialiteEdgvComboFilter.setCurrentIndex(1)
        comboText = self.spatialiteEdgvComboFilter.currentText()
        self.spatialiteCustomSelector.setInitialState(self.dbDict[self.comboDict[comboText]]) 
    
    def clearSpatialiteTab(self):
        pass
    
    @pyqtSlot(int)
    def on_postgisEdgvComboFilter_currentIndexChanged(self):
        comboText = self.postgisEdgvComboFilter.currentText()
        self.postgisCustomSelector.setInitialState(self.dbDict[self.comboDict[comboText]])
        self.resetAll.emit()
    
    @pyqtSlot(int)
    def on_spatialiteEdgvComboFilter_currentIndexChanged(self):
        comboText = self.spatialiteEdgvComboFilter.currentText()
        self.spatialiteCustomSelector.setInitialState(self.dbDict[self.comboDict[comboText]])
        self.resetAll.emit()
    
    def clearPostgisTab(self):
        self.postgisCustomSelector.clearAll()
        self.serverWidget.clearAll()
        self.dbDict = {'2.1.3':[], 'FTer_2a_Ed':[],'Non_EDGV':[]}
        self.selectedDbsDict = dict()
        self.resetAll.emit()
    
    def getStyles(self, type, abstractDb):
        dbVersion = abstractDb.getDatabaseVersion()
        abstractDb.checkAndCreateStyleTable()
        styles = abstractDb.getStyleDict(dbVersion)
        self.styleChanged.emit(type, styles)
    