# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-01-11
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
from PyQt4 import QtGui, uic, QtCore
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QSettings
from PyQt4.QtSql import QSqlQuery

# DSGTools imports
from DsgTools.ServerTools.viewServers import ViewServers
from DsgTools.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.PostgisCustomization.CustomJSONTools.customJSONBuilder import CustomJSONBuilder

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'newDomainValueWidget.ui'))

class NewDomainValueWidget(QtGui.QWidget, FORM_CLASS):
    def __init__(self, abstractDb, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.abstractDb = abstractDb
        self.setupUi(self)
        self.jsonBuilder = CustomJSONBuilder()
        self.populateDomainCombo()
        regex = QtCore.QRegExp('[0-9]*')
        validator = QtGui.QRegExpValidator(regex, self.codeLineEdit)
        self.codeLineEdit.setValidator(validator)

    def populateDomainCombo(self):
        self.domainTableList = self.abstractDb.getDomainTables()
        self.domainComboBox.clear()
        self.domainComboBox.addItem(self.tr('Select a domain'))
        for domain in self.domainTableList:
            self.domainComboBox.addItem(domain)
    
    @pyqtSlot(int)
    def on_domainComboBox_currentIndexChanged(self, idx):
        if idx == 0:
            self.codeLineEdit.clear()
            self.codeLineEdit.setEnabled(False)
            self.codeNameLineEdit.clear()
            self.codeNameLineEdit.setEnabled(False)
        else:
            self.codeLineEdit.setEnabled(True)
            self.codeNameLineEdit.setEnabled(True)

    def getTitle(self):
        return self.title
    
    def setTitle(self, title):
        self.title = title

    def validate(self):
        #TODO
        return True

    def validateDiagnosis(self):
        invalidatedReason = ''
        #TODO
        return invalidatedReason
    
    def getJSONTag(self):
        if not self.validate():
            raise Exception(self.tr('Error in attribute ')+ self.title + ' : ' + self.validateDiagnosis())
        #TODO
            