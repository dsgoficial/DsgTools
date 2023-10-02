# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-08-01
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.DbTools.dbConversionHandler import (
    FeatureProcessor,
    convert_features,
    write_output_features,
)
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
)
from qgis.utils import iface

from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.dsgEnums import DsgEnums


class ClipAndCopyFeaturesBetweenDatabasesAlgorithm(QgsProcessingAlgorithm):
    INPUT_DATABASE = "INPUT_DATABASE"
    DESTINATION_DATABASE = "DESTINATION_DATABASE"
    WKT_POLYGON = "LAYER_WITH_FEATURES_TO_APPEND"
    LOAD_DESTINATION_LAYERS = "LOAD_DESTINATION_LAYERS"
    COMMIT_OUTPUT_FEATURES = "COMMIT_OUTPUT_FEATURES"

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
        self.addParameter(
            QgsProcessingParameterGeometry(
                self.WKT_POLYGON,
                self.tr("WKT Geographic Bounds"),
                geometryTypes=[QgsWkbTypes.PolygonGeometry],
                allowMultipart=True,
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
        geom = self.parameterAsGeometry(parameters, self.WKT_POLYGON, context)
        commitChanges = self.parameterAsBool(
            parameters, self.COMMIT_OUTPUT_FEATURES, context
        )
        loadDestinationLayers = self.parameterAsBool(
            parameters, self.LOAD_DESTINATION_LAYERS, context
        )
        nSteps = 6 if not loadDestinationLayers else 7
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
            inputLayerList, geom, context, multiStepFeedback
        )
        for lyr in inputLayerList:
            QgsProject.instance().removeMapLayer(lyr.id())
        currentStep += 1

        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Converting Features"))
        featureProcessor = FeatureProcessor()
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
        if len(outputLayerDict) > 0:
            self.commitChanges(multiStepFeedback, outputLayerDict)
        if not loadDestinationLayers:
            for lyrName, lyr in outputLayerDict.items():
                QgsProject.instance().removeMapLayer(lyr.id())
        return {}

    def commitChanges(self, multiStepFeedback, outputLayerDict):
        stepSize = 100 / len(outputLayerDict)
        for current, (lyrName, lyr) in enumerate(outputLayerDict.items()):
            if multiStepFeedback is not None:
                multiStepFeedback.pushInfo(
                    self.tr(f"Commiting changes for layer {lyrName}")
                )
            lyr.commitChanges()
            if multiStepFeedback is not None:
                multiStepFeedback.setProgress(current * stepSize)

    def getLayersFromDbConnectionName(
        self,
        inputConnectionName,
        feedback,
        layerNameList=None,
        addToCanvas=False,
        withElements=True,
    ):
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

    def getAbstractDb(self, inputConnectionName):
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

    def clipInputLayerList(self, inputLayerList, geom, context, feedback):
        outputDict = dict()
        multiStepFeedback = (
            QgsProcessingMultiStepFeedback(2 * len(inputLayerList), feedback)
            if feedback is not None
            else None
        )
        clipLayer = (
            self.layerHandler.createMemoryLayerFromGeometry(
                geom=geom, crs=QgsProject.instance().crs()
            )
            if geom is not None and not geom.isEmpty()
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
                    overlayLayer=clipLayer,
                    context=context,
                    feedback=multiStepFeedback,
                )
                if clipLayer is not None
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
        return "clipandcopyfeaturesbetweendatabasesalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Clip and Copy features Between Databases")

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
        return QCoreApplication.translate("AppendFeaturesToLayerAlgorithm", string)

    def createInstance(self):
        return ClipAndCopyFeaturesBetweenDatabasesAlgorithm()
