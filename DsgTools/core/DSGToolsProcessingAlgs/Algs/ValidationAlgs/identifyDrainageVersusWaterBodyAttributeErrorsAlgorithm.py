# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2022-08-31
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

from collections import defaultdict
from typing import Any, Dict, Set
from PyQt5.QtCore import QCoreApplication

import concurrent.futures
import os
from itertools import product, chain
from qgis.core import (
    QgsGeometry,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsFeature,
    QgsProcessingParameterField,
    QgsProcessingParameterExpression,
    QgsProcessingParameterString,
    QgsVectorLayer,
    QgsFeedback,
    QgsWkbTypes,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm
from DsgTools.core.GeometricTools import graphHandler


class IdentifyDrainageVersusWaterBodyAttributeErrorsAlgorithm(ValidationAlgorithm):
    INPUT_DRAINAGES = "INPUT_DRAINAGES"
    INSIDE_POLYGON_ATTRIBUTE = "INSIDE_POLYGON_ATTRIBUTE"
    OUTSIDE_POLYGON_ATTRIBUTE_VALUE = "OUTSIDE_POLYGON_ATTRIBUTE_VALUE"
    WATER_BODY = "WATER_BODY"
    WATER_BODY_WITH_FLOW_EXPRESSION = "WATER_BODY_WITH_FLOW_EXPRESSION"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT_DRAINAGES,
                self.tr("Input Drainages layer"),
                [QgsProcessing.TypeVectorLine],
                defaultValue="elemnat_trecho_drenagem_l",
            )
        )
        self.addParameter(
            QgsProcessingParameterField(
                self.INSIDE_POLYGON_ATTRIBUTE,
                self.tr("Attribute that indicates the relationship with polygon"),
                "situacao_em_poligono",
                parentLayerParameterName=self.INPUT_DRAINAGES,
                type=QgsProcessingParameterField.Any,
                allowMultiple=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterString(
                self.OUTSIDE_POLYGON_ATTRIBUTE_VALUE,
                self.tr("Outside polygon value"),
                defaultValue="1",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.WATER_BODY,
                self.tr("Water body"),
                [QgsProcessing.TypeVectorPolygon],
                defaultValue="cobter_massa_dagua_a",
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.WATER_BODY_WITH_FLOW_EXPRESSION,
                self.tr("Filter expression for water bodies with flow"),
                parentLayerParameterName=self.WATER_BODY,
                optional=True,
                defaultValue=""" "tipo" in (1,2,9,10)""",
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
        inputDrainagesLyr: QgsVectorLayer = self.parameterAsLayer(
            parameters, self.INPUT_DRAINAGES, context
        )
        if inputDrainagesLyr is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT_DRAINAGES)
            )
        polygonRelationshipAttribute = self.parameterAsFields(
            parameters, self.INSIDE_POLYGON_ATTRIBUTE, context
        )[0]
        outsidePolygonValue = self.parameterAsString(
            parameters, self.OUTSIDE_POLYGON_ATTRIBUTE_VALUE, context
        )

        try:
            outsidePolygonValue = int(outsidePolygonValue)
        except:
            raise QgsProcessingException(
                self.tr("Invalid value for parameter OUTSIDE_POLYGON_ATTRIBUTE_VALUE")
            )

        waterBody = self.parameterAsLayer(parameters, self.WATER_BODY, context)
        waterBodyWithFlowExpression = self.parameterAsExpression(
            parameters, self.WATER_BODY_WITH_FLOW_EXPRESSION, context
        )
        self.prepareFlagSink(parameters, inputDrainagesLyr, QgsWkbTypes.LineString, context, addFeatId=True)

        nSteps = 10
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setProgressText(self.tr("Building drainage aux structures"))
        multiStepFeedback.setCurrentStep(currentStep)
        localCache = self.algRunner.runCreateFieldWithExpression(
            inputLyr=inputDrainagesLyr,
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        waterBody = self.algRunner.runCreateFieldWithExpression(
            inputLyr=waterBody,
            expression="$id",
            fieldName="wb_featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        waterBodyWithFlow = self.algRunner.runFilterExpression(
            inputLyr=waterBody,
            expression=waterBodyWithFlowExpression,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            waterBodyWithFlow,
            context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        drainagesOutside = self.algRunner.runExtractByLocation(
            inputLyr=localCache,
            intersectLyr=waterBodyWithFlow,
            predicate=AlgRunner.Disjoint,
            context=context,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        drainagesOutsideWithWrongAttributes = self.algRunner.runFilterExpression(
            inputLyr=drainagesOutside,
            expression=f""""{polygonRelationshipAttribute}" != {outsidePolygonValue}""",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        flagLambda = lambda x: self.flagFeature(
            flagGeom=x.geometry(),
            featid=x["featid"],
            flagText=self.tr(f"Features outside water body with attribute inside water body ({polygonRelationshipAttribute} != {outsidePolygonValue}).")
        )
        list(map(flagLambda, drainagesOutsideWithWrongAttributes.getFeatures()))
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        drainagesWithinWaterBody = self.algRunner.runExtractByLocation(
            inputLyr=localCache,
            intersectLyr=waterBodyWithFlow,
            predicate=AlgRunner.Within,
            context=context,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        drainagesInsideWithWrongAttributes = self.algRunner.runFilterExpression(
            inputLyr=drainagesWithinWaterBody,
            expression=f""""{polygonRelationshipAttribute}" = {outsidePolygonValue}""",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        flagLambda = lambda x: self.flagFeature(
            flagGeom=x.geometry(),
            featid=x["featid"],
            flagText=self.tr(f"Features inside water body with attribute inside water body ({polygonRelationshipAttribute} = {outsidePolygonValue}).")
        )
        list(map(flagLambda, drainagesInsideWithWrongAttributes.getFeatures())) 

        return {self.FLAGS: self.flag_id}


    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifydrainageversuswaterbodyattributeerrorsalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Drainage Versus Water Body Attribute Errors Algorithm")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("QA Tools: Drainage Flow Processes")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - QA Tools: Drainage Flow Processes"

    def tr(self, string):
        return QCoreApplication.translate(
            "IdentifyDrainageVersusWaterBodyAttributeErrorsAlgorithm", string
        )

    def createInstance(self):
        return IdentifyDrainageVersusWaterBodyAttributeErrorsAlgorithm()
