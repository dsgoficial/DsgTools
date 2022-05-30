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
from collections import defaultdict
import os

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal

from .....core.Utils.utils import Utils
from .....core.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from .....core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.dsgEnums import DsgEnums


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'customServerConnectionWidget.ui'))

class CustomServerConnectionWidget(QtWidgets.QWidget, FORM_CLASS):
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
        self.spatialiteCustomFileSelector.filesSelected.connect(self.populateSpatialiteSelector)
        # self.gpkgCustomFileSelector.filesSelected.connect(self.populateGeopackageSelector)
        self.comboDict = {self.tr('Load Database Model EDGV Version 2.1.3'):'2.1.3',
                         self.tr('Load Database Model EDGV Version 2.1.3 Pro'):'2.1.3 Pro',
                         self.tr('Load Database Model EDGV Version 3.0'):'3.0',
                         self.tr('Load Database Model EDGV Version 3.0 Pro'):'3.0 Pro', 
                         self.tr('Load Database Model EDGV Version FTer_2a_Ed'):'FTer_2a_Ed',
                         self.tr('Load Other Database Models'):'Non_EDGV'}
        self.dbNameDict = dict()
        self.selectedDbsDict = defaultdict()
        self.stylesDict = defaultdict(
            lambda: {
                "dbList": [],
                "style": []
            }
        )
        self.postgisCustomSelector.selectionChanged.connect(self.selectedDatabases)
        self.spatialiteCustomSelector.selectionChanged.connect(self.selectedFiles)
        # self.gpkgCustomSelector.selectionChanged.connect(self.selectedGeopackageFiles)
        self.path = None
        self.spatialiteCustomFileSelector.setCaption(self.tr('Select a DSGTools Spatialite File'))
        self.spatialiteCustomFileSelector.setFilter(self.tr('Spatialite file databases (*.sqlite)'))
        self.spatialiteCustomFileSelector.setType('multi')
    
    def selectedDatabases(self, dbList, type):
        """
        Selects databases from a name list and database type
        """
        #1- Iterate over dbList and check if all layers on dbList are on dict. If not, add it.
        if type == 'added':
            (host, port, user, password) = self.serverWidget.abstractDb.getParamsFromConectedDb()
            for dbNameAlias in dbList:
                if dbNameAlias in list(self.selectedDbsDict.keys()):
                    continue
                if not host or not port or not user:
                    continue
                localDb = self.dbFactory.createDbFactory(DsgEnums.DriverPostGIS)
                localDb.connectDatabaseWithParameters(host, port, self.dbNameDict[dbNameAlias], user, password)
                self.selectedDbsDict[dbNameAlias] = localDb
                #do get dicts
                localDict = localDb.getStyleDict(localDb.getDatabaseVersion())
                for key in list(localDict.keys()):
                    self.stylesDict[key]['style'] = localDict[key]
                    if dbNameAlias not in self.stylesDict[key]['dbList']:
                        self.stylesDict[key]['dbList'].append(dbNameAlias)
            self.dbDictChanged.emit('added', dbList)
            self.styleChanged.emit(self.stylesDict)
        #2- Iterate over selectedDbsDict and if there is a key not in dbList, close db and pop item
        if type == 'removed':
            for dbNameAlias in list(self.selectedDbsDict.keys()):
                if dbNameAlias in dbList:
                    self.selectedDbsDict.pop(dbNameAlias)
            self.dbDictChanged.emit('removed', dbList)
            for key in list(self.stylesDict.keys()):
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
        #1- Iterate over dbList and check if all layers on dbList are on dict. If not, add it.
        if type == 'added':
            for dbName in dbList:
                if dbName in self.selectedDbsDict:
                    continue
                localDb = self.dbFactory.createDbFactory(DsgEnums.DriverSpatiaLite)
                localDb.connectDatabase(conn = self.spatialiteDict[dbName])
                self.selectedDbsDict[dbName] = localDb
                #do get dicts
                localDict = localDb.getStyleDict(localDb.getDatabaseVersion())
                for key in list(localDict.keys()):
                    self.stylesDict[key]['style'] = localDict[key]
                    if dbName not in self.stylesDict[key]['dbList']:
                        self.stylesDict[key]['dbList'].append(dbName)
            self.dbDictChanged.emit('added', dbList)
            self.styleChanged.emit(self.stylesDict)
        #2- Iterate over selectedDbsDict and if there is a key not in dbList, close db and pop item
        if type == 'removed':
            for dbName in list(self.selectedDbsDict.keys()):
                if dbName in dbList:
                    self.selectedDbsDict.pop(dbName)
            self.dbDictChanged.emit('removed', dbList)
            for key in list(self.stylesDict.keys()):
                for db in self.stylesDict[key]['dbList']:
                    if db not in dbList:
                        continue
                    idx = self.stylesDict[key]['dbList'].index(db)
                    self.stylesDict[key]['dbList'].pop(idx)
                if len(self.stylesDict[key]['dbList']) == 0:
                    self.stylesDict.pop(key)
            self.styleChanged.emit(self.stylesDict)

    @pyqtSlot(int)
    def on_serverConnectionTab_currentChanged(self, currentTab):
        """
        Changes the database type (spatialite/postgis/geopackage)
        """
        if currentTab == 0:
            self.clearSpatialiteTab()
            self.populatePostgisSelector()
        elif currentTab == 1:
            self.clearPostgisTab()
            self.populateSpatialiteSelector()
    
    def populatePostgisSelector(self):
        """
        Populates the postgis database list according to the database type
        """
        self.dbNameDict = dict()
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
        for (dbName, dbversion, dbimplversion) in dbList:
            self.dbNameDict[self.getDisplayString(dbName, dbversion, dbimplversion)] = dbName
        self.postgisCustomSelector.setInitialState(self.dbNameDict.keys()) 

    def getDisplayString(self, dbName, dbversion, dbimplversion):
        if dbversion in ["2.1.3", "3.0", "2.1.3 Pro", "3.0 Pro"]:
            dbversion = f"EDGV {dbversion}"
        if dbversion == 'Non_EDGV':
            displayString = f"{dbName} (Unknown model)"
        elif dbimplversion == -1:
            displayString = f"{dbName} ({dbversion})"
        else:
            displayString = f"{dbName} ({dbversion} impl. {dbimplversion})"
        return displayString

    def populateSpatialiteSelector(self):
        """
        Populates the spatialite database list according to the databse type
        """
        self.dbNameDict = {}
        self.spatialiteDict = dict()
        dbList = []
        try:
            fileNameList = self.spatialiteCustomFileSelector.fileNameList[0] if self.spatialiteCustomFileSelector.fileNameList else []
            for dbPath in fileNameList:
                auxAbstractDb = self.dbFactory.createDbFactory(DsgEnums.DriverSpatiaLite)
                dbName = os.path.basename(dbPath).split('.')[0]
                self.path = os.path.dirname(dbPath)
                auxAbstractDb.connectDatabase(conn = dbPath)
                version = auxAbstractDb.getDatabaseVersion()
                dbimplversion = auxAbstractDb.getImplementation()
                dbList.append((dbName,version, dbimplversion))
                self.spatialiteDict[dbName] = dbPath
        except Exception as e:
            QMessageBox.critical(self, self.tr('Critical!'), ':'.join(e.args))
            self.clearSpatialiteTab()
        dbList.sort()
        for (dbname, dbversion, dbimplversion) in dbList:
            self.dbNameDict[self.getDisplayString(dbName, dbversion, dbimplversion)] = dbName
        self.spatialiteCustomSelector.setInitialState(self.dbNameDict.keys()) 

    def clearSpatialiteTab(self):
        """
        Clears the postgis tab, returning it to the original state
        """
        self.spatialiteCustomSelector.clearAll()
        self.serverWidget.clearAll()
        self.dbNameDict = {}
        self.spatialiteCustomFileSelector.resetAll()
        self.edgvType = None
        self.selectedDbsDict = dict()
        self.resetAll.emit()

    def clearPostgisTab(self):
        """
        Clears the spatialite tab, returning it to the original state
        """
        self.postgisCustomSelector.clearAll()
        self.serverWidget.clearAll()
        self.dbNameDict = {}
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
