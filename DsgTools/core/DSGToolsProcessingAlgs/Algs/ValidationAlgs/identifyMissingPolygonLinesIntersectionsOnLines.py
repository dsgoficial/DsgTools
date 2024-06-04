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


class IdentifyMissingPolygonLineIntersectionsOnLines(ValidationAlgorithm):
    FLAGS = "FLAGS"
    INPUT_LINES = "INPUT_LINES"
    EXPRESSION_LINES = "EXPRESSION_LINES"
    INPUT_POLYGONS = "INPUT_POLYGONS"
    EXPRESSION_POLYGONS = "EXPRESSION_POLYGONS"
    INPUT_INTERSECTION = "INPUT_INTERSECTION"
    EXPRESSION_INTERSECTION = "EXPRESSION_INTERSECTION"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_LINES,
                self.tr("Line Layers"),
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterExpression(
                self.EXPRESSION_LINES,
                self.tr("Filter expression for line layer"),
                parentLayerParameterName=self.INPUT_LINES,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_POLYGONS,
                self.tr("Polygon Layers"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )

        self.addParameter(
            QgsProcessingParameterExpression(
                self.EXPRESSION_POLYGONS,
                self.tr("Filter expression for polygon layer"),
                parentLayerParameterName=self.INPUT_POLYGONS,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_INTERSECTION,
                self.tr("Intersection Lines Layer"),
                [QgsProcessing.TypeVectorLine],
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
        inputLineLyr = self.parameterAsVectorLayer(
            parameters, self.INPUT_LINES, context
        )
        if inputLineLyr is None or not inputLineLyr.isValid():
            raise QgsProcessingException(self.tr("Line Layer is not valid"))
        expressionLineLyr = self.parameterAsExpression(
            parameters, self.EXPRESSION_LINES, context
        )
        inputPolygonLyr = self.parameterAsVectorLayer(
            parameters, self.INPUT_POLYGONS, context
        )
        if inputPolygonLyr is None or not inputPolygonLyr.isValid():
            raise QgsProcessingException(self.tr("Polygon Layer is not valid"))
        expressionPolygonLyr = self.parameterAsExpression(
            parameters, self.EXPRESSION_POLYGONS, context
        )
        intersectionLineLyr = self.parameterAsVectorLayer(
            parameters, self.INPUT_INTERSECTION, context
        )
        if intersectionLineLyr is None or not intersectionLineLyr.isValid():
            raise QgsProcessingException(
                self.tr("Intersection Line Layer is not valid")
            )
        expressionIntersection = self.parameterAsExpression(
            parameters, self.EXPRESSION_POLYGONS, context
        )
        self.prepareFlagSink(
            parameters,
            inputLineLyr,
            QgsWkbTypes.LineString,
            context,
        )
        if feedback is not None:
            multiStepFeedback = QgsProcessingMultiStepFeedback(4, feedback)
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(0)
            multiStepFeedback.pushInfo(self.tr("Filtering Layers"))
        filteredIntersectionLineLyr = (
            algRunner.runFilterExpression(
                intersectionLineLyr,
                expressionIntersection,
                context,
                feedback=multiStepFeedback,
            )
            if expressionIntersection is not None and expressionIntersection != ""
            else intersectionLineLyr
        )
        filteredLineLyr = (
            algRunner.runFilterExpression(
                inputLineLyr, expressionLineLyr, context, feedback=multiStepFeedback
            )
            if expressionLineLyr is not None and expressionLineLyr != ""
            else inputLineLyr
        )
        filteredPolygonLineLyr = (
            algRunner.runFilterExpression(
                inputPolygonLyr,
                expressionPolygonLyr,
                context,
                feedback=multiStepFeedback,
            )
            if expressionPolygonLyr is not None and expressionPolygonLyr != ""
            else inputPolygonLyr
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(1)
            multiStepFeedback.pushInfo(self.tr("Calculating Intersections"))
        intersections = algRunner.runIntersection(
            filteredLineLyr,
            context,
            overlayLyr=filteredPolygonLineLyr,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(2)
            multiStepFeedback.pushInfo(self.tr("Calculating Differences"))
        algRunner.runCreateSpatialIndex(intersections, context)
        algRunner.runCreateSpatialIndex(filteredIntersectionLineLyr, context)
        difference = algRunner.runDifference(
            filteredIntersectionLineLyr,
            intersections,
            context,
            feedback=multiStepFeedback,
        )
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(3)
            multiStepFeedback.pushInfo(self.tr("Raising Flags"))
        self.raiseFeaturesFlags(difference, multiStepFeedback)
        return {self.FLAGS: self.flag_id}

    def raiseFeaturesFlags(self, layer: QgsVectorLayer, feedback: QgsFeedback):
        size = 100 / layer.featureCount() if layer.featureCount() else 0
        flagText = self.tr("Missing intersection on Line.")
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
        return "identifymissingpolygonlineintersectionsonlines"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Missing Polygon Line Intersections on Lines")

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
            "IdentifyMissingPolygonLineIntersectionsOnLines", string
        )

    def shortHelpString(self):
        return help().shortHelpString(self.name())

    # def helpUrl(self):
    #     return help().helpUrl(self.name())

    def createInstance(self):
        return IdentifyMissingPolygonLineIntersectionsOnLines()
