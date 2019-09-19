# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2019-09-18
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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
from PyQt5.QtCore import QCoreApplication

from DsgTools.core.dsgEnums import DsgEnums
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.Factories.LayerLoaderFactory.layerLoaderFactory import \
    LayerLoaderFactory
import processing
from qgis.core import (QgsCoordinateReferenceSystem, QgsCoordinateTransform,
                       QgsDataSourceUri, QgsFeature, QgsFeatureSink, QgsField,
                       QgsFields, QgsGeometry, QgsProcessing,
                       QgsProcessingAlgorithm, QgsProcessingException,
                       QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputMultipleLayers,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterCrs,
                       QgsProcessingParameterDefinition,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterExpression,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField, QgsProcessingParameterFile,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterString,
                       QgsProcessingParameterType,
                       QgsProcessingParameterVectorLayer, QgsProcessingUtils,
                       QgsProject, QgsSpatialIndex, QgsWkbTypes)
from qgis.utils import iface

class LoadNonSpatialLayersFromPostgreSQLAlgorithm(QgsProcessingAlgorithm):
    HOST = 'HOST'
    PORT = 'PORT'
    DATABASE = 'DATABASE'
    USER = 'USER'
    PASSWORD = 'PASSWORD'
    LAYER_LIST = 'LAYER_LIST'
    LOAD_TO_CANVAS = 'LOAD_TO_CANVAS'
    UNIQUE_LOAD = 'UNIQUE_LOAD'
    SCHEMA_NAME = 'SCHEMA_NAME'
    OUTPUT = 'OUTPUT'
    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterString(
                self.HOST,
                self.tr('Host')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.PORT,
                self.tr('Port')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.DATABASE,
                self.tr('Database')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.USER,
                self.tr('User')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.PASSWORD,
                self.tr('Password')
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.LAYER_LIST,
                self.tr('Layer List')
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.LOAD_TO_CANVAS,
                self.tr('Load layers to canvas'),
                defaultValue=True
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.UNIQUE_LOAD,
                self.tr('Unique load'),
                defaultValue=True
            )
        )
        self.addParameter(
            QgsProcessingParameterString(
                self.SCHEMA_NAME,
                self.tr('Schema name')
            )
        )
        self.addOutput(
            QgsProcessingOutputMultipleLayers(
                self.OUTPUT,
                self.tr('Loaded layers')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        host = self.parameterAsString(
            parameters,
            self.HOST,
            context
        )
        port = self.parameterAsString(
            parameters,
            self.PORT,
            context
        )
        database = self.parameterAsString(
            parameters,
            self.DATABASE,
            context
        )
        user = self.parameterAsString(
            parameters,
            self.USER,
            context
        )
        password = self.parameterAsString(
            parameters,
            self.PASSWORD,
            context
        )
        layerStringList = self.parameterAsString(
            parameters,
            self.LAYER_LIST,
            context
        )
        loadToCanvas = self.parameterAsBoolean(
            parameters,
            self.LOAD_TO_CANVAS,
            context
        )
        uniqueLoad = self.parameterAsBoolean(
            parameters,
            self.UNIQUE_LOAD,
            context
        )
        tableSchema = self.parameterAsString(
            parameters,
            self.SCHEMA_NAME,
            context
        )
        abstractDb = self.getAbstractDb(host, port, database, user, password)
        inputParamList = [(tableSchema, i) for i in layerStringList.split(',')]
        layerLoader = LayerLoaderFactory().makeLoader(
            iface, abstractDb
        )
        if loadToCanvas:
            iface.mapCanvas().freeze(True)
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        outputLayers = layerLoader.loadLayersInsideProcessing(
            inputParamList,
            uniqueLoad=uniqueLoad,
            addToCanvas=loadToCanvas,
            nonSpatial=True,
            feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(1)
        output = processing.run(
            'dsgtools:grouplayers',
            {
                'INPUT_LAYERS' : outputLayers,
                'CATEGORY_EXPRESSION' : "to_string('{name}')".format(
                        name=tableSchema
                    ),
                'OUTPUT' : ':memory'
            },
            context=context,
            feedback=multiStepFeedback
        )
        if loadToCanvas:
            iface.mapCanvas().freeze(False)
        return {self.OUTPUT: [i.id() for i in outputLayers]}
    
    def getAbstractDb(self, host, port, database, user, password):
        abstractDb = DbFactory().createDbFactory(DsgEnums.DriverPostGIS)
        abstractDb.connectDatabaseWithParameters(
            host, port, database, user, password
        )
        return abstractDb

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'LoadNonSpatialLayersFromPostgreSQLAlgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Load Non-Spatial Layers From PostgreSQL')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Layer Management Algorithms')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Layer Management Algorithms'

    def tr(self, string):
        return QCoreApplication.translate('LoadNonSpatialLayersFromPostgreSQLAlgorithm', string)

    def createInstance(self):
        return LoadNonSpatialLayersFromPostgreSQLAlgorithm()

    def flags(self):
        """
        This process is not thread safe due to the fact that removeChildNode
        method from QgsLayerTreeGroup is not thread safe.
        """
        return super().flags() | QgsProcessingAlgorithm.FlagNoThreading
