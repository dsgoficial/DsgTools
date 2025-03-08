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
    QgsWkbTypes,
    QgsProcessingParameterField,
    QgsProcessingParameterExpression,
    QgsProcessingParameterString,
    QgsVectorLayer,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm
from DsgTools.core.GeometricTools import graphHandler


class IdentifyDrainageVersusWaterBodyAttributeProblemsAlgorithm(ValidationAlgorithm):
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
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                self.WATER_BODY_WITH_FLOW_EXPRESSION,
                self.tr("Filter expression for water bodies with flow"),
                parentLayerParameterName=self.WATER_BODY,
                optional=True,
                defaultValue=""" "tipo_massa_dagua" in (1,2,9,10)""",
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
        try:
            import networkx as nx
        except ImportError:
            raise QgsProcessingException(
                self.tr(
                    "This algorithm requires the Python networkx library. Please install this library and try again."
                )
            )
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
        polygonRelationshipAttributeIdx = (
            inputDrainagesLyr.dataProvider().fieldNameIndex(
                polygonRelationshipAttribute
            )
        )
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
        self.prepareFlagSink(
            parameters,
            inputDrainagesLyr,
            inputDrainagesLyr.wkbType(),
            context,
            addFeatId=True,
        )
        featIdsToUpdate = set()

        nSteps = 12
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setProgressText(self.tr("Building drainage aux structures"))
        multiStepFeedback.setCurrentStep(currentStep)
        localCache, nodesLayer = graphHandler.buildAuxLayersPriorGraphBuilding(
            networkLayer=inputDrainagesLyr,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
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
            addEdgeLength=False,
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
            intersectLyr=waterBody,
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
        featIdsToUpdate |= set(
            f["featid"] for f in drainagesOutsideWithWrongAttributes.getFeatures()
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        pointsInsideWaterBodies = self.algRunner.runExtractByLocation(
            inputLyr=nodesLayer,
            intersectLyr=waterBody,
            predicate=AlgRunner.Intersects,
            context=context,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        pointDict = self.buildPointDict(pointsInsideWaterBodies, multiStepFeedback)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        featIdsToUpdate |= set(
            featid
            for featid, nodeSet in pointDict.items()
            if len(nodeSet) < 2
            and edgeDict[featid][polygonRelationshipAttribute] != outsidePolygonValue
        )
        self.updateDrainages(
            inputDrainagesLyr,
            polygonRelationshipAttributeIdx,
            outsidePolygonValue,
            featIdsToUpdate,
            commandMessage="Updating drainages outside polygons",
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        insideValueFeatsMap = self.verifyDrainagesInsideWaterBodies(
            polygonRelationshipAttribute,
            outsidePolygonValue,
            nodeDict,
            edgeDict,
            networkBidirectionalGraph,
            pointDict,
            feedback=multiStepFeedback,
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        for insideValue, featIdSet in insideValueFeatsMap.items():
            self.updateDrainages(
                inputDrainagesLyr,
                polygonRelationshipAttributeIdx,
                insideValue,
                featIdSet,
                commandMessage=self.tr(
                    f"Updating drainage lines inside water bodies with value {insideValue}"
                ),
            )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        invalidPointSet = set(
            featid
            for featid, nodeSet in pointDict.items()
            if len(nodeSet) >= 2
            and edgeDict[featid][polygonRelationshipAttribute] == outsidePolygonValue
        )
        flagLambda = lambda x: self.flagFeature(
            flagGeom=edgeDict[x].geometry(),
            flagText=self.tr(
                f"Drainage inside water body with attribute {polygonRelationshipAttribute}={outsidePolygonValue}"
            ),
            featid=x,
        )
        list(map(flagLambda, invalidPointSet))

        return {self.FLAGS: self.flag_id}

    def verifyDrainagesInsideWaterBodies(
        self,
        polygonRelationshipAttribute,
        outsidePolygonValue,
        nodeDict,
        edgeDict,
        networkBidirectionalGraph,
        pointDict,
        feedback,
    ):
        insideValueFeatsMap = defaultdict(set)
        for featid, nodeSet in pointDict.items():
            if feedback.isCanceled():
                break
            if edgeDict[featid][polygonRelationshipAttribute] != outsidePolygonValue:
                continue
            if len(nodeSet) >= 2:
                continue

            insideNodeFeat = next(iter(nodeSet))
            node_wkb = insideNodeFeat.geometry().asWkb()

            if node_wkb not in nodeDict:
                continue

            node_id = nodeDict[node_wkb]

            # Encontrar feições conectadas através deste nó
            for neighbor in networkBidirectionalGraph.neighbors(node_id):
                if networkBidirectionalGraph.degree(neighbor) != 2:
                    continue
                try:
                    neighbor_featid = networkBidirectionalGraph[node_id][neighbor][
                        "featid"
                    ]
                except:
                    continue

                if neighbor_featid == featid or neighbor_featid not in edgeDict:
                    continue
                if (
                    edgeDict[neighbor_featid][polygonRelationshipAttribute]
                    != outsidePolygonValue
                ):
                    insideValue = edgeDict[neighbor_featid][
                        polygonRelationshipAttribute
                    ]
                    insideValueFeatsMap[insideValue].add(featid)
                    break
        return insideValueFeatsMap

    def updateDrainages(
        self,
        inputDrainagesLyr,
        polygonRelationshipAttributeIdx,
        outsidePolygonValue,
        featIdsToUpdate,
        commandMessage,
    ):
        inputDrainagesLyr.startEditing()
        inputDrainagesLyr.beginEditCommand(commandMessage)
        changeValuesLambda = lambda x: inputDrainagesLyr.changeAttributeValue(
            x, polygonRelationshipAttributeIdx, outsidePolygonValue
        )
        list(map(changeValuesLambda, featIdsToUpdate))
        inputDrainagesLyr.endEditCommand()

    def buildPointDict(self, pointsInsideWaterBodies, feedback):
        pointDict = defaultdict(set)
        for nodeFeat in pointsInsideWaterBodies.getFeatures():
            if feedback.isCanceled():
                break
            geom = nodeFeat.geometry()
            pointDict[nodeFeat["featid"]].add(nodeFeat)
        return pointDict

    def changeAttributeValueOfOutsidePolygonDrainages(self):
        pass

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "identifydrainageversuswaterbodyattributeproblemsalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(
            "Identify Drainage Versus Water Body Attribute Problems Algorithm"
        )

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
            "IdentifyDrainageVersusWaterBodyAttributeProblemsAlgorithm", string
        )

    def createInstance(self):
        return IdentifyDrainageVersusWaterBodyAttributeProblemsAlgorithm()
