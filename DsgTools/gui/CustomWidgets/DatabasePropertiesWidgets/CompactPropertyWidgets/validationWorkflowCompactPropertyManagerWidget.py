# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2017-02-24
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

# Qt imports
from qgis.PyQt import QtGui, uic, QtCore
from qgis.PyQt.QtCore import pyqtSlot, Qt, pyqtSignal
from qgis.PyQt.QtWidgets import QMessageBox, QApplication, QFileDialog
from qgis.PyQt.QtGui import QCursor

# DsgTools imports
from DsgTools.gui.CustomWidgets.DatabasePropertiesWidgets.CompactPropertyWidgets.genericCompactPropertyManagerWidget import (
    GenericCompactPropertyManagerWidget,
)
from DsgTools.core.ServerManagementTools.validationWorkflowManager import (
    ValidationWorkflowManager,
)
from DsgTools.gui.ProductionTools.Toolboxes.ValidationToolbox.validationWorkflowCreator import (
    ValidationWorkflowCreator,
)
from DsgTools.core.Utils.utils import Utils
from DsgTools.core.dsgEnums import DsgEnums

from qgis.core import QgsMessageLog
import json


class ValidationWorkflowCompactPropertyManagerWidget(
    GenericCompactPropertyManagerWidget
):
    def __init__(self, manager=None, parent=None):
        """
        Constructor
        """
        super(ValidationWorkflowCompactPropertyManagerWidget, self).__init__(
            parent=parent
        )

    def populateConfigInterface(self, validationManager, jsonDict=None):
        """
        Must be reimplemented in each child
        """
        dlg = ValidationWorkflowCreator(validationManager, parameterDict=jsonDict)
        if dlg.exec_():
            return dlg.getParameterDict()
        else:
            return None

    def instantiateManagerObject(self, abstractDb, dbDict, edgvVersion):
        return ValidationWorkflowManager(abstractDb, dbDict, edgvVersion)

    @pyqtSlot(bool)
    def on_createPropertyPushButton_clicked(self):
        """
        1. Open custom manager according to property type;
        2. Use manager to apply to database
        """
        setupDict = self.populateConfigInterface(self.parent.validationManager)
        if setupDict:
            self.genericDbManager.createAndInstall(
                propertyName,
                setupDict,
                self.genericDbManager.edgvVersion,
                dbList=[self.abstractDb.db.databaseName()],
            )
            self.refresh()
            QMessageBox.information(
                self,
                self.tr("Success!"),
                self.tr("{0} configuration {1} created successfuly!").format(
                    self.widgetName, propertyName
                ),
            )
