# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2018-12-13
        git sha              : $Format:%H$
        copyright            : (C) 2018 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import os
import requests
from time import sleep

from qgis.core import (QgsProcessingAlgorithm,
                       QgsProcessingException,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterType)
from qgis.PyQt.QtCore import QCoreApplication


class RunRemoteFMEAlgorithm(QgsProcessingAlgorithm):
    FME_MANAGER = "FME_MANAGER"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        managerParameter = ParameterFMEManager(
            self.FME_MANAGER,
            description=self.tr("FME Manager Parameters")
        )
        managerParameter.setMetadata({
            "widget_wrapper": "DsgTools.gui.ProcessingUI.fmeManagerWrapper.FMEManagerWrapper"
        })
        self.addParameter(managerParameter)

    def parameterAsFMEManager(self, parameters, name, context):
        return parameters[name]

    def getRequestFromServer(
            self, url, proxyInfo=None, proxyAuth=None, useSsl=False,
            useProxy=False, timeout=None):
        """
        Sends a POST request to the FME Manager server.
        :param url: (str) FME Manager server's URL.
        :param proxyInfo: (dict) a mapping from supported schemas to its
                          appropriate proxy URL.
        :param proxyAuth: (HTTPProxyAuth) proxy authentication credentials
                          object.
        :param useSsl: (bool) whether connection to server is verified /
                       secured with SSL.
        :param useProxy: (bool) whether connection requires a proxy.
        :param timeout: (int) maximum time in seconds for the connection
                        request attempt.
        :return: (dict) requested data as JSON.
        """
        try:
            if useProxy:
                resp = requests.get(
                    url,
                    proxies=proxyInfo,
                    auth=proxyAuth,
                    verify=useSsl,
                    timeout=timeout or 15
                )
            else:
                resp = requests.get(url, verify=useSsl, timeout=timeout or 15)
        except BaseException as e:
            raise QgsProcessingException(
                self.tr("Unable to get the routine's output from "
                        "FME Manager: '{0}'".format(e))
            )
        return resp.json()

    def postRequestFromServer(
            self, url, fmeParameters, proxyInfo=None, proxyAuth=None,
            useSsl=False, useProxy=False, timeout=None):
        """
        Sends a POST request to the FME Manager server.
        :param url: (str) FME Manager server's URL.
        :param fmeParameters: (dict) the set of parameters mapping for the
                              routine to be run on FME Manager.
        :param proxyInfo: (dict) a mapping from supported schemas to its
                          appropriate proxy URL.
        :param proxyAuth: (HTTPProxyAuth) proxy authentication credentials
                          object.
        :param useSsl: (bool) whether connection to server is verified /
                       secured with SSL.
        :param useProxy: (bool) whether connection requires a proxy.
        :param timeout: (int) maximum time in seconds for the connection
                        request attempt.
        :return: (dict) requested data as JSON.
        """
        try:
            if useProxy:
                resp = requests.post(
                    url,
                    json=fmeParameters,
                    proxies=proxyInfo,
                    auth=proxyAuth,
                    verify=useSsl,
                    timeout=timeout or 15
                )
            else:
                resp = requests.post(
                    url,
                    json=fmeParameters,
                    verify=useSsl,
                    timeout=timeout or 15
                )
        except BaseException as e:
            raise QgsProcessingException(
                self.tr("Unable to send processing request to "
                        "FME Manager: '{0}'".format(e))
            )
        return resp.json()

    def parseLog(self, summaryOutput, version):
        """
        Parses the log from an FME workspace job executed on FME Manager.
        :param summaryOutput: (str / list-of-dict) string containing an output
                              message using '|' as separator for V1. On its V2,
                              FME Manager outputs a mapping for flag counting
                              for each output layer.
        :version: (str) either v1 or v2, string that identifies FME Manager's
                  version on which the workspace was run.
        :return: (? / list-of-dict) mapping from layer output to feature count (flags).
        """
        if version == "v1":
            return summaryOutput.split("|")
        return summaryOutput

    def processAlgorithm(self, parameters, context, feedback):
        """
        Directs algorithm to its actual version.
        """
        fmeDict = self.parameterAsFMEManager(parameters, self.FME_MANAGER, context)
        version = fmeDict.get("version")
        if version == "v1":
            url = "{server}/versions/{workspace_id}/jobs".format(
                server=fmeDict["server"],
                workspace_id=fmeDict["workspace_id"]
            )
            url_to_status = "{server}/jobs/{{uuid}}".format(
                server=fmeDict["server"])
            dataKey = "data"
            jobNameKey = "workspace"
            summaryKey = "log"
            statusKey = "status"
        else:
            url = "{server}/api/rotinas/{workspace_id}/execucao".format(
                server=fmeDict["server"],
                workspace_id=fmeDict["workspace_id"]
            )
            url_to_status = "{server}/api/execucoes/{{uuid}}".format(
                server=fmeDict["server"])
            dataKey = "dados"
            jobNameKey = "rotina"
            summaryKey = "sumario"
            statusKey = "status_id"
        feedback.pushInfo(self.tr("Requesting server to run the workspace..."))
        jobRequest = self.postRequestFromServer(
            url,
            fmeDict.get("parameters"),
            fmeDict.get("proxy_dict"),
            fmeDict.get("auth"), 
            fmeDict.get("use_ssl"),
            fmeDict.get("use_proxy")
        )
        feedback.pushInfo(
            self.tr("Request successful. Waiting for the workspace to "
                    "be executed...")
        )
        url_to_status = url_to_status.format(
            uuid=jobRequest[dataKey]["job_uuid"])
        while True:
            if feedback.isCanceled():
                feedback.pushInfo(self.tr("Canceled by user.\n"))
                break
            sleep(3)
            jobOutput = self.getRequestFromServer(
                url_to_status,
                fmeDict.get("proxy_dict"),
                fmeDict.get("auth"), 
                fmeDict.get("use_ssl"),
                fmeDict.get("use_proxy")
            )
            outputData = jobOutput.get(dataKey)
            statusId = outputData.get(statusKey)
            if statusId == 2:
                feedback.pushInfo(
                    self.tr("Workspace {0} completed with success.\n")\
                        .format(outputData[jobNameKey])
                )
                for flags in self.parseLog(outputData[summaryKey], version):
                    if version == "v1":
                        msg = self.tr("Number of flags: {0}\n").format(flags)
                    else:
                        msg = self.tr("Number of flags in {0}: {1}\n")\
                                .format(flags["classes"], flags["feicoes"])
                    feedback.pushInfo(msg)
                break
            if statusId == 3:
                feedback.reportError(self.tr("Task completed with error.\n"))
                break

        return {'result': jobOutput}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "runremotefme"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Run Remote FME Workspace")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Other Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Other Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("RunRemoteFMEAlgorithm", string)

    def createInstance(self):
        return RunRemoteFMEAlgorithm()


class ParameterFMEManagerType(QgsProcessingParameterType):

    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterFMEManager(name)

    def metadata(self):
        return {"widget_wrapper": "DsgTools.gui.ProcessingUI.fmeManagerWrapper.FMEManagerWrapper"}

    def name(self):
        return QCoreApplication.translate("Processing", "FME Manager Parameters")

    def id(self):
        return "fme_manager"

    def description(self):
        return QCoreApplication.translate("Processing", "FME Manager parameters. Used on Run Remote FME Workspace")


class ParameterFMEManager(QgsProcessingParameterDefinition):

    def __init__(self, name, description=""):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterFMEManager(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return "fme_manager"

    def checkValueIsAcceptable(self, value, context=None):
        if not (value["server"] and value["workspace_id"]):
            return False
        return True

    def valueAsPythonString(self, value, context):
        return str(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()