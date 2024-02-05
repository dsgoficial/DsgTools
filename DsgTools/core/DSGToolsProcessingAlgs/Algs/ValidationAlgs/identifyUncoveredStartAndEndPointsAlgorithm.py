# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2024-02-05
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Philipe Borba - Cartographic Engineer @ Brazilian Army
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

from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingFeatureSourceDefinition,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterExpression,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class IdentifyUncoveredStartAndEndPointsAlgorithm(ValidationAlgorithm):
    INPUT = "INPUT"
    SELECTED = "SELECTED"
    FILTER_EXPRESSION = "FILTER_EXPRESSION"
    FILTER_LINE_LIST = "FILTER_LINE_LIST"
    GEOGRAPHIC_BOUNDARY = "GEOGRAPHIC_BOUNDARY"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr("Input layer"),
                [QgsProcessing.TypeVectorLine],
            )
        )

        self.addParameter(
            QgsProcessingParameterExpression(
                self.FILTER_EXPRESSION,
                self.tr("Filter expression for input"),
                None,
                self.INPUT,
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SELECTED, self.tr("Process only selected features")
            )
        )

        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.FILTER_LINE_LIST,
                self.tr("Linestring Filter Layers"),
                QgsProcessing.TypeVectorLine,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDARY,
                self.tr("Geographic Boundary"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS,
                self.tr("{0} flags").format(self.displayName()),
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        self.algRunner = AlgRunner()
        inputLyr = self.parameterAsLayer(parameters, self.INPUT, context)
        if inputLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )
        onlySelected = self.parameterAsBool(parameters, self.SELECTED, context)
        filterExpression = self.parameterAsExpression(
            parameters, self.FILTER_EXPRESSION, context
        )
        if filterExpression == "":
            filterExpression = None
        lineFilterLyrList = self.parameterAsLayerList(
            parameters, self.FILTER_LINE_LIST, context
        )
        geographicBoundaryLyr = self.parameterAsLayer(
            parameters, self.GEOGRAPHIC_BOUNDARY, context
        )

        self.prepareFlagSink(parameters, inputLyr, QgsWkbTypes.Point, context)

        nSteps = 9 if geographicBoundaryLyr is None else 10
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setProgressText(self.tr("Building aux structures"))
        multiStepFeedback.setCurrentStep(currentStep)
        cacheLyr = self.algRunner.runCreateFieldWithExpression(
            inputLyr=inputLyr
            if not onlySelected
            else QgsProcessingFeatureSourceDefinition(inputLyr.id(), True),
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        filteredInputLyr = self.algRunner.runFilterExpression(
            inputLyr=cacheLyr,
            expression=filterExpression,
            context=context,
            feedback=multiStepFeedback,
        )
        if filteredInputLyr.featureCount() == 0:
            return {self.FLAGS: self.flag_id}
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        nodesLyr = self.algRunner.runExtractSpecificVertices(
            inputLyr=filteredInputLyr,
            vertices="0,-1",
            context=context,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            nodesLyr, context, multiStepFeedback, is_child_algorithm=True
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        selectedNodes = (
            self.algRunner.runExtractByLocation(
                inputLyr=nodesLyr,
                intersectLyr=geographicBoundaryLyr,
                context=context,
                predicate=[AlgRunner.Intersect],
                feedback=multiStepFeedback,
            )
            if geographicBoundaryLyr is not None
            else nodesLyr
        )
        if geographicBoundaryLyr is not None:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            self.algRunner.runCreateSpatialIndex(
                selectedNodes, context, multiStepFeedback, is_child_algorithm=True
            )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        otherLinesLyr = self.algRunner.runMergeVectorLayers(
            inputList=lineFilterLyrList, context=context, feedback=multiStepFeedback
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            otherLinesLyr, context, multiStepFeedback, is_child_algorithm=True
        )

        candidateFlagsLyr = self.algRunner.runExtractByLocation(
            inputLyr=nodesLyr,
            intersectLyr=otherLinesLyr,
            context=context,
            feedback=multiStepFeedback,
            predicate=[AlgRunner.Disjoint],
        )
        nFeatures = candidateFlagsLyr.featureCount()
        if nFeatures == 0:
            return {self.FLAGS: self.flag_id}
        nodesDict = defaultdict(set)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        for nodeFeat in selectedNodes.getFeatures():
            geom = nodeFeat.geometry()
            nodesDict[geom.asWkb()].add(nodeFeat["featid"])
        stepSize = 100 / nFeatures
        for current, candidateFeat in enumerate(candidateFlagsLyr.getFeatures()):
            if feedback.isCanceled():
                break
            geom = candidateFeat.geometry()
            geomWkb = geom.asWkb()
            idSet = nodesDict.get(geomWkb, set())
            if idSet == set() or len(idSet) > 1:
                continue
            featid = idSet.pop()
            self.flagFeature(
                flagGeom=geomWkb,
                flagText=self.tr(
                    f"Feature (id={featid}) from layer {inputLyr.name()} with uncovered start/end point."
                ),
                fromWkb=True,
            )
            multiStepFeedback.setCurrentStep(current * stepSize)

        return {
            self.FLAGS: self.flag_id,
        }

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifyuncoveredstartandendpointsalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Uncovered Start and End Points Algorithm")

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
            "IdentifyUncoveredStartAndEndPointsAlgorithm", string
        )

    def createInstance(self):
        return IdentifyUncoveredStartAndEndPointsAlgorithm()
