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
from collections import defaultdict
from typing import DefaultDict, Dict, Tuple, Union

import processing
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsFeatureRequest, QgsGeometry, QgsPointXY,
                       QgsProcessing, QgsProcessingFeatureSourceDefinition,
                       QgsProcessingFeedback, QgsProcessingMultiStepFeedback,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterVectorLayer, QgsSpatialIndex,
                       QgsVectorLayer, QgsWkbTypes, QgsProcessingParameterFeatureSource)

from .validationAlgorithm import ValidationAlgorithm


class IdentifyUndershootsAlgorithm(ValidationAlgorithm):
    INPUT = 'INPUT'
    SELECTED = 'SELECTED'
    TOLERANCE = 'TOLERANCE'
    REFERENCE = 'REFERENCE'
    FLAGS = 'FLAGS'

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input'),
                [
                    QgsProcessing.TypeVectorLine,
                    QgsProcessing.TypeVectorPolygon,
                ]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.REFERENCE,
                self.tr('Reference polygons'),
                [
                    QgsProcessing.TypeVectorPolygon,
                ]
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.TOLERANCE,
                self.tr('Search radius'),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.0001
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr('{0} Flags').format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.layerHandler = LayerHandler()
        algRunner = AlgRunner()
        inputSource = self.parameterAsSource(parameters, self.INPUT, context)
        searchRadius = self.parameterAsDouble(
            parameters, self.TOLERANCE, context)
        referenceSource = self.parameterAsSource(parameters, self.REFERENCE, context)
        nSteps = 8
        flagSinkType = QgsWkbTypes.Point \
            if QgsWkbTypes.geometryType(inputSource.wkbType()) == QgsWkbTypes.LineGeometry \
            else QgsWkbTypes.Linestring
        self.prepareFlagSink(parameters, inputSource, flagSinkType, context)
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0

        multiStepFeedback.setCurrentStep(currentStep)
        boundaryLyr = self.prepareInputFeatures(
            context, algRunner, parameters[self.INPUT], multiStepFeedback)
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        undershootSet = self.getUndershoots(boundaryLyr, referenceSource, multiStepFeedback)
        currentStep += 1

        nFeats = len(undershootSet)
        if nFeats == 0:
            return {"FLAGS": self.flag_id}

        multiStepFeedback.setCurrentStep(currentStep)
        self.flagFeatures(undershootSet, multiStepFeedback, nFeats)
        return {"FLAGS": self.flag_id}
    
    def getUndershoots(self, boundaryLyr, referenceSource, searchRadius, feedback):

        def evaluate(feat):
            geom = feat.geometry()
            bbox = geom.boundingBox()
            for boundFeat in referenceSource.getFeatures(bbox):
                if feedback.isCanceled():
                    return None
                boundGeom = boundFeat.geometry()
                if not boundGeom.intersects(geom):
                    continue
                buffer = boundGeom.buffer(searchRadius, -1)
                if geom.intersects(buffer):

            return None

        for boundaryFeature in boundaryLyr.getFeatures():
            

    def flagFeatures(self, undershootSet, multiStepFeedback, nFeats):
        size = 100/nFeats
        for current, feat in enumerate(undershootLyr.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            if feat.geometry() in notUndershootSet:
                continue
            self.flagFeature(
                flagGeom=feat.geometry(),
                flagText=self.tr("Undershoot with the reference layer."),
            )
            multiStepFeedback.setProgress(current * size)


    def prepareInputFeatures(self, context, algRunner, inputSource, multiStepFeedback):
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, multiStepFeedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Finding boundaries..."))
        boundaryLyr = algRunner.runBoundary(
            inputSource, context, feedback=multiStepFeedback
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        boundaryLyr = algRunner.runMultipartToSingleParts(
            inputLayer=boundaryLyr,
            context=context,
            feedback=multiStepFeedback
        )

        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Creating Spatial Indexes on boundaries"))
        algRunner.runCreateSpatialIndex(boundaryLyr, context, feedback=multiStepFeedback)
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
        return 'identifyundershoots'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Identify Undershoots')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Quality Assurance Tools (Identification Processes)')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'DSGTools: Quality Assurance Tools (Identification Processes)'

    def tr(self, string):
        return QCoreApplication.translate('IdentifyUndershootsAlgorithm', string)

    def createInstance(self):
        return IdentifyUndershootsAlgorithm()
