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

from qgis.core import (QgsTask,
                       QgsProject,
                       QgsMapLayer,
                       QgsLayerTreeLayer,
                       QgsProcessingFeedback,
                       QgsProcessingModelAlgorithm)
from qgis.PyQt.QtCore import pyqtSignal
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
    modelFinished = pyqtSignal()
    modelFailed = pyqtSignal()
    flagsRaisedWarning = pyqtSignal()

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
            "", QgsTask.CanCancel if flags is None else flags
        )
        self._name = name
        self._param = {} if self.validateParameters(parameters) else parameters
        self.setDescription(taskName or self.displayName())
        self.feedback = feedback or QgsProcessingFeedback()
        self.feedback.progressChanged.connect(lambda x : self.setProgress(int(x)))
        self.feedback.canceled.connect(self.cancel)
        self.output = {
            "result" : dict(),
            "status" : False,
            "executionTime" : .0,
            "errorMessage" : self.tr("Thread not started yet.")
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
                "onFlagsRaised" : "halt",
                "enableLocalFlags" : False,
                "loadOutput" : False
            }
        if "source" not in parameters or not parameters["source"]:
            return self.tr("Model source is not defined.")
        if "type" not in parameters["source"] or \
          parameters["source"]["type"] not in self.MODEL_TYPES:
            return self.tr("Input model type is not supported (or missing).")
        if "data" not in parameters["source"] or \
          not parameters["source"]["data"]:
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
        temp = "./temp_model_{0}.model3".format(hash(time()))
        with open(temp, "w+", encoding="utf-8") as xmlFile:
            xmlFile.write(xml)
        alg = DsgToolsProcessingModel.modelFromFile(temp)
        os.remove(temp)
        return alg

    def metadata(self):
        """
        A map to Worflow's metadata.
        :return: (dict) metadata.
        """
        meta = dict()
        def checkMeta(key):
            return "metadata" in self._param and key in self._param["metadata"]
        for k in ["author", "version", "lastModified"]:
            meta[k] = self._param["metadata"][k] if checkMeta(k) else ""
        return meta

    def author(self):
        """
        Retrieves the model's author name, if available.
        :return: (str) author name.
        """
        if "metadata" not in self._param:
            return ""
        meta = self._param["metadata"]
        return meta["author"] if "author" in meta else ""

    def version(self):
        """
        Retrieves the model's author name, if available.
        :return: (str) author name.
        """
        if "metadata" not in self._param:
            return ""
        meta = self._param["metadata"]
        return meta["version"] if "version" in meta else ""

    def originalName(self):
        """
        When a model is imported from a file-based model, one might want to
        store the original model's name.
        :return: (str) original model's name.
        """
        if "metadata" not in self._param:
            return ""
        meta = self._param["metadata"]
        return meta["originalName"] if "originalName" in meta else ""

    def metadataText(self):
        """
        Retrieves Workflow's metadata string.
        :return: (str) Workflow's metadata string.
        """
        if "metadata" not in self._param:
            return ""
        return self.tr(
            "Model {name} v{version} ({lastModified}) by {author}."
        ).format(name=self.displayName(), **self.metadata())

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
        return self._param["displayName"] if "displayName" in self._param else \
                self.tr("DSGTools Validation Model ({0})").format(self.name())

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
            "xml" : DsgToolsProcessingModel.modelFromXml,
            "file" : DsgToolsProcessingModel.modelFromFile
        }
        return method[self.source()](self.data()) if self.source() in method\
             else QgsProcessingModelAlgorithm()

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

    def loadOutput(self):
        """
        Model behavior when running on a Workflow if flags are raised.
        :return: (str) model behaviour on Workflow.
        """
        return self.flags()["loadOutput"] if self.flags() else False

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
            alg.algorithm().displayName() \
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
        return [
            param.name() \
                for param in model.parameterDefinitions()
        ]

    def addLayerToGroup(self, layer, groupname, subgroupname=None):
        """
        Adds a layer to a group into layer panel.
        :param layer: (QgsMapLayer) layer to be added to canvas.
        :param groupname: (str) name for group to nest the layer.
        :param subgroupname: (str) name for the subgroup to be added.
        """
        root = QgsProject.instance().layerTreeRoot()
        for g in root.children():
            if g.name() == groupname:
                group = g
                break
        else:
            group = root.addGroup(groupname)
        if subgroupname is not None:
            for sg in group.children():
                if sg.name() == subgroupname:
                    subgroup = sg
                    break
            else:
                subgroup = group.addGroup(subgroupname)
        QgsProject.instance().addMapLayer(layer, False)
        subgroup.insertChildNode(1, QgsLayerTreeLayer(layer))

    def runModel(self):
        """
        Executes current model.
        :return: (dict) map to model's outputs.
        """
        # this tool understands every parameter to be filled as an output LAYER
        # it also sets all output to a MEMORY LAYER.
        model = self.model()
        out = processing.run(
            model,
            { param : "memory:" for param in self.modelParameters(model) },
            feedback=self.feedback
        )
        if self.loadOutput():
            for vl in out.values():
                if isinstance(vl, QgsMapLayer):
                    self.addLayerToGroup(
                        vl,
                        self.tr("DSGTools Quality Assurance Models"),
                        model.displayName()
                    )
        return out

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
        Dumps model parameters as a JSON file.
        :param filepath: (str) path to JSON file.
        :return: (dict) DSGTools processing model definitions.
        """
        return self._param

    def run(self):
        """
        Method reimplemented in order to run models in thread as a QgsTask.
        :return: (bool) task success status.
        """
        start = time()
        time
        try:
            self.output = {
                "result" : { k.split(":", 2)[-1] : v for k, v in self.runModel().items() },
                "status" : True,
                "errorMessage" : ""
            }
            self.modelFinished.emit()
        except Exception as e:
            self.output = {
                "result" : {},
                "status" : False,
                "errorMessage" : self.tr("Model has failed:\n'{error}'")\
                                 .format(error=str(e))
            }
            self.modelFailed.emit()
        self.output["executionTime"] = time() - start
        return self.output["status"]
