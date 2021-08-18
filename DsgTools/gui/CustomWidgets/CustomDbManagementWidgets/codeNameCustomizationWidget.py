# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-01
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

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from qgis.PyQt.QtSql import QSqlQuery

# DSGTools imports
from DsgTools.gui.ServerTools.viewServers import ViewServers
from DsgTools.core.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.gui.Misc.PostgisCustomization.CustomJSONTools.customJSONBuilder import CustomJSONBuilder

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'codeNameCustomizationWidget.ui'))

class CodeNameCustomizationWidget(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, abstractDb, uiParameterJsonDict = None, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.abstractDb = abstractDb
        self.setupUi(self)
        self.jsonBuilder = CustomJSONBuilder()
        self.domainDict = dict()
        self.populateDomainCombo()
        self.populateFromUiParameterJsonDict(uiParameterJsonDict)
    
    def populateFromUiParameterJsonDict(self, uiParameterJsonDict):
        """
        builds ui from uiParameterJsonDict
        {
            'domainComboBox': --current text of domainComboBox --
            'oldCodeNameComboBox': ---current text of oldCodeNameComboBox --
            'newCodeNameLineEdit': --current text of newCodeNameLineEdit--
        }
        """
        if uiParameterJsonDict:
            domainIdx = self.domainComboBox.findText(uiParameterJsonDict['domainComboBox'], flags = Qt.MatchExactly)
            self.domainComboBox.setCurrentIndex(domainIdx)
            oldIdx = self.oldCodeNameComboBox.findText(uiParameterJsonDict['oldCodeNameComboBox'], flags = Qt.MatchExactly)
            self.oldCodeNameComboBox.setCurrentIndex(oldIdx)
            self.newCodeNameLineEdit.setText(uiParameterJsonDict['newCodeNameLineEdit'])

    def getTitle(self):
        return self.title
    
    def setTitle(self, title):
        self.title = title
    
    def populateDomainCombo(self):
        self.domainComboBox.clear()
        self.domainComboBox.addItem(self.tr('Choose a domain'))
        domainList = self.abstractDb.getDomainTables()
        for domain in domainList:
            self.domainComboBox.addItem(domain)
    
    @pyqtSlot(int)
    def on_domainComboBox_currentIndexChanged(self, idx):
        if idx != 0:
            domainName = self.domainComboBox.currentText()
            self.oldCodeNameComboBox.setEnabled(True)
            self.oldCodeNameComboBox.clear()
            self.oldCodeNameComboBox.addItem('Choose a code name')
            self.domainDict = self.abstractDb.getDomainDictV2('dominios.'+domainName)
            for codeName in list(self.domainDict.keys()):
                self.oldCodeNameComboBox.addItem(codeName)
            self.newCodeNameLineEdit.setEnabled(True)
            self.newCodeNameLineEdit.clear()
        else:
            self.newCodeNameLineEdit.setEnabled(False)
            self.newCodeNameLineEdit.clear()
            self.oldCodeNameComboBox.setEnabled(False)
            self.oldCodeNameComboBox.clear()
    
    @pyqtSlot(int)
    def on_oldCodeNameComboBox_currentIndexChanged(self, idx):
        self.newCodeNameLineEdit.setEnabled(True)
        self.newCodeNameLineEdit.clear()
    
    def validate(self):
        if self.domainComboBox.currentIndex() == 0:
            return False
        if self.oldCodeNameComboBox.currentIndex() == 0:
            return False
        if self.newCodeNameLineEdit.text() == '':
            return False
        return True

    def validateDiagnosis(self):
        invalidatedReason = ''
        if self.domainComboBox.currentIndex() == 0:
            invalidatedReason += self.tr('A domain table must be chosen.\n')
        if self.oldCodeNameComboBox.currentIndex() == 0:
            invalidatedReason += self.tr('An old code name value must be chosen.\n')
        if self.newCodeNameLineEdit.text() == '':
            invalidatedReason += self.tr('A new code name value must be chosen.\n')        
        invalidatedReason += self.addAttributeWidget.validateDiagnosis()
        return invalidatedReason
    
    def getJSONTag(self):
        if not self.validate():
            raise Exception(self.tr('Error in code name customization ')+ self.title + ' : ' + self.validateDiagnosis())
        domainTable = self.domainComboBox.currentText()
        oldCodeName = self.oldCodeNameComboBox.currentText()
        newCodeName = self.newCodeNameLineEdit.text()
        codeValue = self.domainDict[oldCodeName]
        return [self.jsonBuilder.buildCodeNameToChangeElement(domainTable, codeValue, oldCodeName, newCodeName)]
        
    def getUiParameterJsonDict(self):
        """
        builds a dict with the following format:
        {
            'domainComboBox': --current text of domainComboBox --
            'oldCodeNameComboBox': ---current text of oldCodeNameComboBox --
            'newCodeNameLineEdit': --current text of newCodeNameLineEdit--
        }
        """
        uiParameterJsonDict = dict()
        uiParameterJsonDict['domainComboBox'] = self.domainComboBox.currentText()
        uiParameterJsonDict['oldCodeNameComboBox'] = self.oldCodeNameComboBox.currentText()
        uiParameterJsonDict['newCodeNameLineEdit'] = self.newCodeNameLineEdit.text()
        return uiParameterJsonDict
            