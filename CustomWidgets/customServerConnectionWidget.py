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
        self.setupUi(self)
        self.utils = Utils()
        self.dbFactory = DbFactory()
        self.factory = SqlGeneratorFactory()
        self.serverWidget.populateServersCombo()
        self.serverWidget.abstractDbLoaded.connect(self.populatePostgisSelector)
        self.customFileSelector.filesSelected.connect(self.populateSpatialiteSelector)
        self.comboDict = {self.tr('Load Database Model EDGV Version 2.1.3'):'2.1.3', self.tr('Load Database Model EDGV Version 3.0'):'3.0', self.tr('Load Database Model EDGV Version FTer_2a_Ed'):'FTer_2a_Ed',self.tr('Load Other Database Models'):'Non_EDGV'}
        self.dbDict = {'2.1.3':[], 'FTer_2a_Ed':[],'Non_EDGV':[], '3.0':[]}
        self.selectedDbsDict = dict()
        self.stylesDict = dict()
        self.postgisCustomSelector.selectionChanged.connect(self.selectedDatabases)
        self.spatialiteCustomSelector.selectionChanged.connect(self.selectedFiles)
        self.path = None
        self.customFileSelector.setCaption(self.tr('Select a DSGTools Spatialite file'))
        self.customFileSelector.setFilter(self.tr('Spatialite file databases (*.sqlite)'))
        self.customFileSelector.setType('multi')
        self.edgvType = None
    
    def selectedDatabases(self, dbList, type):
        """
        Selects databases from a name list and database type
        """
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
    
    def selectedFiles(self, dbList, type):
        """
        Selects databases from a name list and database type
        """
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
        """
        Changes the database type (spatialite/postgis)
        """
        if currentTab == 0:
            self.clearSpatialiteTab()
            self.populatePostgisSelector()
        elif currentTab == 1:
            self.clearPostgisTab()
            self.populateSpatialiteSelector()
        pass
    
    def populatePostgisSelector(self):
        """
        Populates the postgis database list according to the databse type
        """
        self.dbDict = {'2.1.3':[], 'FTer_2a_Ed':[],'Non_EDGV':[], '3.0':[]}
        dbList = []
        try:
            if self.serverWidget.abstractDb:
                dbList = self.serverWidget.abstractDb.getEDGVDbsFromServer(parentWidget = self)
            else:
                self.clearPostgisTab()
                return
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), ':'.join(e.args))
            self.clearPostgisTab()
        dbList.sort()
        for (dbname, dbversion) in dbList:
            if dbversion in self.dbDict.keys():
                self.dbDict[dbversion].append(dbname)
            else:
                self.dbDict['Non_EDGV'].append(dbname)
        comboText = self.postgisEdgvComboFilter.currentText()
        self.postgisCustomSelector.setInitialState(self.dbDict[self.comboDict[comboText]]) 
    
    def populateSpatialiteSelector(self):
        """
        Populates the spatialite database list according to the databse type
        """
        self.dbDict = {'2.1.3':[], 'FTer_2a_Ed':[],'Non_EDGV':[], '3.0':[]}
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
            QMessageBox.critical(self, self.tr('Critical!'), ':'.join(e.args))
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
        """
        Clears the postgis tab, returning it to the original state
        """
        self.spatialiteCustomSelector.clearAll()
        self.serverWidget.clearAll()
        self.dbDict = {'2.1.3':[], 'FTer_2a_Ed':[],'Non_EDGV':[],'3.0':[]}
        self.customFileSelector.resetAll()
        self.edgvType = None
        self.selectedDbsDict = dict()
        self.resetAll.emit()
    
    @pyqtSlot(int)
    def on_postgisEdgvComboFilter_currentIndexChanged(self):
        """
        Updates the postgis databases according to its type
        """
        comboText = self.postgisEdgvComboFilter.currentText()
        self.postgisCustomSelector.setInitialState(self.dbDict[self.comboDict[comboText]])
        self.edgvType = self.comboDict[comboText]
        self.resetAll.emit()
    
    @pyqtSlot(int)
    def on_spatialiteEdgvComboFilter_currentIndexChanged(self):
        """
        Updates the postgis databases according to its type
        """
        comboText = self.spatialiteEdgvComboFilter.currentText()
        self.spatialiteCustomSelector.setInitialState(self.dbDict[self.comboDict[comboText]])
        self.edgvType = self.comboDict[comboText]
        self.resetAll.emit()
    
    def clearPostgisTab(self):
        """
        Clears the spatialite tab, returning it to the original state
        """
        self.postgisCustomSelector.clearAll()
        self.serverWidget.clearAll()
        self.dbDict = {'2.1.3':[], 'FTer_2a_Ed':[],'Non_EDGV':[],'3.0':[]}
        self.edgvType = None
        self.selectedDbsDict = dict()
        self.resetAll.emit()
    
    def getStyles(self, type, abstractDb):
        """
        Gets database styles. If the structure to store styles is not yet created, we should create it.
        """
        dbVersion = abstractDb.getDatabaseVersion()
        abstractDb.checkAndCreateStyleTable()
        styles = abstractDb.getStyleDict(dbVersion)
        self.styleChanged.emit(type, styles)