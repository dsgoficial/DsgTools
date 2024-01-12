# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-08-29
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
)
from qgis.PyQt.QtCore import pyqtSignal, QCoreApplication
from processing.tools import dataobjects
import processing


class DsgToolsProcessingModel(QgsTask):
    """
    Handles models and materializes QgsProcessingModels from a DSGTools default
    model parameter set.
    """

    # supported input model formats
    MODEL_TYPES = ["xml", "file", "model"]
    # xml: XML string               #
    # file: path to a local file    #
    # model: qgis resgistered model #
    modelFinished = pyqtSignal(QgsTask)

    # Appending status flags to the existing ones
    n = max(
        [
            QgsTask.Queued,
            QgsTask.OnHold,
            QgsTask.Running,
            QgsTask.Complete,
            QgsTask.Terminated,
        ]
    )
    (
        WarningFlags,
        HaltedOnFlags,
        HaltedOnPossibleFalsePositiveFlags,
        FlagsIgnored,
    ) = range(n + 1, n + 5)
    del n

    def __init__(self, parameters, name, taskName=None, flags=None, feedback=None):
        """
        Class constructor.
        :param parameters: (dict) map of attributes for a model.
        :param name: (str) name to identify current model.
        :param taskName: (str) name to be exposed on progress bar.
        :param flags: (list) a list of QgsTask flags to be set to current model.
        :param feedback: (QgsProcessingFeedback) task progress tracking QGIS
                         object.
        """
        super(DsgToolsProcessingModel, self).__init__(
            # "", QgsTask.CanCancel if flags is None else flags
            taskName
            or QCoreApplication.translate(
                "DsgToolsProcessingModel",
                "DSGTools Quality Assurance Model: {0}".format(name),
            ),
            QgsTask.CanCancel if flags is None else flags,
        )
        self._name = name
        self._param = {} if self.validateParameters(parameters) else parameters
        # self.setTitle(taskName or self.displayName())
        self.feedback = feedback or QgsProcessingFeedback()
        self.feedback.canceled.connect(self.cancel)
        self.output = {
            "result": dict(),
            "status": False,
            "executionTime": 0.0,
            "errorMessage": self.tr("Thread not started yet."),
            "finishStatus": "initial",
        }

    def setTitle(self, title):
        """
        Defines task's title (e.g. text shown as the task's name on QGIS task
        manager).
        """
        self.setDescription(title)

    def validateParameters(self, parameters):
        """
        Validates a set of parameters for a model composing a Workflow.
        :param parameters: (dict) map of attributes for a model.
        :return: (str) invalidation reason.
        """
        if "displayName" not in parameters or not parameters["displayName"]:
            # this is not a mandatory item, but it's a required tag
            parameters["displayName"] = ""
        if "flags" not in parameters or not parameters["flags"]:
            # this is a mandatory item, but it's has a default to be set if missing
            parameters["flags"] = {
                "onFlagsRaised": "halt",
                "enableLocalFlags": False,
                "modelCanHaveFalsePositiveFlags": False,
                "loadOutput": False,
            }
        if "flagLayerNames" not in parameters["flags"]:
            parameters["flags"]["flagLayerNames"] = []
        if "pauseAfterExecution" not in parameters:
            parameters["pauseAfterExecution"] = False
        if "source" not in parameters or not parameters["source"]:
            return self.tr("Model source is not defined.")
        if (
            "type" not in parameters["source"]
            or parameters["source"]["type"] not in self.MODEL_TYPES
        ):
            return self.tr("Input model type is not supported (or missing).")
        if "data" not in parameters["source"] or not parameters["source"]["data"]:
            return self.tr("Input model source was not identified.")
        return ""

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

    @staticmethod
    def modelFromXml(xml):
        """
        Creates a processing model object from XML text.
        :param xml: (str) XML file contents.
        :return: (QgsProcessingModelAlgorithm) model as a processing algorithm.
        """
        temp = os.path.join(
            os.path.dirname(__file__), "temp_model_{0}.model3".format(hash(time()))
        )
        with open(temp, "w+", encoding="utf-8") as xmlFile:
            xmlFile.write(xml)
        alg = DsgToolsProcessingModel.modelFromFile(temp)
        os.remove(temp)
        return alg

    def description(self):
        """
        Retrieves description text as set on model's definition.
        """
        model = self.model()
        return model.shortDescription()

    def metadata(self):
        """
        A map to Worflow's metadata.
        :return: (dict) metadata.
        """
        if "metadata" not in self._param:
            return {"author": "", "version": "", "lastModified": "", "originalName": ""}
        return self._param["metadata"]

    def author(self):
        """
        Retrieves the model's author name, if available.
        :return: (str) author name.
        """
        meta = self.metadata()
        return meta["author"] if "author" in meta else ""

    def version(self):
        """
        Retrieves the model's version, if available.
        :return: (str) model's version.
        """
        meta = self.metadata()
        return meta["version"] if "version" in meta else ""

    def lastModified(self):
        """
        Retrieves the model's last modification timestamp, if available.
        :return: (str) last modification timestamp.
        """
        meta = self.metadata()
        return meta["lastModified"] if "lastModified" in meta else ""

    def originalName(self):
        """
        When a model is imported from a file-based model, one might want to
        store the original model's name.
        :return: (str) original model's name.
        """
        meta = self.metadata()
        return meta["originalName"] if "originalName" in meta else ""

    def metadataText(self):
        """
        Retrieves Workflow's metadata string.
        :return: (str) Workflow's metadata string.
        """
        if "metadata" not in self._param:
            return ""
        return self.tr("Model {name} v{version} ({lastModified}) by {author}.").format(
            name=self.displayName(), **self.metadata()
        )

    def isValid(self):
        """
        Checks whether current model is a valid instance of DSGTools processing
        model.
        :return: (bool) validity status.
        """
        return self._param != dict()

    def data(self):
        """
        Current model's source data. If it's from a file, it's its filepath,
        if from an XML, its contents.
        :return: (str) model's source data.
        """
        return self._param["source"]["data"] if self.isValid() else ""

    def source(self):
        """
        Current model's input mode (XML text, file...).
        :return: (str) model's input source.
        """
        return self._param["source"]["type"] if self.isValid() else ""

    def displayName(self):
        """
        Model's friendly name, if available.
        :return: (str) model's friendly name.
        """
        if not self.isValid():
            return ""
        return (
            self._param["displayName"]
            if "displayName" in self._param
            else self.tr("DSGTools Validation Model ({0})").format(self.name())
        )

    def name(self):
        """
        Name for model identification.
        :return: (str) model's name.
        """
        return self._name

    def model(self):
        """
        Gets the processing model nested into parameters.
        :return: (QgsProcessingModelAlgorithm) model as a processing algorithm.
        """
        if not self.isValid():
            return QgsProcessingModelAlgorithm()
        method = {
            "xml": DsgToolsProcessingModel.modelFromXml,
            "file": DsgToolsProcessingModel.modelFromFile,
        }
        return (
            method[self.source()](self.data())
            if self.source() in method
            else QgsProcessingModelAlgorithm()
        )

    def flags(self):
        """
        Models execution flag when running on Workflow behaviour.
        :return: (dict) flag map.
        """
        flagMap = dict()
        if not self._param:
            return {}
        for flag, value in self._param["flags"].items():
            flagMap[flag] = value
        return flagMap

    def onFlagsRaised(self):
        """
        Model behavior when running on a Workflow if flags are raised.
        :return: (str) model behaviour on Workflow.
        """
        return self.flags()["onFlagsRaised"] if self.flags() else "halt"

    def modelCanHaveFalsePositiveFlags(self):
        return (
            self.flags().get("modelCanHaveFalsePositiveFlags", False)
            if self.flags()
            else False
        )

    def pauseAfterExecution(self):
        return self._param.get("pauseAfterExecution", False)

    def loadOutput(self):
        """
        Model behavior when running on a Workflow if flags are raised.
        :return: (str) model behaviour on Workflow.
        """
        return self.flags()["loadOutput"] if self.flags() else False

    def flagLayerNames(self):
        """
        Model behaviour when flags are raised. Tells which layers should be checked as flags.
        :return: (list) list of layer names
        """
        return self.flags()["flagLayerNames"] if self.flags() else []

    def enableLocalFlags(self):
        """
        Indicates whether model should store its to a local DSGTools default
        database.
        :return: (bool) whether flags would be written on a local database.
        """
        return self.flags()["enableLocalFlags"] if self.flags() else False

    def childAlgorithms(self, model=None):
        """
        A list of all algorithms' names nested into the model.
        :return: (list-of-str) list of all algorithms.
        """
        return [
            alg.algorithm().displayName()
            for alg in (model or self.model()).childAlgorithms().values()
        ]

    def modelParameters(self, model=None):
        """
        A list of parameters needed to be filled for the model to run.
        :param model: (QgsProcessingModelAlgorithm) model to have its parameters
                      checked.
        :return: (list-of-str)
        """
        # IMPORTANT: this method seems to be causing QGIS to crash when called
        # from command line. Error is "corrupted double-linked list / Aborted (core dumped)"
        # seems to be a QGIS mishandling, but should be lloked into deeper.
        # It works just fine running on plugin's thread - e.g. does not crash
        # whilst running an algorithm or using it internally
        # It seems the culprit is the parameterDefinitions method, from
        # QgsProcessingModelAlgorithm
        if not self._param:
            return []
        model = model or self.model()
        return [param.name() for param in model.parameterDefinitions()]

    def addLayerToGroup(
        self, layer, groupname, subgroupname=None, clearGroupBeforeAdding=False
    ):
        """
        Adds a layer to a group into layer panel.
        :param layer: (QgsMapLayer) layer to be added to canvas.
        :param groupname: (str) name for group to nest the layer.
        :param subgroupname: (str) name for the subgroup to be added.
        """
        subGroup = self.createGroups(groupname, subgroupname)
        if clearGroupBeforeAdding:
            self.clearGroup(subGroup)
        layer = (
            layer
            if isinstance(layer, QgsMapLayer)
            else QgsProcessingUtils.mapLayerFromString(layer)
        )
        QgsProject.instance().addMapLayer(layer, addToLegend=False)
        subGroup.addLayer(layer)

    def createGroups(self, groupname, subgroupname):
        root = QgsProject.instance().layerTreeRoot()
        qaGroup = self.createGroup(groupname, root)
        subGroup = self.createGroup(subgroupname, qaGroup)
        return subGroup

    def createGroup(self, groupName, rootNode):
        groupNode = rootNode.findGroup(groupName)
        return groupNode if groupNode else rootNode.addGroup(groupName)

    def prepareGroup(self, model):
        subGroup = self.createGroups(
            "DSGTools_QA_Toolbox", self.model().model.displayName()
        )
        self.clearGroup(subGroup)

    def clearGroup(self, group):
        for lyrGroup in group.findLayers():
            lyr = lyrGroup.layer()
            if isinstance(lyr, QgsVectorLayer):
                lyr.rollBack()
        group.removeAllChildren()

    def runModel(self, feedback=None):
        """
        Executes current model.
        :return: (dict) map to model's outputs.
        :param feedback: (QgsProcessingFeedback) task progress tracking QGIS
                         object.
        """
        # this tool understands every parameter to be filled as an output LAYER
        # it also sets all output to a MEMORY LAYER.
        model = self.model()
        if self.isCanceled():
            return {}
        context = dataobjects.createContext(feedback=feedback)
        out = processing.run(
            model,
            {param: "memory:" for param in self.modelParameters(model)},
            feedback=feedback,
            context=context,
        )
        # not sure exactly when, but on 3.16 LTR output from model runs include
        # new items on it. these new items break our implementation =)
        # hence the popitems
        out.pop("CHILD_INPUTS", None)
        out.pop("CHILD_RESULTS", None)
        if not self.loadOutput():
            return out
        flagLayerNames = self.flagLayerNames()
        for name, vl in out.items():
            if vl is None:
                continue
            if not isinstance(vl, QgsMapLayer) or not vl.isValid():
                continue
            vl.setName(name.split(":", 2)[-1])
            if vl.name() in flagLayerNames and vl.featureCount() == 0:
                continue
            self.addLayerToGroup(vl, "DSGTools_QA_Toolbox", model.displayName())
            self.enableFeatureCount(vl)
        return out

    def enableFeatureCount(self, lyr):
        root = QgsProject.instance().layerTreeRoot()
        lyrNode = root.findLayer(lyr.id())
        lyrNode.setCustomProperty("showFeatureCount", True)

    def export(self, filepath):
        """
        Dumps model parameters as a JSON file.
        :param filepath: (str) path to JSON file.
        :return: (bool) operation success.
        """
        with open(filepath, "w", encoding="utf-8") as fp:
            fp.write(json.dumps(self._param, sort_keys=True, indent=4))
        return os.path.exists(filepath)

    def asDict(self):
        """
        Dumps model parameters as a dict. Returns a copy of current parameters
        and modifications on the output does not modify this object.
        :return: (dict) DSGTools processing model definitions.
        """
        return dict(self._param)

    def run(self):
        """
        Method reimplemented in order to run models in thread as a QgsTask.
        :return: (bool) task success status.
        """
        start = time()
        try:
            if not self.feedback.isCanceled() or not self.isCanceled():
                self.output = {"result": dict(), "status": True, "errorMessage": ""}
                for paramName, vl in self.runModel(self.feedback).items():
                    baseName = paramName.rsplit(":", 1)[-1]
                    name = baseName
                    idx = 1
                    while name in self.output["result"]:
                        name = "{0} ({1})".format(baseName, idx)
                        idx += 1
                    # print(vl)
                    vl.setName(name)
                    # print("PASSED")
                    self.output["result"][name] = vl
        except Exception as e:
            self.output = {
                "result": {},
                "status": False,
                "errorMessage": self.tr("Model has failed:\n'{error}'").format(
                    error=str(e)
                ),
            }
        self.output["executionTime"] = time() - start
        return self.output["status"]

    def hasFlags(self):
        """
        Iterates over the results and finds if there are flags.
        """
        for key, lyr in self.output["result"].items():
            if (
                key in self._param["flags"]["flagLayerNames"]
                and isinstance(lyr, QgsMapLayer)
                and lyr.featureCount() > 0
            ):
                return True
        return False

    def finished(self, result):
        """
        Reimplemented from parent QgsTask. Method works a postprocessing one,
        always called right after run is finished (read the docs on QgsTask).
        :param result: (bool) run returned valued.
        """
        if self.isCanceled():
            return
        if result and self.onFlagsRaised() == "halt" and self.hasFlags():
            self.cancel()
            self.feedback.cancel()
            self.output["finishStatus"] = "halt"
        elif not result:
            self.output["finishStatus"] = "failed"
        else:
            self.output["finishStatus"] = "finished"
        self.modelFinished.emit(self)
