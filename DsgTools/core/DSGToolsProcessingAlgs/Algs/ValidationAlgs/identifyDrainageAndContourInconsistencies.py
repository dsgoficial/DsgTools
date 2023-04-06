# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-03-29
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

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.validationAlgorithm import (
    ValidationAlgorithm,
)
from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner
from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsProcessing,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsFeature,
    QgsField,
    QgsGeometry,
    QgsPointXY,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSource,
    QgsVectorLayerUtils,
    QgsProcessingParameterField,
    QgsWkbTypes,
)
from DsgTools.core.GeometricTools import graphHandler


class IdentifyDrainageAndContourInconsistencies(ValidationAlgorithm):

    INPUT_DRAINAGES = "INPUT_DRAINAGES"
    INPUT_CONTOURS = "INPUT_CONTOURS"

    FLAGS = "FLAGS"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_DRAINAGES,
                self.tr("Input drainages"),
                [QgsProcessing.TypeVectorLine],
                optional=False,
                defaultValue="elemnat_trecho_drenagem_l",
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
                None,
                self.INPUT_CONTOURS,
                QgsProcessingParameterField.Any,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.FLAGS, self.tr("{0} Flags").format(self.displayName())
            )
        )

    def processAlgorithm(self, parameters, context, feedback):

        try:
            import networkx as nx
        except ImportError:
            raise QgsProcessingException(
                self.tr(
                    "This algorithm requires the Python networkx library. Please install this library and try again."
                )
            )
        algRunner = AlgRunner()
        multiStepFeedback = QgsProcessingMultiStepFeedback(6, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        inputDrainagesLyr = algRunner.runCreateFieldWithExpression(
            inputLyr=parameters[self.INPUT_DRAINAGES],
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        inputContoursLyr = algRunner.runCreateFieldWithExpression(
            inputLyr=parameters[self.INPUT_CONTOURS],
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            inputLyr=inputContoursLyr, context=context, feedback=multiStepFeedback
        )
        self.prepareFlagSink(parameters, inputDrainagesLyr, QgsWkbTypes.Point, context)
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        nodesLayer = algRunner.runExtractSpecificVertices(
            inputLyr=inputDrainagesLyr,
            vertices="0,-1",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        intersectionNodesLayer = algRunner.runLineIntersections(
            inputLyr=inputDrainagesLyr,
            intersectLyr=inputContoursLyr,
            context=context,
            feedback=multiStepFeedback,
        )

        return {self.FLAGS: self.flag_id}

    def tr(self, string):
        return QCoreApplication.translate("Processing", string)

    def createInstance(self):
        return IdentifyDrainageAndContourInconsistencies()

    def name(self):
        return "identifydrainageandcontourinconsistencies"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Identify Drainage and Contour Inconsistencies")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Quality Assurance Tools (Network Processes)")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools: Quality Assurance Tools (Network Processes)"

    def shortHelpString(self):
        return self.tr(
            "O algoritmo orderna ou direciona fluxo, como linhas de drenagem "
        )
