# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-09-10
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

import os

from qgis.PyQt import uic
from qgis.PyQt.QtCore import pyqtSlot
from qgis.PyQt.QtWidgets import (QDockWidget,
                                 QProgressBar,
                                 QTableWidgetItem)

from DsgTools.gui.ProductionTools.Toolboxes.QualityAssuranceToolBox.workflowSetupDialog import WorkflowSetupDialog

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'qualityAssutanceDockWidget.ui')
)

class QualityAssutanceDockWidget(QDockWidget, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """
        Class constructor.
        :param iface: (QgsInterface) QGIS interface object to manage actions on
                      main window.
        :param parent: (QtWidgets.*) any widget to parent this object's
                       instance.
        """
        super(QualityAssutanceDockWidget, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self.parent = parent
        self.setState()
        self.workflows = dict()
        self.resetTable()

    def clearTable(self):
        """
        Clears table rows.
        """
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.removeRow(row)
        self.tableWidget.setRowCount(0)

    def resetTable(self):
        """
        Sets table to initial state.
        """
        self.clearTable()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels([
            self.tr("Workflow name"), self.tr("Status")
        ])

    def setState(self, isActive=False):
        """
        Sets GUI to idle (not running a Workflow) or active state (running it).
        :param isActive: (bool) whether GUI is running a Workflow.
        """
        if isActive:
            self.cancelPushButton.show()
            self.continuePushButton.hide()
        else:
            self.cancelPushButton.hide()
            self.continuePushButton.show()

    @pyqtSlot(bool, name="on_addPushButton_clicked")
    def addWorkflow(self):
        """
        Adds a workflow to available list (combo box).
        """
        dlg = WorkflowSetupDialog(parent=self)
        dlg.show()
        if dlg.exec_() == 1:
            # if result is 0, a valid workflow was filled and Ok was pressed
            workflow = dlg.currentWorkflow()
            name = workflow.displayName()
            idx = self.comboBox.findText(name)
            if idx < 0:
                self.comboBox.addItem(name)
                self.comboBox.setCurrentText(name)
                self.workflows[name] = workflow
                self.setWorkflow(workflow)
            else:
                # for now, pass, but if a conflict is raised what to do?
                # 1- check versions; 
                # 2- check last modified, etc
                pass

    def progressWidget(self):
        """
        Retrieves a progress widget bar.
        """
        bar = QProgressBar()
        bar.setTextVisible(True)
        bar.setValue(0)
        return bar

    def setWorkflow(self, workflow):
        """
        Sets workflow to GUI.
        """
        models = workflow.validModels()
        self.tableWidget.setRowCount(len(models))
        for row, modelName in enumerate(models):
            self.tableWidget.setItem(row, 0, QTableWidgetItem(modelName))
            self.tableWidget.setCellWidget(row, 1, self.progressWidget())
