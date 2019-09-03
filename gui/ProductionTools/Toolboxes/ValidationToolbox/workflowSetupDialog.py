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
from qgis.PyQt.QtWidgets import QDialog, QTableWidgetItem

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
            "Model name" : "item",
            "Model source" : "item",
            "Model data" : "item",
            "On flags" : "widget"
        })

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
