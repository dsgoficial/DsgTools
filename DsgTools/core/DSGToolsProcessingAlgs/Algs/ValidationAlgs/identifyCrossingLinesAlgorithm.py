# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-06-28
        git sha              : $Format:%H$
        copyright            : (C) 2023 by Pedro Martins - Cartographic Engineer @ Brazilian Army
        email                : pedromartins.souza@eb.mil.br
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

from typing import List
import processing
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSink,
    QgsWkbTypes,
    QgsFeatureSink,
    QgsProcessingMultiStepFeedback,
    QgsFeedback,
    QgsProcessingContext,
    QgsProcessingParameterVectorLayer,
    QgsVectorLayer,
    QgsProcessingParameterMultipleLayers,
)

from .validationAlgorithm import ValidationAlgorithm


class IdentifyCrossingLinesAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    COMPARE_INPUT_LINES = "COMPARE_INPUT_LINES"
    COMPARE_INPUT_POLYGONS = "COMPARE_INPUT_POLYGONS"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT, self.tr("Input lines"), [QgsProcessing.TypeVectorLine]
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.COMPARE_INPUT_LINES,
                self.tr("Compare layers (lines)"),
                QgsProcessing.TypeVectorLine,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.COMPARE_INPUT_POLYGONS,
                self.tr("Compare layers (polygons)"),
                QgsProcessing.TypeVectorPolygon,
                optional=True,
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
        self.algRunner = AlgRunner()
        input = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        compareList = []
        compareListLines = self.parameterAsLayerList(
            parameters, self.COMPARE_INPUT_LINES, context
        )
        compareListPoygons = self.parameterAsLayerList(
            parameters, self.COMPARE_INPUT_POLYGONS, context
        )
        compareList.extend(compareListLines)
        compareList.extend(compareListPoygons)
        self.prepareFlagSink(parameters, input, QgsWkbTypes.MultiPoint, context)
        nFeats = input.featureCount()
        if input is None or nFeats == 0 or not compareList:
            return {self.FLAGS: self.flag_id}
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        inputLyr = self.makeLyrCache(input, context, multiStepFeedback)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        pointLyr = self.getCrossingPoints(
            inputLyr, compareList, context, multiStepFeedback
        )
        if pointLyr is None:
            return {self.FLAGS: self.flag_id}
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        stepSize = 100 / pointLyr.featureCount()
        for current, feat in enumerate(pointLyr.getFeatures()):
            if feedback is not None and feedback.isCanceled():
                return {self.FLAGS: self.flag_id}
            self.flagSink.addFeature(feat, QgsFeatureSink.FastInsert)
            multiStepFeedback.setProgress(current * stepSize)
        return {self.FLAGS: self.flag_id}

    def makeLyrCache(
        self,
        layer: QgsVectorLayer,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> QgsVectorLayer:
        localCache = self.algRunner.runCreateFieldWithExpression(
            inputLyr=layer,
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=feedback,
            is_child_algorithm=False,
        )
        self.algRunner.runCreateSpatialIndex(localCache, context, feedback)
        return localCache

    def getCrossingPoints(
        self,
        layer1: QgsVectorLayer,
        layerList: List[QgsVectorLayer],
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> QgsVectorLayer:
        if feedback is not None:
            multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
        else:
            multiStepFeedback = None
        verticesLyr = self.algRunner.runExtractSpecificVertices(
            inputLyr=layer1,
            vertices="0, -1",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(inputLyr=verticesLyr, context=context)
        toMergeList = []
        stepSize = 100 / len(layerList)
        for current, layer in enumerate(layerList):
            layerPre = layer
            if layer.geometryType() == QgsWkbTypes.PolygonGeometry:
                layerPre = self.algRunner.runPolygonsToLines(layer, context)
            if layer.geometryType() == QgsWkbTypes.PointGeometry:
                continue
            toMergeList.append(layerPre)
            multiStepFeedback.setProgress(current * stepSize)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        layer2 = self.algRunner.runMergeVectorLayers(
            inputList=toMergeList,
            crs=layer1.crs(),
            context=context,
            feedback=multiStepFeedback,
        )
        self.algRunner.runCreateSpatialIndex(inputLyr=layer2, context=context)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        intersectionLyr = self.getIntersectionLyr(
            layer1, layer2, context, multiStepFeedback
        )
        self.algRunner.runCreateSpatialIndex(inputLyr=intersectionLyr, context=context)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        unjoined = processing.run(
            "native:joinattributesbylocation",
            {
                "INPUT": intersectionLyr,
                "PREDICATE": [2],  # equal
                "JOIN": verticesLyr,
                "JOIN_FIELDS": [],
                "METHOD": 0,
                "DISCARD_NONMATCHING": False,
                "PREFIX": "",
                "NON_MATCHING": "memory:",
            },
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=False,
        )["NON_MATCHING"]
        if unjoined.featureCount() == 0:
            return None
        return unjoined

    def getIntersectionLyr(
        self,
        layer1: QgsVectorLayer,
        layer2: QgsVectorLayer,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ):
        if feedback is not None:
            multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
            currentStep = 0
            multiStepFeedback.setCurrentStep(currentStep)
        else:
            multiStepFeedback = None
        intersectionsMultiLyr = self.algRunner.runLineIntersections(
            inputLyr=layer1,
            intersectLyr=layer2,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        intersectionsLyr = self.algRunner.runMultipartToSingleParts(
            inputLayer=intersectionsMultiLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        return intersectionsLyr

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifycrossinglines"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Crossing Lines")

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
        return QCoreApplication.translate("IdentifyCrossingLinesAlgorithm", string)

    def shortHelpString(self):
        return self.tr(
            """
        Return intersections between 'Input Lines' and the layers selected in 'Compare layers'
        """
        )

    def createInstance(self):
        return IdentifyCrossingLinesAlgorithm()
