# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-08-28
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
from time import sleep
from functools import partial

from qgis.core import (QgsApplication,
                       QgsProcessingFeedback,
                       QgsProcessingMultiStepFeedback)
from qgis.PyQt.QtCore import QObject, pyqtSignal

from DsgTools.core.DSGToolsProcessingAlgs.Models.dsgToolsProcessingModel import DsgToolsProcessingModel

class QualityAssuranceWorkflow(QObject):
    """
    Works as a multi-model runner. Understands all models' parameters as an
    output vector layer.
    """
    workflowFinished = pyqtSignal()
    haltedOnFlags = pyqtSignal(DsgToolsProcessingModel)
    modelStarted = pyqtSignal(DsgToolsProcessingModel)
    modelFinished = pyqtSignal(DsgToolsProcessingModel)
    modelFinishedWithFlags = pyqtSignal(DsgToolsProcessingModel)
    modelFailed = pyqtSignal(DsgToolsProcessingModel)

    def __init__(self, parameters, feedback=None):
        """
        Class constructor. Materializes an workflow set of parameters.
        :param parameters: (dict) map of workflow attributes.
        :param feedback: (QgsProcessingFeedback) task progress tracking QGIS
                         object.
        """
        super(QualityAssuranceWorkflow, self).__init__()
        msg = self.validateParameters(parameters)
        if msg:
            raise Exception(
                self.tr("Invalid workflow parameter:\n{msg}").format(msg=msg)
            )
        self._param = parameters
        self._modelOrderMap = dict()
        self.output = dict()
        self.feedback = feedback or QgsProcessingFeedback()

    def validateParameters(self, parameters):
        """
        Validates a set of parameters for a valid Workflow.
        :param parameters: (dict) map of workflow attributes to be validated.
        :return: (str) invalidation reason.
        """
        if "displayName" not in parameters or not parameters["displayName"]:
            # this is not a mandatory item, but it defaults to a value
            parameters["displayName"] = self.tr("DSGTools Validation Workflow")
        if "models" not in parameters or not parameters["models"]:
            return self.tr("Workflow seems to have no models associated with it.")
        for modelName, modelParam in parameters["models"].items():
            model=DsgToolsProcessingModel(modelParam, modelName)
            if not model.isValid():
                return self.tr("Model {model} is invalid: '{reason}'.").format(
                    model=modelName, reason=model.validateParameters(modelParam)
                )
        # if "flagLayer" not in parameters or not parameters["flagLayer"]:
        #     self.tr("No flag layer was provided.")
        # if "historyLayer" not in parameters or not parameters["historyLayer"]:
        #     self.tr("No history layer was provided.")
        return ""

    def metadata(self):
        """
        A map to Workflow's metadata.
        :return: (dict) metadata.
        """
        return self._param["metadata"] if "metadata" in self._param else dict()

    def author(self):
        """
        Retrieves Workflow's author, if available.
        :return: (str) Workflow's author.
        """
        meta = self.metadata()
        return meta["author"] if "author" in meta else ""

    def version(self):
        """
        Retrieves Workflow's version, if available.
        :return: (str) Workflow's version.
        """
        meta = self.metadata()
        return meta["version"] if "version" in meta else ""

    def lastModified(self):
        """
        Retrieves Workflow's last modification "timestamp", if available.
        :return: (str) Workflow's last modification time and date.
        """
        meta = self.metadata()
        return meta["lastModified"] if "lastModified" in meta else ""

    def metadataText(self):
        """
        Retrieves Workflow's metadata string.
        :return: (str) Workflow's metadata string.
        """
        if not self.metadata():
            return ""
        return self.tr(
            "Workflow {name} v{version} ({lastModified}) by {author}."
        ).format(name=self.displayName(), **self.metadata())

    def displayName(self):
        """
        Friendly name for the workflow.
        :return: (str) display name.
        """
        return self._param["displayName"] if \
                "displayName" in self._param else ""

    def name(self):
        """
        Proxy method for displayName.
        :return: (str) display name.
        """
        return self.displayName()

    def models(self):
        """
        Model parameters defined to run in this workflow.
        :return: (dict) models maps to valid and invalid models.
        """
        models = {"valid" : dict(), "invalid" : dict()}
        self._multiStepFeedback = QgsProcessingMultiStepFeedback(
            len(self._param["models"]), self.feedback
        )
        self._multiStepFeedback.setCurrentStep(0)
        for modelName, modelParam in self._param["models"].items():
            model = DsgToolsProcessingModel(
                modelParam, modelName, feedback=self._multiStepFeedback
            )
            if not model.isValid():
                models["invalid"][modelName] = model.validateParameters(modelParam)
            else:
                models["valid"][modelName] = model
        return models

    def validModels(self):
        """
        Returns all valid models from workflow parameters.
        :return: (dict) models maps to valid and invalid models.
        """
        models = dict()
        self._multiStepFeedback = QgsProcessingMultiStepFeedback(
            len(self._param["models"]), self.feedback
        )
        self._multiStepFeedback.setCurrentStep(0)
        for idx, (modelName, modelParam) in enumerate(self._param["models"].items()):
            model = DsgToolsProcessingModel(
                modelParam, modelName, feedback=self._multiStepFeedback
            )
            if model.isValid():
                models[modelName] = model
            self._modelOrderMap[modelName] = idx
        return models

    def invalidModels(self):
        """
        Returns all valid models from workflow parameters.
        :return: (dict) models maps invalid models to their invalidation reason.
        """
        models = dict()
        self._multiStepFeedback = QgsProcessingMultiStepFeedback(
            len(self._param["models"]), self.feedback
        )
        self._multiStepFeedback.setCurrentStep(0)
        for modelName, modelParam in self._param["models"].items():
            model = DsgToolsProcessingModel(
                modelParam, modelName, feedback=self._multiStepFeedback
            )
            if not model.isValid():
                models[modelName] = model.validateParameters(modelParam)
        return models

    def hasInvalidModel(self):
        """
        Checks if any of the nested models is invalid.
        :return: (bool) if there are invalid models.
        """
        models = dict()
        for modelName, modelParam in self._param["models"].items():
            model = DsgToolsProcessingModel(modelParam, modelName)
            if not model.isValid():
                return True
        return False

    # def flagLayer(self):
    #     """
    #     Layer to work as a sink to flag output for all models.
    #     :return: (QgsVectorLayer) flag layer.
    #     """
    #     return self._param["flagLayer"] if "flagLayer" in self._param else ""

    # def historyLayer(self):
    #     """
    #     A table (a layer with no geometry) to store execution history.
    #     :return: (QgsVectorLayer) flag layer.
    #     """
    #     return self._param["flagLayer"] if "flagLayer" in self._param else ""

    def export(self, filepath):
        """
        Dumps workflow's parameters as a JSON file.
        :param filepath: (str) path to JSON file.
        :return: (bool) operation success.
        """
        with open(filepath, "w", encoding="utf-8") as fp:
            fp.write(json.dumps(self._param, sort_keys=True, indent=4))
        return os.path.exists(filepath)

    def asDict(self):
        """
        Dumps model parameters as a JSON file.
        :param filepath: (str) path to JSON file.
        :return: (dict) DSGTools processing model definitions.
        """
        return dict(self._param)

    def finished(self):
        """
        Executes all post-processing actions.
        """
        # Add default post-processing actions here!
        self.workflowFinished.emit()

    def runOnMainThread(self):
        """
        If, for some reason, Workflow should not be run from secondary threads,
        this method provides a 'static' execution alternative.
        :return: (dict) a map to each model's output.
        """
        output = dict()
        for model in self.validModels().values():
            try:
                output[model.name()] = model.runModel()
            except:
                output[model.name()] = None
        self.finished()
        return output

    def setupModelTask(self, model):
        """
        Sets model to run on QGIS task manager.
        """
        QgsApplication.taskManager().addTask(model)

    def hold(self):
        """
        Puts current active tasks/models on hold.
        """
        if not hasattr(self, "_executionOrder"):
            return
        for m in self._executionOrder.values():
            if m.status() == m.Running:
                m.hold()

    def unhold(self):
        """
        Puts current paused tasks/models back to active status.
        """
        if not hasattr(self, "_executionOrder"):
            return
        for m in self._executionOrder.values():
            if m.status() == m.OnHold:
                m.unhold()

    def currentModel(self):
        """
        Retrieves the model currently running, if any.
        :return: (DsgToolsProcessingModel) current active model.
        """
        if not hasattr(self, "_executionOrder"):
            return None
        for m in self._executionOrder.values():
            if m.status() == m.Running:
                return m
        return None

    def raiseFlagWarning(self, model):
        """
        Advises connected objects that flags were raised even though workflow
        :param model: (DsgToolsProcessingModel) model to have its flags checked.
        """
        if model.hasFlags():
            self.modelFinishedWithFlags.emit(model)
        else:
            self.modelFinished.emit(model)

    def raiseFlagError(self, model):
        """
        It stops the workflow execution if flags are identified.
        :param model: (DsgToolsProcessingModel) model to have its flags checked.
        """
        if model.hasFlags():
            self.feedback.cancel()
            self.haltedOnFlags.emit(model)
        else:
            self.modelFinished.emit(model)
        return self.feedback.isCanceled()

    def handleFlags(self, model):
        """
        Handles Workflow behaviour for a model's flag output.
        :param model: (DsgToolsProcessingModel) model to have its output handled.
        """
        onFlagsMethod = {
            "warn" : partial(self.raiseFlagWarning, model),
            "halt" : partial(self.raiseFlagError, model),
            "ignore" : partial(self.modelFinished.emit, model)
        }[model.onFlagsRaised()]()

    def run(self, firstModelName=None, cooldown=None):
        """
        Executes all models in secondary threads.
        :param firstModelName: (str) first model's name to be executed.
        :param cooldown: (float) time to wait till next model is started.
        """
        self._executionOrder = {
            idx : model for idx, model in enumerate(self.validModels().values())
        }
        modelCount = len(self._executionOrder)
        if self.hasInvalidModel() or modelCount == 0:
            return None
        def modelCompleted(model, step):
            self.output[model.name()] = model.output
            self._multiStepFeedback.setCurrentStep(step)
            self.handleFlags(model)
        if firstModelName is not None:
            for idx, model in self._executionOrder.items():
                if model.name() == firstModelName:
                    initialIdx = idx
                    break
            else:
                # name was not found
                return None
        else:
            initialIdx = 0
            self.output = dict()
        for idx, currentModel in self._executionOrder.items():
            if idx < initialIdx:
                continue
            # all models MUST pass through this postprocessing method
            currentModel.taskCompleted.connect(
                partial(modelCompleted, currentModel, idx + 1)
            )
            currentModel.begun.connect(
                partial(self.modelStarted.emit, currentModel)
            )
            if idx != modelCount - 1:
                self._executionOrder[idx + 1].addSubTask(
                    currentModel,
                    subTaskDependency=currentModel.ParentDependsOnSubTask
                )
            else:
                # last model indicates workflow finish
                currentModel.taskCompleted.connect(self.finished)
        # last model will trigger every dependent model till the first added to
        # the task manager
        self.setupModelTask(currentModel)

    def lastModelName(self):
        """
        Gets the last model prepared to execute but has either failed or not
        run.
        :return: (str) first model's name not to run.
        """
        if not hasattr(self, "_executionOrder"):
            return None
        modelCount = len(self._executionOrder)
        for idx, model in self._executionOrder.items():
            modelName = self._executionOrder[idx].displayName()
            if modelName not in self.output or \
                self.output[modelName]["finishStatus"] != "finished":
                return modelName
        else:
            return None
