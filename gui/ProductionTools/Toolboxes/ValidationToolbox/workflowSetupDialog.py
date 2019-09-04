# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-09-03
        git sha              : $Format:%H$
        copyright            : (C) 2019 by João P. Esperidião - Cartographic Engineer @ Brazilian Army
        email                : esperidiao.joao@eb.mil.br
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

import os, json
from datetime import datetime

from qgis.PyQt import uic
from qgis.core import Qgis
from qgis.gui import QgsMessageBar
from qgis.PyQt.QtCore import QSize, QCoreApplication
from qgis.PyQt.QtWidgets import (QDialog,
                                 QComboBox,
                                 QCheckBox,
                                 QLineEdit,
                                 QFileDialog,
                                 QTableWidgetItem)
from processing.modeler.ModelerUtils import ModelerUtils

from DsgTools.gui.CustomWidgets.SelectionWidgets.selectFileWidget import SelectFileWidget
from DsgTools.core.DSGToolsProcessingAlgs.Models.validationWorkflow import ValidationWorkflow

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'workflowSetupDialog.ui')
)

class WorkflowSetupDialog(QDialog, FORM_CLASS):
    __qgisModelPath__ = ModelerUtils.modelsFolders()[0]
    ON_FLAGS_HALT, ON_FLAGS_WARN, ON_FLAGS_IGNORE = range(3)
    onFlagsDisplayNameMap = {
        ON_FLAGS_HALT : QCoreApplication.translate('WorkflowSetupDialog', "Halt"),
        ON_FLAGS_WARN : QCoreApplication.translate('WorkflowSetupDialog', "Warn"),
        ON_FLAGS_IGNORE : QCoreApplication.translate('WorkflowSetupDialog', "Ignore")
    }
    onFlagsValueMap = {
        ON_FLAGS_HALT : "halt",
        ON_FLAGS_WARN : "warn",
        ON_FLAGS_IGNORE : "ignore"
    }

    def __init__(self, parent=None):
        """
        Class constructor.
        :param headerMap: (dict) a map from each header to be shown and type of
                           cell content (e.g. widget or item).
        :param parent: (QtWidgets.*) any widget parent to current instance.
        """
        super(WorkflowSetupDialog, self).__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.messageBar = QgsMessageBar(self)
        self.orderedTableWidget.setHeaders({
            self.tr("Model name") : {
                "type" : "widget",
                "class" : self.modelNameWidget
            },
            self.tr("Model source") : {
                "type" : "widget",
                "class" : self.modelWidget
            },
            self.tr("On flags") : {
                "type" : "widget",
                "class" : self.onFlagsWidget
            },
            self.tr("Load output") : {
                "type" : "widget",
                "class" : self.loadOutputWidget
            }
        })

    def resizeEvent(self, e):
        """
        Reimplementation in order to use this window's resize event.
        On this object, this method makes sure that message bar is always the
        same size as the window.
        :param e: (QResizeEvent) resize event.
        """
        self.messageBar.resize(
            QSize(
                self.geometry().size().width(),
                40 # this felt nicer than the original height (30)
            )
        )

    def modelNameWidget(self):
        """
        Gets a new instance of model name's setter widget.
        :return: (QLineEdit) widget for model's name setting.
        """
        # no need to pass parenthood as it will be set to the table when added
        # to a cell
        le = QLineEdit()
        # setPlace"h"older, with a lower case "h"...
        le.setPlaceholderText(self.tr("Set a name for the model..."))
        le.setFrame(False)
        return le

    def modelWidget(self):
        """
        Gets a new instance of model settter's widget.
        :return: (SelectFileWidget) DSGTools custom file selection widget.
        """
        widget = SelectFileWidget()
        widget.label.hide()
        widget.selectFilePushButton.setText("...")
        widget.selectFilePushButton.setMaximumWidth(32)
        widget.lineEdit.setPlaceholderText(self.tr("Select a model..."))
        widget.lineEdit.setFrame(False)
        widget.setCaption(self.tr("Select a QGIS Processing model file"))
        widget.setFilter(
            self.tr("Select a QGIS Processing model (*.model *.model3)")
        )
        return widget

    def onFlagsWidget(self):
        """
        Gets a new instance for the widget that sets model's behaviour when
        flags are raised.
        :return: (QComboBox) model's behaviour selection widget. 
        """
        combo = QComboBox()
        combo.addItems([
            self.onFlagsDisplayNameMap[self.ON_FLAGS_HALT],
            self.onFlagsDisplayNameMap[self.ON_FLAGS_WARN],
            self.onFlagsDisplayNameMap[self.ON_FLAGS_IGNORE]
        ])
        return combo

    def loadOutputWidget(self):
        """
        Gets a new instance for the widget that sets output layer loading
        definitions.
        :return: (QWidget) widget for output layer loading behaviour
                 definition.
        """
        cb = QCheckBox()
        cb.setStyleSheet("margin:auto;")
        return cb

    def now(self):
        """
        Gets time and date from the system. Format: "dd/mm/yyyy HH:MM:SS".
        :return: (str) current's date and time
        """
        paddle = lambda n : str(n) if n > 9 else "0{0}".format(n)
        now = datetime.now()
        return "{day}/{month}/{year} {hour}:{minute}:{second}".format(
            year=now.year,
            month=paddle(now.month),
            day=paddle(now.day),
            hour=paddle(now.hour),
            minute=paddle(now.minute),
            second=paddle(now.second)
        )

    def workflowName(self):
        """
        Reads filled workflow name from GUI.
        :return: (str) workflow's name.
        """
        return self.nameLineEdit.text()

    def author(self):
        """
        Reads filled workflow name from GUI.
        :return: (str) workflow's author.
        """
        return self.authorLineEdit.text()

    def version(self):
        """
        Reads filled workflow name from GUI.
        :return: (str) workflow's version.
        """
        return self.versionLineEdit.text()

    def modelCount(self):
        """
        Reads the amount of models (rows added) the user intend to use.
        :return: (int) model count.
        """
        return self.orderedTableWidget.rowCount()

    def readRow(self, row):
        """
        Reads a row's contents and set it as a DsgToolsProcessingModel set of
        parameters.
        :return: (dict) parameters map.
        """
        contents = self.orderedTableWidget.row(row)
        filepath = contents[self.tr("Model source")].lineEdit.text()
        onFlagsIdx = contents[self.tr("On flags")].currentIndex()
        if not os.path.exists(filepath):
            raise Exception(
                self.tr("Model from row {0} does not exist. Check filepath.")\
                    .format(row + 1)
            )
        with open(filepath, "r", encoding="utf-8") as f:
            xml = f.read()
        return {
            "displayName" : contents[self.tr("Model name")].text().strip(),
            "flags" : {
                "onFlagsRaised" : self.onFlagsValueMap[onFlagsIdx],
                "loadOutput" : contents[self.tr("Load output" )].isChecked()
            },
            "source" : {
                "type" : "xml",
                "data" : xml
            }
        }

    def validateRowContents(self, contents):
        """
        Checks if all attributes read from a row are valid.
        :param contents: (dict) map to (already read) row contents.
        :return: (str) invalidation reason
        """
        if contents["displayName"] == "":
            return self.tr("Missing model's name.")
        if contents["source"]["data"] == "":
            return self.tr("Model is empty or file was not found.")
        return ""

    def models(self):
        """
        Reads all table contents and sets it as a DsgToolsProcessingAlgorithm's
        set of parameters.
        :return: (dict) map to each model's set of parameters.
        """
        models = dict()
        for row in range(self.modelCount()):
            contents = self.readRow(row)
            models[contents["displayName"]] = contents
        return models

    def validateModels(self):
        """
        Check if each row on table has a valid input.
        :return: (str) invalidation reason.
        """
        for row in range(self.modelCount()):
            msg = self.validateRowContents(self.readRow(row))
            if msg:
                return "Row {row}: '{error}'".format(row=row, error=msg)
        if len(self.models()) != self.modelCount():
            return self.tr("Check if no model name is repeated.")
        return ""

    def workflowParameterMap(self):
        """
        Generates a Workflow map from input data.
        """
        return {
            "displayName" : self.workflowName(),
            "models" : self.models(),
            "metadata" : {
                "author" : self.author(),
                "version" : self.version(),
                "lastModified" : self.now()
            }
        }

    def validate(self):
        """
        Checks if all filled data generates a valid Workflow object.
        :return: (bool) validation status.
        """
        if self.workflowName() == "":
            return self.tr("Workflow's name needs to be filled.")
        if self.author() == "":
            return self.tr("Workflow's author needs to be filled.")
        if self.version() == "":
            return self.tr("Workflow's version needs to be filled.")
        msg = self.validateModels()
        if msg != "":
            return msg
        return ""

    def export(self, filepath):
        """
        Exports current input data as a workflow JSON, IF input is valid.
        :return: (bool) operation success.
        """
        msg = self.validate()
        if msg != "":
            self.messageBar.pushMessage(
                self.tr('Invalid workflow'), msg, level=Qgis.Critical, duration=5
            )
            return False
        try:
            ValidationWorkflow(self.workflowParameterMap()).export(filepath)
        except:
            self.messageBar.pushMessage(
                self.tr('Invalid workflow'),
                self.tr("Unable to export workflow to '{fp}'").format(fp=filepath),
                level=Qgis.Critical,
                duration=5
            )
            return False
        result = os.path.exists(filepath)
        msg = (self.tr("exported to {fp}") if result else \
                self.tr("Unable to export workflow to '{fp}'")).format(fp=filepath)
        self.messageBar.pushMessage(
                self.tr('Invalid workflow'), msg, level=Qgis.Critical, duration=5
            )
        return result
