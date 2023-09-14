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
    QgsVectorLayer,
    QgsProcessingContext,
)

from .validationAlgorithm import ValidationAlgorithm


class FixSegmentErrorsBetweenLinesAlgorithm(ValidationAlgorithm):
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
        currentStep = 0
        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        multiStepFeedback.setCurrentStep(currentStep)
        flagLyr = self.algRunner.runIdentifySegmentErrorBetweenLines(
            inputLayer=parameters[self.INPUT],
            referenceLineLayer=parameters[self.REFERENCE_LINE],
            searchRadius=searchRadius,
            context=context,
            feedback=multiStepFeedback
        )
        if flagLyr.featureCount() == 0:
            return
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        singlePartFlags = self.algRunner.runMultipartToSingleParts(
            flagLyr, context, is_child_algorithm=True
        )
        currentStep += 1
        
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(singlePartFlags, context, feedback=multiStepFeedback, is_child_algorithm=True)
        currentStep += 1
        
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runSnapLayerOnLayer(
            inputLayer=inputSource,
            referenceLayer=singlePartFlags,
            tol=searchRadius,
        )
        currentStep += 1
        
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runSnapLayerOnLayer(
            inputLayer=referenceSource,
            referenceLayer=singlePartFlags,
            tol=searchRadius,
        )

    

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "fixsegmenterrorsbetweenlines"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Fix Segment Errors Between Lines")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Manipulation Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Manipulation Processes)"

    def tr(self, string):
        return QCoreApplication.translate(
            "FixSegmentErrorsBetweenLinesAlgorithm", string
        )

    def createInstance(self):
        return FixSegmentErrorsBetweenLinesAlgorithm()
