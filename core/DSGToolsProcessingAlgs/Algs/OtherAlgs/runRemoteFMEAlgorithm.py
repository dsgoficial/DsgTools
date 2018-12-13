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
import processing, os, requests
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
                       QgsProcessingParameterString)

class RunRemoteFMEAlgorithm(QgsProcessingAlgorithm):
    SERVER = 'SERVER'
    JOB = 'JOB'
    DBAREA = 'DBAREA'
    DBNAME = 'DBNAME'
    DBPORT = 'DBPORT'
    DBHOST = 'DBHOST'


    def get(self, host, url, header={}):
        try:
            os.environ['NO_PROXY'] = host
            response = requests.get(url, headers=header)
            return response
        except requests.exceptions.InvalidURL:
            return 1
        except requests.exceptions.ConnectionError:
            return 2
    
    def getStatus(self, server, url):
        try:
            os.environ['NO_PROXY'] = server
            response = requests.get(url)
            #['status'] 1 -- rodando, 2 -- executado, 3 -- erro
            return response.json()['data']
        except Exception as e:
            return e 
    
    def get_post_data(self, rotine_data, geomUnit, db_data):
        postData = {}
        for parameter in rotine_data['parameters']:
            if 'dbarea' in parameter:
                postData[parameter] = geomUnit
            elif 'dbname' in parameter:
                postData[parameter] = db_data['dbname']
            elif 'dbport' in parameter:
                postData[parameter] = db_data['port']
            elif 'dbhost' in parameter:
                postData[parameter] = db_data['host']
            else:
                postData[parameter] = ''
        return postData

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterString(
                self.SERVER,
                self.tr('Server address')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.JOB,
                self.tr('Job')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.DBHOST,
                self.tr('Output database host')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.DBPORT,
                self.tr('Output database port')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.DBNAME,
                self.tr('Output database name')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.DBAREA,
                self.tr('Wkt Spatial Area'),
                optional=True
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        server = self.parameterAsString(parameters, self.SERVER, context)
        if server is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.SERVER))
        rotineId = self.parameterAsString(parameters, self.JOB, context)
        if rotineId is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.JOB))
        dbhost = self.parameterAsString(parameters, self.DBHOST, context)
        if rotineId is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.DBHOST))
        dbport = self.parameterAsString(parameters, self.DBPORT, context)
        if dbport is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.DBPORT))
        dbname = self.parameterAsString(parameters, self.DBNAME, context)
        if rotineId is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.DBNAME))
        dbarea = self.parameterAsString(parameters, self.DBAREA, context)
        dbarea = dbarea if not dbarea else ''
        os.environ["NO_PROXY"] = server
        url = 'http://{0}/versions/{1}/jobs'.format(
                server,
                rotineId
            )
        postData = {
            'parameters' : {
                'dbport' : dbport,
                'dbhost' : dbhost,
                'dbname' : dbname,
                'dbarea' : dbarea
            }
        }
        response = requests.post(url, json=postData)

        url_to_status = 'http://{0}/jobs/{1}'.format(
            server, 
            response.json()['data']['job_uuid']
        )
        while True:
            if feedback.isCanceled():
                feedback.pushInfo(self.tr('Canceled by user.\n'))
                break
            sleep(3)
            response = requests.get(url_to_status)
            if response.json()['data']['status']== 2:
                feedback.pushInfo(self.tr('Workspace {0} completed with success.\n').format(response['workspace_name']))
                for flags in response.json()['log'].split('|'):
                    feedback.pushInfo(self.tr('Number of flags: {0}\n').format(flags))
                break
            if response.json()['data']['status'] == 3:
                feedback.pushInfo(self.tr('Task completed with error.\n'))
                break

        return {}

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
        return self.tr('Run Remote FME')

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
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return RunRemoteFMEAlgorithm()