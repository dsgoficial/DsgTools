# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-02-21
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

import copy
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List
import os
from time import time

from qgis.core import (
    QgsTask,
    QgsProject,
    QgsMapLayer,
    QgsProcessingFeedback,
    QgsProcessingModelAlgorithm,
    QgsVectorLayer,
    QgsProcessingUtils,
    QgsProcessingContext,
    QgsMessageLog,
    Qgis,
)
from qgis.PyQt.QtCore import pyqtSignal, QObject
from qgis.utils import iface
from processing.tools import dataobjects
import processing


class ExecutionStatus(Enum):
    INITIAL = "initial"
    RUNNING = "running"
    FAILED = "failed"
    CANCELED = "canceled"
    FINISHED = "finished"
    FINISHED_WITH_FLAGS = "finished with flags"
    ON_HOLD = "on hold"
    PAUSED_BEFORE_RUNNING = "paused before running"
    IGNORE_FLAGS = "ignore flags"

@dataclass
class FlagSettings:
    onFlagsRaised: str
    modelCanHaveFalsePositiveFlags: bool
    loadOutput: bool
    flagLayerNames: List[str] = field(default_factory=[])

    def __post_init__(self):
        if self.onFlagsRaised not in ("halt", "warn", "ignore"):
            raise ValueError("Invalid on flags raised flag.")

@dataclass
class ModelSource:
    type: str
    data: str

    @staticmethod
    def modelFromFile(filepath):
        """
        Initiates a model from a filepath.
        :param filepath: (str) filepath for target file.
        :return: (QgsProcessingModelAlgorithm) model as a processing algorithm.
        """
        alg = QgsProcessingModelAlgorithm()
        alg.fromFile(filepath)
        alg.initAlgorithm()
        return alg

    def modelFromXml(self) -> QgsProcessingModelAlgorithm:
        """
        Creates a processing model object from XML text.
        :param xml: (str) XML file contents.
        :return: (QgsProcessingModelAlgorithm) model as a processing algorithm.
        """
        temp = os.path.join(
            os.path.dirname(__file__), "temp_model_{0}.model3".format(hash(time()))
        )
        with open(temp, "w+", encoding="utf-8") as xmlFile:
            xmlFile.write(self.data)
        alg = ModelSource.modelFromFile(temp)
        os.remove(temp)
        return alg

@dataclass
class Metadata:
    originalName: str

@dataclass
class ModelExecutionOutput:
    result: Dict[str, Any] = field(default_factory=dict)
    executionTime: float = 0.0
    executionMessage: str = ""
    status: ExecutionStatus = ExecutionStatus.INITIAL

@dataclass
class DSGToolsWorkflowItem(QObject):
    displayName: str
    flags: FlagSettings
    pauseAfterExecution: bool
    source: ModelSource
    metadata: Metadata

    def __post_init__(self):
        self.resetItem()
        self.model = self.getModel()
        self.currentTask = None
        self.workflowItemExecutionFinished = pyqtSignal(DSGToolsWorkflowItem)
    
    def resetItem(self):
        self.executionOutput = ModelExecutionOutput()
    
    def as_dict(self) -> Dict[str, str]:
        return {k: v for k, v in asdict(self).items()}

    def getModel(self) -> QgsProcessingModelAlgorithm:
        return self.source.modelFromXml()

    def getModelParameters(self) -> List[str]:
        if self.model is None:
            return []
        return [param.name() for param in self.model.parameterDefinitions()]
    
    def getFlagNames(self) -> List[str]:
        return self.flags.flagLayerNames
    
    def getOutputFlags(self):
        pass

    def getTask(self, feedback: QgsProcessingFeedback) -> QgsTask:
        func = self.getTaskRunningFunction(feedback)
        on_finished_func = self.getOnFinishedFunction(feedback)
        self.currentTask = QgsTask.fromFunction(
            func,
            on_finished=on_finished_func,
        )
        return self.currentTask
    
    def pauseBeforeRunning(self):
        self.executionOutput = ModelExecutionOutput(
            executionMessage=self.tr(f"Workflow item {self.displayName} execution paused by previous step."),
            status=ExecutionStatus.PAUSED_BEFORE_RUNNING,
        )
    
    def setCurrentStateToIgnoreFlags(self):
        if not self.flags.modelCanHaveFalsePositiveFlags:
            return
        self.changeCurrentStatus(
            status=ExecutionStatus.IGNORE_FLAGS,
            executionMessage=self.tr(f"Workflow item {self.displayName} flags were ignored by the user.")
        )
        # não emite sinal pois esse passo é feito fora da execução.

    def changeCurrentStatus(self, status: ExecutionStatus, executionMessage: str) -> None:
        self.executionOutput.status = status
        self.executionOutput.executionMessage = executionMessage

    def cancelCurrentTask(self):
        if self.currentTask is None:
            return
        self.currentTask.cancel()
        self.currentTask = None
    
    def pauseCurrentTask(self):
        if self.currentTask is None:
            return
        self.currentTask.hold()
    
    def resumeCurrentTask(self):
        if self.currentTask is None:
            return
        self.currentTask.unhold()

    def getTaskRunningFunction(self, feedback: QgsProcessingFeedback) -> Callable:
        model = copy.deepcopy(self.model)
        modelParameters = self.getModelParameters()
        def func():
            start = time()
            context = dataobjects.createContext(feedback=feedback)
            context.setProject(QgsProject.instance())
            out = processing.run(
                model,
                {param: "memory:" for param in modelParameters},
                feedback=feedback,
                context=context,
            )
            out.pop("CHILD_INPUTS", None)
            out.pop("CHILD_RESULTS", None)
            out["start_time"] = start
            return out
        return func

    def getOnFinishedFunction(self, feedback: QgsProcessingFeedback) -> Callable:
        def on_finished_func(exception, result=None):
            if exception is not None:
                QgsMessageLog.logMessage(
                    f"Exception: {exception}",
                    "DSGTools Plugin",
                    Qgis.Critical
                )
                self.executionOutput = ModelExecutionOutput(
                    executionMessage=self.tr(f"Workflow item {self.displayName} execution has failed:\n {str(exception)}"),
                    status=ExecutionStatus.FAILED,
                )
                self.workflowItemExecutionFinished.emit(self)
                return
            if result is not None:
                self.handleOutputs(result, feedback)
                self.loadOutputs(feedback)
                status = ExecutionStatus.FINISHED_WITH_FLAGS if any(lyr.featureCount() > 0 for k, lyr in self.executionOutput.result.items() if lyr.name() in self.flagLayerNames()) else ExecutionStatus.FINISHED
                statusMsg = self.tr("finished with flags.") if status == ExecutionStatus.FINISHED_WITH_FLAGS else self.tr("finished.")
                self.changeCurrentStatus(
                    status=status,
                    executionMessage=self.tr(f"Workflow item {self.displayName} {statusMsg}")
                )
            else:
                self.executionOutput = ModelExecutionOutput(
                    executionMessage=self.tr(f"Workflow item {self.displayName} execution was canceled by the user."),
                    status=ExecutionStatus.CANCELED,
                )
            self.workflowItemExecutionFinished.emit(self)
            self.currentTask = None
        
        return on_finished_func

    def handleOutputs(self, result, feedback):
        start = result.pop("start_time")
        context = dataobjects.createContext(feedback=feedback)
        context.setProject(QgsProject.instance())
        for paramName, vl in result.items():
            baseName = paramName.rsplit(":", 1)[-1]
            name = baseName
            idx = 1
            while name in self.executionOutput.result:
                name = "{0} ({1})".format(baseName, idx)
                idx += 1
            if isinstance(vl, str):
                vl = QgsProcessingUtils.mapLayerFromString(vl, context)
            vl.setName(name)
            self.executionOutput.result[name] = vl
        self.executionOutput.executionTime = time() - start
    
    def loadOutput(self) -> bool:
        return self.flags.loadOutput
    
    def getStatus(self) -> ExecutionStatus:
        return self.executionOutput.status
    
    def loadOutputs(self, feedback):
        loadOutput = self.loadOutput()
        if not loadOutput:
            return
        flagLayerNames = self.flagLayerNames()
        context = QgsProcessingContext()
        iface.mapCanvas().freeze(True)
        for name, vl in self.executionOutput.result.items():
            if vl is None:
                continue
            if vl.name() not in flagLayerNames and not loadOutput:
                continue
            if isinstance(vl, str):
                vl = QgsProcessingUtils.mapLayerFromString(vl, context)
                self.executionOutput.result[name] = vl
            if not isinstance(vl, QgsMapLayer) or not vl.isValid():
                continue
            vl.setName(name.split(":", 2)[-1])
            if vl.name() in flagLayerNames and vl.featureCount() == 0:
                continue
            cloneVl = vl.clone()
            self.executionOutput.result[name] = cloneVl
            self.addLayerToGroup(cloneVl, self.displayName(), clearGroupBeforeAdding=True)
            self.enableFeatureCount(cloneVl)
        iface.mapCanvas().freeze(False)
    
    def addLayerToGroup(
        self, layer, subgroupname, clearGroupBeforeAdding=False
    ):
        """
        Adds a layer to a group into layer panel.
        :param layer: (QgsMapLayer) layer to be added to canvas.
        :param subgroupname: (str) name for the subgroup to be added.
        """
        subGroup = self.createGroups(subgroupname)
        if clearGroupBeforeAdding:
            self.clearGroup(subGroup)
        layer = (
            layer
            if isinstance(layer, QgsMapLayer)
            else QgsProcessingUtils.mapLayerFromString(layer)
        )
        QgsProject.instance().addMapLayer(layer, addToLegend=False)
        subGroup.addLayer(layer)

    def createGroups(self, subgroupname):
        rootNode = QgsProject.instance().layerTreeRoot()
        parentGroupName = "DSGTools_QA_Toolbox"
        parentGroupNode = rootNode.findGroup(parentGroupName)
        parentGroupNode = (
            parentGroupNode
            if parentGroupNode
            else rootNode.insertGroup(0, parentGroupName)
        )
        subGroup = self.createGroup(subgroupname, parentGroupNode)
        return subGroup

    def createGroup(self, groupName, rootNode):
        groupNode = rootNode.findGroup(groupName)
        return groupNode if groupNode else rootNode.addGroup(groupName)

    def prepareGroup(self, model):
        subGroup = self.createGroups(
            self.model().model.displayName()
        )
        self.clearGroup(subGroup)

    def clearGroup(self, group):
        for lyrGroup in group.findLayers():
            lyr = lyrGroup.layer()
            if isinstance(lyr, QgsVectorLayer):
                lyr.rollBack()
        group.removeAllChildren()

def load_from_json(input_dict: dict) -> DSGToolsWorkflowItem:
    params = copy.deepcopy(input_dict)
    params["flags"] = FlagSettings(**params["flags"])
    params["source"] = ModelSource(**params["source"])
    params["metadata"] = Metadata(**params["metadata"])
    return DSGToolsWorkflowItem(**params)
