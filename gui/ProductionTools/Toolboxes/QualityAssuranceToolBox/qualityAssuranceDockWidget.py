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

import os, json
from time import time
from functools import partial

from qgis.PyQt import uic
from qgis.core import Qgis
from qgis.PyQt.QtGui import QBrush, QColor
from qgis.PyQt.QtCore import Qt, pyqtSlot
from qgis.PyQt.QtWidgets import (QDockWidget,
                                 QMessageBox,
                                 QProgressBar,
                                 QTableWidgetItem)

from DsgTools.gui.ProductionTools.Toolboxes.QualityAssuranceToolBox.workflowSetupDialog import WorkflowSetupDialog

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'qualityAssuranceDockWidget.ui')
)

class QualityAssuranceDockWidget(QDockWidget, FORM_CLASS):
    # current execution status
    INITIAL, RUNNING, PAUSED, HALTED, CANCELED, FAILED, FINISHED, FINISHED_WITH_FLAGS = range(8)

    def __init__(self, iface, parent=None):
        """
        Class constructor.
        :param iface: (QgsInterface) QGIS interface object to manage actions on
                      main window.
        :param parent: (QtWidgets.*) any widget to parent this object's
                       instance.
        """
        super(QualityAssuranceDockWidget, self).__init__(parent)
        self.setupUi(self)
        self.iface = iface
        self._previousWorkflow = None
        self._firstModel = None
        self.parent = parent
        self.statusMap = {
            self.INITIAL : self.tr("Not yet run"),
            self.RUNNING : self.tr("Running..."),
            self.PAUSED : self.tr("On hold"),
            self.HALTED : self.tr("Halted on flags"),
            self.CANCELED : self.tr("Canceled"),
            self.FAILED : self.tr("Failed"),
            self.FINISHED : self.tr("Completed"),
            self.FINISHED_WITH_FLAGS : self.tr("Completed (raised flags)")
        }
        self.setState()
        self.workflows = dict()
        self.resetTable()
        self.resizeTable()
        self.resetComboBox()
        self.prepareProgressBar()

    def confirmAction(self, msg, showCancel=True):
        """
        Raises a message box for confirmation before executing an action.
        :param msg: (str) message to be exposed.
        :param showCancel: (bool) whether Cancel button should be exposed.
        :return: (bool) whether action was confirmed.
        """
        return QMessageBox.question(
            self, self.tr('DSGTools Q&A Tool Box: Confirm action'), msg,
            QMessageBox.Ok|QMessageBox.Cancel if showCancel else QMessageBox.Ok
        ) == QMessageBox.Ok

    @pyqtSlot(bool, name="on_pausePushButton_clicked")
    def workflowOnHold(self):
        """
        Sets workflow to be on hold.
        """
        self.currentWorkflow().hold()

    @pyqtSlot(bool, name="on_pausePushButton_clicked")
    def workflowOnHold(self):
        """
        Sets workflow to be on hold.
        """
        self.currentWorkflow().unhold()

    def setProgress(self, value):
        """
        Sets progress to global (Workflow) progress.
        :param value: (int/float) current percentage progress.
        """
        try:
            self.progressBar.setValue(int(value))
        except:
            self.progressBar.setValue(0)

    def prepareProgressBar(self):
        """
        Sets global progress bar to 0 and connects progress with current model's
        progress feedback.
        """
        self.progressBar.setValue(0)
        if self._previousWorkflow is not None:
            self._previousWorkflow.feedback.progressChanged.\
                disconnect(self.setProgress)
        self._previousWorkflow = self.currentWorkflow()
        if self._previousWorkflow is not None:
            self._previousWorkflow.feedback.progressChanged.\
                connect(self.setProgress)

    def showEditionButton(self, show=False):
        """
        Shows/hides buttons for workflow edition.
        :param show: (bool) visibility status.
        """
        for button in [self.addPushButton, self.editPushButton,
                        self.removePushButton]:
            getattr(button, "show" if show else "hide")

    def resizeTable(self):
        """
        Resizes table to the proportion 65% display name and 35% progress bar.
        """
        header = self.tableWidget.horizontalHeader()
        dSize = self.geometry().width() - header.geometry().width()
        missingBarSize = self.geometry().size().width() - dSize
        col1Size = int(0.5 * missingBarSize)
        col2Size = int(0.25 * missingBarSize)
        col3Size = missingBarSize - col1Size - col2Size
        header.resizeSection(0, col1Size)
        header.resizeSection(1, col2Size)
        header.resizeSection(2, col3Size)

    def resizeEvent(self, e):
        """
        Reimplementation in order to use this window's resize event.
        This makes sure that the table is resized whenever widget is resized.
        :param e: (QResizeEvent) resize event.
        """
        self.resizeTable()

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
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels([
            self.tr("Model name"), self.tr("Status"), self.tr("Progress")
        ])

    def resetComboBox(self):
        """
        Sets combo box to its initial state.
        """
        self.comboBox.clear()
        self.comboBox.addItem(self.tr("Select a workflow..."))

    def setWorkflowTooltip(self, idx, metadata):
        """
        Sets tooltip for a workflow based on its metadata.
        :para idx: (int) index for target workflow.
        :param metadata: (dict) workflow's metadata.
        """
        self.comboBox.setItemData(
            idx, 
            self.tr(
                "Workflow author: {author}\n"
                "Workflow version: {version}\n"
                "Last modification: {lastModified}"
            ).format(**metadata),
            Qt.ToolTipRole
        )

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
        self.pausePushButton.setEnabled(isActive)
        self.cancelPushButton.setEnabled(isActive)
        self.continuePushButton.setEnabled(isActive)

    def currentWorkflowName(self):
        """
        Gets current workflow's name.
        :return: (str) current workflow's name.
        """
        if self.comboBox.currentIndex() < 1:
            return ""
        return self.comboBox.currentText()

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
                self.setCurrentWorkflow()
            else:
                self.comboBox.setCurrentIndex(idx)
                # what should we do? check version/last modified? replace model?
            self.setWorkflowTooltip(
                self.comboBox.currentIndex(), workflow.metadata()
            )

    @pyqtSlot(bool, name="on_removePushButton_clicked")
    def removeWorkflow(self):
        """
        Removes current workflow selection from combo box options.
        """
        idx = self.comboBox.currentIndex()
        if idx < 1:
            return
        # raise any confirmation question?
        msg = self.tr("Are you sure you want to remove {0}")\
                  .format(self.currentWorkflowName())
        if not self.confirmAction(msg):
            return
        self.comboBox.removeItem(idx)
        self.comboBox.setCurrentIndex(0)
        name = self.currentWorkflowName()
        self.workflows.pop(name, None)

    @pyqtSlot(bool, name="on_editPushButton_clicked")
    def editCurrentWorkflow(self):
        """
        Edits current workflow selection from combo box options.
        """
        workflow = self.currentWorkflow()
        previousName = workflow.displayName()
        if workflow is None:
            return
        dlg = WorkflowSetupDialog(self)
        dlg.show()
        temp = "./temp_workflow_{0}.workflow".format(hash(time()))
        with open(temp, "w+", encoding="utf-8") as f:
            json.dump(workflow.asDict(), f)
        dlg.importWorkflow(temp)
        os.remove(temp)
        if dlg.exec_() == 1:
            # block "if modifications are confirmed by user"
            newWorkflow = dlg.currentWorkflow()
            newName = newWorkflow.displayName()
            if newName != previousName and newName in self.workflows:
                self.iface.messageBar().pushMessage(
                    self.tr("DSGTools Q&A Tool Box"),
                    self.tr(
                        "modified name is already set for other"
                        " workflow. Nothing changed."
                    ),
                    Qgis.Warning,
                    duration=3
                )
                return
            if newName == previousName:
                self.setCurrentWorkflow()
                msg = self.tr("{0} updated (make sure you exported it).")\
                          .format(newName)
            else:
                self.comboBox.setItemText(self.comboBox.currentIndex(), newName)
                self.workflows.pop(previousName, None)
                msg = self.tr(
                    "{1} renamed to {0} and updated (make sure you exported it)."
                ).format(newName, previousName)
            self.workflows[newName] = newWorkflow
            self.setWorkflowTooltip(
                self.comboBox.currentIndex(), newWorkflow.metadata()
            )
            self.setCurrentWorkflow()
            self.iface.messageBar().pushMessage(
                self.tr("DSGTools Q&A Tool Box"),
                msg,
                Qgis.Info,
                duration=3
            )

    def progressWidget(self):
        """
        Retrieves a progress widget bar.
        """
        bar = QProgressBar()
        bar.setTextVisible(True)
        bar.setValue(0)
        return bar

    def currentWorkflow(self):
        """
        Retrieves current selected workflow.
        :return: (QualityAssuranceWorkflow) current workflow.
        """
        name = self.currentWorkflowName()
        return self.workflows[name] if name in self.workflows else None

    def setModelStatus(self, row, code, modelName=None):
        """
        Sets model execution status to its cell.
        :param row: (int) model's row on GUI.
        :param code: (int) code to current status (check this class enumerator).
        :param modelName: (str) para to notify user of status change. This 
                          should be passed only through dynamic changes in order
                          to avoid polluting QGIS main window.
        """
        status = self.statusMap[code]
        item = QTableWidgetItem(status)
        # togle editable flag to make it NOT editable
        item.setFlags(Qt.ItemIsEditable)
        color = {
            self.INITIAL : QColor(0, 0, 0),
            self.RUNNING : QColor(0, 0, 125),
            self.PAUSED : QColor(187, 201, 25),
            self.HALTED : QColor(187, 201, 25),
            self.CANCELED : QColor(200, 0, 0),
            self.FAILED : QColor(169, 18, 28),
            self.FINISHED : QColor(0, 125, 0),
            self.FINISHED_WITH_FLAGS : QColor(90, 135, 39)
        }[code]
        item.setForeground(QBrush(color))
        self.tableWidget.setItem(row, 1, item)
        if modelName is not None:
            # advise user a model status has changed only if it came from a 
            # signal call
            self.iface.messageBar().pushMessage(
                self.tr("DSGTool Q&A Toolbox"),
                self.tr("model {0} finished with status {1}.")\
                    .format(modelName, status),
                {
                    self.RUNNING : Qgis.Info,
                    self.PAUSED : Qgis.Info,
                    self.HALTED : Qgis.Critical,
                    self.CANCELED : Qgis.Warning,
                    self.FAILED : Qgis.Critical,
                    self.FINISHED : Qgis.Info,
                    self.FINISHED_WITH_FLAGS : Qgis.Warning
                }[code],
                duration=3
            )

    def setWorkflow(self, workflow):
        """
        Sets workflow to GUI.
        """
        self.clearTable()
        if workflow is None:
            return
        models = workflow.validModels()
        self.tableWidget.setRowCount(len(models))
        def progressInt(pb, x):
            pb.setValue(int(x))
        for row, (modelName, model) in enumerate(models.items()):
            item = QTableWidgetItem(modelName)
            item.setFlags(Qt.ItemIsEditable)
            item.setForeground(QBrush(QColor(0, 0, 0)))
            self.tableWidget.setItem(row, 0, item)
            self.setModelStatus(row, self.INITIAL)
            pb = self.progressWidget()
            self.tableWidget.setCellWidget(row, 2, pb)

    @pyqtSlot(int, name="on_comboBox_currentIndexChanged")
    @pyqtSlot(str, name="on_comboBox_currentTextChanged")
    def setCurrentWorkflow(self):
        """
        Sets current workflow to table.
        """
        self.prepareProgressBar()
        workflow = self.currentWorkflow()
        enable = workflow is not None
        self.setWorkflow(workflow)
        self.editPushButton.setEnabled(enable)
        self.removePushButton.setEnabled(enable)

    @pyqtSlot(bool, name="on_runPushButton_clicked")
    @pyqtSlot(bool, name="on_resumePushButton_clicked")
    def runWorkflow(self):
        """
        Executes current selected workflow.
        """
        workflow = self.currentWorkflow()
        if workflow is not None:
            self.setState(True)
            def intWrapper(pb, v):
                pb.setValue(int(v))
            def statusChangedWrapper(row, model, status):
                """code: (QgsTask.Enum) status enum"""
                if row is None:
                    for row in range(self.tableWidget.rowCount()):
                        if self.tableWidget.item(row, 0).text() == model.name():
                            break
                code = {
                    model.Queued : self.INITIAL,
                    model.OnHold : self.PAUSED,
                    model.Running : self.RUNNING,
                    model.Complete : self.FINISHED,
                    model.Terminated : self.FAILED
                }[status]
                if code != self.INITIAL:
                    self.setModelStatus(row, code, model.displayName())
            def begin(model):
                for row in range(self.tableWidget.rowCount()):
                    if self.tableWidget.item(row, 0).text() != model.name():
                        continue
                    self.__progressFunc = partial(
                        intWrapper, self.tableWidget.cellWidget(row, 2)
                    )
                    model.feedback.progressChanged.connect(self.__progressFunc)
                    model.statusChanged.connect(
                        partial(statusChangedWrapper, row, model)
                    )
                    return
            def end(model):
                for row in range(self.tableWidget.rowCount()):
                    if self.tableWidget.item(row, 0).text() != model.name():
                        continue
                    model.feedback.progressChanged.disconnect(self.__progressFunc)
                    return
            workflow.modelStarted.connect(begin)
            workflow.modelFinished.connect(end)
            if self.sender().objectName() == "runPushButton":
                workflow.run()
            else:
                workflow.run(firstModelName=self._firstModel)
            self._firstModel = workflow.lastModelName()
        else:
            self.iface.messageBar().pushMessage(
                self.tr("DSGTools Q&A Tool Box"),
                self.tr("please select a valid Workflow."),
                Qgis.Warning,
                duration=3
            )
        self.setState(False)
