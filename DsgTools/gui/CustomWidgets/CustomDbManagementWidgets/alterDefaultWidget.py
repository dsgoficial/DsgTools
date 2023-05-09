# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-01-09
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from builtins import str
import os

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from qgis.PyQt.QtWidgets import QApplication
from qgis.PyQt.QtGui import QCursor

# DSGTools imports
from DsgTools.gui.Misc.PostgisCustomization.CustomJSONTools.customJSONBuilder import (
    CustomJSONBuilder,
)
from DsgTools.core.Utils.utils import Utils

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "alterDefaultWidget.ui")
)


class AlterDefaultWidget(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, abstractDb, uiParameterJsonDict=None, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.abstractDb = abstractDb
        self.setupUi(self)
        self.jsonBuilder = CustomJSONBuilder()
        self.populateSchemaCombo()
        geomTypeDict = self.abstractDb.getGeomTypeDict()
        geomDict = self.abstractDb.getGeomDict(geomTypeDict)
        self.domainDict = self.abstractDb.getDbDomainDict(geomDict)
        self.utils = Utils()
        self.populateFromUiParameterJsonDict(uiParameterJsonDict)

    def populateFromUiParameterJsonDict(self, uiParameterJsonDict):
        """
        builds a dict with the following format:
        {
            'schemaComboBox': --current text of schemaComboBox --
            'tableComboBox': --current text of tableComboBox--
            'allAttributesCheckBox': --state of allAttributesCheckBox--
            'allTablesCheckBox': --state of allTablesCheckBox--
            'attributeComboBox': --current text of attributeComboBox--
            'singleValueComboBox': --current text of singleValueComboBox--
        }
        """
        if uiParameterJsonDict:
            if uiParameterJsonDict["allTablesCheckBox"]:
                self.allTablesCheckBox.setCheckState(Qt.Checked)
            else:
                schemaIdx = self.schemaComboBox.findText(
                    uiParameterJsonDict["schemaComboBox"], flags=Qt.MatchExactly
                )
                self.schemaComboBox.setCurrentIndex(schemaIdx)
                tableIdx = self.tableComboBox.findText(
                    uiParameterJsonDict["tableComboBox"], flags=Qt.MatchExactly
                )
                self.tableComboBox.setCurrentIndex(tableIdx)
                if uiParameterJsonDict["allAttributesCheckBox"]:
                    self.allAttributesCheckBox.setCheckState(Qt.Checked)
                else:
                    attributeIdx = self.attributeComboBox.findText(
                        uiParameterJsonDict["attributeComboBox"], flags=Qt.MatchExactly
                    )
                    self.attributeComboBox.setCurrentIndex(attributeIdx)
                idx = self.singleValueComboBox.findText(
                    uiParameterJsonDict["singleValueComboBox"], flags=Qt.MatchExactly
                )
                self.singleValueComboBox.setCurrentIndex(idx)

    def populateSchemaCombo(self):
        self.schemaComboBox.clear()
        self.schemaComboBox.addItem(self.tr("Select a schema"))
        schemaList = self.abstractDb.getGeometricSchemaList()
        for schema in schemaList:
            if schema not in ["views", "validation"]:
                self.schemaComboBox.addItem(schema)

    @pyqtSlot(int)
    def on_schemaComboBox_currentIndexChanged(self, idx):
        if idx == 0:
            self.tableComboBox.clear()
            self.tableComboBox.setEnabled(False)
            self.attributeComboBox.clear()
            self.attributeComboBox.setEnabled(False)
            self.singleValueComboBox.clear()
        else:
            schema = self.schemaComboBox.currentText()
            self.tableComboBox.setEnabled(True)
            self.tableComboBox.clear()
            self.tableComboBox.addItem(self.tr("Select a table"))
            tableList = self.abstractDb.getGeometricTableListFromSchema(schema)
            for table in tableList:
                self.tableComboBox.addItem(table)

    @pyqtSlot(int)
    def on_tableComboBox_currentIndexChanged(self, idx):
        if idx == 0:
            self.attributeComboBox.clear()
            self.attributeComboBox.setEnabled(False)
        else:
            schema = self.schemaComboBox.currentText()
            tableName = self.tableComboBox.currentText()
            self.attributeComboBox.setEnabled(True)
            self.attributeComboBox.clear()
            self.attributeComboBox.addItem(self.tr("Select an attribute"))
            if tableName in list(self.domainDict.keys()):
                attributeList = list(self.domainDict[tableName]["columns"].keys())
                for attribute in attributeList:
                    self.attributeComboBox.addItem(attribute)
            self.singleValueComboBox.clear()

    @pyqtSlot(int, name="on_schemaComboBox_currentIndexChanged")
    @pyqtSlot(int, name="on_tableComboBox_currentIndexChanged")
    def populateOnSelectAll(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        if self.allTablesCheckBox.checkState() == 2 or (
            self.allAttributesCheckBox.checkState() == 2
            and self.schemaComboBox.currentIndex() != 0
            and self.tableComboBox.currentIndex() != 0
        ):
            self.attributeComboBox.clear()
            self.attributeComboBox.setEnabled(False)
            self.singleValueComboBox.clear()
            self.singleValueComboBox.addItem(self.tr("Select a value to alter"))
            if self.allAttributesCheckBox.checkState() == 2:
                tableList = [self.tableComboBox.currentText()]
            else:
                tableList = list(self.domainDict.keys())
            allValueList = []
            idxList = []
            for tableName in tableList:
                for attrName in list(self.domainDict[tableName]["columns"].keys()):
                    for code in self.domainDict[tableName]["columns"][attrName][
                        "values"
                    ]:
                        value = self.domainDict[tableName]["columns"][attrName][
                            "values"
                        ][code]
                        if value not in allValueList:
                            allValueList.append(value)
            for value in allValueList:
                for tableName in tableList:
                    for attrName in list(self.domainDict[tableName]["columns"].keys()):
                        if value not in list(
                            self.domainDict[tableName]["columns"][attrName][
                                "values"
                            ].values()
                        ):
                            idx = allValueList.index(value)
                            if idx not in idxList:
                                idxList.append(idx)
            idxList.sort(reverse=True)
            for idx in idxList:
                allValueList.pop(idx)
            for value in allValueList:
                self.singleValueComboBox.addItem(value)
        QApplication.restoreOverrideCursor()

    @pyqtSlot(int)
    def on_attributeComboBox_currentIndexChanged(self, idx):
        if idx == 0:
            QApplication.restoreOverrideCursor()
            return
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        filterList = []
        attributeName = self.attributeComboBox.currentText()
        tableFilter = []
        filterToList = []
        self.singleValueComboBox.clear()
        self.singleValueComboBox.addItem(self.tr("Select a value to alter"))
        tableName = self.tableComboBox.currentText()
        attributeName = self.attributeComboBox.currentText()
        if tableName in list(self.domainDict.keys()):
            if attributeName in list(self.domainDict[tableName]["columns"].keys()):
                attrDomainDict = self.domainDict[tableName]["columns"][attributeName][
                    "values"
                ]
                for value in list(attrDomainDict.values()):
                    self.singleValueComboBox.addItem(value)
                defaultCode = self.abstractDb.getDefaultFromDb(
                    self.schemaComboBox.currentText(), tableName, attributeName
                )
                if defaultCode:
                    if "ARRAY" in defaultCode or "@" in defaultCode:
                        # done to extract value from multi array
                        defaultCodeInt = int(
                            defaultCode.replace("ARRAY", "")
                            .replace("(", "")
                            .replace(")", "")
                            .replace("]", "")
                            .replace("[", "")
                            .replace("@", "")
                            .replace("<", "")
                            .split(":")[0]
                        )
                    else:
                        defaultCodeInt = int(defaultCode)
                    if defaultCodeInt in list(attrDomainDict.keys()):
                        comboItem = self.singleValueComboBox.findText(
                            attrDomainDict[defaultCodeInt], flags=Qt.MatchExactly
                        )
                        self.singleValueComboBox.setCurrentIndex(comboItem)
        QApplication.restoreOverrideCursor()

    @pyqtSlot(int)
    def on_allTablesCheckBox_stateChanged(self, state):
        self.singleValueComboBox.clear()
        if state == 0:
            self.allAttributesCheckBox.setEnabled(True)
            self.schemaComboBox.setCurrentIndex(0)
            self.schemaComboBox.setEnabled(True)
        elif state == 2:
            self.allAttributesCheckBox.setEnabled(False)
            self.allAttributesCheckBox.setCheckState(0)
            self.schemaComboBox.setCurrentIndex(0)
            self.schemaComboBox.setEnabled(False)
            self.populateOnSelectAll()

    @pyqtSlot(int)
    def on_allAttributesCheckBox_stateChanged(self, state):
        self.singleValueComboBox.clear()
        if state == 2:
            self.allTablesCheckBox.setEnabled(False)
            self.allTablesCheckBox.setCheckState(0)
            self.attributeComboBox.setCurrentIndex(0)
            self.attributeComboBox.setEnabled(False)
            self.populateOnSelectAll()
        if state == 0:
            self.allTablesCheckBox.setEnabled(True)
            self.attributeComboBox.setEnabled(True)
            idx = self.tableComboBox.currentIndex()
            self.tableComboBox.currentIndexChanged.emit(idx)

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def validate(self):
        if self.allTablesCheckBox.checkState() == 2:
            if self.singleValueComboBox.currentIndex() == 0:
                return False
        elif self.allAttributesCheckBox.checkState() == 2:
            if self.singleValueComboBox.currentIndex() == 0:
                return False
            if self.schemaComboBox.currentIndex() == 0:
                return False
            if self.tableComboBox.currentIndex() == 0:
                return False
        else:
            if self.singleValueComboBox.currentIndex() == 0:
                return False
            if self.schemaComboBox.currentIndex() == 0:
                return False
            if self.tableComboBox.currentIndex() == 0:
                return False
            if self.attributeComboBox.currentIndex() == 0:
                return False
        return True

    def validateDiagnosis(self):
        invalidatedReason = ""
        if self.allTablesCheckBox.checkState() == 2:
            if self.singleValueComboBox.currentIndex() == 0:
                invalidatedReason += self.tr("A value must be chosen.\n")
        elif self.allAttributesCheckBox.checkState() == 2:
            if self.singleValueComboBox.currentIndex() == 0:
                invalidatedReason += self.tr("A value must be chosen.\n")
            if self.schemaComboBox.currentIndex() == 0:
                invalidatedReason += self.tr("A schema must be chosen.\n")
            if self.tableComboBox.currentIndex() == 0:
                invalidatedReason += self.tr("A table must be chosen.\n")
        else:
            if self.singleValueComboBox.currentIndex() == 0:
                invalidatedReason += self.tr("A value must be chosen.\n")
            if self.schemaComboBox.currentIndex() == 0:
                invalidatedReason += self.tr("A schema must be chosen.\n")
            if self.tableComboBox.currentIndex() == 0:
                invalidatedReason += self.tr("A table must be chosen.\n")
            if self.attributeComboBox.currentIndex() == 0:
                invalidatedReason += self.tr("An attribute must be chosen.\n")
        return invalidatedReason

    def getJSONTag(self):
        if not self.validate():
            raise Exception(
                self.tr("Error in default customization ")
                + self.title
                + " : "
                + self.validateDiagnosis()
            )
        jsonList = []
        inhConstrDict = self.abstractDb.getInheritanceConstraintDict()
        if self.allAttributesCheckBox.checkState() == 2:
            tableName = self.tableComboBox.currentText()
            schema = self.schemaComboBox.currentText()
            if tableName in list(self.domainDict.keys()):
                for attrName in list(self.domainDict[tableName]["columns"].keys()):
                    self.getJsonTagFromOneTable(schema, tableName, attrName, jsonList)
        elif self.allTablesCheckBox.checkState() == 2:
            for tableName in list(self.domainDict.keys()):
                schema = self.abstractDb.getTableSchemaFromDb(tableName)
                for attrName in list(self.domainDict[tableName]["columns"].keys()):
                    self.getJsonTagFromOneTable(schema, tableName, attrName, jsonList)
        else:
            tableName = self.tableComboBox.currentText()
            schema = self.schemaComboBox.currentText()
            attrName = self.attributeComboBox.currentText()
            self.getJsonTagFromOneTable(schema, tableName, attrName, jsonList)
        return jsonList

    def getJsonTagFromOneTable(self, schema, tableName, attrName, jsonList):
        if tableName in list(self.domainDict.keys()):
            if attrName in list(self.domainDict[tableName]["columns"].keys()):
                attrDomainDict = self.domainDict[tableName]["columns"][attrName][
                    "values"
                ]
                oldDefaultText = self.abstractDb.getDefaultFromDb(
                    self.schemaComboBox.currentText(), tableName, attrName
                )
                if oldDefaultText:
                    if "ARRAY" in oldDefaultText or "@" in oldDefaultText:
                        # done to build multi array
                        oldDefaultInt = int(
                            oldDefaultText.replace("ARRAY", "")
                            .replace("(", "")
                            .replace(")", "")
                            .replace("]", "")
                            .replace("[", "")
                            .replace("@", "")
                            .replace("<", "")
                            .split(":")[0]
                        )
                    else:
                        oldDefaultInt = int(oldDefaultText)
                newDefaultText = self.singleValueComboBox.currentText()
                newDefaultInt = [
                    i
                    for i in list(attrDomainDict.keys())
                    if attrDomainDict[i] == newDefaultText
                ][0]
                if oldDefaultText:
                    newDefault = oldDefaultText.replace(
                        str(oldDefaultInt), str(newDefaultInt)
                    )
                else:
                    newDefault = str(newDefaultInt)
                newElement = self.jsonBuilder.buildChangeDefaultElement(
                    schema, tableName, attrName, oldDefaultText, newDefault
                )
                if newElement not in jsonList:
                    jsonList.append(newElement)

    def getUiParameterJsonDict(self):
        """
        builds a dict with the following format:
        {
            'schemaComboBox': --current text of schemaComboBox --
            'tableComboBox': --current text of tableComboBox--
            'allAttributesCheckBox': --state of allAttributesCheckBox--
            'allTablesCheckBox': --state of allTablesCheckBox--
            'attributeComboBox': --current text of attributeComboBox--
            'singleValueComboBox': --current text of singleValueComboBox--
        }
        """
        uiParameterJsonDict = dict()
        uiParameterJsonDict["schemaComboBox"] = self.schemaComboBox.currentText()
        uiParameterJsonDict["tableComboBox"] = self.tableComboBox.currentText()
        uiParameterJsonDict[
            "allAttributesCheckBox"
        ] = self.allAttributesCheckBox.isChecked()
        uiParameterJsonDict["allTablesCheckBox"] = self.allTablesCheckBox.isChecked()
        uiParameterJsonDict["attributeComboBox"] = self.attributeComboBox.currentText()
        uiParameterJsonDict[
            "singleValueComboBox"
        ] = self.singleValueComboBox.currentText()
        return uiParameterJsonDict
