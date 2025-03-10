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
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm
from DsgTools.core.GeometricTools import graphHandler


class FixDrainageVersusWaterBodyAttributeAlgorithm(ValidationAlgorithm):
    INPUT_DRAINAGES = "INPUT_DRAINAGES"
    INSIDE_POLYGON_ATTRIBUTE = "INSIDE_POLYGON_ATTRIBUTE"
    OUTSIDE_POLYGON_ATTRIBUTE_VALUE = "OUTSIDE_POLYGON_ATTRIBUTE_VALUE"
    WATER_BODY = "WATER_BODY"
    WATER_BODY_WITH_FLOW_EXPRESSION = "WATER_BODY_WITH_FLOW_EXPRESSION"

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
        
        featIdsToUpdate |= set(
            f["featid"] for f in drainagesOutsideWithWrongAttributes.getFeatures()
        )

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        pointsInsideWaterBodies = self.algRunner.runJoinAttributesByLocation(
            inputLyr=nodesLayer,
            joinLyr=waterBody,
            predicateList=[AlgRunner.Intersects],
            context=context,
            feedback=multiStepFeedback,
        )
        
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        
        wbBounds = self.algRunner.runBoundary(
            inputLayer=waterBodyWithFlow,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(wbBounds, context=context, feedback=multiStepFeedback, is_child_algorithm=True)
        
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        drainagesThatIntersectWaterBodyWithFlowBounds = self.algRunner.runExtractByLocation(
            inputLyr=localCache,
            intersectLyr=wbBounds,
            context=context,
            predicate=AlgRunner.Intersects,
            feedback=multiStepFeedback
        )
        drainagesThatIntersectWBIdSet = set(f["featid"] for f in drainagesThatIntersectWaterBodyWithFlowBounds.getFeatures())
        
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        pointDict = self.buildPointDict(pointsInsideWaterBodies, drainagesThatIntersectWBIdSet, multiStepFeedback)
        
        drainagesWithinWaterBody = self.algRunner.runExtractByLocation(
            inputLyr=localCache,
            intersectLyr=waterBodyWithFlow,
            predicate=AlgRunner.Within,
            context=context,
            feedback=multiStepFeedback,
        )

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
        multiStepFeedback.pushInfo(self.tr(f"{len(featIdsToUpdate)} outside polygons changed to {polygonRelationshipAttribute} = {outsidePolygonValue}"))

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        drainagesWithinWithWrongAttributes = self.algRunner.runFilterExpression(
            inputLyr=drainagesWithinWaterBody,
            expression=f""""{polygonRelationshipAttribute}" = {outsidePolygonValue}""",
            context=context,
            feedback=multiStepFeedback,
        )
        if drainagesWithinWithWrongAttributes.featureCount() == 0:
            return {}
        
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        drainagesWithinWaterBodySet = set(f["featid"] for f in drainagesWithinWaterBody.getFeatures())
        insideValueFeatsMap = self.verifyDrainagesInsideWaterBodies(
            drainagesWithinWithWrongAttributes,
            drainagesWithinWaterBodySet,
            polygonRelationshipAttribute,
            outsidePolygonValue,
            edgeDict,
            networkBidirectionalGraph,
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

        return {}

    def verifyDrainagesInsideWaterBodies(
        self,
        drainagesWithinWithWrongAttributes: QgsVectorLayer,
        drainagesWithinWaterBodySet: Set[int],
        polygonRelationshipAttribute: str,
        outsidePolygonValue: int,
        edgeDict: Dict[int, QgsFeature],
        networkBidirectionalGraph: Any,
        feedback: QgsFeedback,
    ) -> Dict[int, Dict[int, set]]:
        insideValueFeatsMap = defaultdict(set)
        for feat in drainagesWithinWithWrongAttributes.getFeatures():
            featid = feat["featid"]
            if feedback.isCanceled():
                break
            neighborFeatIds = graphHandler.connectedEdgesFeatIds(networkBidirectionalGraph, featid)
            neighborFeatIdsWithinWaterBody = neighborFeatIds.intersection(drainagesWithinWaterBodySet)
            if len(neighborFeatIdsWithinWaterBody) > 2:
                continue
            neighborAttributeDict = defaultdict(int)
            for nid in neighborFeatIdsWithinWaterBody:
                attr = edgeDict[nid][polygonRelationshipAttribute]
                if attr == outsidePolygonValue:
                    continue
                neighborAttributeDict[attr] += 1
            if len(neighborAttributeDict) > 1:
                continue
            attrValue = [i for i in neighborAttributeDict.keys()][0]
            insideValueFeatsMap[attrValue].add(featid)
        return insideValueFeatsMap

    def updateDrainages(
        self,
        inputDrainagesLyr,
        polygonRelationshipAttributeIdx,
        outsidePolygonValue,
        featIdsToUpdate,
        commandMessage,
    ):
        if len(featIdsToUpdate) == 0:
            return
        inputDrainagesLyr.startEditing()
        inputDrainagesLyr.beginEditCommand(commandMessage)
        for fieldId in featIdsToUpdate:
            inputDrainagesLyr.changeAttributeValue(
                fieldId, polygonRelationshipAttributeIdx, outsidePolygonValue
            )
        # changeValuesLambda = lambda x: inputDrainagesLyr.changeAttributeValue(
        #     x, polygonRelationshipAttributeIdx, outsidePolygonValue
        # )
        # list(map(changeValuesLambda, featIdsToUpdate))
        inputDrainagesLyr.endEditCommand()

    def buildPointDict(self, pointsInsideWaterBodies, drainagesThatIntersectWBIdSet, feedback):
        pointDict = defaultdict(set)
        for nodeFeat in pointsInsideWaterBodies.getFeatures():
            if feedback.isCanceled():
                break
            featid = nodeFeat["featid"]
            if featid not in drainagesThatIntersectWBIdSet:
                continue
            pointDict[featid].add(nodeFeat)
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
        return "fixdrainageversuswaterbodyattributealgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(
            "Fix Drainage Versus Water Body Attribute Algorithm"
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
            "FixDrainageVersusWaterBodyAttributeAlgorithm", string
        )

    def createInstance(self):
        return FixDrainageVersusWaterBodyAttributeAlgorithm()
