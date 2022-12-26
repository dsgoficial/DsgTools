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
import os

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings, Qt
from qgis.PyQt.QtSql import QSqlQuery

# DSGTools imports
from DsgTools.gui.Misc.PostgisCustomization.CustomJSONTools.customJSONBuilder import (
    CustomJSONBuilder,
)

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "changeNullityWidget.ui")
)


class ChangeNullityWidget(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, abstractDb, uiParameterJsonDict=None, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.abstractDb = abstractDb
        self.setupUi(self)
        self.jsonBuilder = CustomJSONBuilder()
        self.populateSchemaCombo()
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
            'actionComboBoxIdx': --current index of actionComboBox--
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
                self.actionComboBox.setCurrentIndex(
                    uiParameterJsonDict["actionComboBoxIdx"]
                )

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
            attributeList = self.abstractDb.getAttributeListFromTable(schema, tableName)
            for attribute in attributeList:
                self.attributeComboBox.addItem(attribute)

    @pyqtSlot(int)
    def on_allTablesCheckBox_stateChanged(self, state):
        if state == 0:
            self.allAttributesCheckBox.setEnabled(True)
            self.schemaComboBox.setCurrentIndex(0)
            self.schemaComboBox.setEnabled(True)
        elif state == 2:
            self.allAttributesCheckBox.setEnabled(False)
            self.allAttributesCheckBox.setCheckState(0)
            self.schemaComboBox.setCurrentIndex(0)
            self.schemaComboBox.setEnabled(False)

    @pyqtSlot(int)
    def on_allAttributesCheckBox_stateChanged(self, state):
        if state == 2:
            self.allTablesCheckBox.setEnabled(False)
            self.allTablesCheckBox.setCheckState(0)
            self.attributeComboBox.setCurrentIndex(0)
            self.attributeComboBox.setEnabled(False)
        if state == 0:
            self.allTablesCheckBox.setEnabled(True)
            self.attributeComboBox.setEnabled(True)

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

    def validate(self):
        if self.actionComboBox.currentIndex() == 0:
            return False
        if self.allTablesCheckBox.checkState() == 2:
            return True
        if self.schemaComboBox.currentIndex() == 0:
            return False
        if self.tableComboBox.currentIndex() == 0:
            return False
        if self.allAttributesCheckBox.checkState() == 2:
            return True
        elif self.attributeComboBox.currentIndex() == 0:
            return False
        return True

    def validateDiagnosis(self):
        invalidatedReason = ""
        if self.schemaComboBox.currentIndex() == 0:
            invalidatedReason += self.tr("A schema must be chosen.\n")
        if self.tableComboBox.currentIndex() == 0:
            invalidatedReason += self.tr("A table must be chosen.\n")
        if self.actionComboBox.currentIndex() == 0:
            invalidatedReason += self.tr("An action be chosen.\n")
        if (
            self.allAttributesCheckBox.checkState() != 2
            and self.attributeComboBox.currentIndex() == 0
        ):
            invalidatedReason += self.tr("An attribute must be chosen.\n")
        return invalidatedReason

    def getJSONTag(self):
        if not self.validate():
            raise Exception(
                self.tr("Error in change nullity customization ")
                + self.title
                + " : "
                + self.validateDiagnosis()
            )
        if self.actionComboBox.currentIndex() == 1:
            notNull = True
        elif self.actionComboBox.currentIndex() == 2:
            notNull = False
        jsonList = []
        if self.allTablesCheckBox.checkState() == 2:
            attributeJsonList = self.abstractDb.getAttributeJsonFromDb()
            for attributeJson in attributeJsonList:
                schema = attributeJson["table_schema"]
                table = attributeJson["table_name"]
                for attrName in attributeJson["attributelist"]:
                    jsonList.append(
                        self.jsonBuilder.buildChangeNullityElement(
                            schema, table, attrName, notNull
                        )
                    )
        else:
            schema = self.schemaComboBox.currentText()
            table = self.tableComboBox.currentText()
            if self.allAttributesCheckBox.checkState() == 2:
                attrList = self.abstractDb.getAttributeListFromTable(schema, table)
                for attrName in attrList:
                    jsonList.append(
                        self.jsonBuilder.buildChangeNullityElement(
                            schema, table, attrName, notNull
                        )
                    )
            else:
                attrName = self.attributeComboBox.currentText()
                jsonList.append(
                    self.jsonBuilder.buildChangeNullityElement(
                        schema, table, attrName, notNull
                    )
                )
        return jsonList

    def getUiParameterJsonDict(self):
        """
        builds a dict with the following format:
        {
            'schemaComboBox': --current text of schemaComboBox --
            'tableComboBox': --current text of tableComboBox--
            'allAttributesCheckBox': --state of allAttributesCheckBox--
            'allTablesCheckBox': --state of allTablesCheckBox--
            'attributeComboBox': --current text of attributeComboBox--
            'actionComboBoxIdx': --current index of actionComboBox--
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
        uiParameterJsonDict["actionComboBoxIdx"] = self.actionComboBox.currentIndex()
        return uiParameterJsonDict
