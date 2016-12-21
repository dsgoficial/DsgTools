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
from DsgTools.CustomWidgets.CustomDbManagementWidgets.domainSetter import DomainSetter
from DsgTools.PostgisCustomization.CustomJSONTools.customJSONBuilder import CustomJSONBuilder

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'newAttributeWidget.ui'))

class NewAttributeWidget(QtGui.QWidget, FORM_CLASS):
    def __init__(self, abstractDb, parent = None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        regex = QtCore.QRegExp('[a-z]*')
        validator = QtGui.QRegExpValidator(regex, self.nameLineEdit)
        self.nameLineEdit.setValidator(validator)
        self.domainSetter = None
        self.abstractDb = abstractDb
        self.jsonBuilder = CustomJSONBuilder()
    
    def enableItems(self, enabled):
        self.referencesLabel.setEnabled(enabled)
        self.referencesLineEdit.setEnabled(enabled)
        self.referencesPushButton.setEnabled(enabled)
        self.defaultLabel.setEnabled(enabled)
        self.defaultComboBox.setEnabled(enabled)
    
    @pyqtSlot(int)
    def on_typeComboBox_currentIndexChanged(self, idx):
        if idx == 5:
            self.enableItems(True)
        else:
            self.enableItems(False)
            self.referencesLineEdit.setText('')
            self.defaultComboBox.clear()
            self.domainSetter = None
    
    @pyqtSlot(bool)
    def on_referencesPushButton_clicked(self):
        if not self.domainSetter:
            self.domainSetter = DomainSetter(self.abstractDb)
            self.domainSetter.domainChanged.connect(self.populateDefaultCombo)
            self.domainSetter.exec_()
        else:
            self.domainSetter.show()
    
    @pyqtSlot(str, dict, list)
    def populateDefaultCombo(self, domainName, domainDict, filterClause):
        self.referencesLineEdit.setText(domainName)
        self.defaultComboBox.clear()
        self.defaultComboBox.addItem('')
        for domain in domainDict.keys():
            if filterClause == dict(): 
                self.defaultComboBox.addItem(domain)
            elif domain in filterClause.keys():
                self.defaultComboBox.addItem(domain)
    
    def getChildWidgets(self):
        return self.domainSetter

    def validate(self):
        invalidatedList = []
        if self.nameLineEdit.text() == '':
            return False
        if self.typeComboBox.currentIndex() == 0:
            return False
        return True
    
    def validateDiagnosis(self):
        invalidatedReason = ''
        if self.nameLineEdit.text() == '':
            invalidatedReason += self.tr('Attribute must have a name.\n')
        if self.typeComboBox.currentIndex() == 0:
            invalidatedReason += self.tr('Attribute must have a type.\n')
        return invalidatedReason

    def getJSONTag(self):
        if not self.validate():
            raise Exception(self.validateDiagnosis())
        attrName = self.nameLineEdit.text()
        attrType = self.typeComboBox.currentText()
        if attrType == self.tr('EDGV Domain'):
            attrType = 'smallint'
        isPk = False
        if self.notNullcheckBox.isChecked():
            isNullable = False
        else:
            isNullable = True
        defaultComboCurrentText = self.defaultCombo.currentText()
        if defaultComboCurrentText == '':
            defaultValue = None
        else:
            defaultValue = self.domainSetter.domainDict[defaultComboCurrentText]
        references = self.domainSetter.domainName
        filter = self.domainSetter.filterClause.values()
        return self.jsonBuilder.buildAttributeElement(attrName, attrType, isPk, isNullable, defaultValue, references, filter)
        