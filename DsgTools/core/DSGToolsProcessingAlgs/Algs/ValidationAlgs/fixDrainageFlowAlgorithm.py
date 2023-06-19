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
from itertools import tee
from PyQt5.QtCore import QCoreApplication
from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler

import processing
from DsgTools.core.GeometricTools.layerHandler import LayerHandler
from DsgTools.core.GeometricTools import graphHandler
from qgis.core import (
    QgsDataSourceUri,
    QgsFeature,
    QgsFeatureSink,
    QgsGeometry,
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingException,
    QgsProcessingMultiStepFeedback,
    QgsProcessingOutputVectorLayer,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterDistance,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFeatureSink,
    QgsProcessingParameterFeatureSource,
    QgsProcessingParameterField,
    QgsProcessingParameterMultipleLayers,
    QgsProcessingParameterNumber,
    QgsProcessingParameterVectorLayer,
    QgsProcessingUtils,
    QgsProject,
    QgsSpatialIndex,
    QgsWkbTypes,
)

from ....dsgEnums import DsgEnums
from ...algRunner import AlgRunner
from .validationAlgorithm import ValidationAlgorithm


class FixDrainageFlowAlgorithm(ValidationAlgorithm):
    NETWORK_LAYER = "NETWORK_LAYER"
    # SINK_LAYER = "SINK_LAYER"
    GEOGRAPHIC_BOUNDS_LAYER = "GEOGRAPHIC_BOUNDS_LAYER"
    # WATER_BODY_LAYERS = "WATER_BODY_LAYERS"
    # OCEAN_LAYER = "OCEAN_LAYER"
    # SEARCH_RADIUS = "SEARCH_RADIUS"
    # POINT_FLAGS = "FLAGS"
    # LINE_FLAGS = "LINE_FLAGS"

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
            QgsProcessingParameterVectorLayer(
                self.GEOGRAPHIC_BOUNDS_LAYER,
                self.tr("Reference layer"),
                [QgsProcessing.TypeVectorPolygon],
                optional=True,
            )
        )
        # self.addParameter(
        #     QgsProcessingParameterVectorLayer(
        #         self.OCEAN_LAYER,
        #         self.tr("Ocean layer"),
        #         [QgsProcessing.TypeVectorPolygon],
        #         optional=True,
        #     )
        # )
        # self.addParameter(
        #     QgsProcessingParameterVectorLayer(
        #         self.SINK_LAYER,
        #         self.tr("Water sink layer"),
        #         [QgsProcessing.TypeVectorPoint],
        #         optional=True,
        #     )
        # )
        # self.addParameter(
        #     QgsProcessingParameterMultipleLayers(
        #         self.WATER_BODY_LAYERS,
        #         self.tr("Water body layers"),
        #         QgsProcessing.TypeVectorPolygon,
        #         optional=True,
        #     )
        # )
        # self.addParameter(
        #     QgsProcessingParameterNumber(
        #         self.SEARCH_RADIUS,
        #         self.tr("Search radius"),
        #         minValue=0,
        #         defaultValue=1,
        #         type=QgsProcessingParameterNumber.Double,
        #     )
        # )
        # self.addParameter(
        #     QgsProcessingParameterFeatureSink(
        #         self.POINT_FLAGS,
        #         self.tr("{0} network node errors").format(self.displayName()),
        #     )
        # )
        # self.addParameter(
        #     QgsProcessingParameterFeatureSink(
        #         self.LINE_FLAGS, self.tr("{0} line errors").format(self.displayName())
        #     )
        # )

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
        layerHandler = LayerHandler()
        geometryHandler = GeometryHandler()
        algRunner = AlgRunner()
        networkLayer = self.parameterAsLayer(parameters, self.NETWORK_LAYER, context)
        # waterBodyClasses = self.parameterAsLayer(
        #     parameters, self.WATER_BODY_LAYERS, context
        # )
        # waterSinkLayer = self.parameterAsLayer(parameters, self.SINK_LAYER, context)
        geographicBoundsLayer = self.parameterAsLayer(
            parameters, self.GEOGRAPHIC_BOUNDS_LAYER, context
        )
        # searchRadius = self.parameterAsDouble(parameters, self.SEARCH_RADIUS, context)
        multiStepFeedback = QgsProcessingMultiStepFeedback(
            8 if geographicBoundsLayer is not None else 6, feedback
        )
        currentStep = 0
        multiStepFeedback.setCurrentStep(currentStep)
        localCache = algRunner.runCreateFieldWithExpression(
            inputLyr=networkLayer,
            expression="$id",
            fieldName="featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        if geographicBoundsLayer is not None:
            multiStepFeedback.setCurrentStep(currentStep)
            algRunner.runCreateSpatialIndex(
                inputLyr=localCache, context=context, feedback=multiStepFeedback
            )
            currentStep += 1
            multiStepFeedback.setCurrentStep(currentStep)
            localCache = algRunner.runExtractByLocation(
                inputLyr=localCache,
                intersectLyr=geographicBoundsLayer,
                context=context,
                feedback=multiStepFeedback,
            )
            currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            inputLyr=localCache, context=context, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        nodesLayer = algRunner.runExtractSpecificVertices(
            inputLyr=localCache,
            vertices="0,-1",
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
        ) = graphHandler.buildAuxStructures(
            nx, nodesLayer=nodesLayer, edgesLayer=localCache, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        (fixedInNodeSet, fixedOutNodeSet) = self.getInAndOutNodes(
            nodeDict=nodeDict,
            nodeIdDict=nodeIdDict,
            edgesLayer=localCache,
            geographicBoundsLayer=geographicBoundsLayer
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        featuresToUpdateDict = self.fixDrainageFlow(
            nodeDict,
            nodeIdDict,
            edgeDict,
            hashDict,
            networkBidirectionalGraph,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        self.updateFeatures(
            networkLayer, featuresToUpdateDict, feedback=multiStepFeedback
        )

        return {
            self.NETWORK_LAYER: networkLayer,
            # self.POINT_FLAGS: self.flag_id,
            # self.LINE_FLAGS: flag_line_sink_id,
        }
    
    def getInAndOutNodes(self, nodeDict):
        pass

    def updateFeatures(self, networkLayer, featuresToUpdateDict, feedback):
        nFeatsToUpdate = len(featuresToUpdateDict)
        if nFeatsToUpdate == 0:
            return
        stepSize = 100 / nFeatsToUpdate
        networkLayer.startEditing()
        networkLayer.beginEditCommand("Fixing drainage flow")
        for current, (_, feat) in enumerate(featuresToUpdateDict.items()):
            if feedback.isCanceled():
                break
            networkLayer.changeGeometry(feat["featid"], feat.geometry())
            feedback.setProgress(current * stepSize)
        networkLayer.endEditCommand()

    def fixDrainageFlow(self, nodeDict, nodeIdDict, edgeDict, hashDict, G, feedback):
        firstOrderNodes = [node for node in G.nodes if G.degree(node) == 1]
        featuresToUpdateDict = dict()
        stepSize = 100 / len(nodeDict)

        def nodeCompairFunc(a, edgeId, startNode=True):
            geom_a, geom_b = QgsGeometry(), QgsGeometry()
            geom_a.fromWkb(nodeIdDict[a])
            idx = 0 if startNode else 1
            geom_b.fromWkb(hashDict[edgeId][idx])
            return geom_a.equals(geom_b)

        current = 0
        while len(firstOrderNodes) > 0:
            if feedback.isCanceled():
                return featuresToUpdateDict
            for node in firstOrderNodes:
                connectedNodes = fetch_connected_nodes(G, node, 2)
                if len(connectedNodes) == 1:
                    current += 1
                    n0 = connectedNodes[0]
                    n1 = list(G.neighbors(n0))[0]
                    edgeId = G[n0][n1]["featid"]
                    if nodeCompairFunc(n0, edgeId, startNode=True):
                        continue
                    newFeat = self.flipLine(edgeDict, edgeId)
                    featuresToUpdateDict[edgeId] = newFeat
                    feedback.setProgress(current * stepSize)
                    continue
                for n0, n1 in pairwise(connectedNodes):
                    current += 1
                    if feedback.isCanceled():
                        return featuresToUpdateDict
                    edgeId = G[n0][n1]["featid"]
                    if nodeCompairFunc(n0, edgeId, startNode=True):
                        continue
                    newFeat = self.flipLine(edgeDict, edgeId)
                    featuresToUpdateDict[edgeId] = newFeat
                    feedback.setProgress(current * stepSize)
                for n in connectedNodes:
                    G.remove_node(n)
            firstOrderNodes = [node for node in G.nodes if G.degree(node) == 1]
        return featuresToUpdateDict

    def flipLine(self, edgeDict, edgeId):
        edgeFeat = edgeDict[edgeId]
        edgeGeomAsQgsLine = edgeFeat.geometry().constGet()
        reversedGeom = QgsGeometry(edgeGeomAsQgsLine.reversed())
        newFeat = QgsFeature(edgeFeat)
        newFeat.setGeometry(reversedGeom)
        return newFeat

    def getRelatedNode(self, node, lineFeat):
        p0, pn = self.firstAndLastNode(lineFeat)
        p0 = QgsGeometry.fromPointXY(p0)
        nodeGeom = QgsGeometry()
        nodeGeom.fromWkb(node)
        return nodeGeom.equals(p0)

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

    def tr(self, string):
        return QCoreApplication.translate("FixDrainageFlowAlgorithm", string)

    def createInstance(self):
        return FixDrainageFlowAlgorithm()


def fetch_connected_nodes(G, node, max_degree, seen=None):
    if seen == None:
        seen = [node]
    for neighbor in G.neighbors(node):
        if G.degree(neighbor) > max_degree:
            continue
        if neighbor not in seen:
            seen.append(neighbor)
            fetch_connected_nodes(G, neighbor, max_degree, seen)
    return seen


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
