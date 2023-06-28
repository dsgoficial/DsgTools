# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-06-08
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

from collections import defaultdict
from typing import Dict
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterFeatureSink,
    QgsWkbTypes,
    QgsGeometry,
    QgsProcessingParameterNumber,
    QgsProcessingMultiStepFeedback,
    QgsFeedback,
    QgsProcessingFeatureSource,
    QgsProcessingContext,
)

from .validationAlgorithm import ValidationAlgorithm


class IdentifySegmentErrorsBetweenLinesAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    REFERENCE_LINE = "REFERENCE_LINE"
    SEARCH_RADIUS = "SEARCH_RADIUS"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT, self.tr("Input lines"), [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.REFERENCE_LINE,
                self.tr("Reference lines"),
                [QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.SEARCH_RADIUS,
                self.tr("Search Radius"),
                type=QgsProcessingParameterNumber.Double,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        layerHandler = LayerHandler()
        self.algRunner = AlgRunner()
        inputSource = self.parameterAsSource(parameters, self.INPUT, context)
        referenceSource = self.parameterAsSource(
            parameters, self.REFERENCE_LINE, context
        )
        searchRadius = self.parameterAsDouble(parameters, self.SEARCH_RADIUS, context)
        self.prepareFlagSink(parameters, inputSource, QgsWkbTypes.MultiPoint, context)
        nFeats = inputSource.featureCount()
        nReferenceFeats = referenceSource.featureCount()
        if inputSource is None or nFeats == 0 or nReferenceFeats == 0:
            return {self.FLAGS: self.flag_id}
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        vertexNearEdgeFlagDict = layerHandler.getUnsharedVertexOnSharedEdgesDict(
            [parameters[self.INPUT], parameters[self.REFERENCE_LINE]],
            [],
            searchRadius,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        vertexFlagSet = self.getFlagVertexesFromGeomDict(
            vertexNearEdgeFlagDict, feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        intersectedFeats = self.algRunner.runDifference(
            inputLyr=parameters[self.INPUT],
            overlayLyr=parameters[self.REFERENCE_LINE],
            context=context,
            feedback=multiStepFeedback,
        )
        intersectFeatCount = intersectedFeats.featureCount()
        if len(vertexFlagSet) == 0 and intersectFeatCount == 0:
            return {self.FLAGS: self.flag_id}
        if intersectFeatCount > 0:
            intersectedVertexes = self.algRunner.runExtractVertices(
                inputLyr=intersectedFeats,
                context=context,
            )
            vertexFlagSet = vertexFlagSet.union(
                set(v.geometry().asWkt() for v in intersectedVertexes.getFeatures())
            )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        self.raiseFlagsFromVertexFlagSet(
            parameters[self.INPUT], vertexFlagSet, context, feedback=multiStepFeedback
        )
        return {self.FLAGS: self.flag_id}

    def getFlagVertexesFromGeomDict(
        self, geomDict: Dict[int, Dict[str, QgsGeometry]], feedback: QgsFeedback
    ):
        size = 100 / len(geomDict) if geomDict else 0
        outputSet = set()
        for current, (featid, vertexDict) in enumerate(geomDict.items()):
            if feedback.isCanceled():
                break
            outputSet = outputSet.union(vertexDict.keys())
            feedback.setProgress(size * current)
        return outputSet

    def raiseFlagsFromVertexFlagSet(
        self,
        inputSource: QgsProcessingFeatureSource,
        vertexFlagSet: set,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ):
        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        multiStepFeedback.setCurrentStep(0)
        localCache = self.algRunner.runCreateFieldWithExpression(
            inputLyr=inputSource,
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=False,
        )
        multiStepFeedback.setCurrentStep(1)
        vertexLyr = self.algRunner.runExtractVertices(
            inputLyr=localCache, context=context, feedback=multiStepFeedback
        )
        multiStepFeedback.setCurrentStep(2)
        vertexDict = defaultdict(set)
        stepSize = 100 / vertexLyr.featureCount()
        for current, vertexFeat in enumerate(vertexLyr.getFeatures()):
            if multiStepFeedback.isCanceled():
                return
            geom = vertexFeat.geometry()
            if geom.asWkt() not in vertexFlagSet:
                continue
            vertexDict[vertexFeat["featid"]].add(geom)
            multiStepFeedback.setProgress(current * stepSize)
        multiStepFeedback.setCurrentStep(3)
        stepSize = 100 / len(vertexDict)
        for current, (featid, vertexSet) in enumerate(vertexDict.items()):
            if multiStepFeedback.isCanceled():
                return
            flagText = f"Line with id={featid} from input has construction errors with reference layer."
            baseGeom, *geomList = list(vertexSet)
            if len(geomList) > 0:
                for g in geomList:
                    baseGeom = baseGeom.combine(g)
            self.flagFeature(flagGeom=baseGeom, flagText=flagText)
            multiStepFeedback.setProgress(current * stepSize)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifysegmenterrorsbetweenlines"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Segment Errors Between Lines")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Identification Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Identification Processes)"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifySegmentErrorsBetweenLinesAlgorithm", string
        )

    def createInstance(self):
        return IdentifySegmentErrorsBetweenLinesAlgorithm()
