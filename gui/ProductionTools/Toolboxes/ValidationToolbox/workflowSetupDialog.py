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
from qgis.PyQt.QtWidgets import (QDialog,
                                 QComboBox,
                                 QCheckBox,
                                 QLineEdit,
                                 QTableWidgetItem)

from DsgTools.gui.CustomWidgets.SelectionWidgets.selectFileWidget import SelectFileWidget

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'workflowSetupDialog.ui')
)

class WorkflowSetupDialog(QDialog, FORM_CLASS):
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
        self.orderedTableWidget.setHeaders({
            "Model name" : {
                "type" : "widget",
                "class" : self.modelNameWidget
            },
            "Model source" : {
                "type" : "widget",
                "class" : self.modelWidget
            },
            "On flags" : {
                "type" : "widget",
                "class" : self.onFlagsWidget
            },
            "Load output" : {
                "type" : "widget",
                "class" : self.loadOutputWidget
            }
        })

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
            self.tr("Halt"),
            self.tr("Warn"),
            self.tr("Ignore")
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

    def readModels(self):
        """
        Reads all table contents and sets it as a DsgToolsProcessingAlgorithm's
        set of parameters.
        :return: (dict) map to each model's set of parameters.
        """
        return dict()

    def validate(self):
        """
        Checks if all filled data generates a valid Workflow object.
        :return: (bool) validation status.
        """
        return False

    def workflowParameterMap(self):
        """
        Generates a Workflow map from input data.
        """
        return {
            "displayName" : self.workflowName(),
            "models" : self.readModels(),
            "metadata" : {
                "author" : self.author(),
                "version" : self.version(),
                "lastModified" : self.now()
            }
        }

    def export(self, filepath):
        """
        Exports current input data as a workflow JSON, IF input is valid.
        """
        pass
