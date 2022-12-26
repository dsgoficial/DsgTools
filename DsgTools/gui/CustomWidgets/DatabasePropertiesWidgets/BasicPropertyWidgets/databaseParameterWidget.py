# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2016-08-26
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

from DsgTools.core.Factories.DbFactory.abstractDb import AbstractDb

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, pyqtSignal, QSettings
from qgis.PyQt.QtSql import QSqlQuery
from qgis.PyQt.QtWidgets import QFileDialog, QMessageBox, QRadioButton


FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "databaseParameterWidget.ui")
)


class DatabaseParameterWidget(QtWidgets.QWidget, FORM_CLASS):
    filesSelected = pyqtSignal()
    changeSize = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.serverAbstractDb = None
        self.selectedAbstractDb = None
        self.setInitialState()
        self.useFrame = True

    @pyqtSlot(
        AbstractDb, name="on_comboBoxPostgis_dbChanged"
    )  # check this out luiz! hahahahaha
    def populateSelectedAbstractDb(self, abstractDb):
        self.selectedAbstractDb = abstractDb
        if self.useFrame:
            self.populateFrameComboBox()

    def populateFrameComboBox(self):
        if self.selectedAbstractDb:
            areaDict = self.selectedAbstractDb.getGeomColumnDictV2(
                primitiveFilter=["a"], excludeValidation=True
            )
            self.frameComboBox.clear()
            self.frameComboBox.addItem(self.tr("Select a table from database"))
            self.tableDict = dict()
            sortedKeys = list(areaDict.keys())
            sortedKeys.sort()
            for key in sortedKeys:
                tableKey = "{0}.{1}:{2}".format(
                    areaDict[key]["tableSchema"],
                    areaDict[key]["tableName"],
                    areaDict[key]["geom"],
                )
                self.tableDict[tableKey] = areaDict[key]
                self.frameComboBox.addItem(tableKey)

    @pyqtSlot(int, name="on_frameComboBox_currentIndexChanged")
    def populateCombos(self, idx):
        if self.selectedAbstractDb:
            if idx > 0:
                self.indexComboBox.clear()
                self.inomComboBox.clear()
                self.indexComboBox.addItem(
                    self.tr("Select an attribute from selected table")
                )
                self.inomComboBox.addItem(
                    self.tr("Select an attribute from selected table")
                )
                selected = self.tableDict[self.frameComboBox.currentText()]
                attributeList = self.selectedAbstractDb.getAttributesFromTable(
                    selected["tableSchema"],
                    selected["tableName"],
                    typeFilter=["character", "character varying", "text"],
                )
                for attr in attributeList:
                    self.indexComboBox.addItem(attr)
                    self.inomComboBox.addItem(attr)

    def setServerDb(self, abstractDb):
        self.serverAbstractDb = abstractDb
        self.dbTemplateRadioButton.setEnabled(True)
        self.comboBoxPostgis.setServerDb(self.serverAbstractDb)

    def setInitialState(self):
        """
        Sets the initial state
        """
        self.prefixVisible = True
        self.sufixVisible = True
        self.dbNameVisible = True
        self.frameGroupBox.hide()
        if not self.serverAbstractDb:
            self.dbTemplateRadioButton.setEnabled(False)

    def setPrefixVisible(self, visible):
        """
        Sets if the database prefix should be visible
        """
        if isinstance(visible, bool):
            self.prefixLineEdit.setVisible(visible)
            self.prefixLabel.setVisible(visible)
            self.prefixVisible = visible

    def setSufixVisible(self, visible):
        """
        Sets if the database sufix should be visible
        """
        if isinstance(visible, bool):
            self.sufixLineEdit.setVisible(visible)
            self.sufixLabel.setVisible(visible)
            self.sufixVisible = visible

    def setDbNameVisible(self, visible):
        """
        Sets if the database name should be visible
        """
        if isinstance(visible, bool):
            self.dbNameLineEdit.setVisible(visible)
            self.dbNameLabel.setVisible(visible)
            self.dbNameVisible = visible

    def getVersion(self):
        """
        Get the database version
        """
        return self.versionComboBox.currentText()

    def validate(self):
        """
        Validate database name
        """
        errorMsg = ""
        if self.dbNameVisible:
            if self.dbNameLineEdit.text() == "":
                errorMsg += self.tr("Enter a database name!\n")
        if self.mQgsProjectionSelectionWidget.crs().authid() == "":
            errorMsg += self.tr("Select a coordinate reference system!\n")
        if not self.edgvTemplateRadioButton.isChecked():
            if not self.comboBoxPostgis.currentDb():
                errorMsg += self.tr("Select a template database!\n")
            if self.useFrame:
                if self.frameComboBox.currentIndex() == 0:
                    errorMsg += self.tr("Select a frame layer!\n")
                if self.indexComboBox.currentIndex() == 0:
                    errorMsg += self.tr("Select an index attribute!\n")
                if self.inomComboBox.currentIndex() == 0:
                    errorMsg += self.tr("Select an INOM attribute!\n")

        if errorMsg != "":
            QMessageBox.critical(self, self.tr("Critical!"), errorMsg)
            return False
        else:
            return True

    @pyqtSlot(bool, name="on_edgvTemplateRadioButton_toggled")
    def changeInterfaceState(self, edgvTemplateToggled, hideInterface=True):
        if edgvTemplateToggled:
            self.comboBoxPostgis.setEnabled(False)
            self.frameComboBox.setEnabled(False)
            self.versionComboBox.setEnabled(True)
            self.frameGroupBox.hide()
        else:
            self.comboBoxPostgis.show()
            if self.useFrame:
                self.frameGroupBox.show()
            self.comboBoxPostgis.setEnabled(True)
            self.versionComboBox.setEnabled(False)
        if not isinstance(self.sender(), QRadioButton):
            if hideInterface:
                self.frameGroupBox.hide()
                self.comboBoxPostgis.hide()
                self.dbTemplateRadioButton.hide()
            else:
                self.comboBoxPostgis.show()
                self.dbTemplateRadioButton.show()

    def getTemplateName(self):
        if self.edgvTemplateRadioButton.isChecked():
            return None
        else:
            return self.comboBoxPostgis.currentDb()

    def getTemplateParameters(self):
        if self.edgvTemplateRadioButton.isChecked():
            paramDict = dict()
            if self.serverAbstractDb:
                paramDict["templateName"] = self.serverAbstractDb.getTemplateName(
                    self.versionComboBox.currentText()
                )
            paramDict["version"] = self.versionComboBox.currentText()
            paramDict["isTemplateEdgv"] = True
            return paramDict
        else:
            paramDict = dict()
            paramDict["templateName"] = self.comboBoxPostgis.currentDb()
            paramDict["isTemplateEdgv"] = False
            if self.useFrame:
                selected = self.tableDict[self.frameComboBox.currentText()]
                paramDict["tableSchema"] = selected["tableSchema"]
                paramDict["tableName"] = selected["tableName"]
                paramDict["geom"] = selected["geom"]
                paramDict["miAttr"] = self.indexComboBox.currentText()
                paramDict["inomAttr"] = self.inomComboBox.currentText()
                paramDict["geomType"] = selected["geomType"]
            return paramDict
