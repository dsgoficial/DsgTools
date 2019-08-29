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

from qgis.PyQt.QtCore import QObject

from DsgTools.core.DSGToolsProcessingAlgs.Models.dsgToolsProcessingModel import DsgToolsProcessingModel

class ValidationWorkflow(QObject):
    """
    Works as a multi-model runner. Understands all models' parameters as an
    output vector layer.
    """
    def __init__(self, parameters):
        """
        Class constructor. Materializes an workflow set of parameters.
        :param parameters: (dict) map of workflow attributes.
        """
        super(ValidationWorkflow, self).__init__()
        msg = self.validateParameters(parameters)
        if msg:
            raise Exception(
                self.tr("Invalid workflow parameter:\n{msg}").format(msg=msg)
            )
        self._param = parameters

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
            return self.tr("This workflow seems to have no models associated to it.")
        # if "flagLayer" not in parameters or not parameters["flagLayer"]:
        #     self.tr("No flag layer was provided.")
        # if "historyLayer" not in parameters or not parameters["historyLayer"]:
        #     self.tr("No history layer was provided.")
        return ""

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
        for modelName, modelParam in self._param["models"].items():
            model = DsgToolsProcessingModel(modelParam)
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
        for modelName, modelParam in self._param["models"].items():
            model = DsgToolsProcessingModel(modelParam)
            if model.isValid():
                models[modelName] = model
        return models

    def invalidModels(self):
        """
        Returns all valid models from workflow parameters.
        :return: (dict) models maps invalid models to their invalidation reason.
        """
        models = dict()
        for modelName, modelParam in self._param["models"].items():
            model = DsgToolsProcessingModel(modelParam)
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
            model = DsgToolsProcessingModel(modelParam)
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

    def exportAsDict(self):
        """
        Dumps model parameters as a JSON file.
        :param filepath: (str) path to JSON file.
        :return: (dict) DSGTools processing model definitions.
        """
        return self._param
