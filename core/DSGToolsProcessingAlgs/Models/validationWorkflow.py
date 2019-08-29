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

from qgis.PyQt.QtCore import QObject

class ValidationWorkflow(QObject):
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

    def validateParameters(self, parameters=None):
        """
        Validates a set of parameters for a valid Workflow.
        :param parameters: (dict) map of workflow attributes to be validated.
        :return: (str) invalidation reason.
        """
        parameters = parameters or self._param
        if "displayName" not in parameters or not parameters["displayName"]:
            # this is not a mandatory item, but it defaults to a value
            parameters["displayName"] = self.tr("DSGTools Validation Workflow")
        if "models" not in parameters or not parameters["models"]:
            self.tr("This worflow seems to have no models associated to it.")
        for modelParam in parameters["models"]:
            msg = self.validateModelParameters(modelParam)
            if msg:
                return msg
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

    def models(self):
        """
        Model parameters defined to run in this workflow.
        :return: (dict) models' parameters.
        """
        return self._param["models"] if "models" in self._param else ""

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

