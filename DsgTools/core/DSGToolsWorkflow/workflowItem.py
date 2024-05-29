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
from enum import Enum, unique
from typing import Any, Callable, Dict, List, Optional
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


@unique
class ExecutionStatus(str, Enum):
    """Enumeration representing the execution status of a workflow item.

    Attributes:
        INITIAL: Initial state.
        RUNNING: Currently running.
        FAILED: Execution failed.
        CANCELED: Execution canceled.
        FINISHED: Execution finished successfully.
        FINISHED_WITH_FLAGS: Execution finished with flags raised.
        ON_HOLD: Execution on hold.
        PAUSED_BEFORE_RUNNING: Execution paused before running.
        IGNORE_FLAGS: Flags are ignored for this step.
    """

    INITIAL = "initial"
    RUNNING = "running"
    FAILED = "failed"
    CANCELED = "canceled"
    FINISHED = "finished"
    FINISHED_WITH_FLAGS = "finished with flags"
    PAUSED_BEFORE_RUNNING = "paused before running"
    IGNORE_FLAGS = "ignore flags"


@dataclass
class FlagSettings:
    """Dataclass representing settings related to flags in a workflow item.

    Attributes:
        onFlagsRaised (str): Action to take when flags are raised - "halt", "warn", or "ignore".
        modelCanHaveFalsePositiveFlags (bool): Whether the model can have false positive flags.
        loadOutput (bool): Whether to load the output.
        flagLayerNames (List[str]): List of flag layer names.
    """

    onFlagsRaised: str
    modelCanHaveFalsePositiveFlags: bool
    loadOutput: bool
    flagLayerNames: List[str] = field(default_factory=[])

    def __post_init__(self):
        if self.onFlagsRaised not in ("halt", "warn", "ignore"):
            raise ValueError("Invalid on flags raised flag.")


@dataclass
class ModelSource:
    """Dataclass representing the source of a processing model.

    Attributes:
        type (str): Type of the model source.
        data (str): Data related to the model source.

    Methods:
        modelFromFile(filepath: str) -> QgsProcessingModelAlgorithm:
            Initiates a model from a filepath.

        modelFromXml() -> QgsProcessingModelAlgorithm:
            Creates a processing model object from XML text.
    """

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
    """Dataclass representing metadata for a workflow item.

    Attributes:
        originalName (str): The original name of the workflow item.
    """

    originalName: str


@dataclass
class ModelExecutionOutput:
    """Dataclass representing the output of a model execution.

    Attributes:
        result (Dict[str, Any]): Execution result.
        executionTime (float): Execution time in seconds.
        executionMessage (str): Message related to the execution.
        status (ExecutionStatus): Execution status.
    """

    result: Dict[str, Any] = field(default_factory=dict)
    executionTime: float = 0.0
    executionMessage: str = ""
    status: ExecutionStatus = ExecutionStatus.INITIAL

    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = ExecutionStatus(self.status)


@dataclass
class DSGToolsWorkflowItem(QObject):
    """Class representing a workflow item in DSGTools.

    Attributes:
        displayName (str): Display name of the workflow item.
        flags (FlagSettings): Settings related to flags in the workflow item.
        pauseAfterExecution (bool): Whether to pause after execution.
        source (ModelSource): Source of the processing model.
        metadata (Metadata): Metadata related to the workflow item.

    Signals:
        workflowItemExecutionFinished: Emitted when the workflow item execution is finished.
    """

    displayName: str
    flags: FlagSettings
    pauseAfterExecution: bool
    source: ModelSource
    metadata: Metadata

    workflowItemExecutionFinished = pyqtSignal(object)

    def __post_init__(self):
        """Initialize post dataclass creation."""
        super().__init__()
        self.resetItem()
        self.model = self.getModel()
        self.currentTask = None
        self.executionOutput = ModelExecutionOutput()
        self.feedback = QgsProcessingFeedback()
        self.context = dataobjects.createContext(feedback=self.feedback)
        self.context.setProject(QgsProject.instance())

    def resetItem(self):
        """Reset the workflow item."""
        if hasattr(self, "executionOutput"):
            self.clearOutputs()
        self.executionOutput = ModelExecutionOutput()

    def as_dict(self) -> Dict[str, str]:
        """Convert the workflow item to a dictionary."""
        return {
            k: v
            for k, v in asdict(self).items()
            if k not in ["workflowItemExecutionFinished"]
        }

    def setStatusFromDict(self, data: dict[str, Any]):
        self.executionOutput = ModelExecutionOutput(**data)

    def executionStatusAsDict(self):
        d = asdict(self.executionOutput)
        d.pop("result")
        return d

    def getModel(self) -> QgsProcessingModelAlgorithm:
        """Get the processing model from the source.

        Returns:
            QgsProcessingModelAlgorithm: The processing model.
        """
        return self.source.modelFromXml()

    def getModelParameters(self) -> List[str]:
        """Get the parameters of the processing model.

        Returns:
            List[str]: List of parameter names.
        """
        if self.model is None:
            return []
        return [param.name() for param in self.model.parameterDefinitions()]

    def getFlagNames(self) -> List[str]:
        """Get the names of flag layers.

        Returns:
            List[str]: List of flag layer names.
        """
        return self.flags.flagLayerNames
    
    def getAllOutputNamesFromModel(self) -> List[str]:
        return [
            outputDef.name().split(":")[-1] for outputDef in self.model.outputDefinitions()
        ]

    def flagsCanHaveFalsePositiveResults(self) -> bool:
        return self.flags.modelCanHaveFalsePositiveFlags

    def getDescription(self) -> str:
        return self.model.shortDescription()

    def getOutputFlags(self):
        """Get the output flags."""
        pass

    def getTask(self) -> QgsTask:
        """Prepare the task for the workflow item execution.

        Args:
            feedback (QgsProcessingFeedback): Feedback for the task.

        Returns:
            QgsTask: The prepared task.
        """
        func = self.getTaskRunningFunction()
        on_finished_func = self.getOnFinishedFunction()
        self.currentTask = QgsTask.fromFunction(
            self.model.name(),
            func,
            on_finished=on_finished_func,
        )
        return self.currentTask

    def pauseBeforeRunning(self):
        """Pause the workflow item before running."""
        self.executionOutput = ModelExecutionOutput(
            executionMessage=self.tr(
                f"Workflow item {self.displayName} execution paused by previous step."
            ),
            status=ExecutionStatus.PAUSED_BEFORE_RUNNING,
        )

    def setCurrentStateToIgnoreFlags(self):
        """Set the status to ignore flags on the current workflow step."""
        if not self.flagsCanHaveFalsePositiveResults():
            return
        if self.executionOutput.status == ExecutionStatus.IGNORE_FLAGS:
            self.changeCurrentStatus(
                status=ExecutionStatus.FINISHED_WITH_FLAGS,
                executionMessage=self.tr(
                    f"Workflow item {self.displayName} status changed from ignore flags to finished with flags."
                ),
            )
            return
        self.changeCurrentStatus(
            status=ExecutionStatus.IGNORE_FLAGS,
            executionMessage=self.tr(
                f"Workflow item {self.displayName} flags were ignored by the user."
            ),
        )
        # não emite sinal pois esse passo é feito fora da execução.

    def changeCurrentStatus(
        self,
        status: ExecutionStatus,
        executionMessage: Optional[str] = None,
        executionTime: Optional[float] = None,
    ) -> None:
        """Change the current status of the workflow item.

        Args:
            status (ExecutionStatus): The new status.
            executionMessage (str): Message related to the status change.
        """
        self.executionOutput.status = (
            status if isinstance(status, ExecutionStatus) else ExecutionStatus(status)
        )
        self.executionOutput.executionMessage = (
            executionMessage if executionMessage is not None else ""
        )
        if executionTime is not None:
            self.executionOutput.executionTime = executionTime

    def cancelCurrentTask(self):
        """Cancel the current task."""
        if self.currentTask is None:
            return
        try:
            self.currentTask.cancel()
        except:
            pass
        self.currentTask = None
        self.changeCurrentStatus(
            status=ExecutionStatus.CANCELED,
            executionMessage=self.tr(
                f"Workflow item {self.displayName} canceled by user."
            ),
        )

    def getTaskRunningFunction(self) -> Callable:
        """Get the function to run for the task.

        Args:
            feedback (QgsProcessingFeedback): Feedback for the task.

        Returns:
            Callable: The function to run for the task.
        """
        modelParameters = self.getModelParameters()
        self.feedback.setProgress(0)

        def func(obj=None):
            start = time()
            out = processing.run(
                self.model,
                {param: "memory:" for param in modelParameters},
                feedback=self.feedback,
                context=self.context,
            )
            out.pop("CHILD_INPUTS", None)
            out.pop("CHILD_RESULTS", None)
            out["start_time"] = start
            return out

        return func

    def getOnFinishedFunction(self) -> Callable:
        """Get the function to run when the task is finished.

        Args:
            feedback (QgsProcessingFeedback): Feedback for the task.

        Returns:
            Callable: The function to run when the task is finished.
        """

        def on_finished_func(exception, result=None):
            if exception is not None:
                QgsMessageLog.logMessage(
                    f"Exception: {exception}", "DSGTools Plugin", Qgis.Critical
                )
                self.executionOutput = ModelExecutionOutput(
                    executionMessage=self.tr(
                        f"Workflow item {self.displayName} execution has failed:\n {str(exception)}"
                    ),
                    status=ExecutionStatus.FAILED,
                )
                self.workflowItemExecutionFinished.emit(self)
                return
            if result is not None:
                self.handleOutputs(result, self.feedback)
                self.loadOutputs(self.feedback)
                status = (
                    ExecutionStatus.FINISHED_WITH_FLAGS
                    if any(
                        lyr.featureCount() > 0
                        for k, lyr in self.executionOutput.result.items()
                        if lyr.name() in self.flags.flagLayerNames
                    )
                    else ExecutionStatus.FINISHED
                )
                statusMsg = (
                    self.tr("finished with flags.")
                    if status == ExecutionStatus.FINISHED_WITH_FLAGS
                    else self.tr("finished.")
                )
                self.changeCurrentStatus(
                    status=status,
                    executionMessage=self.tr(
                        f"Workflow item {self.displayName} {statusMsg}"
                    ),
                )
            else:
                self.executionOutput = ModelExecutionOutput(
                    executionMessage=self.tr(
                        f"Workflow item {self.displayName} execution was canceled by the user."
                    ),
                    status=ExecutionStatus.CANCELED,
                )
            self.workflowItemExecutionFinished.emit(self)
            self.currentTask = None

        return on_finished_func

    def handleOutputs(self, result, feedback):
        """Handle the outputs of the task.

        Args:
            result: The result of the task.
            feedback (QgsProcessingFeedback): Feedback for the task.
        """
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
        """Check if output loading is enabled.

        Returns:
            bool: True if output loading is enabled, False otherwise.
        """
        return self.flags.loadOutput

    def getStatus(self) -> ExecutionStatus:
        """Get the current status of the workflow item.

        Returns:
            ExecutionStatus: The current status.
        """
        return self.executionOutput.status

    def loadOutputs(self, feedback):
        """Load the outputs of the workflow item.

        Args:
            feedback (QgsProcessingFeedback): Feedback for the task.
        """
        loadOutput = self.loadOutput()
        flagLayerNames = self.flags.flagLayerNames
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
            self.executionOutput.result[cloneVl.name()] = cloneVl
            self.addLayerToGroup(cloneVl, self.displayName, clearGroupBeforeAdding=True)
            self.enableFeatureCount(cloneVl)
        iface.mapCanvas().freeze(False)

    def addLayerToGroup(self, layer, subgroupname, clearGroupBeforeAdding=False):
        """Add a layer to a group in the layer panel.

        Args:
            layer (QgsMapLayer): The layer to be added.
            subgroupname (str): Name for the subgroup to be added.
            clearGroupBeforeAdding (bool): Whether to clear the group before adding the layer.
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
    
    def clearOutputs(self, onlyFlags=False):
        lyrKeysToPop = []
        iface.mapCanvas().freeze(True)
        for lyrName, vl in self.executionOutput.result.items():
            if onlyFlags and lyrName not in self.flags.flagLayerNames:
                continue
            try:
                QgsProject.instance().removeMapLayer(vl.id())
            except:
                pass
            lyrKeysToPop.append(lyrName)
        for key in lyrKeysToPop:
            self.executionOutput.result.pop(key)
        iface.mapCanvas().freeze(False)

    def createGroups(self, subgroupname):
        """Create groups in the layer panel.

        Args:
            subgroupname (str): Name for the subgroup to be created.

        Returns:
            QgsLayerTreeGroup: The created subgroup.
        """
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
        """Create a group in the layer panel.

        Args:
            groupName (str): Name for the group.
            rootNode (QgsLayerTree): The root node for the group.

        Returns:
            QgsLayerTreeGroup: The created group.
        """
        groupNode = rootNode.findGroup(groupName)
        return groupNode if groupNode else rootNode.addGroup(groupName)

    def prepareGroup(self, model):
        """Prepare the group for the layer panel.

        Args:
            model: The model to be prepared.
        """
        subGroup = self.createGroups(self.model().model.displayName())
        self.clearGroup(subGroup)

    def clearGroup(self, group):
        """Clear a group in the layer panel.

        Args:
            group (QgsLayerTreeGroup): The group to be cleared.
        """
        for lyrGroup in group.findLayers():
            lyr = lyrGroup.layer()
            if isinstance(lyr, QgsVectorLayer):
                lyr.rollBack()
        group.removeAllChildren()

    def enableFeatureCount(self, lyr):
        root = QgsProject.instance().layerTreeRoot()
        lyrNode = root.findLayer(lyr.id())
        lyrNode.setCustomProperty("showFeatureCount", True)


def load_from_json(input_dict: dict) -> DSGToolsWorkflowItem:
    """Load a DSGToolsWorkflowItem from a JSON-like dictionary.

    Args:
        input_dict (dict): The dictionary containing the information for the workflow item.

    Returns:
        DSGToolsWorkflowItem: The loaded DSGToolsWorkflowItem.
    """
    params = copy.deepcopy(input_dict)
    params["flags"] = FlagSettings(**params["flags"])
    params["source"] = ModelSource(**params["source"])
    params["metadata"] = Metadata(**params["metadata"])
    return DSGToolsWorkflowItem(**params)
