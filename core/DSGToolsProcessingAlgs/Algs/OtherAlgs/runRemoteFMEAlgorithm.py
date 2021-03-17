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
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from ...algRunner import AlgRunner
import processing
import os
import requests
from time import sleep
from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsFeature,
                       QgsDataSourceUri,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterVectorLayer,
                       QgsWkbTypes,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingUtils,
                       QgsSpatialIndex,
                       QgsGeometry,
                       QgsProcessingParameterField,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterExpression,
                       QgsProcessingException,
                       QgsProcessingParameterString,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterType)


class RunRemoteFMEAlgorithm(QgsProcessingAlgorithm):
    FME_MANAGER = 'FME_MANAGER'

    def getStatus(self, server, url):
        try:
            os.environ['NO_PROXY'] = server
            response = requests.get(url)
            # ['status'] 1 -- rodando, 2 -- executado, 3 -- erro
            return response.json()['data']
        except Exception as e:
            return e

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        managerParameter = ParameterFMEManager(
            self.FME_MANAGER,
            description=self.tr('FME Manager Parameters')
        )
        managerParameter.setMetadata({
            'widget_wrapper': 'DsgTools.gui.ProcessingUI.fmeManagerWrapper.FMEManagerWrapper'
        })
        self.addParameter(managerParameter)

    def parameterAsFMEManager(self, parameters, name, context):
        return parameters[name]

    def processAlgorithm(self, parameters, context, feedback):
        """
        Directs algorithm to its actual version.
        """
        fmeDict = self.parameterAsFMEManager(parameters, self.FME_MANAGER, context)

        if fmeDict.get('version') == 'v1':
            self.runFMEAlgorithmV1(fmeDict, feedback)
        elif fmeDict.get('version') == 'v2':
            self.runFMEAlgorithmV2(fmeDict, feedback)

        return {}

    def runFMEAlgorithmV1(self, fmeDict, feedback):
        """
        Runs first version
        """
        url = '{server}/versions/{workspace_id}/jobs'.format(
            server=fmeDict['server'],
            workspace_id=fmeDict['workspace_id']
        )
        response = requests.post(
            url,
            json=fmeDict['parameters'],
            proxies=fmeDict['proxy_dict'],
            auth=fmeDict['auth'],
            verify=False
        )
        url_to_status = '{server}/jobs/{uuid}'.format(
            server=fmeDict['server'],
            uuid=response.json()['data']['job_uuid'])
        while True:
            if feedback.isCanceled():
                feedback.pushInfo(self.tr('Canceled by user.\n'))
                break
            sleep(3)
            response = requests.get(
                url_to_status,
                proxies=fmeDict['proxy_dict'],
                auth=fmeDict['auth']
            )
            if response.json()['data']['status'] == 2:
                feedback.pushInfo(self.tr('Workspace {0} completed with success.\n').format(
                    response.json()['data']['workspace']))
                for flags in response.json()['data']['log'].split('|'):
                    feedback.pushInfo(self.tr('Number of flags: {0}\n').format(
                        flags))
                break
            if response.json()['data']['status'] == 3:
                feedback.pushInfo(self.tr('Task completed with error.\n'))
                break

    def runFMEAlgorithmV2(self, fmeDict, feedback):
        """
        Runs second version
        """
        url = '{server}/api/rotinas/{workspace_id}/execucao'.format(
            server=fmeDict['server'],
            workspace_id=fmeDict['workspace_id']
        )
        response = requests.post(
            url,
            json=fmeDict['parameters'],
            proxies=fmeDict['proxy_dict'],
            auth=fmeDict['auth'],
            verify=False
        )
        url_to_status = '{server}/api/execucoes/{uuid}'.format(
            server=fmeDict['server'],
            uuid=response.json()['dados']['job_uuid'])

        while True:
            if feedback.isCanceled():
                feedback.pushInfo(self.tr('Canceled by user.\n'))
                break
            sleep(3)
            response = requests.get(
                url_to_status,
                proxies=fmeDict['proxy_dict'],
                auth=fmeDict['auth'],
                verify=False
            )
            if response.json()['dados']['status_id'] == 2:
                feedback.pushInfo(self.tr('Workspace {0} completed with success.\n').format(
                    response.json()['dados']['rotina']))
                for flags in response.json()['dados']['sumario']:
                    feedback.pushInfo(self.tr('Number of flags in {0}: {1}\n').format(
                        flags['classes'], flags['feicoes']))
                break
            if response.json()['dados']['status_id'] == 3:
                feedback.pushInfo(self.tr('Task completed with error.\n'))
                break

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'runremotefme'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Run Remote FME Workspace')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Other Algorithms')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Other Algorithms'

    def tr(self, string):
        return QCoreApplication.translate('RunRemoteFMEAlgorithm', string)

    def createInstance(self):
        return RunRemoteFMEAlgorithm()


class ParameterFMEManagerType(QgsProcessingParameterType):

    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterFMEManager(name)

    def metadata(self):
        return {'widget_wrapper': 'DsgTools.gui.ProcessingUI.fmeManagerWrapper.FMEManagerWrapper'}

    def name(self):
        return QCoreApplication.translate('Processing', 'FME Manager Parameters')

    def id(self):
        return 'fme_manager'

    def description(self):
        return QCoreApplication.translate('Processing', 'FME Manager parameters. Used on Run Remote FME Workspace')


class ParameterFMEManager(QgsProcessingParameterDefinition):

    def __init__(self, name, description=''):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterFMEManager(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @ staticmethod
    def typeName():
        return 'fme_manager'

    def checkValueIsAcceptable(self, value, context=None):
        return True

    def valueAsPythonString(self, value, context):
        return str(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @ classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()
