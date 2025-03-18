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
    QgsFeatureRequest,
)
from DsgTools.core.GeometricTools import graphHandler


class IdentifyWaterBodyAndContourInconsistencies(ValidationAlgorithm):

    INPUT_WATER_BODIES = "INPUT_WATER_BODIES"
    INPUT_CONTOURS = "INPUT_CONTOURS"
    CONTOUR_ATTR = "CONTOUR_ATTR"
    CONTOUR_INSIDE_WATER_BODY_EXPRESSION = "CONTOUR_INSIDE_WATER_BODY_EXPRESSION"
    DAM_LAYER = "DAM_LAYER"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_WATER_BODIES,
                self.tr("Input water bodies"),
                [QgsProcessing.TypeVectorPolygon],
                optional=False,
                defaultValue="cobter_massa_dagua_a",
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_CONTOURS,
                self.tr("Input contours"),
                [QgsProcessing.TypeVectorLine],
                optional=False,
                defaultValue="elemnat_curva_nivel_l",
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
            QgsProcessingParameterFeatureSource(
                self.DAM_LAYER,
                self.tr("Dam Layer"),
                [QgsProcessing.TypeVectorLine],
                optional=True,
                defaultValue="infra_barragem_l",
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        algRunner = AlgRunner()
        multiStepFeedback = QgsProcessingMultiStepFeedback(8, feedback)
        inputContours = self.parameterAsVectorLayer(
            parameters, self.INPUT_CONTOURS, context
        )
        contourExpression = self.parameterAsExpression(
            parameters, self.CONTOUR_INSIDE_WATER_BODY_EXPRESSION, context
        )
        inputWaterBodiesLyr = self.parameterAsVectorLayer(
            parameters, self.INPUT_WATER_BODIES, context
        )
        damLyr = self.parameterAsVectorLayer(
            parameters, self.DAM_LAYER, context
        )
        self.prepareFlagSink(
            parameters, inputContours, QgsWkbTypes.LineString, context
        )
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        if inputWaterBodiesLyr is None or inputWaterBodiesLyr.featureCount() == 0 or inputContours.featureCount() == 0:
            return {self.FLAGS: self.flag_id}
        inputWaterBodiesLyr = algRunner.runCreateFieldWithExpression(
            inputLyr=parameters[self.INPUT_WATER_BODIES],
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(inputWaterBodiesLyr, context, multiStepFeedback, is_child_algorithm=True)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        # caso curva de nivel com atributo dentro_de_massa_dagua = 1 e disjunto de massa d'água
        disjointContoursFromWaterBodies = algRunner.runExtractByLocation(
            inputLyr=parameters[self.INPUT_CONTOURS],
            intersectLyr=inputWaterBodiesLyr,
            context=context,
            predicate=AlgRunner.Disjoint,
            feedback=multiStepFeedback
        )
        flagLambda = lambda x: self.flagFeature(
            x.geometry(),
            flagText=self.tr("Contours with attribute inside water body that do not intersect a water body"),
        )
        request = QgsFeatureRequest()
        request.setFilterExpression(expression=contourExpression)
        list(map(flagLambda, disjointContoursFromWaterBodies.getFeatures(request)))

        # daqui para baixo são intersecções de curvas dentro de massas d'água
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
        clippedContours = algRunner.runMultipartToSingleParts(
            inputLayer=clippedContours,
            context=context,
            feedback=multiStepFeedback
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        _, clippedContoursWithAttributeOutsideWaterBody = algRunner.runFilterExpressionWithFailOutput(
            inputLyr=clippedContours,
            expression=contourExpression,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(clippedContoursWithAttributeOutsideWaterBody, context, multiStepFeedback, is_child_algorithm=True)
        flagLambda = lambda x: self.flagFeature(
            x.geometry(),
            flagText=self.tr("Contours with attribute outside water body that intersect a water body"),
        )
        if clippedContoursWithAttributeOutsideWaterBody.featureCount() == 0:
            return {self.FLAGS: self.flag_id}
        if damLyr is None:
            list(map(flagLambda, clippedContoursWithAttributeOutsideWaterBody.getFeatures()))
            return {self.FLAGS: self.flag_id}
        flagLyr = algRunner.runExtractByLocation(
            inputLyr=clippedContoursWithAttributeOutsideWaterBody,
            intersectLyr=damLyr,
            context=context,
            predicate=AlgRunner.Disjoint,
            feedback=multiStepFeedback
        )
        list(map(flagLambda, flagLyr.getFeatures()))
        

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
