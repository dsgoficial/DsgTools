# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-06-01
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Pedro Martins - Cartographic Engineer @ Brazilian Army
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

from PyQt5.QtCore import QCoreApplication

from qgis.core import (
    QgsProcessing,
    QgsProcessingException,
    QgsFeedback,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSink,
    QgsVectorLayer,
    QgsProcessingParameterExpression,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm
from ..Help.algorithmHelpCreator import HTMLHelpCreator as help


class IdentifyMissingLineIntersectionsOnPoints(ValidationAlgorithm):
    FLAGS = "FLAGS"
    INPUT_LINES_1 = "INPUT_LINES_1"
    EXPRESSION_LINES_1 = "EXPRESSION_LINES_1"
    INPUT_INTERSECTION = "INPUT_INTERSECTION"
    EXPRESSION_INTERSECTION = "EXPRESSION_INTERSECTION"
    INPUT_LINES_2 = "INPUT_LINES_2"
    EXPRESSION_LINES_2 = "EXPRESSION_LINES_2"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LINES_1,
                self.tr("First Line Layer"),
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterExpression(
                self.EXPRESSION_LINES_1,
                self.tr("Filter expression for first line layer"),
                parentLayerParameterName=self.EXPRESSION_LINES_1,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LINES_2,
                self.tr("Second Line Layer"),
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterExpression(
                self.EXPRESSION_LINES_2,
                self.tr("Filter expression for second line layer"),
                parentLayerParameterName=self.EXPRESSION_LINES_2,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_INTERSECTION,
                self.tr("Intersection Point Layer"),
                [QgsProcessing.TypeVectorPoint],
            )
        )

        self.addParameter(
            QgsProcessingParameterExpression(
                self.EXPRESSION_INTERSECTION,
                self.tr("Filter expression for intersection layer"),
                parentLayerParameterName=self.INPUT_INTERSECTION,
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
        algRunner = AlgRunner()
        inputFirstLineLyr = self.parameterAsVectorLayer(
            parameters, self.INPUT_LINES_1, context
        )
        if inputFirstLineLyr is None or not inputFirstLineLyr.isValid():
            raise QgsProcessingException(self.tr("First Line Layer is not valid"))
        expressionFirstLyr = self.parameterAsExpression(
            parameters, self.EXPRESSION_LINES_1, context
        )
        inputSecondLineLyr = self.parameterAsVectorLayer(
            parameters, self.INPUT_LINES_2, context
        )
        if inputSecondLineLyr is None or not inputSecondLineLyr.isValid():
            raise QgsProcessingException(self.tr("Second Line Layer is not valid"))
        expressionSecondLyr = self.parameterAsExpression(
            parameters, self.EXPRESSION_LINES_2, context
        )
        intersectionPointLyr = self.parameterAsVectorLayer(
            parameters, self.INPUT_INTERSECTION, context
        )
        if intersectionPointLyr is None or not intersectionPointLyr.isValid():
            raise QgsProcessingException(
                self.tr("Intersection Point Layer is not valid")
            )
        expressionIntersection = self.parameterAsExpression(
            parameters, self.EXPRESSION_INTERSECTION, context
        )
        self.prepareFlagSink(
            parameters,
            inputFirstLineLyr,
            QgsWkbTypes.Point,
            context,
        )
        if feedback is not None:
            multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
            multiStepFeedback.pushInfo(self.tr("Filtering Layers"))
        filteredIntersectionPointLyr = (
            algRunner.runFilterExpression(
                intersectionPointLyr, expressionIntersection, context
            )
            if expressionIntersection is not None and expressionIntersection != ""
            else intersectionPointLyr
        )
        filteredFirstLyr = (
            algRunner.runFilterExpression(
                inputFirstLineLyr, expressionFirstLyr, context
            )
            if expressionFirstLyr is not None and expressionFirstLyr != ""
            else inputFirstLineLyr
        )
        filteredSecondLyr = (
            algRunner.runFilterExpression(
                inputSecondLineLyr, expressionSecondLyr, context
            )
            if expressionSecondLyr is not None and expressionSecondLyr != ""
            else inputSecondLineLyr
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
            multiStepFeedback.pushInfo(self.tr("Calculating Intersections"))
        algRunner.runCreateSpatialIndex(filteredFirstLyr, context)
        algRunner.runCreateSpatialIndex(filteredSecondLyr, context)
        intersections = algRunner.runLineIntersections(
            filteredFirstLyr, filteredSecondLyr, context, feedback=multiStepFeedback
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(2)
            multiStepFeedback.pushInfo(self.tr("Calculating Differences"))
        algRunner.runCreateSpatialIndex(intersections, context)
        algRunner.runCreateSpatialIndex(filteredIntersectionPointLyr, context)
        difference = algRunner.runExtractByLocation(
            filteredIntersectionPointLyr,
            intersections,
            context,
            predicate=[2],
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(3)
            multiStepFeedback.pushInfo(self.tr("Raising Flags"))
        self.raiseFeaturesFlags(difference, multiStepFeedback)
        return {self.FLAGS: self.flag_id}

    def raiseFeaturesFlags(self, layer: QgsVectorLayer, feedback: QgsFeedback):
        size = 100 / layer.featureCount() if layer.featureCount() else 0
        flagText = self.tr("Missing intersection on Point.")
        for current, feature in enumerate(layer.getFeatures()):
            if feedback.isCanceled():
                break
            geom = feature.geometry()
            geomWkb = geom.asWkb()
            self.flagFeature(geomWkb, flagText, fromWkb=True)
            feedback.setProgress(size * current)

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifymissinglineintersectionsonpoints"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Missing Line Intersections on Points")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Object Proximity and Relationships")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Object Proximity and Relationships"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifyMissingLineIntersectionsOnPoints", string
        )

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    # def helpUrl(self):
    #     return help().helpUrl(self.name())

    def createInstance(self):
        return IdentifyMissingLineIntersectionsOnPoints()
