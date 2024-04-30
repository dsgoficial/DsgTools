# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-03-04
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from dataclasses import asdict, dataclass, field
import json
from typing import Any, Dict, List

from qgis.core import (
    QgsApplication,
    QgsProcessingFeedback,
    QgsProcessingMultiStepFeedback,
    QgsTask,
)
from qgis.PyQt.QtCore import pyqtSignal, QObject

from DsgTools.core.DSGToolsWorkflow.workflowItem import (
    DSGToolsWorkflowItem,
    ExecutionStatus,
    load_from_json,
)


@dataclass
class WorkflowMetadata:
    """Dataclass representing metadata for a workflow.

    Attributes:
        author (str): The author of the workflow.
        version (str): The version of the workflow.
        lastModified (str): The last modification date of the workflow.
    """

    author: str
    version: str
    lastModified: str


@dataclass
class DSGToolsWorkflow(QObject):
    """Class representing a workflow in DSGTools.

    Attributes:
        displayName (str): The display name of the workflow.
        metadata (WorkflowMetadata): Metadata associated with the workflow.
        workflowItemList (List[DSGToolsWorkflowItem]): List of workflow items.

    Signals:
        currentWorkflowItemStatusChanged: Emitted when the status of the current workflow item changes.
        workflowHasBeenReset: Emitted when the workflow has been reset.
        workflowPaused: Emitted when the workflow is paused.
        currentTaskChanged: Emitted when the current task changes.
    """

    displayName: str
    metadata: WorkflowMetadata
    workflowItemList: List[DSGToolsWorkflowItem]

    def __post_init__(self):
        """Initialize post dataclass creation."""
        super().__init__()
        self.currentStepIndex = 0
        self.feedback = QgsProcessingFeedback()
        self.multiStepFeedback = QgsProcessingMultiStepFeedback(
            len(self.workflowItemList), self.feedback
        )
        self.currentWorkflowItemStatusChanged = pyqtSignal(int, DSGToolsWorkflowItem)
        self.workflowHasBeenReset = pyqtSignal()
        self.workflowPaused = pyqtSignal()
        self.currentTaskChanged = pyqtSignal(int, QgsTask)

    def as_dict(self) -> Dict[str, Any]:
        """Convert the workflow object to a dictionary."""
        return {k: v for k, v in asdict(self).items()}

    def getCurrentWorkflowStepIndex(self) -> int:
        """Get the index of the current workflow step.

        Returns:
            int: The index of the current workflow step.
        """
        return self.currentStepIndex

    def getNextWorkflowStep(self) -> int:
        """Get the index of the next workflow step.

        Returns:
            int: The index of the next workflow step, or None if at the end of the workflow.
        """
        nextIndex = self.currentStepIndex + 1
        return nextIndex if nextIndex <= len(self.workflowItemList) - 1 else None

    def getCurrentWorkflowItem(self) -> DSGToolsWorkflowItem:
        """Get the current workflow item.

        Returns:
            DSGToolsWorkflowItem: The current workflow item.
        """
        idx = self.getCurrentWorkflowStepIndex()
        return self.workflowItemList[idx]

    def setCurrentWorkflowItem(self, idx) -> None:
        """Set the current workflow item by index.

        Args:
            idx (int): The index of the workflow item to set as current.
        """
        if idx < 0 or idx >= len(self.workflowItemList):
            return
        self.currentStepIndex = idx

    def connectSignals(self) -> None:
        """Connect signals for each workflow item."""
        for workflowItem in self.workflowItemList:
            workflowItem.workflowItemExecutionFinished.connect(
                self.postProcessWorkflowItem
            )

    def resetWorkflowItems(self):
        """Reset all workflow items."""
        for workflowItem in self.workflowItemList:
            workflowItem.resetItem()

    def prepareTask(self) -> QgsTask:
        """Prepare the current task based on the current workflow item.

        Returns:
            QgsTask: The prepared task.
        """
        currentWorkflowItem: DSGToolsWorkflowItem = self.getCurrentWorkflowItem()
        return currentWorkflowItem.getTask(self.feedback)

    def postProcessWorkflowItem(self, workflowItem: DSGToolsWorkflowItem):
        """Handle post-processing for a completed workflow item.

        Args:
            workflowItem (DSGToolsWorkflowItem): The completed workflow item.
        """
        self.currentTask = None
        self.currentWorkflowItemStatusChanged.emit(self.currentStepIndex, workflowItem)
        if workflowItem.getStatus() in [
            ExecutionStatus.FAILED,
            ExecutionStatus.FINISHED_WITH_FLAGS,
            ExecutionStatus.CANCELED,
        ]:
            self.multiStepFeedback.setCurrentStep(self.currentStepIndex)
            return
        self.currentStepIndex = self.getNextWorkflowStep()
        if self.currentStepIndex is None:
            self.multiStepFeedback.setProgress(100)
            return
        if workflowItem.pauseAfterExecution:
            currentWorkflowItem = self.getCurrentWorkflowItem()
            currentWorkflowItem.pauseBeforeRunning()
            self.currentWorkflowItemStatusChanged.emit(
                self.currentStepIndex, currentWorkflowItem
            )
            return
        self.run(resumeFromStart=False)

    def run(self, resumeFromStart=True):
        """Run the workflow.

        Args:
            resumeFromStart (bool): Whether to resume the workflow from the start.

        """
        if resumeFromStart:
            self.resetWorkflowItems()
            self.setCurrentWorkflowItem(0)
            self.workflowHasBeenReset.emit()
        currentWorkflowItem = self.getCurrentWorkflowItem()
        if currentWorkflowItem.getStatus() == ExecutionStatus.IGNORE_FLAGS:
            self.currentStepIndex = self.getNextWorkflowStep()
            if self.currentStepIndex is None:
                self.multiStepFeedback.setProgress(100)
                return
            currentWorkflowItem = self.getCurrentWorkflowItem()
        currentTask: QgsTask = self.prepareTask()
        currentWorkflowItem.changeCurrentStatus(
            status=ExecutionStatus.RUNNING,
            executionMessage=self.tr("Execution started"),
        )
        self.multiStepFeedback.setCurrentStep(self.currentStepIndex)
        self.currentWorkflowItemStatusChanged.emit(
            self.currentStepIndex, currentWorkflowItem
        )
        self.currentTaskChanged.emit(self.currentStepIndex, currentTask)
        QgsApplication.taskManager().addTask(currentTask)

    def setIgnoreFlagsStatusOnCurrentStep(self):
        """Set the status to ignore flags on the current workflow step."""
        currentWorkflowItem = self.getCurrentWorkflowItem()
        currentWorkflowItem.setCurrentStateToIgnoreFlags()

    def cancelCurrentRun(self):
        """Cancel the current run of the workflow."""
        currentWorkflowItem = self.getCurrentWorkflowItem()
        currentWorkflowItem.cancelCurrentTask()
        self.multiStepFeedback.setCurrentStep(self.currentStepIndex)
        self.currentWorkflowItemStatusChanged.emit(
            self.currentStepIndex, currentWorkflowItem
        )

    def pauseCurrentRun(self):
        """Pause the current run of the workflow."""
        currentWorkflowItem = self.getCurrentWorkflowItem()
        currentWorkflowItem.pauseCurrentTask()
        self.currentWorkflowItemStatusChanged.emit(
            self.currentStepIndex, currentWorkflowItem
        )

    def resumeCurrentRun(self):
        """Resume the current run of the workflow."""
        currentWorkflowItem = self.getCurrentWorkflowItem()
        currentWorkflowItem.pauseCurrentTask()
        self.currentWorkflowItemStatusChanged.emit(
            self.currentStepIndex, currentWorkflowItem
        )

def dsgtools_workflow_from_json(json_file):
    """Create a DSGToolsWorkflow object from a JSON file."""
    with open(json_file, 'r') as f:
        data = json.load(f)
    return dsgtools_workflow_from_dict(data)

def dsgtools_workflow_from_dict(data):
    # Extract data for initialization
    display_name = data.get('displayName')
    metadata = WorkflowMetadata(
        author=data['metadata'].get('author'),
        version=data['metadata'].get('version'),
        lastModified=data['metadata'].get('lastModified')
    )

    if display_name is None or None in (metadata.author, metadata.version, metadata.lastModified):
        raise ValueError("Display name, author, version, and last modified are required fields.")

    workflow_item_list = [
        load_from_json(item_data)
        for item_data in data.get('workflowItemList', [])
    ]

    if not workflow_item_list:
        raise ValueError("Workflow item list cannot be empty.")

    # Create and return DSGToolsWorkflow object
    return DSGToolsWorkflow(displayName=display_name, metadata=metadata, workflowItemList=workflow_item_list)