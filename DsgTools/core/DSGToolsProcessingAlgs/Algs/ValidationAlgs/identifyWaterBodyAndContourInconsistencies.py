# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-10-05
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

from itertools import product
import os
import concurrent.futures
import processing

from collections import defaultdict
from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingParameterFeatureSink,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterNumber,
    QgsProcessingParameterField,
    QgsWkbTypes,
    QgsProcessingParameterExpression,
)
from DsgTools.core.GeometricTools import graphHandler


class IdentifyWaterBodyAndContourInconsistencies(ValidationAlgorithm):

    INPUT_WATER_BODIES = "INPUT_WATER_BODIES"
    INPUT_CONTOURS = "INPUT_CONTOURS"
    CONTOUR_ATTR = "CONTOUR_ATTR"
    CONTOUR_INSIDE_WATER_BODY_EXPRESSION = "CONTOUR_INSIDE_WATER_BODY_EXPRESSION"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_WATER_BODIES,
                self.tr("Input water bodies"),
                [QgsProcessing.TypeVectorPolygon],
                optional=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_CONTOURS,
                self.tr("Input contours"),
                [QgsProcessing.TypeVectorLine],
                optional=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.CONTOUR_ATTR,
                self.tr("Contour value field"),
                "cota",
                self.INPUT_CONTOURS,
                QgsProcessingParameterField.Any,
            )
        )

        self.addParameter(
            QgsProcessingParameterExpression(
                self.CONTOUR_INSIDE_WATER_BODY_EXPRESSION,
                self.tr("Filter expression for cotours inside water bodies"),
                """"dentro_de_massa_dagua" = 1""",
                self.INPUT_CONTOURS,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        algRunner = AlgRunner()
        multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        inputContours = self.parameterAsVectorLayer(
            parameters, self.INPUT_CONTOURS, context
        )
        contourExpression = self.parameterAsExpression(
            parameters, self.CONTOUR_INSIDE_WATER_BODY_EXPRESSION, context
        )
        self.prepareFlagSink(
            parameters, inputContours, QgsWkbTypes.MultiLineString, context
        )
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        inputWaterBodiesLyr = algRunner.runCreateFieldWithExpression(
            inputLyr=self.INPUT_WATER_BODIES,
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        clippedContours = algRunner.runClip(
            inputLayer=parameters[self.INPUT_CONTOURS],
            overlayLayer=inputWaterBodiesLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        if clippedContours.featureCount() == 0:
            return {self.FLAGS: self.flag_id}

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        expectedContours = algRunner.runFilterExpression(
            inputLyr=parameters[self.INPUT_CONTOURS],
            expression=contourExpression,
            context=context,
            feedback=multiStepFeedback,
        )
        flagLambda = lambda x: self.flagFeature(
            x, flagText=self.tr("Invalid intersection between water body and contours")
        )
        if expectedContours.featureCount() == 0:
            list(map(flagLambda, clippedContours.getFeatures()))
            return {self.FLAGS: self.flag_id}
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        flagCandidatesLyr = processing.run(
            "native:joinattributesbylocation",
            {
                "INPUT": clippedContours,
                "PREDICATE": [2],  # equal
                "JOIN": expectedContours,
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
        list(map(flagLambda, flagCandidatesLyr.getFeatures()))

        return {self.FLAGS: self.flag_id}

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return IdentifyWaterBodyAndContourInconsistencies()

    def name(self):
        return "identifywaterbodyandcontourinconsistencies"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Water Bodies and Contour Inconsistencies")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Terrain Processes")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Terrain Processes"

    def shortHelpString(self):
        return self.tr(
            "O algoritmo confronta massas d'água com as curvas de nível, verificando se uma curva intersecta mais de uma vez uma curva de nível."
        )
