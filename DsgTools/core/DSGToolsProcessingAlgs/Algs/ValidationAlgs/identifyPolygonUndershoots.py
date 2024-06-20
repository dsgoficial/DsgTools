# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-07-14
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
import concurrent.futures
import os

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsWkbTypes,
)

from .validationAlgorithm import ValidationAlgorithm
from ..Help.algorithmHelpCreator import HTMLHelpCreator as help


class IdentifyPolygonUndershootsAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    TOLERANCE = "TOLERANCE"
    REFERENCE = "REFERENCE"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr("Input"),
                [
                    QgsProcessing.TypeVectorPolygon,
                ],
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.REFERENCE,
                self.tr("Reference polygons"),
                [
                    QgsProcessing.TypeVectorPolygon,
                ],
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE,
                self.tr("Search radius"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.0001,
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
        self.layerHandler = LayerHandler()
        algRunner = AlgRunner()
        inputSource = self.parameterAsSource(parameters, self.INPUT, context)
        self.prepareFlagSink(parameters, inputSource, QgsWkbTypes.LineString, context)
        if inputSource is None:
            return {"FLAGS": self.flag_id}
        searchRadius = self.parameterAsDouble(parameters, self.TOLERANCE, context)
        referenceSource = self.parameterAsSource(parameters, self.REFERENCE, context)
        nSteps = 8
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0

        multiStepFeedback.setCurrentStep(currentStep)
        boundaryLyr = self.prepareInputFeatures(
            context, algRunner, parameters[self.INPUT], multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        filteredBoundaryLyr = algRunner.runClip(
            inputLayer=boundaryLyr,
            overlayLayer=parameters[self.REFERENCE],
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        filteredBoundaryLyr = algRunner.runMultipartToSingleParts(
            inputLayer=filteredBoundaryLyr, context=context, feedback=multiStepFeedback
        )

        multiStepFeedback.setCurrentStep(currentStep)
        referenceBoundary = algRunner.runBoundary(
            inputLayer=parameters[self.REFERENCE],
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        referenceSegments = algRunner.runExplodeLines(
            referenceBoundary, context, feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            referenceSegments,
            context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        undershootSet = self.getUndershoots(
            filteredBoundaryLyr,
            referenceSegments,
            searchRadius=searchRadius,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        self.flagFeatures(undershootSet, multiStepFeedback)
        return {"FLAGS": self.flag_id}

    def getUndershoots(self, boundaryLyr, referenceSegmentsLyr, searchRadius, feedback):
        undershootSet = set()
        nFeats = boundaryLyr.featureCount()
        if nFeats == 0:
            return undershootSet

        def evaluate(feat):
            geom = feat.geometry()
            geomBuffer = geom.buffer(searchRadius, -1)
            bbox = geomBuffer.boundingBox()
            for boundFeat in referenceSegmentsLyr.getFeatures(bbox):
                if feedback.isCanceled():
                    return None
                boundGeom = boundFeat.geometry()
                buffer = boundGeom.buffer(searchRadius, -1)
                if not geom.intersects(buffer):
                    continue
                if geom.distance(boundGeom) > 10**-9:
                    return geom
            return None

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count() - 1)
        futures = set()
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        for current, boundaryFeature in enumerate(boundaryLyr.getFeatures()):
            if feedback.isCanceled():
                break
            futures.add(pool.submit(evaluate, boundaryFeature))
            feedback.setProgress(current * 100 / nFeats)
        multiStepFeedback.setCurrentStep(1)
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                break
            result = future.result()
            if result is not None:
                undershootSet.add(result)
            feedback.setProgress(current * 100 / nFeats)
        return undershootSet

    def flagFeatures(self, undershootSet, multiStepFeedback):
        nPoints = len(undershootSet)
        if nPoints == 0:
            return
        size = 100 / nPoints
        for current, geom in enumerate(undershootSet):
            if multiStepFeedback.isCanceled():
                break
            self.flagFeature(
                flagGeom=geom,
                flagText=self.tr("Undershoot with the reference layer."),
            )
            multiStepFeedback.setProgress(current * size)

    def prepareInputFeatures(self, context, algRunner, inputSource, multiStepFeedback):
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, multiStepFeedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Finding boundaries..."))
        boundaryLyr = algRunner.runBoundary(
            inputSource, context, feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        if boundaryLyr.geometryType() == QgsWkbTypes.LineGeometry:
            boundaryLyr = algRunner.runExplodeLines(
                boundaryLyr, context, feedback=multiStepFeedback
            )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        boundaryLyr = algRunner.runMultipartToSingleParts(
            inputLayer=boundaryLyr, context=context, feedback=multiStepFeedback
        )

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Creating Spatial Indexes on boundaries")
        )
        algRunner.runCreateSpatialIndex(
            boundaryLyr, context, feedback=multiStepFeedback, is_child_algorithm=True
        )
        currentStep += 1
        return boundaryLyr

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifypolygonundershoots"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Polygon Undershoots")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Polygon Handling")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Polygon Handling"

    def tr(self, string):
        return QCoreApplication.translate("IdentifyPolygonUndershootsAlgorithm", string)

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    def helpUrl(self):
        return help().helpUrl(self.name())

    def createInstance(self):
        return IdentifyPolygonUndershootsAlgorithm()
