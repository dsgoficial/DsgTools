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
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from qgis.PyQt.QtSql import QSqlQuery

# DSGTools imports
from DsgTools.gui.ServerTools.viewServers import ViewServers
from DsgTools.core.Factories.SqlFactory.sqlGeneratorFactory import SqlGeneratorFactory
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.gui.Misc.PostgisCustomization.CustomJSONTools.customJSONBuilder import (
    CustomJSONBuilder,
)

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "newDomainValueWidget.ui")
)


class NewDomainValueWidget(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, abstractDb, uiParameterJsonDict=None, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.abstractDb = abstractDb
        self.setupUi(self)
        self.jsonBuilder = CustomJSONBuilder()
        self.populateDomainCombo()
        regex = QtCore.QRegExp("[0-9]*")
        validator = QtGui.QRegExpValidator(regex, self.codeLineEdit)
        self.codeLineEdit.setValidator(validator)
        self.populateFromUiParameterJsonDict(uiParameterJsonDict)

    def populateFromUiParameterJsonDict(self, uiParameterJsonDict):
        """
        builds ui from uiParameterJsonDict
        {
            'domainComboBox': --current text of domainComboBox --
            'allDomainCheckBox': --state of allDomainCheckBox--
            'codeLineEdit': --current text of codeLineEdit--
            'codeNameLineEdit': --current text of codeNameLineEdit--
        }
        """
        if uiParameterJsonDict:
            if uiParameterJsonDict["allDomainCheckBox"]:
                self.allDomainCheckBox.setCheckState(Qt.Checked)
            else:
                domainIdx = self.domainComboBox.findText(
                    uiParameterJsonDict["domainComboBox"], flags=Qt.MatchExactly
                )
                self.domainComboBox.setCurrentIndex(domainIdx)
            self.codeLineEdit.setText(uiParameterJsonDict["codeLineEdit"])
            self.codeNameLineEdit.setText(uiParameterJsonDict["codeNameLineEdit"])

    def populateDomainCombo(self):
        self.domainTableList = self.abstractDb.getDomainTables()
        self.domainComboBox.clear()
        self.domainComboBox.addItem(self.tr("Select a domain"))
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
        self.codeLineEdit.editingFinished.emit()

    @pyqtSlot(int)
    def on_allDomainCheckBox_stateChanged(self, state):
        if state == 2:
            self.domainComboBox.clear()
        else:
            self.populateDomainCombo()
        self.codeLineEdit.editingFinished.emit()

    @pyqtSlot()
    def on_codeLineEdit_editingFinished(self):
        if self.domainComboBox.currentIndex() == 0:
            self.codeLineEdit.setStyleSheet("")
            self.codeLineEdit.setToolTip("")
            return
        if self.allDomainCheckBox.checkState() == 2:
            domainValues = self.abstractDb.getAllDomainValues()
        else:
            domainValues = self.abstractDb.getAllDomainValues(
                domainTableList=[self.domainComboBox.currentText()]
            )
        currentValue = self.codeLineEdit.text()
        if currentValue == "":
            self.codeLineEdit.setStyleSheet("")
            self.codeLineEdit.setToolTip("")
        elif int(currentValue) in domainValues:
            self.codeLineEdit.setStyleSheet("border: 1px solid red;")
            self.codeLineEdit.setToolTip(
                self.tr("Code value already exists, choose another.")
            )
        else:
            self.codeLineEdit.setStyleSheet("")
            self.codeLineEdit.setToolTip("")

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def validate(self):
        if self.codeLineEdit.text() == "":
            return False
        if self.codeNameLineEdit.text() == "":
            return False
        if self.allDomainCheckBox.checkState() == 2:
            return True
        else:
            if self.domainComboBox.currentIndex() == 0:
                return False
        return True

    def validateDiagnosis(self):
        invalidatedReason = ""
        if self.codeLineEdit.text() == "":
            invalidatedReason += self.tr("A code value must be entered.\n")
        if self.codeNameLineEdit.text() == "":
            invalidatedReason += self.tr("A code name value must be entered.\n")
        if (
            self.domainComboBox.currentIndex() == 0
            and self.allDomainCheckBox.checkState() != 2
        ):
            invalidatedReason += self.tr("A domain table must be chosen.\n")
        return invalidatedReason

    def getJSONTag(self):
        if not self.validate():
            raise Exception(
                self.tr("Error in new domain value ")
                + self.title
                + " : "
                + self.validateDiagnosis()
            )
        code = self.codeLineEdit.text()
        codeName = self.codeNameLineEdit.text()
        jsonList = []
        if self.allDomainCheckBox.checkState() != 2:
            domainName = self.domainComboBox.currentText()
            jsonList.append(
                self.jsonBuilder.addDomainValueElement(domainName, code, codeName)
            )
        else:
            for domainName in self.domainTableList:
                jsonList.append(
                    self.jsonBuilder.addDomainValueElement(domainName, code, codeName)
                )
        return jsonList

    def getUiParameterJsonDict(self):
        """
        builds a dict with the following format:
        {
            'domainComboBox': --current text of domainComboBox --
            'allDomainCheckBox': --state of allDomainCheckBox--
            'codeLineEdit': --current text of codeLineEdit--
            'codeNameLineEdit': --current text of codeNameLineEdit--
        }
        """
        uiParameterJsonDict = dict()
        uiParameterJsonDict["domainComboBox"] = self.domainComboBox.currentText()
        uiParameterJsonDict["allDomainCheckBox"] = self.allDomainCheckBox.isChecked()
        uiParameterJsonDict["codeLineEdit"] = self.codeLineEdit.text()
        uiParameterJsonDict["codeNameLineEdit"] = self.codeNameLineEdit.text()
        return uiParameterJsonDict
