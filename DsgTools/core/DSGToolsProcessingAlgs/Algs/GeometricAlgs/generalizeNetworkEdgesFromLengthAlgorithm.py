# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-11-27
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
from typing import Dict, Set, Tuple
from PyQt5.QtCore import QCoreApplication
from DsgTools.core.GeometricTools import graphHandler
from qgis.PyQt.QtCore import QByteArray
from qgis.core import (
    Qgis,
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterEnum,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsFeedback,
    QgsProcessingContext,
    QgsGeometry,
    QgsFeature,
    QgsVectorLayer,
    QgsProcessingParameterNumber,
    QgsProcessingParameterBoolean,
)

from ...algRunner import AlgRunner
from ..ValidationAlgs.validationAlgorithm import ValidationAlgorithm


class GeneralizeNetworkEdgesWithLengthAlgorithm(ValidationAlgorithm):
    NETWORK_LAYER = "NETWORK_LAYER"
    MIN_LENGTH = "MIN_LENGTH"
    GEOGRAPHIC_BOUNDS_LAYER = "GEOGRAPHIC_BOUNDS_LAYER"
    WATER_BODIES_LAYER = "WATER_BODIES_LAYER"
    METHOD = "METHOD"

    def initAlgorithm(self, config):
        """
        Parameter setting.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.NETWORK_LAYER,
                self.tr("Network layer"),
                [QgsProcessing.TypeVectorLine],
            )
        )
        self.addParameter(
            QgsProcessingParameterNumber(
                self.MIN_LENGTH,
                self.tr("Minimum size"),
                minValue=0,
                type=QgsProcessingParameterNumber.Double,
                defaultValue=0.001,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.WATER_BODIES_LAYER,
                self.tr("Water bodies layer"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDS_LAYER,
                self.tr("Reference layer"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )
        self.selectionIdDict = {
            1: Qgis.SelectBehavior.SetSelection,
            2: Qgis.SelectBehavior.AddToSelection,
            3: Qgis.SelectBehavior.IntersectSelection,
            4: Qgis.SelectBehavior.RemoveFromSelection,
        }
        self.method = [
            self.tr("Remove features from input layer"),
            self.tr("Modify current selection by creating new selection"),
            self.tr("Modify current selection by adding to current selection"),
            self.tr("Modify current selection by selecting within current selection"),
            self.tr("Modify current selection by removing from current selection"),
        ]

        self.addParameter(
            QgsProcessingParameterEnum(
                self.METHOD, self.tr("Method"), options=self.method, defaultValue=0
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """
        try:
            import networkx as nx
        except ImportError:
            raise QgsProcessingException(
                self.tr(
                    "This algorithm requires the Python networkx library. Please install this library and try again."
                )
            )
        # get the network handler
        self.algRunner = AlgRunner()
        networkLayer = self.parameterAsLayer(parameters, self.NETWORK_LAYER, context)
        filterExpression = self.parameterAsExpression(
            parameters, self.FILTER_EXPRESSION, context
        )
        if filterExpression == "":
            filterExpression = None
        oceanLayer = self.parameterAsLayer(parameters, self.WATER_BODIES_LAYER, context)
        waterBodyWithFlowLayer = self.parameterAsLayer(
            parameters, self.WATER_BODY_WITH_FLOW_LAYER, context
        )
        waterSinkLayer = self.parameterAsLayer(parameters, self.SINK_LAYER, context)
        geographicBoundsLayer = self.parameterAsLayer(
            parameters, self.GEOGRAPHIC_BOUNDS_LAYER, context
        )
        nSteps = (
            15
            + (runFlowCheck is True)
            + (runLoopCheck is True)
            + (waterBodyWithFlowLayer is not None)
        )
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Building aux structures"))
        localCache, nodesLayer = graphHandler.buildAuxLayersPriorGraphBuilding(
            networkLayer=networkLayer,
            context=context,
            geographicBoundsLayer=geographicBoundsLayer,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Building graph aux structures"))
        (
            nodeDict,
            nodeIdDict,
            edgeDict,
            hashDict,
            networkBidirectionalGraph,
            nodeLayerIdDict,
        ) = graphHandler.buildAuxStructures(
            nx,
            nodesLayer=nodesLayer,
            edgesLayer=localCache,
            feedback=multiStepFeedback,
            useWkt=False,
            computeNodeLayerIdDict=True,
            addEdgeLength=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "generalizenetworkedgeswithlengthalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Generalize Network Edges With Length Algorithm")

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr("Generalization Algorithms")

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "DSGTools - Generalization Algorithms"

    def tr(self, string):
        return QCoreApplication.translate(
            "GeneralizeNetworkEdgesWithLengthAlgorithm", string
        )

    def createInstance(self):
        return GeneralizeNetworkEdgesWithLengthAlgorithm()
