# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-12-20
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
from builtins import range
import os

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from qgis.PyQt.QtSql import QSqlQuery
from qgis.PyQt.QtWidgets import QListWidgetItem, QDialog

# DSGTools imports
from DsgTools.gui.ServerTools.viewServers import ViewServers
from DsgTools.core.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.gui.Misc.PostgisCustomization.CustomJSONTools.customJSONBuilder import CustomJSONBuilder

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'domainSetter.ui'))

class DomainSetter(QtWidgets.QDialog, FORM_CLASS):
    domainChanged = pyqtSignal(str, dict, dict)
    def __init__(self, abstractDb, uiParameterJsonDict = None, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.abstractDb = abstractDb
        self.populateDomainList()
        self.domainName = None
        self.domainDict = None
        self.filterClause = dict()
        self.jsonBuilder = CustomJSONBuilder()
        self.populateFromUiParameterJsonDict(uiParameterJsonDict)
    
    def populateFromUiParameterJsonDict(self, uiParameterJsonDict):
        """
        populates ui from  uiParameterJsonDict with the following keys:
        {
            'domainListWidget': --text of selected item on domainListWidget --
            'filterCheckBox': --True or False for filterCheckBox isChecked --
            'filterListWidgetCheckedItems' : [--list of selected code names--]
        }
        """
        if uiParameterJsonDict:
            item = self.domainListWidget.findItems(uiParameterJsonDict['domainListWidget'], Qt.MatchExactly)
            if isinstance(item,list):
                item = item[0]
            self.domainListWidget.setCurrentItem(item)
            if uiParameterJsonDict['filterCheckBox']:
                self.filterCheckBox.setCheckState(QtCore.Qt.Checked)
                for codeName in uiParameterJsonDict['filterListWidgetCheckedItems']:
                    codeNameItem = self.filterListWidget.findItems(codeName, Qt.MatchExactly)
                    if isinstance(codeNameItem,list):
                        codeNameItem = codeNameItem[0]
                    else:
                        codeNameItem = codeNameItem
                    codeNameItem.setCheckState(QtCore.Qt.Checked)
            self.applyChanges()

    def populateDomainList(self):
        self.domainTableList = self.abstractDb.getDomainTables()
        self.domainListWidget.clear()
        for domain in self.domainTableList:
            self.domainListWidget.addItem(domain)
    
    def clearAll(self):
        self.filterLineEdit.clear()
        self.filterListWidget.clear()
        self.filterCheckBox.setCheckState(QtCore.Qt.Unchecked)
        self.domainName = None
        self.domainDict = None
        self.filterClause = dict()
        self.populateDomainList()

    def enableItems(self, enabled):
        self.filterListWidget.setEnabled(enabled)
    
    def clearCheckableItems(self):
        for idx in range(self.filterListWidget.__len__()):
            item = self.filterListWidget.item(idx)
            item.setCheckState(QtCore.Qt.Unchecked)
    
    @pyqtSlot(int)
    def on_filterCheckBox_stateChanged(self, idx):
        if idx == 2:
            state = True
        else:
            state = False
            self.clearCheckableItems()
        self.enableItems(state)
    
    def getSelectedDomain(self):
        return self.domainListWidget.selectedItems()[0].data()
    
    @pyqtSlot(int)
    def on_domainListWidget_currentRowChanged(self, idx):
        curItem = self.domainListWidget.item(idx)
        self.filterListWidget.clear()
        if curItem:
            self.domainName = curItem.data(0)
            self.domainDict = self.abstractDb.getDomainDictV2('dominios.'+self.domainName)
            for codeName in list(self.domainDict.keys()):
                newItem = QListWidgetItem(codeName)
                newItem.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsTristate | QtCore.Qt.ItemIsUserCheckable)
                newItem.setCheckState(QtCore.Qt.Unchecked)
                self.filterListWidget.addItem(newItem)
    
    def on_filterLineEdit_textChanged(self, text):
        '''
        Filters the items to make it easier to spot and select them
        '''
        classes = [edgvDomain for edgvDomain in self.domainTableList if text in edgvDomain]
        self.domainListWidget.clear()
        self.domainListWidget.addItems(classes)
        self.domainListWidget.sortItems()
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        self.clearAll()

    @pyqtSlot(name='on_buttonBox_accepted')
    def applyChanges(self):
        for idx in range(self.filterListWidget.__len__()):
            item = self.filterListWidget.item(idx)
            if item.checkState() == 2:
                codeName = item.data(0) 
                if codeName not in list(self.filterClause.keys()):
                    self.filterClause[codeName] = self.domainDict[codeName]
        self.domainChanged.emit(self.domainName, self.domainDict, self.filterClause)
    
    def getChildWidgets(self):
        return None
    
    def getUiParameterJsonDict(self):
        """
        builds a dict with the following format:
        {
            'domainListWidget': --text of selected item on domainListWidget --
            'filterCheckBox': --True or False for filterCheckBox isChecked --
            'filterListWidgetCheckedItems' : [--list of selected code names--]
        }
        """
        uiParameterJsonDict = dict()
        uiParameterJsonDict['domainListWidget'] = self.domainListWidget.currentItem().data(0)
        uiParameterJsonDict['filterCheckBox'] = self.filterCheckBox.isChecked()
        uiParameterJsonDict['filterListWidgetCheckedItems'] = []
        for idx in range(self.filterListWidget.__len__()):
            item = self.filterListWidget.item(idx)
            if item.checkState() == 2:
                uiParameterJsonDict['filterListWidgetCheckedItems'].append(item.data(0))
        return uiParameterJsonDict