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
from typing import Callable, Dict, List
import os, json
from time import time, sleep

from qgis.core import (
    QgsTask,
    QgsProject,
    QgsMapLayer,
    QgsLayerTreeLayer,
    QgsProcessingFeedback,
    QgsProcessingModelAlgorithm,
    QgsVectorLayer,
    QgsProcessingUtils,
    QgsProcessingContext,
)
from qgis.PyQt.QtCore import pyqtSignal, QCoreApplication
from qgis.utils import iface
from processing.tools import dataobjects
import processing

@dataclass
class FlagSettings:
    onFlagsRaised: str
    modelCanHaveFalsePositiveFlags: bool
    loadOutput: bool
    flagLayerNames: List[str] = field(default_factory=[])

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
class DSGToolsWorkflowItem:
    displayName: str
    flags: FlagSettings
    pauseAfterExecution: bool
    source: ModelSource
    metadata: Metadata

    def __post_init__(self):
        self.output = {
            "result": dict(),
            "status": False,
            "executionTime": 0.0,
            "errorMessage": "Thread not started yet.",
            "finishStatus": "initial",
        }
        self.model = self.getModel()
    
    def as_dict(self) -> Dict[str, str]:
        return {k: str(v) for k, v in asdict(self).items()}

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
        on_finished_func = self.getOnFinishedFunction()
        return QgsTask.fromFunction(
            func,
            on_finished=on_finished_func,
        )

    def getTaskRunningFunction(self, feedback: QgsProcessingFeedback) -> Callable:
        model = copy.deepcopy(self.model)
        modelParameters = self.getModelParameters()
        def func():
            context = dataobjects.createContext(feedback=feedback)
            out = processing.run(
                model,
                {param: "memory:" for param in modelParameters},
                feedback=feedback,
                context=context,
            )
            out.pop("CHILD_INPUTS", None)
            out.pop("CHILD_RESULTS", None)
            return out
        return func

    def getOnFinishedFunction(self):
        return

def load_from_json(input_dict: dict) -> DSGToolsWorkflowItem:
    params = copy.deepcopy(input_dict)
    params["flags"] = FlagSettings(**params["flags"])
    params["source"] = ModelSource(**params["source"])
    params["metadata"] = Metadata(**params["metadata"])
    return DSGToolsWorkflowItem(**params)
