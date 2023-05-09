# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-02-25
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from builtins import map
from builtins import range
import os, json
from os.path import expanduser

from qgis.core import QgsMessageLog

# Qt imports
from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import pyqtSlot, Qt, QSettings
from qgis.PyQt.QtWidgets import (
    QListWidgetItem,
    QMessageBox,
    QMenu,
    QApplication,
    QFileDialog,
)
from qgis.PyQt.QtGui import QCursor
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "validationWorkflowItemWidget.ui")
)


class ValidationWorkflowItemWidget(QtWidgets.QWidget, FORM_CLASS):
    def __init__(self, parameterDict={}, parent=None):
        """Constructor."""
        super(ValidationWorkflowItemWidget, self).__init__(parent=parent)
        self.setupUi(self)
        self.validKeys = ["name", "validationProcessList"]
        self.parent = parent
        if self.parent:
            self.validationManager = parent.validationManager
        if parameterDict != {}:
            self.populateInterface(parameterDict)

    def clearAll(self):
        """
        Clears all widget information
        """
        pass

    def getParameterDict(self):
        """
        Components:
        parameterDict = {'layerName':--name of the layer--,
                         'attributeName': --name of the attribute,
                         'attributeRule': --expression--,
                         'description': --description--}
        """
        if not self.validate():
            raise Exception(self.invalidatedReason())
        parameterDict = dict()
        parameterDict["attributeRuleType"] = self.attributeRuleTypeLineEdit.text()
        parameterDict["ruleColor"] = ",".join(
            map(str, self.mColorButton.color().getRgb())
        )
        return parameterDict

    def populateInterface(self, parameterDict):
        """
        Populates interface with parameters from parameterDict.
        """
        if parameterDict:
            if not self.validateJson(parameterDict):
                raise Exception(
                    self.tr("Invalid Attribute Rule Type Widget json config!")
                )
            # set layer combo
            self.attributeRuleTypeLineEdit.setText(parameterDict["attributeRuleType"])
            R, G, B, A = list(
                map(int, parameterDict["ruleColor"].split(","))
            )  # QColor only accepts int values
            self.mColorButton.setColor(QColor(R, G, B, A))

    def validateJson(self, inputJson):
        """
        Validates input json
        """
        inputKeys = list(inputJson.keys())
        inputKeys.sort()
        if self.validKeys != inputKeys:
            return False
        else:
            return True

    def validate(self):
        """
        Validates fields. Returns True if all information are filled correctly.
        """
        if self.attributeRuleTypeLineEdit.text() == "":
            return False
        return True

    def invalidatedReason(self):
        """
        Error reason
        """
        msg = ""
        if self.attributeRuleTypeLineEdit.text() == "":
            msg += self.tr("Invalid rule name!\n")
        return msg

    @pyqtSlot(bool)
    def on_mGroupBox_collapsedStateChanged(self):
        for i in range(self.parent.tableWidget.rowCount()):
            self.parent.tableWidget.resizeRowToContents(i)

    @pyqtSlot(str)
    def on_workspaceItemLineEdit_textEdited(self, text):
        self.mGroupBox.setTitle(text)
