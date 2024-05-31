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

from functools import partial
import os, json
from pathlib import Path
from time import time
from datetime import datetime

from DsgTools.core.DSGToolsWorkflow.workflowItem import DSGToolsWorkflowItem, ModelSource
from DsgTools.gui.CustomWidgets.SelectionWidgets.customCheckableComboBox import CustomCheckableComboBox
from DsgTools.gui.CustomWidgets.SelectionWidgets.importExportFileWidget import ImportExportFileWidget
from qgis.PyQt import uic, QtCore, QtWidgets
from qgis.core import Qgis
from qgis.gui import QgsMessageBar, QgsCheckableComboBox
from qgis.PyQt.QtCore import QSize, QCoreApplication, pyqtSlot, Qt
from qgis.PyQt.QtWidgets import (
    QDialog,
    QComboBox,
    QCheckBox,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QTableWidgetItem,
)
from processing.modeler.ModelerUtils import ModelerUtils

from DsgTools.gui.CustomWidgets.SelectionWidgets.selectFileWidget import (
    SelectFileWidget,
)
from DsgTools.core.DSGToolsWorkflow.workflow import DSGToolsWorkflow, WorkflowMetadata, dsgtools_workflow_from_dict, dsgtools_workflow_from_json

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), "workflowSetupDialog.ui")
)


class WorkflowSetupDialog(QDialog, FORM_CLASS):
    __qgisModelPath__ = ModelerUtils.modelsFolders()[0]
    (
        ON_FLAGS_HALT,
        ON_FLAGS_WARN,
        ON_FLAGS_IGNORE,
    ) = range(3)
    onFlagsDisplayNameMap = {
        ON_FLAGS_HALT: QCoreApplication.translate("WorkflowSetupDialog", "Halt"),
        ON_FLAGS_WARN: QCoreApplication.translate("WorkflowSetupDialog", "Warn"),
        ON_FLAGS_IGNORE: QCoreApplication.translate("WorkflowSetupDialog", "Ignore"),
    }
    onFlagsValueMap = {
        ON_FLAGS_HALT: "halt",
        ON_FLAGS_WARN: "warn",
        ON_FLAGS_IGNORE: "ignore",
    }
    (
        MODEL_NAME_HEADER,
        MODEL_SOURCE_HEADER,
        FLAG_KEYS_HEADER,
        ON_FLAGS_HEADER,
        FLAG_CAN_BE_FALSE_POSITIVE_HEADER,
        PAUSE_AFTER_EXECUTION_HEADER,
        LOAD_OUTPUTS_THAT_ARE_NOT_FLAG_HEADER,
    ) = range(7)

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
        self.orderedTableWidget.setHeaders(
            {
                self.MODEL_NAME_HEADER: {
                    "header": self.tr("Model name"),
                    "type": "widget",
                    "widget": self.modelNameWidget,
                    "setter": "setText",
                    "getter": "text",
                },
                self.MODEL_SOURCE_HEADER: {
                    "header": self.tr("Model source"),
                    "type": "widget",
                    "widget": self.modelWidget,
                    "setter": "setFile",
                    "getter": "getFile",
                },
                self.FLAG_KEYS_HEADER: {
                    "header": self.tr("Flag keys"),
                    "type": "widget",
                    "widget": self.loadFlagLayers,
                    "setter": "setData",
                    "getter": "checkedItems",
                },
                self.ON_FLAGS_HEADER: {
                    "header": self.tr("On flags"),
                    "type": "widget",
                    "widget": self.onFlagsWidget,
                    "setter": "setCurrentIndex",
                    "getter": "currentIndex",
                },
                self.FLAG_CAN_BE_FALSE_POSITIVE_HEADER: {
                    "header": self.tr("Flags can be false positive"),
                    "type": "widget",
                    "widget": self.falsePositiveFlagsWidget,
                    "setter": "setChecked",
                    "getter": "isChecked",
                },
                self.PAUSE_AFTER_EXECUTION_HEADER: {
                    "header": self.tr("Pause after execution"),
                    "type": "widget",
                    "widget": self.pauseAfterExecutionWidget,
                    "setter": "setChecked",
                    "getter": "isChecked",
                },
                self.LOAD_OUTPUTS_THAT_ARE_NOT_FLAG_HEADER: {
                    "header": self.tr("Load output layers that are not flags"),
                    "type": "widget",
                    "widget": self.loadOutputWidget,
                    "setter": "setChecked",
                    "getter": "isChecked",
                },
            }
        )
        self.orderedTableWidget.setHeaderDoubleClickBehaviour("replicate")
        self.orderedTableWidget.horizontalHeader().setStretchLastSection(True)
        self.orderedTableWidget.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.orderedTableWidget.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.orderedTableWidget.tableWidget.horizontalHeader().setMinimumSectionSize(100)
        self.orderedTableWidget.tableWidget.horizontalHeader().resizeSection(self.MODEL_NAME_HEADER, 200)
        self.orderedTableWidget.tableWidget.horizontalHeader().resizeSection(self.MODEL_SOURCE_HEADER, 250)
        self.orderedTableWidget.tableWidget.horizontalHeader().resizeSection(self.FLAG_KEYS_HEADER, 200)
        self.orderedTableWidget.tableWidget.horizontalHeader().resizeSection(self.ON_FLAGS_HEADER, 100)
        self.promptToAll = None
        self.orderedTableWidget.rowAdded.connect(self.postAddRowStandard)

    def postAddRowStandard(self, row):
        """
        Sets up widgets to work as expected right after they are added to GUI.
        :param row: (int) row to have its widgets setup.
        """
        # in standard GUI, the layer selectors are QgsMapLayerComboBox, and its
        # layer changed signal should be connected to the filter expression
        # widget setup
        importExportFileWidget = self.orderedTableWidget.itemAt(row, self.MODEL_SOURCE_HEADER)
        importExportFileWidget.fileSelected.connect(
            partial(self._getModelOutputs, row)
        )
    
    def _getModelOutputs(self, row, fileName, fileContent):
        currentModelSource = ModelSource(
            type="xml",
            data=fileContent
        )
        currentModel = currentModelSource.modelFromXml()
        outputs = [
            outputDef.name().split(":")[-1] for outputDef in currentModel.outputDefinitions()
        ]
        currentCheckableCombobBox = self.orderedTableWidget.itemAt(row, self.FLAG_KEYS_HEADER)
        currentCheckableCombobBox.clear()
        currentCheckableCombobBox.setData(outputs)

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
                40,  # this felt nicer than the original height (30)
            )
        )

    def confirmAction(self, msg, showCancel=True, addPromptToAll=False):
        """
        Raises a message box for confirmation before executing an action.
        :param msg: (str) message to be exposed.
        :param showCancel: (bool) whether Cancel button should be exposed.
        :return: (bool) whether action was confirmed.
        """
        if not addPromptToAll:  # comportamento antigo
            if showCancel:
                return (
                    QMessageBox.question(
                        self,
                        self.tr("Confirm Action"),
                        msg,
                        QMessageBox.Ok | QMessageBox.Cancel,
                    )
                    == QMessageBox.Ok
                )
            else:
                return (
                    QMessageBox.question(
                        self, self.tr("Confirm Action"), msg, QMessageBox.Ok
                    )
                    == QMessageBox.Ok
                )
        # prompt to all == true daqui para frente
        if self.promptToAll is not None:
            return self.promptToAll
        # prompt to all == true daqui para frente e self.promptToAll is None
        # (o usuario nao mandou algum sim ou nao para todos)
        buttonPromptList = QMessageBox.Ok | QMessageBox.YesAll | QMessageBox.NoAll
        if showCancel:
            buttonPromptList = buttonPromptList | QMessageBox.Cancel
        answer = QMessageBox.question(
            self, self.tr("Confirm Action"), msg, buttonPromptList
        )
        if answer in [QMessageBox.YesAll, QMessageBox.NoAll]:
            self.promptToAll = answer == QMessageBox.YesAll
            return self.promptToAll
        return answer == QMessageBox.Ok

    def clear(self):
        """
        Clears all input data from GUI.
        """
        self.authorLineEdit.setText("")
        self.nameLineEdit.setText("")
        self.versionLineEdit.setText("")
        self.orderedTableWidget.clear()
        self.promptToAll = None

    def modelNameWidget(self, name=None):
        """
        Gets a new instance of model name's setter widget.
        :param name: (str) model name to be filled.
        :return: (QLineEdit) widget for model's name setting.
        """
        # no need to pass parenthood as it will be set to the table when added
        # to a cell
        le = QLineEdit()
        # setPlace"h"older, with a lower case "h"...
        le.setPlaceholderText(self.tr("Set a name for the model..."))
        if name is not None:
            le.setText(name)
        le.setFrame(False)
        le.textChanged.connect(lambda x: le.setToolTip(x))
        return le

    def modelWidget(self, filepath=None):
        """
        Gets a new instance of model settter's widget.
        :parma filepath: (str) path to a model.
        :return: (SelectFileWidget) DSGTools custom file selection widget.
        """
        widget = ImportExportFileWidget()
        widget.selectFilePushButton.setMaximumWidth(32)
        widget.lineEdit.setPlaceholderText(self.tr("Select a model..."))
        widget.lineEdit.setFrame(False)
        widget.setCaption(self.tr("Select a QGIS Processing model file"))
        widget.setFilter(self.tr("Select a QGIS Processing model (*.model *.model3)"))
        # defining setter and getter methods for composed widgets into OTW
        widget.fileExported.connect(lambda x: self.pushMessage(x))
        return widget

    def onFlagsWidget(self, option=None):
        """
        Gets a new instance for the widget that sets model's behaviour when
        flags are raised.
        :param option: (str) on flags raised behaviour (non translatable text).
        :return: (QComboBox) model's behaviour selection widget.
        """
        combo = QComboBox()
        combo.addItems(
            [
                self.onFlagsDisplayNameMap[self.ON_FLAGS_HALT],
                self.onFlagsDisplayNameMap[self.ON_FLAGS_WARN],
                self.onFlagsDisplayNameMap[self.ON_FLAGS_IGNORE],
            ]
        )
        if option is not None:
            optIdx = None
            for idx, txt in self.onFlagsValueMap.items():
                if option == txt:
                    optIdx = idx
                    break
            optIdx = optIdx if optIdx is not None else 0
            combo.setCurrentIndex(optIdx)
        return combo

    def falsePositiveFlagsWidget(self, option=None):
        cb = QCheckBox()
        cb.setChecked(False)
        cb.setStyleSheet("margin-left:50%;margin-right:50%;")
        if option is not None:
            cb.setChecked(option)
        return cb

    def pauseAfterExecutionWidget(self, option=None):
        cb = QCheckBox()
        cb.setChecked(False)
        cb.setStyleSheet("margin-left:50%;margin-right:50%;")
        if option is not None:
            cb.setChecked(option)
        return cb

    def loadOutputWidget(self, option=None):
        """
        Gets a new instance for the widget that sets output layer loading
        definitions.
        :param option: (bool) if output should be loaded.
        :return: (QWidget) widget for output layer loading behaviour
                 definition.
        """
        cb = QCheckBox()
        cb.setStyleSheet("margin-left:50%;margin-right:50%;")
        if option is not None:
            cb.setChecked(option)
        return cb

    def loadFlagLayers(self):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        widget = CustomCheckableComboBox()
        widget.setSizePolicy(sizePolicy)
        widget.setMinimumSize(QtCore.QSize(100, 25))
        return widget

    def now(self):
        """
        Gets time and date from the system. Format: "dd/mm/yyyy HH:MM:SS".
        :return: (str) current's date and time
        """
        paddle = lambda n: str(n) if n > 9 else "0{0}".format(n)
        now = datetime.now()
        return "{day}/{month}/{year} {hour}:{minute}:{second}".format(
            year=now.year,
            month=paddle(now.month),
            day=paddle(now.day),
            hour=paddle(now.hour),
            minute=paddle(now.minute),
            second=paddle(now.second),
        )

    def workflowName(self):
        """
        Reads filled workflow name from GUI.
        :return: (str) workflow's name.
        """
        return self.nameLineEdit.text().strip()

    def setWorkflowName(self, name):
        """
        Sets workflow name to GUI.
        :param name: (str) workflow's name.
        """
        self.nameLineEdit.setText(name)

    def author(self):
        """
        Reads filled workflow name from GUI.
        :return: (str) workflow's author.
        """
        return self.authorLineEdit.text().strip()

    def setWorkflowAuthor(self, author):
        """
        Sets workflow author name to GUI.
        :param author: (str) workflow's author name.
        """
        self.authorLineEdit.setText(author)

    def version(self):
        """
        Reads filled workflow name from GUI.
        :return: (str) workflow's version.
        """
        return self.versionLineEdit.text().strip()

    def setWorkflowVersion(self, version):
        """
        Sets workflow version to GUI.
        :param version: (str) workflow's version.
        """
        self.versionLineEdit.setText(version)

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
        fileName, xml = contents[self.MODEL_SOURCE_HEADER]
        onFlagsIdx = contents[self.ON_FLAGS_HEADER]
        name = contents[self.MODEL_NAME_HEADER].strip()
        loadOutput = contents[self.LOAD_OUTPUTS_THAT_ARE_NOT_FLAG_HEADER]
        modelCanHaveFalsePositiveFlags = contents[
            self.FLAG_CAN_BE_FALSE_POSITIVE_HEADER
        ]
        flagLayerNames = contents[self.FLAG_KEYS_HEADER]
        pauseAfterExecution = contents[self.PAUSE_AFTER_EXECUTION_HEADER]
        return {
            "displayName": name,
            "flags": {
                "onFlagsRaised": self.onFlagsValueMap[onFlagsIdx],
                "modelCanHaveFalsePositiveFlags": modelCanHaveFalsePositiveFlags,
                "loadOutput": loadOutput,
                "flagLayerNames": flagLayerNames,
            },
            "pauseAfterExecution": pauseAfterExecution,
            "source": {
                "type": "xml",
                "data": xml,
            },
            "metadata": {
                "originalName": fileName,
            },
        }

    def setModelToRow(self, row: int, workflowItem: DSGToolsWorkflowItem):
        """
        Reads model's parameters from model parameters default map.
        :param row: (int) row to have its widgets filled with model's
                    parameters.
        :param model: (DsgToolsProcessingModel) model object.
        """
        # all model files handled by this tool are read/written on QGIS model dir
        data = workflowItem.source.data
        meta = workflowItem.metadata
        originalName = Path(meta.originalName).name
        self.orderedTableWidget.addRow(
            contents={
                self.MODEL_NAME_HEADER: workflowItem.displayName,
                self.MODEL_SOURCE_HEADER: {"fileName":originalName, "fileContent":data},
                self.ON_FLAGS_HEADER: {
                    "halt": self.ON_FLAGS_HALT,
                    "warn": self.ON_FLAGS_WARN,
                    "ignore": self.ON_FLAGS_IGNORE,
                }[workflowItem.flags.onFlagsRaised],
                self.FLAG_CAN_BE_FALSE_POSITIVE_HEADER: workflowItem.flags.modelCanHaveFalsePositiveFlags,
                self.LOAD_OUTPUTS_THAT_ARE_NOT_FLAG_HEADER: workflowItem.flags.loadOutput,
                self.FLAG_KEYS_HEADER: {
                    "items": workflowItem.getAllOutputNamesFromModel(),
                    "checkedItems": ",".join(
                        map(lambda x: str(x).strip(), workflowItem.flags.flagLayerNames)
                    )
                },
                self.PAUSE_AFTER_EXECUTION_HEADER: workflowItem.pauseAfterExecution,
            }
        )
        return True

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

    def workflowItems(self):
        """
        Reads all table contents and sets it as a DsgToolsProcessingAlgorithm's
        set of parameters.
        :return: (dict) map to each model's set of parameters.
        """
        return [
            self.readRow(row) for row in range(self.modelCount())
        ]

    def validateModels(self):
        """
        Check if each row on table has a valid input.
        :return: (str) invalidation reason.
        """
        for row in range(self.modelCount()):
            msg = self.validateRowContents(self.readRow(row))
            if msg:
                return "Row {row}: '{error}'".format(row=row + 1, error=msg)
        if len(self.workflowItems()) != self.modelCount():
            return self.tr("Check if no model name is repeated.")
        return ""

    def workflowParameterMap(self):
        """
        Generates a Workflow map from input data.
        """
        return {
            "displayName": self.workflowName(),
            "workflowItemList": self.workflowItems(),
            "metadata": {
                "author": self.author(),
                "version": self.version(),
                "lastModified": self.now(),
            },
        }

    def currentWorkflow(self):
        """
        Returns current workflow object as read from GUI.
        :return: (QualityAssuranceWorkflow) current workflow object.
        """
        try:
            return dsgtools_workflow_from_dict(self.workflowParameterMap())
        except:
            return None

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

    def exportWorkflow(self, filepath: str) -> bool:
        """
        Exports current data to a JSON file.
        :param filepath: (str) output file directory.
        """
        workflow = dsgtools_workflow_from_dict(self.workflowParameterMap())
        return workflow.export(filepath=filepath)
    
    def pushMessage(self, message):
        self.messageBar.pushMessage(
            self.tr("Info"), message, level=Qgis.Warning, duration=5
        )

    @pyqtSlot(bool, name="on_exportPushButton_clicked")
    def export(self):
        """
        Exports current input data as a workflow JSON, IF input is valid.
        :return: (bool) operation success.
        """
        msg = self.validate()
        if msg != "":
            self.messageBar.pushMessage(
                self.tr("Invalid workflow"), msg, level=Qgis.Warning, duration=5
            )
            return False
        fd = QFileDialog()
        filename = fd.getSaveFileName(
            caption=self.tr("Export DSGTools Workflow"),
            filter=self.tr("DSGTools Workflow (*.workflow)"),
        )
        filename = filename[0] if isinstance(filename, tuple) else ""
        if filename == "":
            return False
        filename = (
            filename
            if filename.lower().endswith(".workflow")
            else "{0}.workflow".format(filename)
        )
        try:
            result = self.exportWorkflow(filename)
        except Exception as e:
            self.messageBar.pushMessage(
                self.tr("Invalid workflow"),
                self.tr("Unable to export workflow to '{fp}' ({error}).").format(
                    fp=filename, error=str(e)
                ),
                level=Qgis.Warning,
                duration=5,
            )
            return False
        msg = (
            self.tr("Workflow exported to {fp}")
            if result
            else self.tr("Unable to export workflow to '{fp}'")
        ).format(fp=filename)
        lvl = Qgis.Success if result else Qgis.Warning
        self.messageBar.pushMessage(
            self.tr("Workflow exporting"), msg, level=lvl, duration=5
        )
        return result

    def importWorkflow(self, filepath: str) -> None:
        """
        Sets workflow contents from an imported DSGTools Workflow dump file.
        :param filepath: (str) workflow file to be imported.
        """
        workflow = dsgtools_workflow_from_json(filepath)
        self.clear()
        self.setWorkflowAuthor(workflow.metadata.author)
        self.setWorkflowVersion(workflow.metadata.version)
        self.setWorkflowName(workflow.displayName)
        for row, workflowItem in enumerate(workflow.workflowItemList):
            self.setModelToRow(row, workflowItem)

    @pyqtSlot(bool, name="on_importPushButton_clicked")
    def import_(self) -> None:
        """
        Request a file for Workflow importation and sets it to GUI.
        :return: (bool) operation status.
        """
        fd = QFileDialog()
        filename = fd.getOpenFileName(
            caption=self.tr("Select a Workflow file"),
            filter=self.tr("DSGTools Workflow (*.workflow *.json)"),
        )
        filename = filename[0] if isinstance(filename, tuple) else ""
        if not filename:
            return False
        try:
            self.importWorkflow(filename)
        except Exception as e:
            self.messageBar.pushMessage(
                self.tr("Invalid workflow"),
                self.tr("Unable to export workflow to '{fp}' ({error}).").format(
                    fp=filename, error=str(e)
                ),
                level=Qgis.Critical,
                duration=5,
            )
            return False
        self.messageBar.pushMessage(
            self.tr("Success"),
            self.tr("Workflow '{fp}' imported!").format(fp=filename),
            level=Qgis.Info,
            duration=5,
        )
        return True

    @pyqtSlot(bool, name="on_okPushButton_clicked")
    def ok(self) -> None:
        """
        Closes dialog and checks if current workflow is valid.
        """
        msg = self.validate()
        if msg == "" and self.currentWorkflow():
            self.done(1)
        else:
            self.messageBar.pushMessage(
                self.tr("Invalid workflow"),
                self.validate(),
                level=Qgis.Warning,
                duration=5,
            )

    @pyqtSlot(bool, name="on_cancelPushButton_clicked")
    def cancel(self) -> None:
        """
        Restores GUI to last state and closes it.
        """
        self.done(0)
