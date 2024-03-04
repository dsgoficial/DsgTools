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

from dataclasses import dataclass, field
from typing import List

from qgis.core import (QgsApplication, QgsProcessingFeedback,
                       QgsProcessingMultiStepFeedback, QgsTask)
from qgis.PyQt.QtCore import pyqtSignal, QObject

from DsgTools.core.DSGToolsWorkflow.workflowItem import DSGToolsWorkflowItem, ExecutionStatus


@dataclass
class WorkflowMetadata:
    author: str
    version: str
    lastModified: str

@dataclass
class DSGToolsWorkflow(QObject):
    workflowItemList: List[DSGToolsWorkflowItem]
    displayName: str
    metadata: WorkflowMetadata

    def __post_init__(self):
        self.currentStepIndex = 0
        self.feedback = QgsProcessingFeedback()
        self.multiStepFeedback = QgsProcessingMultiStepFeedback(
            len(self.workflowItemList), self.feedback
        )
        self.currentWorkflowItemStatusChanged = pyqtSignal(int, DSGToolsWorkflowItem)
        self.currentTaskChanged = pyqtSignal(int, QgsTask)
        if not self.validateWorkflowItems():
            raise Exception("Invalid workflow")

    def validateWorkflowItems(self):
        # TODO
        return True

    def getCurrentWorkflowStepIndex(self) -> int:
        return self.currentStepIndex
    
    def getNextWorkflowStep(self) -> int:
        nextIndex = self.currentStepIndex + 1
        return nextIndex if nextIndex <= len(self.workflowItemList) - 1 else None
    
    def getCurrentWorkflowItem(self) -> DSGToolsWorkflowItem:
        idx = self.getCurrentWorkflowStepIndex()
        return self.workflowItemList[idx]
    
    def setCurrentWorkflowItem(self, idx) -> None:
        if idx < 0 or idx >= len(self.workflowItemList):
            return
        self.currentStepIndex = idx
    
    def connectSignals(self) -> None:
        for workflowItem in self.workflowItemList:
            workflowItem.workflowItemExecutionFinished.connect(self.postProcessWorkflowItem)
    
    def resetWorkflowItems(self):
        for workflowItem in self.workflowItemList:
            workflowItem.resetItem()
    
    def prepareTask(self) -> QgsTask:
        currentWorkflowItem: DSGToolsWorkflowItem = self.getCurrentWorkflowItem()
        return currentWorkflowItem.getTask(self.feedback)

    def postProcessWorkflowItem(self, workflowItem: DSGToolsWorkflowItem):
        self.currentTask = None
        self.currentWorkflowItemStatusChanged.emit(self.currentStepIndex, workflowItem)
        if workflowItem.getStatus() in [ExecutionStatus.FAILED, ExecutionStatus.FINISHED_WITH_FLAGS, ExecutionStatus.CANCELED]:
            self.multiStepFeedback.setCurrentStep(self.currentStepIndex)
            return
        self.currentStepIndex = self.getNextWorkflowStep()
        if self.currentStepIndex is None:
            self.multiStepFeedback.setProgress(100)
            return
        self.run(resumeFromStart=False)
    
    def run(self, resumeFromStart=True):
        if resumeFromStart:
            self.resetWorkflowItems()
            self.setCurrentWorkflowItem(0)
        currentTask: QgsTask = self.prepareTask()
        self.multiStepFeedback.setCurrentStep(self.currentStepIndex)
        self.currentWorkflowItemStatusChanged.emit(self.currentStepIndex, self.getCurrentWorkflowItem())
        self.currentTaskChanged.emmit(self.currentStepIndex, currentTask)
        QgsApplication.taskManager().addTask(currentTask)
    
    def cancelCurrentRun(self):
        currentWorkflowItem = self.getCurrentWorkflowItem()
        currentWorkflowItem.cancelCurrentTask()
        self.currentWorkflowItemStatusChanged.emit(self.currentStepIndex, currentWorkflowItem)
    
    def pauseCurrentRun(self):
        currentWorkflowItem = self.getCurrentWorkflowItem()
        currentWorkflowItem.pauseCurrentTask()
        self.currentWorkflowItemStatusChanged.emit(self.currentStepIndex, currentWorkflowItem)