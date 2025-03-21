# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-01-02
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
    QgsProcessing,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterVectorLayer,
    QgsWkbTypes,
    QgsFeedback,
    QgsProcessingContext,
    QgsGeometry,
    QgsFeature,
    QgsVectorLayer,
    QgsProcessingParameterExpression,
    QgsProcessingParameterBoolean,
)

from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class FixDrainageFlowAlgorithm(ValidationAlgorithm):
    NETWORK_LAYER = "NETWORK_LAYER"
    NETWORK_FILTER_EXPRESSION = "NETWORK_FILTER_EXPRESSION"
    SINK_AND_SPILLWAY_LAYER = "SINK_AND_SPILLWAY_LAYER"
    SINK_FILTER_EXPRESSION = "SINK_FILTER_EXPRESSION"
    SPILLWAY_FILTER_EXPRESSION = "SPILLWAY_FILTER_EXPRESSION"
    GEOGRAPHIC_BOUNDS_LAYER = "GEOGRAPHIC_BOUNDS_LAYER"
    WATER_BODY_LAYER = "WATER_BODY_LAYER"
    WATER_BODY_WITH_FLOW_FILTER_EXPRESSION = "WATER_BODY_WITH_FLOW_FILTER_EXPRESSION"
    WATER_BODY_WITHOUT_FLOW_FILTER_EXPRESSION = (
        "WATER_BODY_WITHOUT_FLOW_FILTER_EXPRESSION"
    )
    OCEAN_FILTER_EXPRESSION = "OCEAN_FILTER_EXPRESSION"
    RUN_FLOW_CHECK = "RUN_FLOW_CHECK"
    RUN_LOOP_CHECK = "RUN_LOOP_CHECK"
    POINT_FLAGS = "POINT_FLAGS"
    LINE_FLAGS = "LINE_FLAGS"
    POLYGON_FLAGS = "POLYGON_FLAGS"

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
            QgsProcessingParameterExpression(
                name=self.NETWORK_FILTER_EXPRESSION,
                description=self.tr("Filter expression for nodes with fixed flow"),
                parentLayerParameterName=self.NETWORK_LAYER,
                optional=True,
                defaultValue=""""direcao_fixada" = 1""",
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDS_LAYER,
                self.tr("Reference layer"),
                [QgsProcessing.TypeVectorPolygon],
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.WATER_BODY_LAYER,
                self.tr("Water body layer"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                name=self.WATER_BODY_WITH_FLOW_FILTER_EXPRESSION,
                description=self.tr("Filter expression for water bodies with flow"),
                parentLayerParameterName=self.WATER_BODY_LAYER,
                defaultValue=""""tipo" in (1,2,9,10)""",
                optional=True,
            )
        )

        self.addParameter(
            QgsProcessingParameterExpression(
                name=self.WATER_BODY_WITHOUT_FLOW_FILTER_EXPRESSION,
                description=self.tr("Filter expression for water bodies without flow"),
                parentLayerParameterName=self.WATER_BODY_LAYER,
                defaultValue=""""tipo" in (6,7)""",
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                name=self.OCEAN_FILTER_EXPRESSION,
                description=self.tr("Filter expression for ocean"),
                parentLayerParameterName=self.WATER_BODY_LAYER,
                defaultValue=""""tipo" in (3,4,5)""",
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.SINK_AND_SPILLWAY_LAYER,
                self.tr("Water sink and spillway layer"),
                [QgsProcessing.TypeVectorPoint],
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                name=self.SINK_FILTER_EXPRESSION,
                description=self.tr("Filter expression for sink layer"),
                parentLayerParameterName=self.SINK_AND_SPILLWAY_LAYER,
                optional=True,
                defaultValue=""""tipo" in (3,4)""",
            )
        )
        self.addParameter(
            QgsProcessingParameterExpression(
                name=self.SPILLWAY_FILTER_EXPRESSION,
                description=self.tr("Filter expression for spillway layer"),
                parentLayerParameterName=self.SINK_AND_SPILLWAY_LAYER,
                optional=True,
                defaultValue=""""tipo" in (5)""",
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.RUN_FLOW_CHECK,
                self.tr("Run flow checks at the end of the process"),
                defaultValue=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.RUN_LOOP_CHECK,
                self.tr("Run loop checks at the end of the process"),
                defaultValue=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POINT_FLAGS,
                self.tr("{0} network node errors").format(self.displayName()),
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.LINE_FLAGS, self.tr("{0} line errors").format(self.displayName())
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.POLYGON_FLAGS,
                self.tr("{0} polygon errors").format(self.displayName()),
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
            parameters, self.NETWORK_FILTER_EXPRESSION, context
        )
        if filterExpression == "":
            filterExpression = None
        waterBodyLayer = self.parameterAsLayer(
            parameters, self.WATER_BODY_LAYER, context
        )
        oceanFilterExpression = self.parameterAsExpression(
            parameters, self.OCEAN_FILTER_EXPRESSION, context
        )
        if oceanFilterExpression == "":
            oceanFilterExpression = None
        if waterBodyLayer is not None and oceanFilterExpression is None:
            raise QgsProcessingException(
                "There must be a oceanFilterExpression if a water body layer is selected."
            )
        waterBodyWithFlowFilterExpression = self.parameterAsExpression(
            parameters, self.WATER_BODY_WITH_FLOW_FILTER_EXPRESSION, context
        )
        if waterBodyWithFlowFilterExpression == "":
            waterBodyWithFlowFilterExpression = None
        waterBodyWithoutFlowFilterExpression = self.parameterAsExpression(
            parameters, self.WATER_BODY_WITHOUT_FLOW_FILTER_EXPRESSION, context
        )
        if waterBodyWithoutFlowFilterExpression == "":
            waterBodyWithoutFlowFilterExpression = None
        if waterBodyLayer is not None and (
            waterBodyWithFlowFilterExpression is None
            or waterBodyWithoutFlowFilterExpression is None
        ):
            raise QgsProcessingException(
                "There must be a waterBodyWithFlowExpression and a waterBodyWithoutFlowExpression if a water body layer is selected."
            )
        sinkAndSpillwayLayer = self.parameterAsLayer(
            parameters, self.SINK_AND_SPILLWAY_LAYER, context
        )
        sinkFilterExpression = self.parameterAsExpression(
            parameters, self.SINK_FILTER_EXPRESSION, context
        )
        if sinkFilterExpression == "":
            sinkFilterExpression = None
        spillwayFilterExpression = self.parameterAsExpression(
            parameters, self.SPILLWAY_FILTER_EXPRESSION, context
        )
        if spillwayFilterExpression == "":
            spillwayFilterExpression = None
        if sinkAndSpillwayLayer is not None and (
            sinkFilterExpression is None or spillwayFilterExpression is None
        ):
            raise QgsProcessingException(
                "There must be a sinkFilterExpression and a spillwayFilterExpression if a sinkAndSpillwayLayer is selected."
            )
        geographicBoundsLayer = self.parameterAsLayer(
            parameters, self.GEOGRAPHIC_BOUNDS_LAYER, context
        )
        runFlowCheck = self.parameterAsBool(parameters, self.RUN_FLOW_CHECK, context)
        runLoopCheck = self.parameterAsBool(parameters, self.RUN_LOOP_CHECK, context)
        (self.point_flags_sink, self.point_flags_sink_id) = self.parameterAsSink(
            parameters,
            self.POINT_FLAGS,
            context,
            self.getFlagFields(),
            QgsWkbTypes.Point,
            networkLayer.sourceCrs(),
        )
        (self.line_flags_sink, self.line_flags_sink_id) = self.parameterAsSink(
            parameters,
            self.LINE_FLAGS,
            context,
            self.getFlagFields(),
            QgsWkbTypes.LineString,
            networkLayer.sourceCrs(),
        )
        (self.polygon_flags_sink, self.polygon_flags_sink_id) = self.parameterAsSink(
            parameters,
            self.POLYGON_FLAGS,
            context,
            self.getFlagFields(),
            QgsWkbTypes.Polygon,
            networkLayer.sourceCrs(),
        )
        nSteps = (
            15
            + (sinkAndSpillwayLayer is not None)
            + (waterBodyLayer is not None) * 2
            + (runFlowCheck is True)
            + (runLoopCheck is True)
        )
        multiStepFeedback = QgsProcessingMultiStepFeedback(nSteps, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Running preliminary checks"))
        if not self.networkHasFlowIssues(
            parameters, context, feedback=multiStepFeedback
        ):
            multiStepFeedback.pushInfo(
                self.tr("Found 0 errors on data, skipping process.")
            )
            return {
                self.NETWORK_LAYER: networkLayer,
                self.POINT_FLAGS: self.point_flags_sink_id,
                self.LINE_FLAGS: self.line_flags_sink_id,
            }
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Building aux structures"))
        localCache = self.algRunner.runCreateFieldWithExpression(
            inputLyr=networkLayer,
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        drainagesWithCorrectFlow = (
            self.algRunner.runFilterExpression(
                inputLyr=localCache,
                expression=filterExpression,
                context=context,
                feedback=multiStepFeedback,
            )
            if filterExpression is not None
            else None
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=localCache,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        localCache = self.algRunner.runExtractByLocation(
            inputLyr=localCache,
            intersectLyr=geographicBoundsLayer,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=localCache,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        nodesLayer = self.algRunner.runExtractSpecificVertices(
            inputLyr=localCache,
            vertices="0,-1",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        nodesLayer = self.algRunner.runCreateFieldWithExpression(
            inputLyr=nodesLayer,
            expression="$id",
            fieldName="nfeatid",
            fieldType=1,
            context=context,
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
        initialDiG = (
            None
            if drainagesWithCorrectFlow is None
            else graphHandler.buildDirectionalGraphFromIdList(
                nx,
                networkBidirectionalGraph,
                nodeDict,
                hashDict,
                set(f["featid"] for f in drainagesWithCorrectFlow.getFeatures()),
                feedback=multiStepFeedback,
            )
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Computing constraint nodes"))
        (fixedInNodeSet, fixedOutNodeSet) = self.getInAndOutNodesOnGeographicBounds(
            nodeDict=nodeDict,
            nodesLayer=nodesLayer,
            geographicBoundsLayer=geographicBoundsLayer,
            context=context,
            feedback=multiStepFeedback,
        )
        constantSinkPointSet = set()
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        if sinkAndSpillwayLayer is not None:
            waterSinkLayer = (
                self.algRunner.runFilterExpression(
                    inputLyr=sinkAndSpillwayLayer,
                    expression=sinkFilterExpression,
                    context=context,
                    feedback=multiStepFeedback,
                )
                if sinkFilterExpression is not None
                else sinkAndSpillwayLayer
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            selectedNodesFromWaterSink = self.algRunner.runExtractByLocation(
                inputLyr=nodesLayer,
                intersectLyr=waterSinkLayer,
                context=context,
                predicate=[AlgRunner.Equals],
                feedback=multiStepFeedback,
            )
            for feat in selectedNodesFromWaterSink.getFeatures():
                if multiStepFeedback.isCanceled():
                    break
                constantSinkPointSet.add(nodeDict[nodeLayerIdDict[feat["nfeatid"]]])
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        if waterBodyLayer is not None and waterBodyLayer.featureCount() > 0:
            oceanLayer = self.algRunner.runFilterExpression(
                inputLyr=parameters[self.WATER_BODY_LAYER],
                expression=oceanFilterExpression,
                context=context,
                feedback=multiStepFeedback,
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            if oceanLayer.featureCount() > 0:
                buffer = self.algRunner.runBuffer(
                    inputLayer=oceanLayer,
                    distance=1e-6,
                    context=context,
                    is_child_algorithm=True,
                )
                selectedNodesFromOcean = self.algRunner.runExtractByLocation(
                    inputLyr=nodesLayer,
                    intersectLyr=buffer,
                    context=context,
                    predicate=[AlgRunner.Intersects],
                    feedback=multiStepFeedback,
                )
                for feat in selectedNodesFromOcean.getFeatures():
                    if multiStepFeedback.isCanceled():
                        break
                    constantSinkPointSet.add(nodeDict[nodeLayerIdDict[feat["nfeatid"]]])
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            waterBodyWithFlowLayer = self.algRunner.runFilterExpression(
                inputLyr=waterBodyLayer,
                expression=waterBodyWithFlowFilterExpression,
                context=context,
                feedback=multiStepFeedback,
            )
            if waterBodyWithFlowLayer.featureCount() > 0:
                selectedNodes = self.algRunner.runExtractByLocation(
                    inputLyr=nodesLayer,
                    intersectLyr=waterBodyWithFlowLayer,
                    context=context,
                    predicate=[AlgRunner.Intersects],
                    feedback=multiStepFeedback,
                )
                nodesDict = defaultdict(list)
                for nodeFeat in selectedNodes.getFeatures():
                    nodesDict[nodeFeat["featid"]].append(nodeFeat)
                edgesWithinWaterBodiesIdSet = set(featid for featid in nodesDict.keys())
                # penalize edges not in water bodies
                for (a, b) in networkBidirectionalGraph.edges:
                    if (
                        networkBidirectionalGraph[a][b]["featid"]
                        in edgesWithinWaterBodiesIdSet
                    ):
                        continue
                    networkBidirectionalGraph[a][b]["length"] = (
                        networkBidirectionalGraph[a][b]["length"] * 1e8
                    )
                    networkBidirectionalGraph[a][b]["inside_river"] = True

        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(self.tr("Computing flow graph"))
        DiG = graphHandler.buildAuxFlowGraph(
            nx,
            networkBidirectionalGraph,
            fixedInNodeSet,
            fixedOutNodeSet,
            nodeIdDict,
            constantSinkPointSet,
            DiG=initialDiG,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.updateFeatures(
            networkLayer,
            DiG,
            nodeIdDict,
            edgeDict,
            hashDict,
            feedback=multiStepFeedback,
        )
        if runFlowCheck:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.setProgressText(self.tr("Finding flow issues"))
            (
                pointFlagLyr,
                lineFlagLyr,
                polygonFlagLyr,
            ) = (
                self.algRunner.self.algRunner.runIdentifyDrainageFlowIssuesWithHydrographyElementsAlgorithm(
                    inputDrainagesLayer=networkLayer,
                    waterBodyLayer=parameters[self.WATER_BODY_LAYER],
                    waterBodyWithFlowExpression=parameters[
                        self.WATER_BODY_WITH_FLOW_FILTER_EXPRESSION
                    ],
                    waterBodyWithoutFlowExpression=parameters[
                        self.WATER_BODY_WITHOUT_FLOW_FILTER_EXPRESSION
                    ],
                    sinkAndSpillwayLayer=parameters[self.SINK_AND_SPILLWAY_LAYER],
                    sinkFilterExpression=parameters[self.SINK_FILTER_EXPRESSION],
                    spillwayFilterExpression=parameters[self.SPILLWAY_FILTER_EXPRESSION],
                    geographicBoundsLayer=parameters[self.GEOGRAPHIC_BOUNDS_LAYER],
                    context=context,
                    feedback=multiStepFeedback,
                )
            )
            pointFlagLambda = lambda x: self.flagFeature(
                x.geometry(), flagText=x["reason"], sink=self.point_flags_sink
            )
            list(map(pointFlagLambda, pointFlagLyr.getFeatures()))
            multiStepFeedback.setProgressText(
                self.tr(f"Found {pointFlagLyr.featureCount()} points of flow issues.")
            )
            lineFlagLambda = lambda x: self.flagFeature(
                x.geometry(), flagText=x["reason"], sink=self.line_flags_sink
            )
            list(map(lineFlagLambda, lineFlagLyr.getFeatures()))
            multiStepFeedback.setProgressText(
                self.tr(f"Found {lineFlagLyr.featureCount()} lines of flow issues.")
            )
            polygonFlagLambda = lambda x: self.flagFeature(
                x.geometry(), flagText=x["reason"], sink=self.polygon_flags_sink
            )
            list(map(polygonFlagLambda, polygonFlagLyr.getFeatures()))
            multiStepFeedback.setProgressText(
                self.tr(
                    f"Found {polygonFlagLyr.featureCount()} polygon of flow issues."
                )
            )

        if runLoopCheck:
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            multiStepFeedback.pushInfo(self.tr("Finding loop issues"))
            lineFlagLyr = self.algRunner.runIdentifyLoops(
                inputLyr=networkLayer,
                context=context,
                buildLocalCache=True,
                feedback=multiStepFeedback,
            )
            lineFlagLambda = lambda x: self.flagFeature(
                x.geometry(), flagText=x["reason"], sink=self.line_flags_sink
            )
            list(map(lineFlagLambda, lineFlagLyr.getFeatures()))

            multiStepFeedback.pushInfo(
                self.tr(f"Found {lineFlagLyr.featureCount()} loop issues.")
            )
        return {
            self.NETWORK_LAYER: networkLayer,
            self.POINT_FLAGS: self.point_flags_sink_id,
            self.LINE_FLAGS: self.line_flags_sink_id,
        }

    def networkHasFlowIssues(self, parameters, context, feedback):
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        lineFlagLyr = self.algRunner.runIdentifyLoops(
            inputLyr=parameters[self.NETWORK_LAYER],
            context=context,
            buildLocalCache=True,
            feedback=multiStepFeedback,
        )
        if lineFlagLyr.featureCount() > 0:
            return True
        multiStepFeedback.setCurrentStep(1)
        outputFlagsLayers = self.algRunner.runIdentifyDrainageFlowIssuesWithHydrographyElementsAlgorithm(
            inputDrainagesLayer=parameters[self.NETWORK_LAYER],
            waterBodyLayer=parameters[self.WATER_BODY_LAYER],
            waterBodyWithFlowExpression=parameters[
                self.WATER_BODY_WITH_FLOW_FILTER_EXPRESSION
            ],
            waterBodyWithoutFlowExpression=parameters[
                self.WATER_BODY_WITHOUT_FLOW_FILTER_EXPRESSION
            ],
            sinkAndSpillwayLayer=parameters[self.SINK_AND_SPILLWAY_LAYER],
            sinkFilterExpression=parameters[self.SINK_FILTER_EXPRESSION],
            spillwayFilterExpression=parameters[self.SPILLWAY_FILTER_EXPRESSION],
            geographicBoundsLayer=parameters[self.GEOGRAPHIC_BOUNDS_LAYER],
            context=context,
            feedback=multiStepFeedback,
        )
        if any(lyr.featureCount() > 0 for lyr in outputFlagsLayers):
            return True
        return False

    def getInAndOutNodesOnGeographicBounds(
        self,
        nodeDict: Dict[QByteArray, int],
        nodesLayer: QgsVectorLayer,
        geographicBoundsLayer: QgsVectorLayer,
        context: QgsProcessingContext,
        feedback: QgsFeedback,
    ) -> Tuple[Set[int], Set[int]]:
        """
        Get the in-nodes and out-nodes that fall within the geographic bounds.

        Args:
            self: The instance of the class.
            nodeDict: A dictionary mapping node geometry to an auxiliary ID.
            nodesLayer: A QgsVectorLayer representing nodes in the network.
            geographicBoundsLayer: The geographic bounds layer.
            context: The context object for the processing.
            feedback: The QgsFeedback object for providing feedback during processing.

        Returns:
            A tuple containing two sets: fixedInNodeSet and fixedOutNodeSet.
            - fixedInNodeSet: A set of in-nodes that fall within the geographic bounds.
            - fixedOutNodeSet: A set of out-nodes that fall within the geographic bounds.

        Notes:
            This function performs the following steps:
            1. Creates a spatial index for the nodesLayer.
            2. Extracts the nodes that are outside the geographic bounds.
            3. Iterates over the nodes outside the geographic bounds and adds them to the appropriate set.
            4. Returns the sets of in-nodes and out-nodes within the geographic bounds.

            The feedback object is used to monitor the progress of the function.
        """
        multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback)
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        self.algRunner.runCreateSpatialIndex(
            inputLyr=nodesLayer,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        nodesOutsideGeographicBounds = self.algRunner.runExtractByLocation(
            inputLyr=nodesLayer,
            intersectLyr=geographicBoundsLayer,
            predicate=[AlgRunner.Disjoint],
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1

        multiStepFeedback.setCurrentStep(currentStep)
        fixedInNodeSet, fixedOutNodeSet = set(), set()
        nFeats = nodesOutsideGeographicBounds.featureCount()
        if nFeats == 0:
            return fixedInNodeSet, fixedOutNodeSet
        stepSize = 100 / nFeats
        for current, nodeFeat in enumerate(nodesOutsideGeographicBounds.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            selectedSet = (
                fixedInNodeSet if nodeFeat["vertex_pos"] == 0 else fixedOutNodeSet
            )
            geom = nodeFeat.geometry()
            selectedSet.add(nodeDict[geom.asWkb()])
            multiStepFeedback.setProgress(current * stepSize)
        return fixedInNodeSet, fixedOutNodeSet

    def updateFeatures(
        self, networkLayer, DiG, nodeIdDict, edgeDict, hashDict, feedback
    ):
        def nodeCompairFunc(a, edgeId, startNode=True):
            geom_a, geom_b = QgsGeometry(), QgsGeometry()
            geom_a.fromWkb(nodeIdDict[a])
            idx = 0 if startNode else 1
            geom_b.fromWkb(hashDict[edgeId][idx])
            return geom_a.equals(geom_b)

        nEdges = len(DiG.edges)
        if nEdges == 0:
            return
        stepSize = 100 / nEdges
        networkLayer.startEditing()
        networkLayer.beginEditCommand("Fixing drainage flow")
        for current, (p0, pn) in enumerate(DiG.edges):
            if feedback.isCanceled():
                break
            featid = DiG[p0][pn]["featid"]
            if nodeCompairFunc(p0, featid):
                continue
            feat = self.flipLine(edgeDict, featid)
            networkLayer.changeGeometry(featid, feat.geometry(), skipDefaultValue=True)
            feedback.setProgress(current * stepSize)
        networkLayer.endEditCommand()

    def flipLine(self, edgeDict, edgeId):
        edgeFeat = edgeDict[edgeId]
        edgeGeomAsQgsLine = edgeFeat.geometry().constGet()
        reversedGeom = QgsGeometry(edgeGeomAsQgsLine.reversed())
        newFeat = QgsFeature(edgeFeat)
        newFeat.setGeometry(reversedGeom)
        return newFeat

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return "fixdrainageflowalgorithm"

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr("Fix Drainage Flow Algoritm")

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
        return QCoreApplication.translate("FixDrainageFlowAlgorithm", string)

    def createInstance(self):
        return FixDrainageFlowAlgorithm()
