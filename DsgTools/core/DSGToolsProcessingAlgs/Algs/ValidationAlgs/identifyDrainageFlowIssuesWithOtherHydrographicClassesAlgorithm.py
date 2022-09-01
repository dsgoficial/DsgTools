# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-08-31
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

import processing
from itertools import product
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.GeometricTools.networkHandler import NetworkHandler
from qgis.core import (QgsDataSourceUri, QgsFeature, QgsFeatureSink,
                       QgsGeometry, QgsProcessing, QgsProcessingAlgorithm,
                       QgsProcessingException, QgsProcessingMultiStepFeedback,
                       QgsProcessingOutputVectorLayer,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterDistance,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer, QgsProcessingUtils,
                       QgsProject, QgsSpatialIndex, QgsWkbTypes)

from ....dsgEnums import DsgEnums
from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class IdentifyDrainageFlowIssuesWithHydrographyElementsAlgorithm(ValidationAlgorithm):
    INPUT_DRAINAGES = 'INPUT_DRAINAGES'
    SINK_LAYER = 'SINK_LAYER'
    SPILLWAY_LAYER = 'SPILLWAY_LAYER'
    WATER_BODY_WITH_FLOW_LAYER = 'WATER_BODY_WITH_FLOW_LAYER'
    WATER_BODY_WITHOUT_FLOW_LAYER = 'WATER_BODY_WITHOUT_FLOW_LAYER'
    OCEAN_LAYER = 'OCEAN_LAYER'
    SEARCH_RADIUS = 'SEARCH_RADIUS'
    FLAGS = 'FLAGS'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_DRAINAGES,
                self.tr('Input Drainages layer'),
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.SINK_LAYER,
                self.tr('Water sink layer'),
                [QgsProcessing.TypeVectorPoint],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.SPILLWAY_LAYER,
                self.tr('Spillway layer'),
                [QgsProcessing.TypeVectorPoint],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.WATER_BODY_WITH_FLOW_LAYER,
                self.tr('Water body with flow layer'),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.WATER_BODY_WITHOUT_FLOW_LAYER,
                self.tr('Water body without flow layer'),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.OCEAN_LAYER,
                self.tr('Ocean layer'),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SEARCH_RADIUS,
                self.tr('Search radius'),
                minValue=0,
                defaultValue=0.000001,
                type=QgsProcessingParameterNumber.Double
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr('{0} flags').format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.algRunner = AlgRunner()
        inputDrainagesLyr = self.parameterAsLayer(parameters, self.INPUT_DRAINAGES, context)
        if inputDrainagesLyr is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT_DRAINAGES))
        waterSinkLayer = self.parameterAsLayer(parameters, self.SINK_LAYER, context)
        spillwayLayer = self.parameterAsLayer(parameters, self.SPILLWAY_LAYER, context)
        waterBodyWithFlowLyr = self.parameterAsLayer(parameters, self.WATER_BODY_WITH_FLOW_LAYER, context)
        waterBodyWithoutFlowLyr = self.parameterAsLayer(parameters, self.WATER_BODY_WITHOUT_FLOW_LAYER, context)
        oceanLyr = self.parameterAsLayer(parameters, self.OCEAN_LAYER, context)
        self.prepareFlagSink(parameters, inputDrainagesLyr, QgsWkbTypes.Point, context)
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        currentStep = 0
        multiStepFeedback.setProgressText(self.tr('Building aux structures'))
        multiStepFeedback.setCurrentStep(currentStep)
        (
            waterSinkLayer,
            spillwayLayer,
            waterBodyWithFlowLyr,
            waterBodyWithoutFlowLyr,
            oceanLyr,
        ) = self.buildCacheAndSpatialIndexOnLayerList(
            layerList=[waterSinkLayer, spillwayLayer, waterBodyWithFlowLyr, waterBodyWithoutFlowLyr, oceanLyr],
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        
        multiStepFeedback.setProgressText(self.tr('Building drainage aux structures'))
        multiStepFeedback.setCurrentStep(currentStep)
        (
            cachedDrainagesLyr,
            startPointsLyr,
            endPointsLyr,
            drainageDict,
        ) = self.buildAuxStructures(
            inputDrainagesLyr=inputDrainagesLyr,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr('Validating elements against each other'))
        self.validateElementsAgainstEachOther(
            waterSinkLayer,
            spillwayLayer,
            waterBodyWithFlowLyr,
            waterBodyWithoutFlowLyr,
            oceanLyr,
            context=context,
            feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        if waterSinkLayer is not None:
            self.validateIntersection(
                lyrA=startPointsLyr,
                lyrB=waterSinkLayer,
                flagText=self.tr('Drainage starting in a water sink.'),
                context=context,
                feedback=multiStepFeedback
            )
        currentStep += 1
        
        multiStepFeedback.setCurrentStep(currentStep)
        if oceanLyr is not None:
            self.validateIntersection(
                lyrA=startPointsLyr,
                lyrB=oceanLyr,
                flagText=self.tr('Drainage starting in the ocean.'),
                context=context,
                feedback=multiStepFeedback
            )
        currentStep += 1
        
        multiStepFeedback.setCurrentStep(currentStep)
        if spillwayLayer is not None:
            self.validateIntersection(
                lyrA=endPointsLyr,
                lyrB=spillwayLayer,
                flagText=self.tr('Drainage ending in a spillway.'),
                context=context,
                feedback=multiStepFeedback
            )
        currentStep += 1
        
        return {self.FLAGS: self.flag_id}
    
    def buildCacheAndSpatialIndexOnLayerList(self, layerList, context, feedback):
        multiStepFeedback = QgsProcessingMultiStepFeedback(len(layerList), feedback)
        outputList = []
        for i, lyr in enumerate(layerList):
            if multiStepFeedback.isCanceled():
                return outputList
            multiStepFeedback.setCurrentStep(i)
            cachedLyr = self.buildCacheAndSpatialIndex(
                layer=lyr, context=context, feedback=multiStepFeedback
            )
            outputList.append(cachedLyr)
        return outputList
    
    def buildCacheAndSpatialIndex(self, layer, context, feedback):
        if layer is None or layer.featureCount() == 0:
            return None
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        cacheLyr = self.algRunner.runAddAutoIncrementalField(
            inputLyr=layer,
            context=context,
            feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(1)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=cacheLyr, context=context, feedback=multiStepFeedback
        )
        return cacheLyr

    def buildAuxStructures(self, inputDrainagesLyr, context, feedback):
        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        multiStepFeedback.setCurrentStep(0)
        inputDrainagesLyr = self.algRunner.runMultipartToSingleParts(
            inputLayer=inputDrainagesLyr, context=context, feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(1)
        cachedInputDrainagesLyr = self.buildCacheAndSpatialIndex(
            layer=inputDrainagesLyr,
            context=context,
            feedback=multiStepFeedback
        )
        drainageDict = {feat['featid']:feat for feat in cachedInputDrainagesLyr.getFeatures()}
        multiStepFeedback.setCurrentStep(2)
        startPointsLyr = self.algRunner.runExtractSpecificVertices(
            inputLyr=cachedInputDrainagesLyr,
            vertices='0',
            context=context,
            feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(3)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=startPointsLyr, context=context, feedback=multiStepFeedback
        )
        endPointsLyr = self.algRunner.runExtractSpecificVertices(
            inputLyr=cachedInputDrainagesLyr,
            vertices='-1',
            context=context,
            feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(4)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=endPointsLyr, context=context, feedback=multiStepFeedback
        )
        return (
            cachedInputDrainagesLyr,
            startPointsLyr,
            endPointsLyr,
            drainageDict,
        )
    
    def validateElementsAgainstEachOther(self, waterSinkLayer, spillwayLayer, waterBodyWithFlowLyr, waterBodyWithoutFlowLyr, oceanLyr, context, feedback):
        if all(x is None for x in (waterSinkLayer, spillwayLayer, waterBodyWithFlowLyr, waterBodyWithoutFlowLyr, oceanLyr)):
            return
        multiStepFeedback = QgsProcessingMultiStepFeedback(7, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        if waterSinkLayer is not None and spillwayLayer is not None:
            self.validateIntersection(
                lyrA=waterSinkLayer,
                lyrB=spillwayLayer,
                flagText=self.tr('Invalid intersection between water sink feature and spillway feature.'),
                context=context,
                feedback=multiStepFeedback
            )
        currentStep += 1
        pointList = [
            (self.tr('water sink'), waterSinkLayer),
            (self.tr('spillway'), spillwayLayer),
        ]
        polygonList = [
            (self.tr('water body with flow'), waterBodyWithFlowLyr),
            (self.tr('water body without flow'), waterBodyWithoutFlowLyr),
            (self.tr('ocean'), oceanLyr),
        ]
        for (pointStr, pointLyr), (polygonStr, polygonLyr) in product(pointList, polygonList):
            multiStepFeedback.setCurrentStep(currentStep)
            if pointLyr is not None and polygonLyr is not None:
                self.validateIntersection(
                    lyrA=pointLyr,
                    lyrB=polygonLyr,
                    flagText=self.tr(f'Invalid intersection between {pointStr} feature and {polygonStr} feature.'),
                    context=context,
                    feedback=multiStepFeedback
                )
            currentStep += 1

    def validateIntersection(self, lyrA, lyrB, flagText, context, feedback):
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        invalidIntersection = self.algRunner.runExtractByLocation(
                inputLyr=lyrA, intersectLyr=lyrB, context=context, feedback=multiStepFeedback
            )
        multiStepFeedback.setCurrentStep(1)
        flagLambda = lambda x: self.flagFeature(
                x.geometry(),
                flagText=flagText
            )
        list(map(flagLambda, invalidIntersection.getFeatures()))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'identifydrainageflowissueswithhydrographyelementsalgorithm'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Drainage Flow Issues With Hydrography Elements Algorithm')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Quality Assurance Tools (Network Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Quality Assurance Tools (Network Processes)'

    def tr(self, string):
        return QCoreApplication.translate('IdentifyDrainageFlowIssuesWithHydrographyElementsAlgorithm', string)

    def createInstance(self):
        return IdentifyDrainageFlowIssuesWithHydrographyElementsAlgorithm()
