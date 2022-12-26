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
from DsgTools.gui.CustomWidgets.CustomDbManagementWidgets.domainSetter import (
    DomainSetter,
)
from DsgTools.gui.Misc.PostgisCustomization.CustomJSONTools.customJSONBuilder import (
    CustomJSONBuilder,
)

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "addAttributeWidget.ui")
)


class AddAttributeWidget(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, abstractDb, uiParameterJsonDict=None, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.abstractDb = abstractDb
        self.setupUi(self)
        regex = QtCore.QRegExp("[a-z]*")
        validator = QtGui.QRegExpValidator(regex, self.nameLineEdit)
        self.nameLineEdit.setValidator(validator)
        self.domainSetter = None
        self.jsonBuilder = CustomJSONBuilder()
        self.populateFromUiParameterJsonDict(uiParameterJsonDict)

    def populateFromUiParameterJsonDict(self, uiParameterJsonDict):
        """
        populates ui from  uiParameterJsonDict with the following keys:
        {
            'nameLineEdit': --text of selected item on nameLineEdit --
            'typeComboBox': --index of selected item on typeComboBox --
            'notNullcheckBox' : --True or False for notNullcheckBox isChecked --
            'defaultComboBox' : --text of selected item on typeComboBox --
            'references' : dict from domainSetter
        }
        """
        if uiParameterJsonDict:
            self.nameLineEdit.setText(uiParameterJsonDict["nameLineEdit"])
            if uiParameterJsonDict["references"]:
                idx = self.typeComboBox.findText(
                    self.tr("EDGV Domain"), flags=Qt.MatchExactly
                )
                self.typeComboBox.setCurrentIndex(idx)
                self.instantiateDomainSetter(uiParameterJsonDict["references"])
            else:
                self.typeComboBox.setCurrentIndex(
                    int(uiParameterJsonDict["typeComboBox"])
                )
            if uiParameterJsonDict["notNullcheckBox"]:
                self.notNullcheckBox.setCheckState(2)
            idx = self.defaultComboBox.findText(
                uiParameterJsonDict["defaultComboBox"], flags=Qt.MatchExactly
            )
            self.defaultComboBox.setCurrentIndex(idx)

    def enableItems(self, enabled):
        self.referencesLabel.setEnabled(enabled)
        self.referencesLineEdit.setEnabled(enabled)
        self.referencesPushButton.setEnabled(enabled)
        self.defaultLabel.setEnabled(enabled)
        self.defaultComboBox.setEnabled(enabled)

    @pyqtSlot(int)
    def on_typeComboBox_currentIndexChanged(self, idx):
        edgvDomainIdx = self.typeComboBox.findText(
            self.tr("EDGV Domain"), flags=Qt.MatchExactly
        )
        if idx == edgvDomainIdx:
            self.enableItems(True)
        else:
            self.enableItems(False)
            self.referencesLineEdit.setText("")
            self.defaultComboBox.clear()
            self.domainSetter = None

    @pyqtSlot(bool)
    def on_referencesPushButton_clicked(self):
        if not self.domainSetter:
            self.instantiateDomainSetter()
        else:
            self.domainSetter.show()

    def instantiateDomainSetter(self, uiParameterJsonDict=None):
        self.domainSetter = DomainSetter(self.abstractDb, uiParameterJsonDict)
        self.domainSetter.domainChanged.connect(self.populateDefaultCombo)
        if not uiParameterJsonDict:
            self.domainSetter.exec_()
        else:
            self.domainSetter.applyChanges()

    @pyqtSlot(str, dict, list)
    def populateDefaultCombo(self, domainName, domainDict, filterClause):
        self.referencesLineEdit.setText(domainName)
        self.defaultComboBox.clear()
        addList = [""]
        for domain in list(domainDict.keys()):
            if filterClause == dict():
                if domain not in addList:
                    addList.append(domain)
            elif domain in list(filterClause.keys()):
                if domain not in addList:
                    addList.append(domain)
        for item in addList:
            self.defaultComboBox.addItem(item)

    def getChildWidgets(self):
        return self.domainSetter

    def validate(self):
        invalidatedList = []
        if self.nameLineEdit.text() == "":
            return False
        if self.typeComboBox.currentIndex() == 0:
            return False
        return True

    def validateDiagnosis(self):
        invalidatedReason = ""
        if self.nameLineEdit.text() == "":
            invalidatedReason += self.tr("Attribute must have a name.\n")
        if self.typeComboBox.currentIndex() == 0:
            invalidatedReason += self.tr("Attribute must have a type.\n")
        return invalidatedReason

    def getJSONTag(self):
        if not self.validate():
            raise Exception(self.validateDiagnosis())
        attrName = self.nameLineEdit.text()
        attrType = self.typeComboBox.currentText()
        if attrType == self.tr("EDGV Domain"):
            attrType = "smallint"
        isPk = False
        if self.notNullcheckBox.isChecked():
            isNullable = False
        else:
            isNullable = True
        defaultComboCurrentText = self.defaultComboBox.currentText()
        if not self.domainSetter:
            return self.jsonBuilder.buildAttributeElement(
                attrName, attrType, isPk, isNullable
            )
        else:
            if defaultComboCurrentText == "":
                defaultValue = None
            else:
                defaultValue = self.domainSetter.domainDict[defaultComboCurrentText]
            references = self.domainSetter.domainName
            filter = list(self.domainSetter.filterClause.values())
            return [
                self.jsonBuilder.buildAttributeElement(
                    attrName,
                    attrType,
                    isPk,
                    isNullable,
                    defaultValue,
                    references,
                    filter,
                )
            ]

    def getUiParameterJsonDict(self):
        """
        builds a dict with the following format:
        {
            'nameLineEdit': --text of selected item on nameLineEdit --
            'typeComboBox': --text of selected item on typeComboBox --
            'notNullcheckBox' : --True or False for notNullcheckBox isChecked --
            'defaultComboBox' : --text of selected item on typeComboBox --
            'references' : dict from domainSetter
        }
        """
        uiParameterJsonDict = dict()
        uiParameterJsonDict["nameLineEdit"] = self.nameLineEdit.text()
        uiParameterJsonDict["typeComboBox"] = self.typeComboBox.currentText()
        uiParameterJsonDict["notNullcheckBox"] = self.notNullcheckBox.isChecked()
        uiParameterJsonDict["defaultComboBox"] = self.defaultComboBox.currentText()
        uiParameterJsonDict["references"] = None
        if self.domainSetter:
            uiParameterJsonDict[
                "references"
            ] = self.domainSetter.getUiParameterJsonDict()
        return uiParameterJsonDict
