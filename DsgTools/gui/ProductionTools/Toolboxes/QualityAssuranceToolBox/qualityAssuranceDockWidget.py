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

from collections import defaultdict
import os, json
from time import time
from functools import partial
from typing import Dict, List, OrderedDict

from qgis.PyQt import uic
from qgis.core import (
    Qgis,
    QgsProject,
    QgsMessageLog,
    QgsProcessingFeedback,
    QgsExpressionContextUtils,
    QgsVectorLayer,
)
from qgis.PyQt.QtGui import QBrush, QColor
from qgis.PyQt.QtCore import Qt, pyqtSlot, QEvent
from qgis.PyQt.QtWidgets import (
    QAction,
    QLineEdit,
    QFileDialog,
    QDockWidget,
    QMessageBox,
    QProgressBar,
    QTableWidgetItem,
    QMenu,
)

from DsgTools.gui.ProductionTools.Toolboxes.QualityAssuranceToolBox.workflowSetupDialog import (
    WorkflowSetupDialog,
)
from DsgTools.core.DSGToolsProcessingAlgs.Models.qualityAssuranceWorkflow import (
    QualityAssuranceWorkflow,
)


FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "qualityAssuranceDockWidget.ui")
)


class QualityAssuranceDockWidget(QDockWidget, FORM_CLASS):
    # current execution status
    (
        INITIAL,
        RUNNING,
        PAUSED,
        HALTED,
        CANCELED,
        FAILED,
        FINISHED,
        FINISHED_WITH_FLAGS,
        IGNORE_FLAGS,
    ) = range(9)

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
        self.__workflowCanceled = False
        self._showButtons = True
        self.parent = parent
        self.statusMap = {
            self.INITIAL: self.tr("Not yet run"),
            self.RUNNING: self.tr("Running..."),
            self.PAUSED: self.tr("On hold. Check data and resume."),
            self.HALTED: self.tr("Halted on flags"),
            self.CANCELED: self.tr("Canceled"),
            self.FAILED: self.tr("Failed"),
            self.FINISHED: self.tr("Completed"),
            self.FINISHED_WITH_FLAGS: self.tr("Completed (raised flags)"),
            self.IGNORE_FLAGS: self.tr("Completed (false positive flags)"),
        }
        self.colorForeground = {
            self.INITIAL: (0, 0, 0),
            self.RUNNING: (0, 0, 125),
            self.PAUSED: (187, 201, 25),
            self.HALTED: (187, 201, 25),
            self.CANCELED: (200, 0, 0),
            self.FAILED: (169, 18, 28),
            self.FINISHED: (0, 125, 0),
            self.FINISHED_WITH_FLAGS: (100, 150, 20),
            self.IGNORE_FLAGS: (0, 0, 0),
        }
        self.colorBackground = {
            self.INITIAL: (255, 255, 255, 75),
            self.RUNNING: (0, 0, 125, 90),
            self.PAUSED: (187, 201, 25, 20),
            self.HALTED: (200, 215, 40, 20),
            self.CANCELED: (200, 0, 0, 85),
            self.FAILED: (169, 18, 28, 85),
            self.FINISHED: (0, 125, 0, 90),
            self.FINISHED_WITH_FLAGS: (100, 150, 20, 45),
            self.IGNORE_FLAGS: (255, 230, 1),
        }
        self.qgisStatusDict = {
            self.RUNNING: Qgis.Info,
            self.PAUSED: Qgis.Info,
            self.HALTED: Qgis.Critical,
            self.CANCELED: Qgis.Warning,
            self.FAILED: Qgis.Critical,
            self.FINISHED: Qgis.Info,
            self.FINISHED_WITH_FLAGS: Qgis.Warning,
            self.IGNORE_FLAGS: Qgis.Warning,
        }
        self.workflowStatusDict = defaultdict(OrderedDict)
        self.ignoreFlagsMenuDict = defaultdict(dict)
        self.setGuiState()
        self.continuePushButton.hide()
        self.workflows = dict()
        self.resetComboBox()
        self.resetTable()
        self.loadState()
        self.prepareProgressBar()
        # make sure workflows are loaded as per project instances
        QgsProject.instance().projectSaved.connect(self.saveState)
        # self.iface.newProjectCreated.connect(self.saveState)
        # self.iface.newProjectCreated.connect(self.loadState)
        self.iface.projectRead.connect(self.loadState)

    def generateMenu(self, pos, idx, widget, modelName, workflow):
        workflowName = workflow.name()
        currentStatusDict = self.workflowStatusDict.get(workflowName, {})
        if idx == -1 or currentStatusDict.get(modelName, self.INITIAL) not in [
            self.FINISHED_WITH_FLAGS,
            self.IGNORE_FLAGS,
        ]:
            return
        if (
            currentStatusDict.get(modelName, self.INITIAL) == self.IGNORE_FLAGS
            and currentStatusDict.get(workflow.getNextModelName(idx), self.INITIAL)
            != self.INITIAL
        ):
            return
        if idx not in self.ignoreFlagsMenuDict[workflowName]:
            return

        out = self.ignoreFlagsMenuDict[workflowName][idx].exec_(widget.mapToGlobal(pos))

    def prepareIgnoreFlagMenuDictItem(self, idx, modelName, workflow):
        workflowName = workflow.name()
        self.ignoreFlagsMenuDict[workflowName][idx] = QMenu(self)
        action = QAction(
            self.tr(f"Ignore false positive flags on model {modelName}"),
            self.ignoreFlagsMenuDict[workflowName][idx],
        )
        func = partial(
            self.setModelStatus, row=idx, modelName=modelName, raiseMessage=True
        )
        callback = lambda x: func(
            code=self.IGNORE_FLAGS if x else self.FINISHED_WITH_FLAGS
        )
        action.setCheckable(True)
        action.triggered.connect(callback)
        self.ignoreFlagsMenuDict[workflowName][idx].addAction(action)

    def confirmAction(self, msg, showCancel=True):
        """
        Raises a message box for confirmation before executing an action.
        :param msg: (str) message to be exposed.
        :param showCancel: (bool) whether Cancel button should be exposed.
        :return: (bool) whether action was confirmed.
        """
        return (
            QMessageBox.question(
                self,
                self.tr("DSGTools Q&A Tool Box: Confirm action"),
                msg,
                QMessageBox.Ok | QMessageBox.Cancel if showCancel else QMessageBox.Ok,
            )
            == QMessageBox.Ok
        )

    @pyqtSlot(bool, name="on_pausePushButton_clicked")
    def workflowOnHold(self, currentModel=None):
        """
        Sets workflow to be on hold.
        """
        self.currentWorkflow().hold()
        self.pausePushButton.hide()
        self.continuePushButton.show()
        self.runPushButton.setEnabled(False)
        self.resumePushButton.setEnabled(False)

    @pyqtSlot(bool, name="on_continuePushButton_clicked")
    def continueWorkflow(self):
        """
        Sets workflow to be on hold.
        """
        self.currentWorkflow().unhold()
        self.pausePushButton.show()
        self.continuePushButton.hide()
        self.runPushButton.setEnabled(False)
        self.resumePushButton.setEnabled(False)

    @pyqtSlot(bool, name="on_cancelPushButton_clicked")
    def cancelWorkflow(self):
        """
        Cancels current workflow's execution.
        """
        self.currentWorkflow().feedback.cancel()
        self.pausePushButton.show()
        self.continuePushButton.hide()
        self.setGuiState(False)
        self.__workflowCanceled = True

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
            self._previousWorkflow.feedback.progressChanged.disconnect(self.setProgress)
        self._previousWorkflow = self.currentWorkflow()
        if self._previousWorkflow is not None:
            self._previousWorkflow.feedback.progressChanged.connect(self.setProgress)

    def showEditionButton(self, show=False):
        """
        Shows/hides buttons for workflow edition.
        :param show: (bool) visibility status.
        """
        for button in [
            self.addPushButton,
            self.editPushButton,
            self.removePushButton,
            self.importPushButton,
            self.splitter,
        ]:
            getattr(button, "show" if show else "hide")()
        self._showButtons = show

    def resizeTable(self):
        """
        Resizes table to the proportion 40% display name and 40% progress bar.
        """
        header = self.tableWidget.horizontalHeader()
        dSize = abs(self.geometry().width() - header.geometry().width())
        missingBarSize = self.geometry().size().width() - dSize
        col1Size = int(0.4 * missingBarSize)
        col2Size = int(0.3 * missingBarSize)
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
        self.tableWidget.setHorizontalHeaderLabels(
            [self.tr("Model name"), self.tr("Status"), self.tr("Progress")]
        )
        self.resizeTable()

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
            Qt.ToolTipRole,
        )

    def setGuiState(self, isActive=False):
        """
        Sets GUI to idle (not running a Workflow) or active state (running it).
        :param isActive: (bool) whether GUI is running a Workflow.
        """
        self.pausePushButton.setEnabled(isActive)
        self.cancelPushButton.setEnabled(isActive)
        self.continuePushButton.setEnabled(isActive)
        self.runPushButton.setEnabled(not isActive)
        self.resumePushButton.setEnabled(not isActive)

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
        # if result is 0, a valid workflow was filled and Ok was pressed
        if dlg.exec_() != 1:
            return
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
        self.setWorkflowTooltip(self.comboBox.currentIndex(), workflow.metadata())
        self.saveState()

    @pyqtSlot(bool, name="on_removePushButton_clicked")
    def removeWorkflow(self):
        """
        Removes current workflow selection from combo box options.
        """
        idx = self.comboBox.currentIndex()
        if idx < 1:
            return
        # raise any confirmation question?
        name = self.currentWorkflowName()
        msg = self.tr(f"Are you sure you want to remove workflow {name}?")
        if not self.confirmAction(msg):
            return
        self.comboBox.removeItem(idx)
        self.comboBox.setCurrentIndex(0)
        self.workflows.pop(name, None)
        self.ignoreFlagsMenuDict.pop(name, None)
        self.workflowStatusDict.pop(name, None)
        self.saveState()

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
        temp = os.path.join(
            os.path.dirname(__file__), "temp_workflow_{0}.workflow".format(hash(time()))
        )
        with open(temp, "w+", encoding="utf-8") as f:
            json.dump(workflow.asDict(), f)
        dlg.importWorkflow(temp)
        os.remove(temp)
        if dlg.exec_() != 1:
            return
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
                duration=3,
            )
            return
        if newName == previousName:
            self.setCurrentWorkflow()
            msg = self.tr("{0} updated (make sure you exported it).").format(newName)
        else:
            self.comboBox.setItemText(self.comboBox.currentIndex(), newName)
            self.workflows.pop(previousName, None)
            msg = self.tr(
                "{1} renamed to {0} and updated (make sure you exported it)."
            ).format(newName, previousName)
        self.workflows[newName] = newWorkflow
        self.setWorkflowTooltip(self.comboBox.currentIndex(), newWorkflow.metadata())
        self.setCurrentWorkflow()
        self.iface.messageBar().pushMessage(
            self.tr("DSGTools Q&A Tool Box"), msg, Qgis.Info, duration=3
        )
        self.saveState()

    def progressWidget(self, value=0):
        """
        Retrieves a progress widget bar.
        """
        bar = QProgressBar()
        bar.setTextVisible(True)
        bar.setValue(value)
        return bar

    def currentWorkflow(self):
        """
        Retrieves current selected workflow.
        :return: (QualityAssuranceWorkflow) current workflow.
        """
        name = self.currentWorkflowName()
        return self.workflows[name] if name in self.workflows else None

    def setRowColor(self, row, backgroundColor, foregroundColor):
        """
        Sets cell colors for model's name and its status.
        :param row: (int) model's row on GUI.
        :param backgroundColor: (tuple-of-int) tuple containing RGBA values.
        :param foregroundColor: (tuple-of-int) tuple containing RGB values.
        """
        styleSheet = (
            "*{ background-color:rgba"
            + str(backgroundColor)
            + "; color:rgb"
            + str(foregroundColor)
            + "; } "
            + "QToolTip{ background-color:black; color:white; }"
        )
        self.tableWidget.cellWidget(row, 0).setStyleSheet(styleSheet)
        self.tableWidget.cellWidget(row, 1).setStyleSheet(styleSheet)

    def setModelStatus(self, row, code, modelName, raiseMessage=False):
        """
        Sets model execution status to its cell.
        :param row: (int) model's row on GUI.
        :param code: (int) code to current status (check this class enumerator).
        :param modelName: (str) para to notify user of status change. This
                          should be passed only through dynamic changes in order
                          to avoid polluting QGIS main window.
        """
        status = self.statusMap[code]
        self.setRowStatus(row, code)
        self.tableWidget.cellWidget(row, 1).setText(status)
        if raiseMessage or code in [self.HALTED, self.FAILED, self.FINISHED_WITH_FLAGS]:
            # advise user a model status has changed only if it came from a
            # signal call
            self.iface.messageBar().pushMessage(
                self.tr("DSGTools Q&A Toolbox"),
                self.tr("model {0} status changed to {1}.").format(modelName, status),
                self.qgisStatusDict[code],
                duration=3,
            )
        elif code != self.INITIAL:
            QgsMessageLog.logMessage(
                self.tr("Model {0} status changed to {1}.").format(modelName, status),
                "DSGTools Plugin",
                self.qgisStatusDict[code],
            )
        if (
            modelName in self.workflowStatusDict[self.comboBox.currentText()]
            and code == self.workflowStatusDict[self.comboBox.currentText()][modelName]
        ):
            return
        if code == self.FINISHED and self.workflowStatusDict[
            self.comboBox.currentText()
        ][modelName] in [self.FAILED, self.HALTED, self.FINISHED_WITH_FLAGS]:
            return
        if (
            modelName in self.workflowStatusDict[self.comboBox.currentText()]
            and code == self.INITIAL
            and self.workflowStatusDict[self.comboBox.currentText()][modelName]
            in [self.FAILED, self.FINISHED_WITH_FLAGS]
        ):
            return
        if code == self.IGNORE_FLAGS:
            workflow = self.currentWorkflow()
            outputStatusDict = workflow.getOutputStatusDict()
            outputStatusDict[modelName]["finishStatus"] = "finished"
            workflow.setOutputStatusDict(outputStatusDict)
            self.workflowStatusDict[self.comboBox.currentText()][modelName] = code
            return
        self.workflowStatusDict[self.comboBox.currentText()][modelName] = code

    def setRowStatus(self, row, code):
        colorForeground = self.colorForeground[code]
        colorBackground = self.colorBackground[code]
        if code == self.INITIAL:
            # dark mode does not look good with this color pallete...
            self.tableWidget.cellWidget(row, 0).setStyleSheet("")
            self.tableWidget.cellWidget(row, 1).setStyleSheet("")
        else:
            self.setRowColor(row, colorBackground, colorForeground)

    def customLineWidget(self, text, tooltip=None):
        """
        Retrieves a QLineEdit widget ready to be added to the model's table.
        :param text: (str) text to be filled.
        :param tooltip: (str) text to be shown when cell is hovered.
        """
        le = QLineEdit()
        le.setReadOnly(True)
        le.setText(text)
        if tooltip:
            le.setToolTip(tooltip)
        le.setFrame(False)
        # make it not selectable
        le.selectionChanged.connect(lambda: le.setSelection(0, 0))
        return le

    def setWorkflow(self, workflow):
        """
        Sets workflow to GUI.
        """
        self.clearTable()
        if workflow is None:
            return
        models = workflow.validModels()
        self.tableWidget.setRowCount(len(models))

        currentStatusDict = self.workflowStatusDict.get(workflow.name(), {})
        for row, (modelName, model) in enumerate(models.items()):
            tooltip = self.tr(
                f"Model name: {model.displayName()}\n{model.description()}"
            )
            if model.modelCanHaveFalsePositiveFlags():
                self.prepareIgnoreFlagMenuDictItem(row, modelName, workflow)
            nameWidget = self.customLineWidget(modelName, tooltip)
            nameWidget.setContextMenuPolicy(Qt.CustomContextMenu)
            nameWidget.customContextMenuRequested.connect(
                partial(
                    self.generateMenu,
                    idx=row,
                    widget=nameWidget,
                    modelName=modelName,
                    workflow=workflow,
                )
            )
            self.tableWidget.setCellWidget(row, 0, nameWidget)
            statusWidget = self.customLineWidget("", tooltip)
            statusWidget.setContextMenuPolicy(Qt.CustomContextMenu)
            statusWidget.customContextMenuRequested.connect(
                partial(
                    self.generateMenu,
                    idx=row,
                    widget=statusWidget,
                    modelName=modelName,
                    workflow=workflow,
                )
            )
            self.tableWidget.setCellWidget(row, 1, statusWidget)
            code = currentStatusDict.get(modelName, self.INITIAL)
            self.setModelStatus(row, code, modelName)
            pb = self.progressWidget(
                value=100
                if code
                in [
                    self.FINISHED,
                    self.FINISHED_WITH_FLAGS,
                    self.IGNORE_FLAGS,
                ]
                else 0
            )
            pb.setContextMenuPolicy(Qt.CustomContextMenu)
            self.tableWidget.setCellWidget(row, 2, pb)

    def preProcessing(self, firstModel=None):
        """
        Clears all progresses and set status to intial state.
        :param firstModel: (str) first model to be run.
        """
        isAfter = False
        for row in range(self.tableWidget.rowCount()):
            modelName = self.tableWidget.cellWidget(row, 0).text()
            if firstModel is not None and modelName != firstModel and not isAfter:
                continue
            isAfter = True
            self.setModelStatus(row, self.INITIAL, modelName)
            self.tableWidget.cellWidget(row, 2).setValue(0)

    def saveState(self):
        """
        Makes sure all added workflows are stored to active instance of
        QgsProject, making it "loadable" along with saved QGIS projects.
        """
        # workflow objects cannot be serialized, so they must be passed as dict
        workflows = {
            w.displayName(): w.asDict(withOutputDict=True)
            for w in self.workflows.values()
        }

        QgsExpressionContextUtils.setProjectVariable(
            QgsProject.instance(),
            "dsgtools_qatoolbox_state",
            json.dumps(
                {
                    "workflows": workflows,
                    "current_workflow": self.comboBox.currentIndex(),
                    "show_buttons": self._showButtons,
                    "workflow_status_dict": self.workflowStatusDict,
                }
            ),
        )

    def loadState(self, state=None):
        """
        Loads all loaded workflows from current QgsProject instance.
        :param state: (str) this should be a strigfied map to QA's state
                      variables. If none is given, state is retrieved from the
                      project.
        """
        state = json.loads(
            state
            or QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable(
                "dsgtools_qatoolbox_state"
            )
            or "{}"
        )
        workflows = state["workflows"] if "workflows" in state else {}
        workflow_status_dict = state.get("workflow_status_dict", {})
        self.resetComboBox()
        for idx, (name, workflowMap) in enumerate(workflows.items()):
            self.workflows[name] = QualityAssuranceWorkflow(workflowMap)
            self.comboBox.addItem(name)
            self.setWorkflowTooltip(idx + 1, self.workflows[name].metadata())
            self.workflowStatusDict[name] = OrderedDict(
                workflow_status_dict.get(name, {})
            )
        currentIdx = state["current_workflow"] if "current_workflow" in state else 0
        self.comboBox.setCurrentIndex(currentIdx)
        showButtons = state["show_buttons"] if "show_buttons" in state else True
        self.showEditionButton(showButtons)

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
        if workflow is None:
            self.iface.messageBar().pushMessage(
                self.tr("DSGTools Q&A Tool Box"),
                self.tr("please select a valid Workflow."),
                Qgis.Warning,
                duration=3,
            )
            return
        self.setGuiState(True)
        # these methods are defined locally as they are not supposed to be
        # outside thread execution setup and should all be handled from
        # within this method - at runtime
        def refreshFeedback():
            # refresh feedback track to not carry "bias" to next execution
            workflow.feedback.progressChanged.disconnect(self.setProgress)
            del workflow.feedback
            workflow.feedback = QgsProcessingFeedback()
            workflow.feedback.progressChanged.connect(self.setProgress)

        def intWrapper(pb, v):
            pb.setValue(int(v))

        def statusChangedWrapper(row, model, status):
            """status: (QgsTask.Enum) status enum"""
            if row is None:
                for row in range(self.tableWidget.rowCount()):
                    if self.tableWidget.cellWidget(row, 0).text() == model.name():
                        break
            code = {
                model.Queued: self.INITIAL,
                model.OnHold: self.PAUSED,
                model.Running: self.RUNNING,
                model.Complete: self.FINISHED,
                model.Terminated: self.FAILED,
                model.WarningFlags: self.HALTED,
                model.HaltedOnFlags: self.FINISHED_WITH_FLAGS,
                model.HaltedOnPossibleFalsePositiveFlags: self.IGNORE_FLAGS,
            }[status]
            if (
                status == model.Complete
                and model.output.get("finishStatus", None) == "halt"
            ):
                code = self.FINISHED_WITH_FLAGS
            if (
                status == model.Terminated
                and model.output.get("finishStatus", None) != "halt"
            ):
                if self.__workflowCanceled:
                    code = self.CANCELED
                # if workflow was canceled (through the cancel push button),
                # workflowFinished signal will not be emited...
                postProcessing()
                self.__workflowCanceled = False
            if code != self.INITIAL:
                self.setModelStatus(row, code, model.displayName(), raiseMessage=True)

        def begin(model):
            for row in range(self.tableWidget.rowCount()):
                if self.tableWidget.cellWidget(row, 0).text() != model.name():
                    continue
                self.__progressFunc = partial(
                    intWrapper, self.tableWidget.cellWidget(row, 2)
                )
                model.feedback.progressChanged.connect(self.__progressFunc)
                self.__statusFunc = partial(statusChangedWrapper, row, model)
                model.statusChanged.connect(self.__statusFunc)
                self.setModelStatus(row, self.RUNNING, model.displayName())
                return

        def end(model):
            for row in range(self.tableWidget.rowCount()):
                if self.tableWidget.cellWidget(row, 0).text() != model.name():
                    continue
                model.feedback.progressChanged.disconnect(self.__progressFunc)
                model.statusChanged.disconnect(self.__statusFunc)
                return

        def pause(model):
            for row in range(self.tableWidget.rowCount()):
                if self.tableWidget.cellWidget(row, 0).text() != model.name():
                    continue
                self.setModelStatus(row, self.PAUSED, model.displayName())
            postProcessing()

        def stopOnFlags(model):
            refreshFeedback()
            isAfter = False
            for row in range(self.tableWidget.rowCount()):
                if (
                    self.tableWidget.cellWidget(row, 0).text() != model.name()
                    and not isAfter
                ):
                    continue
                if isAfter:
                    code = self.INITIAL
                    self.tableWidget.cellWidget(row, 2).setValue(0)
                else:
                    model.feedback.progressChanged.disconnect(self.__progressFunc)
                    model.statusChanged.disconnect(self.__statusFunc)
                    code = self.FINISHED_WITH_FLAGS
                isAfter = True
                self.setModelStatus(row, code, model.displayName())
            postProcessing()

        def warningFlags(model):
            for row in range(self.tableWidget.rowCount()):
                if self.tableWidget.cellWidget(row, 0).text() != model.name():
                    continue
                model.feedback.progressChanged.disconnect(self.__progressFunc)
                model.statusChanged.disconnect(self.__statusFunc)
                self.setModelStatus(row, self.FINISHED_WITH_FLAGS, model.displayName())
                return

        def postProcessing():
            """
            When workflow finishes, its signals are kept connected and that
            might cause missbehaviour on next executions.
            """
            workflow.modelStarted.disconnect(begin)
            workflow.modelFinished.disconnect(end)
            workflow.haltedOnFlags.disconnect(stopOnFlags)
            workflow.modelFinishedWithFlags.disconnect(warningFlags)
            workflow.workflowFinished.disconnect(postProcessing)
            workflow.workflowPaused.disconnect(pause)
            refreshFeedback()
            self.setGuiState(False)
            self.pausePushButton.show()
            self.continuePushButton.hide()
            for m in workflow.validModels().values():
                if m.hasFlags():
                    msg = self.tr("workflow {0} finished with flags.")
                    lvl = Qgis.Warning
                    break
            else:
                msg = self.tr("workflow {0} finished.")
                lvl = Qgis.Success
            self.iface.messageBar().pushMessage(
                self.tr("DSGTools Q&A Toolbox"),
                msg.format(workflow.displayName()),
                lvl,
                duration=3,
            )

        sender = self.sender()
        isFirstModel = sender is None or sender.objectName() == "runPushButton"
        idx, lastModelDisplayName = workflow.lastModelName(returnIdx=True)
        if idx != 0 and sender.objectName() == "runPushButton":
            if not self.confirmAction(msg=self.tr("The workflow has already started running. Would you like to start over?"), showCancel=True):
                refreshFeedback()
                self.setGuiState(False)
                self.pausePushButton.show()
                self.continuePushButton.hide()
                return
        workflow.modelStarted.connect(begin)
        workflow.modelFinished.connect(end)
        workflow.haltedOnFlags.connect(stopOnFlags)
        workflow.modelFinishedWithFlags.connect(warningFlags)
        workflow.workflowFinished.connect(postProcessing)
        workflow.workflowPaused.connect(pause)
        self.prepareOutputTreeNodes(
            lastModelDisplayName=lastModelDisplayName,
            clearBeforeRunning=True,
        )
        self.preProcessing(firstModel=None if isFirstModel else lastModelDisplayName)
        workflow.run(firstModelName=None if isFirstModel else lastModelDisplayName)

    def prepareOutputTreeNodes(self, lastModelDisplayName, clearBeforeRunning=False):
        self.iface.mapCanvas().freeze(True)
        rootNode = QgsProject.instance().layerTreeRoot()
        parentGroupName = "DSGTools_QA_Toolbox"
        parentGroupNode = rootNode.findGroup(parentGroupName)
        parentGroupNode = (
            parentGroupNode
            if parentGroupNode
            else rootNode.insertGroup(0, parentGroupName)
        )
        if lastModelDisplayName is None:
            return parentGroupName
        lyrsToRemoveIds = []
        lastModelGroup = parentGroupNode.findGroup(lastModelDisplayName)
        if lastModelGroup is None:
            self.iface.mapCanvas().freeze(False)
            return parentGroupName
        if not clearBeforeRunning:
            self.iface.mapCanvas().freeze(False)
            return parentGroupName
        for lyrGroup in lastModelGroup.findLayers():
            lyr = lyrGroup.layer()
            if isinstance(lyr, QgsVectorLayer):
                lyr.rollBack()
            lyrsToRemoveIds.append(lyr.id())
        for lyrId in lyrsToRemoveIds:
            QgsProject.instance().removeMapLayer(lyrId)
        if len(lastModelGroup.children()) == 0:
            parentGroupNode.removeChildrenGroupWithoutLayers()
        self.iface.mapCanvas().freeze(False)
        return parentGroupName

    @pyqtSlot(bool, name="on_importPushButton_clicked")
    def importWorkflow(self):
        """
        Directly imports an workflow instead of going through the Workflow
        Setup Dialog.
        """
        fd = QFileDialog()
        paths = fd.getOpenFileNames(
            caption=self.tr("Select Workflow files"),
            filter=self.tr("DSGTools Workflow (*.workflow *.json)"),
        )
        paths = paths[0] if isinstance(paths, tuple) else ""
        if not paths:
            return
        for wPath in paths:
            try:
                with open(wPath, "r", encoding="utf-8") as f:
                    wMap = json.load(f)
                workflow = QualityAssuranceWorkflow(wMap)
            except Exception as e:
                self.iface.messageBar().pushMessage(
                    self.tr("DSGTools Q&A Tool Box"),
                    self.tr("workflow '{path}' was not imported: '{msg}'").format(
                        path=wPath, msg=str(e)
                    ),
                    Qgis.Critical,
                    duration=3,
                )
                continue
            self.addWorkflowItem(workflow)

    def addWorkflowItem(self, workflow: QualityAssuranceWorkflow):
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
        self.setWorkflowTooltip(self.comboBox.currentIndex(), workflow.metadata())
        self.saveState()
        QgsMessageLog.logMessage(
            self.tr("Model {model} imported.").format(model=name),
            "DSGTools Plugin",
            Qgis.Info,
        )

    def importWorkflowFromJsonPayload(self, data: List[Dict]):
        for workflow_dict in data:
            try:
                workflow = QualityAssuranceWorkflow(workflow_dict)
            except Exception as e:
                self.iface.messageBar().pushMessage(
                    self.tr("DSGTools Q&A Tool Box"),
                    self.tr("Error importing workflow. Error message: {msg}'").format(
                        msg=str(e)
                    ),
                    Qgis.Critical,
                    duration=3,
                )
                continue
            self.addWorkflowItem(workflow)

    def unload(self):
        """
        Safely clears GUI.
        """
        QgsProject.instance().projectSaved.disconnect(self.saveState)
        self.iface.newProjectCreated.disconnect(self.saveState)
        self.iface.newProjectCreated.disconnect(self.loadState)
        self.iface.projectRead.disconnect(self.loadState)
        self.blockSignals(True)

    def workflowIsFinished(self, modelName=None) -> bool:
        """
        Returns True if all steps executed and finished or finished with
        possible false positive flags.
        """
        modelName = modelName if modelName is not None else self.comboBox.currentText()
        if modelName not in self.workflowStatusDict:
            return False
        return all(
            value in (self.FINISHED, self.IGNORE_FLAGS)
            for _, value in self.workflowStatusDict[modelName].items()
        )

    def allWorkflowsAreFinishedWithoutFlags(self) -> bool:
        for name in self.workflows.keys():
            if name not in self.workflowStatusDict:
                return False
            if not self.workflowIsFinished(modelName=name):
                return False
        return True
