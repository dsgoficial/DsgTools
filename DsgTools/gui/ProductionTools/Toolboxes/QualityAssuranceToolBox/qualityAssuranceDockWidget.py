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
from DsgTools.core.DSGToolsWorkflow.workflowItem import DSGToolsWorkflowItem, ExecutionStatus
from DsgTools.core.DSGToolsWorkflow.workflow import (
    DSGToolsWorkflow,
    dsgtools_workflow_from_dict,
    dsgtools_workflow_from_json,
)


FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "qualityAssuranceDockWidget.ui")
)


class QualityAssuranceDockWidget(QDockWidget, FORM_CLASS):
    # current execution status

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
            ExecutionStatus.INITIAL: self.tr("Not yet run"),
            ExecutionStatus.RUNNING: self.tr("Running..."),
            ExecutionStatus.PAUSED_BEFORE_RUNNING: self.tr(
                "On hold. Check data and resume."
            ),
            ExecutionStatus.CANCELED: self.tr("Canceled"),
            ExecutionStatus.FAILED: self.tr("Failed"),
            ExecutionStatus.FINISHED: self.tr("Completed"),
            ExecutionStatus.FINISHED_WITH_FLAGS: self.tr("Completed (raised flags)"),
            ExecutionStatus.IGNORE_FLAGS: self.tr("Completed (false positive flags)"),
        }
        self.colorForeground = {
            ExecutionStatus.INITIAL: (0, 0, 0),
            ExecutionStatus.RUNNING: (0, 0, 125),
            ExecutionStatus.PAUSED_BEFORE_RUNNING: (187, 201, 25),
            ExecutionStatus.CANCELED: (200, 0, 0),
            ExecutionStatus.FAILED: (169, 18, 28),
            ExecutionStatus.FINISHED: (0, 125, 0),
            ExecutionStatus.FINISHED_WITH_FLAGS: (100, 150, 20),
            ExecutionStatus.IGNORE_FLAGS: (0, 0, 0),
        }
        self.colorBackground = {
            ExecutionStatus.INITIAL: (255, 255, 255, 75),
            ExecutionStatus.RUNNING: (0, 0, 125, 90),
            ExecutionStatus.PAUSED_BEFORE_RUNNING: (187, 201, 25, 20),
            ExecutionStatus.CANCELED: (200, 0, 0, 85),
            ExecutionStatus.FAILED: (169, 18, 28, 85),
            ExecutionStatus.FINISHED: (0, 125, 0, 90),
            ExecutionStatus.FINISHED_WITH_FLAGS: (100, 150, 20, 45),
            ExecutionStatus.IGNORE_FLAGS: (255, 230, 1),
        }
        self.qgisStatusDict = {
            ExecutionStatus.RUNNING: Qgis.Info,
            ExecutionStatus.PAUSED_BEFORE_RUNNING: Qgis.Info,
            ExecutionStatus.CANCELED: Qgis.Warning,
            ExecutionStatus.FAILED: Qgis.Critical,
            ExecutionStatus.FINISHED: Qgis.Info,
            ExecutionStatus.FINISHED_WITH_FLAGS: Qgis.Warning,
            ExecutionStatus.IGNORE_FLAGS: Qgis.Warning,
        }
        self.workflowStatusDict = defaultdict(OrderedDict)
        self.ignoreFlagsMenuDict = defaultdict(dict)
        self.setGuiState()
        self.workflows = dict()
        self.resetComboBox()
        self.resetTable()
        # self.loadState()
        self.prepareProgressBar()
        # make sure workflows are loaded as per project instances
        # QgsProject.instance().projectSaved.connect(self.saveState)
        # self.iface.newProjectCreated.connect(self.saveState)
        # self.iface.newProjectCreated.connect(self.loadState)
        # self.iface.projectRead.connect(self.loadState)

    def generateMenu(self, pos, idx, widget, modelName, workflow):
        workflowName = workflow.displayName
        currentWorkflowItem = workflow.getWorklowItemFromName(modelName)
        if currentWorkflowItem is None:
            return
        currentWorkflowStatus = currentWorkflowItem.getStatus()
        if idx == -1 or currentWorkflowStatus not in [
            ExecutionStatus.FINISHED_WITH_FLAGS,
            ExecutionStatus.IGNORE_FLAGS,
        ]:
            return
        nextWorkflowItem = workflow.getCurrentWorkflowItem()
        if currentWorkflowStatus == ExecutionStatus.IGNORE_FLAGS and (
            nextWorkflowItem is not None
            and nextWorkflowItem.getStatus() != ExecutionStatus.INITIAL
        ):
            return
        if idx not in self.ignoreFlagsMenuDict[workflowName]:
            return

        out = self.ignoreFlagsMenuDict[workflowName][idx].exec_(widget.mapToGlobal(pos))

    def prepareIgnoreFlagMenuDictItem(self, idx, modelName, workflow):
        workflowName = workflow.displayName
        self.ignoreFlagsMenuDict[workflowName][idx] = QMenu(self)
        action = QAction(
            self.tr(f"Ignore false positive flags on model {modelName}"),
            self.ignoreFlagsMenuDict[workflowName][idx],
        )
        func = partial(
            self.setCurrentWorkflowItemToIgnoreFlags, row=idx
        )
        callback = lambda x: func()
        action.setCheckable(True)
        action.triggered.connect(callback)
        self.ignoreFlagsMenuDict[workflowName][idx].addAction(action)
    
    def setCurrentWorkflowItemToIgnoreFlags(self, row):
        workflow: DSGToolsWorkflow = self.currentWorkflow()
        workflow.setIgnoreFlagsStatusOnCurrentStep()
        code = workflow.getCurrentWorkflowItemStatus()
        self.setRowStatus(row, code)
        self.tableWidget.cellWidget(row, 1).setText(self.statusMap[code])


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

    @pyqtSlot(bool, name="on_cancelPushButton_clicked")
    def cancelWorkflow(self):
        """
        Cancels current workflow's execution.
        """
        self.currentWorkflow().cancelCurrentRun()
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
        currentWorkflow = self.currentWorkflow()
        if currentWorkflow is not None:
            currentWorkflow.feedback.progressChanged.connect(self.setProgress)

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
                f"Workflow author: {metadata.author}\n"
                f"Workflow version: {metadata.version}\n"
                f"Last modification: {metadata.lastModified}"
            ),
            Qt.ToolTipRole,
        )

    def setGuiState(self, isActive=False):
        """
        Sets GUI to idle (not running a Workflow) or active state (running it).
        :param isActive: (bool) whether GUI is running a Workflow.
        """
        self.cancelPushButton.setEnabled(isActive)
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
        name = workflow.displayName
        idx = self.comboBox.findText(name)
        if idx < 0:
            self.comboBox.addItem(name)
            self.comboBox.setCurrentText(name)
            self.workflows[name] = workflow
            self.setCurrentWorkflow()
        else:
            self.comboBox.setCurrentIndex(idx)
            # what should we do? check version/last modified? replace model?
        self.setWorkflowTooltip(self.comboBox.currentIndex(), workflow.metadata)
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
        previousName = workflow.displayName
        if workflow is None:
            return
        dlg = WorkflowSetupDialog(self)
        dlg.show()
        temp = os.path.join(
            os.path.dirname(__file__), "temp_workflow_{0}.workflow".format(hash(time()))
        )
        with open(temp, "w+", encoding="utf-8") as f:
            json.dump(workflow.as_dict(), f)
        dlg.importWorkflow(temp)
        os.remove(temp)
        if dlg.exec_() != 1:
            return
        # block "if modifications are confirmed by user"
        newWorkflow = dlg.currentWorkflow()
        newName = newWorkflow.displayName
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
        self.setWorkflowTooltip(self.comboBox.currentIndex(), newWorkflow.metadata)
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
        return self.workflows.get(name, None)
    
    def currentWorkflowFinishedExecutionMessage(self):
        currentWorkflow = self.currentWorkflow()
        if currentWorkflow is None:
            return
        self.iface.messageBar().pushMessage(
            self.tr("DSGTools Q&A Tool Box"),
            self.tr(f"Workflow {currentWorkflow.displayName} execution has finished."),
            Qgis.Info, duration=3
        )
        self.progressBar.setValue(100)
        self.resumePushButton.setEnabled(False)

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

    def setModelStatus(self, row, workflowItem):
        """
        Sets model execution status to its cell.
        :param row: (int) model's row on GUI.
        :param code: (int) code to current status (check this class enumerator).
        :param modelName: (str) para to notify user of status change. This
                          should be passed only through dynamic changes in order
                          to avoid polluting QGIS main window.
        """
        code = workflowItem.getStatus()
        status = self.statusMap[code]
        self.setRowStatus(row, code)
        self.tableWidget.cellWidget(row, 1).setText(status)
        self.setGuiState(code == ExecutionStatus.RUNNING)
        if code in [ExecutionStatus.FAILED, ExecutionStatus.FINISHED_WITH_FLAGS, ExecutionStatus.IGNORE_FLAGS]:
            # advise user a model status has changed only if it came from a
            # signal call
            self.iface.messageBar().pushMessage(
                self.tr("DSGTools Q&A Toolbox"),
                self.tr(
                    f"model {workflowItem.displayName} status changed to {status}."
                ),
                self.qgisStatusDict[code],
                duration=3,
            )
        elif code != ExecutionStatus.INITIAL:
            QgsMessageLog.logMessage(
                self.tr(
                    f"Model {workflowItem.displayName} status changed to {status}."
                ),
                "DSGTools Plugin",
                self.qgisStatusDict[code],
            )

    def setRowStatus(self, row, code):
        colorForeground = self.colorForeground[code]
        colorBackground = self.colorBackground[code]
        if code == ExecutionStatus.INITIAL:
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
        self.tableWidget.setRowCount(len(workflow.workflowItemList))
        for row, workflowItem in enumerate(workflow.workflowItemList):
            tooltip = self.tr(
                f"Model name: {workflowItem.displayName}\n{workflowItem.getDescription()}"
            )
            if workflowItem.flagsCanHaveFalsePositiveResults():
                self.prepareIgnoreFlagMenuDictItem(
                    row, workflowItem.displayName, workflow
                )
            nameWidget = self.customLineWidget(workflowItem.displayName, tooltip)
            nameWidget.setContextMenuPolicy(Qt.CustomContextMenu)
            nameWidget.customContextMenuRequested.connect(
                partial(
                    self.generateMenu,
                    idx=row,
                    widget=nameWidget,
                    modelName=workflowItem.displayName,
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
                    modelName=workflowItem.displayName,
                    workflow=workflow,
                )
            )
            self.tableWidget.setCellWidget(row, 1, statusWidget)
            code = workflowItem.getStatus()
            self.setModelStatus(row, workflowItem)
            pb = self.progressWidget(
                value=100
                if code
                in [
                    ExecutionStatus.FINISHED,
                    ExecutionStatus.FINISHED_WITH_FLAGS,
                    ExecutionStatus.IGNORE_FLAGS,
                ]
                else 0
            )
            pb.setContextMenuPolicy(Qt.CustomContextMenu)
            workflowItem.feedback.progressChanged.connect(partial(self.intWrapper, row))
            self.tableWidget.setCellWidget(row, 2, pb)
        workflow.currentWorkflowItemStatusChanged.connect(self.setModelStatus)
        workflow.currentWorkflowExecutionFinished.connect(self.currentWorkflowFinishedExecutionMessage)
        # workflow.currentTaskChanged.connect(self.setupProgressBar)
    
    def intWrapper(self, idx, v):
        pb = self.tableWidget.cellWidget(idx, 2)
        pb.setValue(int(v))

    def setupProgressBar(self, idx, currentTask):
        currentTask.progressChanged.connect(
            lambda x: self.tableWidget.cellWidget(idx, 2).setValue(x)
        )

    def saveState(self):
        """
        Makes sure all added workflows are stored to active instance of
        QgsProject, making it "loadable" along with saved QGIS projects.
        """
        # workflow objects cannot be serialized, so they must be passed as dict
        workflows = {w.displayName: w.as_dict() for w in self.workflows.values()}
        workflowStatusDict = {
            w.displayName: w.getStatusDict() for w in self.workflows.values()
        }

        QgsExpressionContextUtils.setProjectVariable(
            QgsProject.instance(),
            "dsgtools_qatoolbox_state",
            json.dumps(
                {
                    "workflows": workflows,
                    "current_workflow": self.comboBox.currentIndex(),
                    "show_buttons": self._showButtons,
                    "workflow_status_dict": workflowStatusDict,
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
            self.workflows[name] = dsgtools_workflow_from_dict(workflowMap)
            self.comboBox.addItem(name)
            self.setWorkflowTooltip(idx + 1, self.workflows[name].metadata)
            self.workflows[name].setStatusDict(workflow_status_dict[name])
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
        sender = self.sender()
        if sender.objectName() == "runPushButton":
            self.resumePushButton.setEnabled(True)
        resumeFromStart = sender is None or sender.objectName() == "runPushButton"
        if resumeFromStart:
            workflow.resetWorkflowItems()
            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.cellWidget(row, 2).setValue(0)
        workflow.run(resumeFromStart=resumeFromStart)

    @pyqtSlot(bool, name="on_importPushButton_clicked")
    def importWorkflow(self) -> None:
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
                workflow = dsgtools_workflow_from_json(wPath)
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

    def addWorkflowItem(self, workflow: DSGToolsWorkflow) -> None:
        name = workflow.displayName
        idx = self.comboBox.findText(name)
        if idx < 0:
            self.comboBox.addItem(name)
            self.comboBox.setCurrentText(name)
            self.workflows[name] = workflow
            self.setCurrentWorkflow()
        else:
            self.comboBox.setCurrentIndex(idx)
            # what should we do? check version/last modified? replace model?
        self.setWorkflowTooltip(self.comboBox.currentIndex(), workflow.metadata)
        self.saveState()
        QgsMessageLog.logMessage(
            self.tr("Model {model} imported.").format(model=name),
            "DSGTools Plugin",
            Qgis.Info,
        )

    def importWorkflowFromJsonPayload(self, data: List[Dict]) -> None:
        for workflow_dict in data:
            try:
                workflow = dsgtools_workflow_from_dict(workflow_dict)
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
            value in (ExecutionStatus.FINISHED, ExecutionStatus.IGNORE_FLAGS)
            for _, value in self.workflowStatusDict[modelName].items()
        )

    def allWorkflowsAreFinishedWithoutFlags(self) -> bool:
        for name in self.workflows.keys():
            if name not in self.workflowStatusDict:
                return False
            if not self.workflowIsFinished(modelName=name):
                return False
        return True
