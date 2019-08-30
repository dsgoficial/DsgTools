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

from qgis.core import (QgsProcessingModelAlgorithm,
                       QgsTask,
                       QgsProcessingFeedback)
from qgis.PyQt.QtCore import QObject
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

    def __init__(self, parameters, taskName=None, flags=None, feedback=None):
        """
        Class constructor.
        :param parameters: (dict) map of attributes for a model.
        :param taskName: (str) name to be exposed on progress bar.
        :param flags: (list) a list of QgsTask flags to be set to current model.
        """
        super(DsgToolsProcessingModel, self).__init__(
            taskName or QObject().tr("DSGTools Validation Model"),
            QgsTask.CanCancel if flags is None else flags
        )
        self._param = {} if self.validateParameters(parameters) else parameters
        self.feedback = feedback or QgsProcessingFeedback()
        self.feedback.progressChanged.connect(self.setProgress)
        self.feedback.canceled.connect(self.cancel)
        self.output = {
            "result" : dict(),
            "status" : False,
            "executionTime" : .0,
            "errorMessage" : self.tr("Thread not started yet.")
        }

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
                "enableLocalFlags" : False
            }
        if "source" not in parameters or not parameters["source"]:
            return self.tr("Model source is not defined.")
        if "type" not in parameters["source"] or \
          parameters["source"]["type"] not in self.MODEL_TYPES:
            return self.tr("Input model type is not supported (or missing).")
        if "data" not in parameters["source"] or \
          not parameters["source"]["data"]:
            return self.tr("Input model source was not identified.")

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
        with open(temp, "w") as xmlFile:
            xmlFile.write(xml)
        alg = DsgToolsProcessingModel.modelFromFile(temp)
        os.remove(temp)
        return alg

    def isValid(self):
        """
        Checks whether current model is a valid instance of DSGTools processing
        model.
        :return: (bool) validity status.
        """
        return self._param != dict()

    def _data(self):
        """
        Current model's source data. If it's from a file, it's its filepath,
        if from an XML, its contents.
        :return: (str) model's source data.
        """
        return self._param["source"]["data"] if self.isValid() else ""    

    def displayName(self):
        """
        Current model's source data. If it's from a file, it's its filepath,
        if from an XML, its contents.
        :return: (str) model's source data.
        """
        if not self.isValid():
            return ""
        return self._param["displayName"] if "displayName" in self._param \
                 else self.model().displayName()

    def name(self):
        """
        Proxy method for displayName.
        :return: (str) display name.
        """
        return self.displayName()

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
        modelType = self._param["source"]["type"]
        return method[modelType](self._data()) if modelType in method\
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

    def runModel(self):
        """
        Executes current model.
        :return: ?
        """
        # this tool understands every parameter to be filled as an output LAYER
        # it also sets all output to a MEMORY LAYER.
        model = self.model()
        out = processing.run(
            model,
            {param : "memory:" for param in self.modelParameters(model)},
            feedback=self.feedback
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

    def exportAsDict(self):
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
                "result" : self.runModel(),
                "status" : True,
                "errorMessage" : ""
            }
        except Exception as e:
            self.output = {
                "result" : {},
                "status" : False,
                "errorMessage" : self.tr("Model has failed:\n'{error}'").format(str(e))
            }
        self.output["executionTime"] = time() - start
        return self.output["status"]
