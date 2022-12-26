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
from DsgTools.gui.Misc.PostgisCustomization.CustomJSONTools.customJSONBuilder import (
    CustomJSONBuilder,
)

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "newAttributeWidget.ui")
)


class NewAttributeWidget(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, abstractDb, uiParameterJsonDict=None, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.abstractDb = abstractDb
        self.setupUi(self)
        self.addAttributeWidget.abstractDb = abstractDb
        self.jsonBuilder = CustomJSONBuilder()
        self.populateSchemaCombo()
        self.populateFromUiParameterJsonDict(uiParameterJsonDict)

    def populateFromUiParameterJsonDict(self, uiParameterJsonDict):
        """
        {
            'schemaComboBox': --current text of schemaComboBox --
            'tableComboBox': --current text of tableComboBox--
            'allTablesCheckBox': --state of allTablesCheckBox--
            'attrWidget' : -- uiParameterJson from addAttributeWidget--
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
            self.addAttributeWidget.populateFromUiParameterJsonDict(
                uiParameterJsonDict["attrWidget"]
            )

    def getTitle(self):
        return self.title

    def setTitle(self, title):
        self.title = title

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
        else:
            schema = self.schemaComboBox.currentText()
            self.tableComboBox.setEnabled(True)
            self.tableComboBox.clear()
            self.tableComboBox.addItem(self.tr("Select a table"))
            tableList = self.abstractDb.getGeometricTableListFromSchema(schema)
            for table in tableList:
                self.tableComboBox.addItem(table)

    @pyqtSlot(int)
    def on_allTablesCheckBox_stateChanged(self, idx):
        if idx == 2:
            self.tableComboBox.clear()
            self.tableComboBox.setEnabled(False)
            self.schemaComboBox.clear()
            self.schemaComboBox.setEnabled(False)
        else:
            self.schemaComboBox.setEnabled(True)
            self.populateSchemaCombo()

    def validate(self):
        if not self.allTablesCheckBox.isChecked():
            if self.tableComboBox.currentText() == "":
                return False
            if self.schemaComboBox.currentText() == "":
                return False
        return self.addAttributeWidget.validate()

    def validateDiagnosis(self):
        invalidatedReason = ""
        if self.tableComboBox.currentIndex() == 0:
            invalidatedReason += self.tr("A table name must be chosen.\n")
        if self.schemaComboBox.currentIndex() == 0:
            invalidatedReason += self.tr("A schema must be chosen.\n")
        invalidatedReason += self.addAttributeWidget.validateDiagnosis()
        return invalidatedReason

    def getJSONTag(self):
        if not self.validate():
            raise Exception(
                self.tr("Error in attribute ")
                + self.title
                + " : "
                + self.validateDiagnosis()
            )
        schema = self.schemaComboBox.currentText()
        tableName = self.tableComboBox.currentText()
        attrList = [self.addAttributeWidget.getJSONTag()]
        if not self.allTablesCheckBox.isChecked():
            bloodLine = [
                i
                for i in self.abstractDb.getInheritanceBloodLine(tableName)
                if i != tableName
            ]
            return [
                self.jsonBuilder.buildNewAttributeElement(
                    schema, tableName, attrList, childrenToAlter=bloodLine
                )
            ]
        else:
            attrModList = []
            classTuppleList = self.abstractDb.getParentGeomTables(getTupple=True)
            for tupple in classTuppleList:
                schema, tableName = tupple
                if schema not in ("views", "validation"):
                    bloodLine = [
                        i
                        for i in self.abstractDb.getInheritanceBloodLine(tableName)
                        if i != tableName
                    ]
                    attrModList.append(
                        self.jsonBuilder.buildNewAttributeElement(
                            schema, tableName, attrList, childrenToAlter=bloodLine
                        )
                    )
            return attrModList

    def getUiParameterJsonDict(self):
        """
        builds a dict with the following format:
        {
            'schemaComboBox': --current text of schemaComboBox --
            'tableComboBox': --current text of tableComboBox--
            'allTablesCheckBox': --state of allTablesCheckBox--
            'attrWidget' : -- uiParameterJson from addAttributeWidget--
        }
        """
        uiParameterJsonDict = dict()
        uiParameterJsonDict["schemaComboBox"] = self.schemaComboBox.currentText()
        uiParameterJsonDict["tableComboBox"] = self.tableComboBox.currentText()
        uiParameterJsonDict["allTablesCheckBox"] = self.allTablesCheckBox.isChecked()
        uiParameterJsonDict[
            "attrWidget"
        ] = self.addAttributeWidget.getUiParameterJsonDict()
        return uiParameterJsonDict
