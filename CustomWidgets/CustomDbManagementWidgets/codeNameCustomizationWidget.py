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

from qgis.core import QgsMessageLog

# Qt imports
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings
from PyQt4.QtSql import QSqlQuery

# DSGTools imports
from DsgTools.ServerTools.viewServers import ViewServers
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.PostgisCustomization.CustomJSONTools.customJSONBuilder import CustomJSONBuilder

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'codeNameCustomizationWidget.ui'))

class CodeNameCustomizationWidget(QtGui.QWidget, FORM_CLASS):
    def __init__(self, abstractDb, jsonTag = None, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.abstractDb = abstractDb
        self.setupUi(self)
        self.jsonBuilder = CustomJSONBuilder()
        self.domainDict = dict()
        self.populateDomainCombo()
    
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
        if idx <> 0:
            domainName = self.domainComboBox.currentText()
            self.oldCodeNameComboBox.setEnabled(True)
            self.oldCodeNameComboBox.clear()
            self.oldCodeNameComboBox.addItem('Choose a code name')
            self.domainDict = self.abstractDb.getDomainDictV2('dominios.'+domainName)
            for codeName in self.domainDict.keys():
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
        
        
            