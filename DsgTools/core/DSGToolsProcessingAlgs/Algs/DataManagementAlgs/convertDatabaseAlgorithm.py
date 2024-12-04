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

import json
from typing import Dict, List, Optional
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
    QgsProcessingFeatureSource,
)
from qgis.utils import iface

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.dsgEnums import DsgEnums


class ConvertDatabasesAlgorithm(QgsProcessingAlgorithm):
    INPUT_DATABASE = "INPUT_DATABASE"
    DESTINATION_DATABASE = "DESTINATION_DATABASE"
    CONVERSION_MAPS_STRUCTURE = "CONVERSION_MAPS_STRUCTURE"
    LOAD_DESTINATION_LAYERS = "LOAD_DESTINATION_LAYERS"
    COMMIT_OUTPUT_FEATURES = "COMMIT_OUTPUT_FEATURES"
    GEOGRAPHIC_BOUNDS = "GEOGRAPHIC_BOUNDS"
    NOT_CONVERTED_POINT = "NOT_CONVERTED_POINT"
    NOT_CONVERTED_LINE = "NOT_CONVERTED_LINE"
    NOT_CONVERTED_POLYGON = "NOT_CONVERTED_POLYGON"

    def flags(self):
        return (
            super().flags()
            | QgsProcessingAlgorithm.FlagNotAvailableInStandaloneTool
            | QgsProcessingAlgorithm.FlagRequiresProject
            | QgsProcessingAlgorithm.FlagNoThreading
        )

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
            QgsProcessingParameterFeatureSource(
                self.GEOGRAPHIC_BOUNDS,
                self.tr("Geographic Bounds"),
                [QgsWkbTypes.PolygonGeometry],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.LOAD_DESTINATION_LAYERS,
                self.tr("Load destination layers"),
                defaultValue=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.COMMIT_OUTPUT_FEATURES,
                self.tr("Commit converted features to destination layers"),
                defaultValue=True,
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
        destinationConnectionName = self.parameterAsConnectionName(
            parameters, self.DESTINATION_DATABASE, context
        )
        conversionMapList = self.parameterAsConversionMapList(
            parameters, self.CONVERSION_MAPS_STRUCTURE, context
        )
        geographicSource = self.parameterAsSource(
            parameters, self.GEOGRAPHIC_BOUNDS, context
        )
        commitChanges = self.parameterAsBool(
            parameters, self.COMMIT_OUTPUT_FEATURES, context
        )
        loadDestinationLayers = self.parameterAsBool(
            parameters, self.LOAD_DESTINATION_LAYERS, context
        )
        nSteps = 5 + len(conversionMapList)
        if loadDestinationLayers:
            nSteps += 1
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(nSteps, feedback)
            if feedback is not None
            else None
        )
        currentStep = 0
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(
                self.tr("Loading layers with elements from input database")
            )
        inputLayerList = self.getLayersFromDbConnectionName(
            inputConnectionName, feedback=multiStepFeedback
        )
        if len(inputLayerList) == 0:
            return {}
        currentStep += 1

        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Clipping input layer list"))
        clippedLayerDict = self.clipInputLayerList(
            inputLayerList, geographicSource, context, multiStepFeedback
        )
        for lyr in inputLayerList:
            QgsProject.instance().removeMapLayer(lyr.id())
        currentStep += 1

        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Converting Features"))
        firstConversionData = conversionMapList[0]
        featureProcessor = MappingFeatureProcessor(
            mappingDictPath=firstConversionData["conversionJson"],
            mappingType=firstConversionData["mode"],
        )
        convertedFeatureDict = convert_features(
            inputLayerDict={
                lyrName: lyr
                for lyrName, lyr in clippedLayerDict.items()
                if lyr.featureCount() > 0
            },
            featureProcessor=featureProcessor,
            feedback=multiStepFeedback,
            layerNameAttr="layerName",
        )
        currentStep += 1
        for conversionData in conversionMapList[1::]:
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(currentStep)
            featureProcessor = MappingFeatureProcessor(
                mappingDictPath=conversionData["conversionJson"],
                mappingType=conversionData["mode"],
            )
            convertedFeatureDict = convert_features(
                inputLayerDict=convertedFeatureDict,
                featureProcessor=featureProcessor,
                feedback=multiStepFeedback,
            )
            currentStep += 1

        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Loading output layers"))
        destinationLayerList = self.getLayersFromDbConnectionName(
            inputConnectionName=destinationConnectionName,
            feedback=multiStepFeedback,
            layerNameList=list(convertedFeatureDict.keys()),
            addToCanvas=loadDestinationLayers,
            withElements=False,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Writing to output"))
        outputLayerDict = {lyr.name(): lyr for lyr in destinationLayerList}
        write_output_features(
            convertedFeatureDict,
            outputLayerDict=outputLayerDict,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        if not commitChanges:
            return {}
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
        if not loadDestinationLayers:
            for lyrName, lyr in outputLayerDict.items():
                QgsProject.instance().removeMapLayer(lyr.id())
        return {}

    def parameterAsConversionMapList(self, parameters, name, context):
        return parameters[name]

    def getLayersFromDbConnectionName(
        self,
        inputConnectionName: str,
        feedback: QgsProcessingFeedback,
        layerNameList: Optional[List[QgsVectorLayer]] = None,
        addToCanvas: Optional[bool] = False,
        withElements: Optional[bool] = True,
    ) -> List[QgsVectorLayer]:
        inputAbstractDb = self.getAbstractDb(inputConnectionName)
        layerLoader = LayerLoaderFactory().makeLoader(iface, inputAbstractDb)
        inputParamList = inputAbstractDb.listGeomClassesFromDatabase(
            withElements=withElements
        )
        inputParamList = list(map(lambda x: x.split(".")[-1], inputParamList))
        if layerNameList is not None and layerNameList != []:
            inputParamList = list(filter(lambda x: x in layerNameList, inputParamList))
        loadedLayerList = layerLoader.loadLayersInsideProcessing(
            inputParamList, addToCanvas=addToCanvas, feedback=feedback
        )
        del inputAbstractDb
        del layerLoader
        return loadedLayerList

    def getAbstractDb(self, inputConnectionName: str) -> AbstractDb:
        try:
            md = QgsProviderRegistry.instance().providerMetadata("postgres")
            conn = md.createConnection(inputConnectionName)
        except QgsProviderConnectionException:
            raise QgsProcessingException(
                self.tr("Could not retrieve connection details for {}").format(
                    inputConnectionName
                )
            )
        uri = QgsDataSourceUri(conn.uri())
        abstractDb = DbFactory().createDbFactory(DsgEnums.DriverPostGIS)
        abstractDb.connectDatabaseWithParameters(
            uri.host(),
            int(uri.port()),
            uri.database(),
            uri.username(),
            uri.password(),
        )
        return abstractDb

    def clipInputLayerList(
        self,
        inputLayerList: List[QgsVectorLayer],
        geographicBoundSource: QgsProcessingFeatureSource,
        context: QgsProcessingContext,
        feedback: QgsProcessingFeedback,
    ) -> Dict[str, QgsVectorLayer]:
        outputDict = dict()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2 * len(inputLayerList), feedback)
            if feedback is not None
            else None
        )
        for currentIdx, lyr in enumerate(inputLayerList):
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                return outputDict
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(2 * currentIdx)
            clippedLyr = (
                self.algRunner.runClip(
                    inputLayer=lyr,
                    overlayLayer=geographicBoundSource,
                    context=context,
                    feedback=multiStepFeedback,
                )
                if geographicBoundSource is not None
                else lyr
            )
            if multiStepFeedback is not None:
                multiStepFeedback.setCurrentStep(2 * currentIdx + 1)
            outputDict[lyr.name()] = self.algRunner.runCreateFieldWithExpression(
                inputLyr=clippedLyr,
                expression=f"'{lyr.name()}'",
                fieldType=2,
                fieldName="layerName",
                feedback=multiStepFeedback,
                context=context,
                is_child_algorithm=False,
            )
        return outputDict

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


class ParameterDbConversionType(QgsProcessingParameterType):
    def __init__(self):
        super().__init__()

    def create(self, name):
        return ParameterDbConversion(name)  # mudar

    def metadata(self):
        return {
            "widget_wrapper": "DsgTools.gui.ProcessingUI.dbConversionWrapper.DbConversionWrapper"
        }  # mudar

    def name(self):
        return QCoreApplication.translate("Processing", "Database Conversion Maps")

    def id(self):
        return "db_conversion_maps"

    def description(self):
        return QCoreApplication.translate(
            "Processing",
            "A list of database conversion maps. Used in the Convert Database algorithm.",
        )


class ParameterDbConversion(QgsProcessingParameterDefinition):
    def __init__(self, name, description=""):
        super().__init__(name, description)

    def clone(self):
        copy = ParameterDbConversion(self.name(), self.description())
        return copy

    def type(self):
        return self.typeName()

    @staticmethod
    def typeName():
        return "db_conversion_maps"

    def checkValueIsAcceptable(self, value, context=None):
        return True

    def valueAsPythonString(self, value, context):
        return json.dumps(value)

    def asScriptCode(self):
        raise NotImplementedError()

    @classmethod
    def fromScriptCode(cls, name, description, isOptional, definition):
        raise NotImplementedError()
