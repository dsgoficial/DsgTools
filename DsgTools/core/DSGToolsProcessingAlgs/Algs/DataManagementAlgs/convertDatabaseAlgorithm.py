# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-12-02
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import fnmatch
import json
from typing import Any, Dict, List, Optional
from PyQt5.QtCore import QVariant, QMetaType, QDateTime
from DsgTools.core.DSGToolsProcessingAlgs.Algs.DataManagementAlgs.abstractConvertDatabaseAlgorithm import AbstractDatabaseAlgorithm
from DsgTools.core.DSGToolsProcessingAlgs.Algs.DataManagementAlgs.conversionParameterTypes import ParameterDbConversion
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.DbTools.dbConversionHandler import (
    FeatureProcessor,
    MappingFeatureProcessor,
    convert_features,
    write_output_features,
)
from DsgTools.core.Factories.DbFactory.abstractDb import AbstractDb
from DsgTools.core.Factories.DbFactory.dbFactory import DbFactory
from DsgTools.core.Factories.LayerLoaderFactory.layerLoaderFactory import (
    LayerLoaderFactory,
)
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingException,
    QgsProviderConnectionException,
    QgsWkbTypes,
    QgsWkbTypes,
    QgsProviderRegistry,
    QgsProject,
    QgsProcessingParameterProviderConnection,
    QgsProcessingAlgorithm,
    QgsProcessingParameterGeometry,
    QgsDataSourceUri,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterDefinition,
    QgsProcessingParameterType,
    QgsVectorLayer,
    QgsProcessingFeedback,
    QgsProcessingParameterFeatureSink,
    QgsProcessingContext,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterString,
    QgsProcessingFeatureSource,
    QgsFields,
    QgsField,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsCoordinateReferenceSystem,
)
from qgis.utils import iface

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.dsgEnums import DsgEnums


class ConvertDatabasesAlgorithm(AbstractDatabaseAlgorithm):
    INPUT_DATABASE = "INPUT_DATABASE"
    INPUT_LAYERS_TO_EXCLUDE = "INPUT_LAYERS_TO_EXCLUDE"
    DESTINATION_DATABASE = "DESTINATION_DATABASE"
    CONVERSION_MAPS_STRUCTURE = "CONVERSION_MAPS_STRUCTURE"
    COMMIT_OUTPUT_FEATURES = "COMMIT_OUTPUT_FEATURES"
    GEOGRAPHIC_BOUNDS = "GEOGRAPHIC_BOUNDS"
    NOT_CONVERTED_POINT = "NOT_CONVERTED_POINT"
    NOT_CONVERTED_LINE = "NOT_CONVERTED_LINE"
    NOT_CONVERTED_POLYGON = "NOT_CONVERTED_POLYGON"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        origin_db_param = QgsProcessingParameterProviderConnection(
            self.INPUT_DATABASE,
            self.tr("Input Database (connection name)"),
            "postgres",
        )
        self.addParameter(origin_db_param)

        self.addParameter(
            QgsProcessingParameterString(
                self.INPUT_LAYERS_TO_EXCLUDE,
                description=self.tr(
                    "Input layers to be excluded (csv format, can use * patterns)"
                ),
                multiLine=False,
                defaultValue="aux_moldura_area_continua_a,delimitador*,centroide*",
                optional=True,
            )
        )

        destination_db_param = QgsProcessingParameterProviderConnection(
            self.DESTINATION_DATABASE,
            self.tr("Destination Database (connection name)"),
            "postgres",
        )
        self.addParameter(destination_db_param)

        hierarchy = ParameterDbConversion(
            self.CONVERSION_MAPS_STRUCTURE, description=self.tr("Conversion maps")
        )
        hierarchy.setMetadata(
            {
                "widget_wrapper": "DsgTools.gui.ProcessingUI.dbConversionWrapper.DbConversionWrapper"
            }
        )
        self.addParameter(hierarchy)

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDS,
                self.tr("Geographic Bounds"),
                [QgsWkbTypes.PolygonGeometry],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.COMMIT_OUTPUT_FEATURES,
                self.tr("Commit converted features to destination layers"),
                defaultValue=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.NOT_CONVERTED_POINT,
                self.tr("Points not converted"),
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.NOT_CONVERTED_LINE,
                self.tr("Lines not converted"),
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.NOT_CONVERTED_POLYGON,
                self.tr("Polygons not converted"),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.layerHandler = LayerHandler()
        self.algRunner = AlgRunner()
        inputConnectionName = self.parameterAsConnectionName(
            parameters, self.INPUT_DATABASE, context
        )
        layerExclusionFilter = self.parameterAsString(
            parameters, self.INPUT_LAYERS_TO_EXCLUDE, context
        )
        layerExclusionFilter = (
            layerExclusionFilter.split(",") if layerExclusionFilter else None
        )
        destinationConnectionName = self.parameterAsConnectionName(
            parameters, self.DESTINATION_DATABASE, context
        )
        conversionMapList = self.parameterAsConversionMapList(
            parameters, self.CONVERSION_MAPS_STRUCTURE, context
        )
        geographicBoundLyr = self.parameterAsVectorLayer(
            parameters, self.GEOGRAPHIC_BOUNDS, context
        )
        commitChanges = self.parameterAsBool(
            parameters, self.COMMIT_OUTPUT_FEATURES, context
        )
        nSteps = 6 + commitChanges
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(nSteps, feedback)
            if feedback is not None
            else None
        )
        currentStep = 0
        if inputConnectionName == destinationConnectionName:
            raise QgsProcessingException(self.tr("The destination connection must be different than the input connection!"))
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(
                self.tr("Loading layers with elements from input database")
            )
        inputLayerList = self.getLayersFromDbConnectionName(
            inputConnectionName,
            feedback=multiStepFeedback,
            context=context,
            layerExclusionFilter=layerExclusionFilter,
        )
        if len(inputLayerList) == 0:
            return {}
        currentStep += 1
        self.fields = self.fieldsFlag()
        outputCrs = self.getOutputCRS(destinationConnectionName)

        self.buildOutputSinks(parameters, context, outputCrs)

        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Clipping input layer list"))
        clippedLayerDict = self.prepareInputData(
            inputLayerList, geographicBoundLyr, outputCrs, context, multiStepFeedback
        )
        for lyr in inputLayerList:
            QgsProject.instance().removeMapLayer(lyr.id())
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        convertedFeatureDict = self.convertFeaturesWithConversionMaps(conversionMapList, clippedLayerDict, multiStepFeedback)

        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Loading output layers"))
        destinationLayerList = self.getLayersFromDbConnectionName(
            inputConnectionName=destinationConnectionName,
            feedback=multiStepFeedback,
            context=context,
            layerNameList=list(convertedFeatureDict.keys()),
            addToCanvas=True,
            withElements=False,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Writing to output"))
        outputLayerDict = {lyr.name(): lyr for lyr in destinationLayerList}
        notConvertedDict = write_output_features(
            {k.split(".")[-1]: v for k, v in convertedFeatureDict.items()},
            outputLayerDict=outputLayerDict,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        if len(notConvertedDict) > 0:
            stepSize = 100 / len(notConvertedDict)
            for geomType, featDictList in notConvertedDict.items():
                if multiStepFeedback.isCanceled():
                    break
                list(
                    map(
                        lambda x: self.flagSinkDict[geomType].addFeature(
                            self.buildFlagFeat(x), QgsFeatureSink.FastInsert
                        ),
                        featDictList,
                    )
                )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        if not commitChanges:
            return {
                self.NOT_CONVERTED_POINT: self.point_flag_id,
                self.NOT_CONVERTED_LINE: self.line_flag_id,
                self.NOT_CONVERTED_POLYGON: self.poly_flag_id,
            }
        if multiStepFeedback is not None:
            multiStepFeedback.pushInfo(self.tr("Commiting changes"))
        stepSize = 100 / len(outputLayerDict)
        for current, (lyrName, lyr) in enumerate(outputLayerDict.items()):
            if multiStepFeedback is not None:
                multiStepFeedback.pushInfo(
                    self.tr(f"Commiting changes for layer {lyrName}")
                )
            lyr.commitChanges()
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)
        return {
            self.NOT_CONVERTED_POINT: self.point_flag_id,
            self.NOT_CONVERTED_LINE: self.line_flag_id,
            self.NOT_CONVERTED_POLYGON: self.poly_flag_id,
        }

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "convertdatabasesalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Convert Databases")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Data Management Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Data Management Algorithms"

    def tr(self, string):
        return QCoreApplication.translate("ConvertDatabasesAlgorithm", string)

    def createInstance(self):
        return ConvertDatabasesAlgorithm()
