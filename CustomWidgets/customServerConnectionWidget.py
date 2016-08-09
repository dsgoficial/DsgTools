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
        self.serverWidget.abstractDbLoaded.connect(self.getDatabasesFromServer)
        self.comboDict = {self.tr('Load EDGV v. 2.1.3'):'2.1.3', self.tr('Load EDGV v. FTer_2a_Ed'):'FTer_2a_Ed'}
        self.dbDict = {'2.1.3':[], 'FTer_2a_Ed':[]}
        self.selectedDbsDict = dict()
        self.postgisCustomSelector.selectionChanged.connect(self.selectedDatabases)
    
    def selectedDatabases(self,dbList,type):
        #TODO: build selectedDbsDict and emit dbDictChanged()
        #1- Iterate over dbList and check if all layers on dbList are on dict. If not, add it.
        if type == 'added':
            (host, port, user, password) = self.serverWidget.getServerParameters()
            for dbName in dbList:
                if dbName not in self.selectedDbsDict.keys():
                    if host and port and user and password:
                        localDb = self.dbFactory.createDbFactory('QPSQL')
                        localDb.connectDatabaseWithParameters(host, port, dbName, user, password)
                        self.selectedDbsDict[dbName] = localDb
            self.dbDictChanged.emit('added', dbList)
        #2- Iterate over selectedDbsDict and if there is a key not in dbList, close db and pop item
        if type == 'removed':
            for dbName in self.selectedDbsDict.keys():
                if dbName in dbList:
                    self.selectedDbsDict.pop(dbName)
            self.dbDictChanged.emit('removed', dbList)
    
    def getDatabasesFromServer(self):
        if self.serverConnectionTab.currentIndex() == 0:
            self.populatePostgisSelector()
        elif self.serverConnectionTab.currentIndex() == 1:
            self.populateSpatialiteSelector()
    
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
        self.dbDict = {'2.1.3':[], 'FTer_2a_Ed':[]}
        dbList = []
        try:
            if self.serverWidget.abstractDb:
                dbList = self.serverWidget.abstractDb.getEDGVDbsFromServer()
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
        comboText = self.postgisEdgvComboFilter.currentText()
        self.postgisCustomSelector.setInitialState(self.dbDict[self.comboDict[comboText]]) 
    
    def populateSpatialiteSelector(self):
        pass
    
    def clearSpatialiteTab(self):
        pass
    
    @pyqtSlot(int)
    def on_postgisEdgvComboFilter_currentIndexChanged(self):
        comboText = self.postgisEdgvComboFilter.currentText()
        self.postgisCustomSelector.setInitialState(self.dbDict[self.comboDict[comboText]]) 
    
    def clearPostgisTab(self):
        self.postgisCustomSelector.clearAll()
        self.serverWidget.clearAll()
        self.dbDict = {'2.1.3':[], 'FTer_2a_Ed':[]}
        self.selectedDbsDict = dict()
        self.resetAll.emit()
    