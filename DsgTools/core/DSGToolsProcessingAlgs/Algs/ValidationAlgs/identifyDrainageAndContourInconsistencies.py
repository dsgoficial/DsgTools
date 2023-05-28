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

from itertools import product
import os
import concurrent.futures

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
)
from DsgTools.core.GeometricTools import graphHandler


class IdentifyDrainageAndContourInconsistencies(ValidationAlgorithm):

    INPUT_DRAINAGES = "INPUT_DRAINAGES"
    INPUT_CONTOURS = "INPUT_CONTOURS"
    CONTOUR_ATTR = "CONTOUR_ATTR"
    CONTOUR_INTERVAL = "CONTOUR_INTERVAL"
    FLAGS = "FLAGS"

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_DRAINAGES,
                self.tr("Input drainages"),
                [QgsProcessing.TypeVectorLine],
                optional=False,
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_CONTOURS,
                self.tr("Input contours"),
                [QgsProcessing.TypeVectorLine],
                optional=False,
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
            QgsProcessingParameterNumber(
                self.CONTOUR_INTERVAL,
                self.tr("Contour interval"),
                type=QgsProcessingParameterNumber.Double,
                minValue=0,
                defaultValue=10,
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
        multiStepFeedback = QgsProcessingMultiStepFeedback(12, feedback)
        contourAttr = self.parameterAsFields(parameters, self.CONTOUR_ATTR, context)[0]
        contourInterval = self.parameterAsDouble(
            parameters, self.CONTOUR_INTERVAL, context
        )
        currentStep = 0
        multiStepFeedback.setProgressText(
            self.tr("Building local caches and spatial indexes...")
        )
        multiStepFeedback.setCurrentStep(currentStep)
        inputDrainagesLyr = algRunner.runCreateFieldWithExpression(
            inputLyr=parameters[self.INPUT_DRAINAGES],
            expression="$id",
            fieldName="d_featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
        )
        drainageDict = {
            feat["d_featid"]: feat for feat in inputDrainagesLyr.getFeatures()
        }
        self.prepareFlagSink(
            parameters, inputDrainagesLyr, QgsWkbTypes.MultiPoint, context
        )
        if len(drainageDict) == 0:
            return {self.FLAGS: self.flag_id}
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        inputContoursLyr = algRunner.runCreateFieldWithExpression(
            inputLyr=parameters[self.INPUT_CONTOURS],
            expression="$id",
            fieldName="c_featid",
            fieldType=1,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            inputLyr=inputDrainagesLyr,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            inputLyr=inputContoursLyr,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setProgressText(self.tr("Running line intersections..."))
        multiStepFeedback.setCurrentStep(currentStep)
        multiPartIntersectionNodesLayer = algRunner.runLineIntersections(
            inputLyr=inputDrainagesLyr,
            intersectLyr=inputContoursLyr,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        intersectionNodesLayer = algRunner.runMultipartToSingleParts(
            inputLayer=multiPartIntersectionNodesLayer,
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Building Intersection search structure...")
        )
        intersectionDict = self.buildIntersectionSearchStructure(
            intersectionNodesLayer, drainageDict, feedback=multiStepFeedback
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        flagDict = self.findIntersectionErrors(
            intersectionDict, contourAttr, contourInterval, feedback=multiStepFeedback
        )
        flagLambda = lambda x: self.flagFeature(
            flagGeom=x[0], flagText=x[1], fromWkb=True
        )
        if len(flagDict) > 0:
            list(map(flagLambda, flagDict.items()))
            return {self.FLAGS: self.flag_id}

        multiStepFeedback.setCurrentStep(currentStep)
        nodesLayer = algRunner.runExtractSpecificVertices(
            inputLyr=inputDrainagesLyr,
            vertices="0,-1",
            context=context,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        nodesDict, G = self.buildGraphSeachStructures(
            nx,
            nodesLayer=nodesLayer,
            intersectionDict=intersectionDict,
            contourAttr=contourAttr,
            feedback=multiStepFeedback,
        )
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Finding continuity errors...")
        )
        flagDict = self.findContinuityErrorsOnGraph(
            nx, nodesDict, G, contourInterval, feedback=multiStepFeedback
        )
        if len(flagDict) > 0:
            list(map(flagLambda, flagDict.items()))
            return {self.FLAGS: self.flag_id}
        currentStep += 1
        multiStepFeedback.setCurrentStep(currentStep)
        multiStepFeedback.setProgressText(
            self.tr("Finding errors on confluence and ramifications...")
        )
        flagDict = self.findMissingErrorsOnGraphConsideringRamificationsAndConfluences(
            nodesDict, G, feedback=multiStepFeedback
        )
        if len(flagDict) > 0:
            list(map(flagLambda, flagDict.items()))
        return {self.FLAGS: self.flag_id}

    def buildIntersectionSearchStructure(
        self, intersectionNodesLayer, drainageDict, feedback
    ):
        intersectionDict = defaultdict(list)
        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        nFeats = intersectionNodesLayer.featureCount()
        if nFeats == 0:
            return intersectionDict
        stepSize = 100 / nFeats
        for current, feat in enumerate(intersectionNodesLayer.getFeatures()):
            if multiStepFeedback.isCanceled():
                return intersectionDict
            intersectionDict[feat["d_featid"]].append(feat)
            multiStepFeedback.setProgress(current * stepSize)
        multiStepFeedback.setCurrentStep(1)
        nKeys = len(intersectionDict)
        stepSize = 100 / nKeys
        for current, (d_featid, featList) in enumerate(intersectionDict.items()):
            if multiStepFeedback.isCanceled():
                return intersectionDict
            drainageGeom = drainageDict[d_featid].geometry()
            sortedList = sorted(
                featList, key=lambda feat: drainageGeom.lineLocatePoint(feat.geometry())
            )
            intersectionDict[d_featid] = sortedList
            multiStepFeedback.setProgress(current * stepSize)
        return intersectionDict

    def findIntersectionErrors(
        self, intersectionDict, contourAttr, contourInterval, feedback
    ):
        nItems = len(intersectionDict)
        flagDict = dict()
        if nItems == 0:
            return flagDict
        stepSize = 100 / nItems

        def findError(featList):
            if feedback.isCanceled():
                return None
            if len(featList) < 2:
                return None
            for f1, f2 in graphHandler.pairwise(featList):
                diff = f1[contourAttr] - f2[contourAttr]
                if diff == contourInterval:
                    continue
                if diff < 0:
                    flagText = self.tr(
                        f"Drainage line going uphill. This drainage already intercepted countour with height {f2[contourAttr]} after intercepting contour with height {f1[contourAttr]}."
                    )
                elif diff == 0:
                    flagText = self.tr(
                        f"Invalid intercection between drainage and contour lines. This drainage intercepted twice the countour with height {f2[contourAttr]}."
                    )
                else:
                    flagText = self.tr(
                        f"Drainage line intercepted countour with height {f2[contourAttr]} after intercepting contour with height {f1[contourAttr]}. Since the contour interval is {contourInterval}, there are missing contours in this region. Check the contours for missing features."
                    )
                g1 = f1.geometry()
                g2 = f2.geometry()
                flagGeom = g1.combine(g2)
                return {flagGeom.asWkb(): flagText}
            return None

        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(
            self.tr(
                "Building Intersection search structure: Submitting features to thread..."
            )
        )
        pool = concurrent.futures.ThreadPoolExecutor(os.cpu_count())
        futures = set()
        for current, featList in enumerate(intersectionDict.values()):
            if multiStepFeedback.isCanceled():
                pool.shutdown(wait=False)
                return flagDict
            futures.add(pool.submit(findError, featList))
            multiStepFeedback.setProgress(current * stepSize)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(
            self.tr("Building Intersection search structure: Evaluating results...")
        )
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                pool.shutdown(wait=False)
                return flagDict
            result = future.result()
            if result is None:
                continue
            flagDict.update(result)
            multiStepFeedback.setProgress(current * stepSize)
        return flagDict

    def buildGraphSeachStructures(
        self, nx, nodesLayer, intersectionDict, contourAttr, feedback
    ):
        multiStepFeedback = QgsProcessingMultiStepFeedback(5, feedback)
        multiStepFeedback.setCurrentStep(0)
        nNodes = nodesLayer.featureCount()
        stepSize = 100 / nNodes
        nodesDict = dict()
        nodesWkbToIdDict = dict()
        drainageNodeDict = defaultdict(dict)
        for current, feat in enumerate(nodesLayer.getFeatures()):
            if multiStepFeedback.isCanceled():
                break
            nodesDict[feat.id()] = feat
            nodesWkbToIdDict[feat.geometry().asWkb()] = feat.id()
            drainageNodeDict[feat["d_featid"]][
                feat["vertex_pos"]
            ] = feat.geometry().asWkb()
            multiStepFeedback.setProgress(current * stepSize)
        newNodeId = max(nodesDict.keys()) + 1
        stepSize = 100 / len(drainageNodeDict)

        G = nx.DiGraph(h=None)
        addEdgeLambda = lambda x: G.add_edge(x[0], x[1])
        for current, (drainageId, startEndDict) in enumerate(drainageNodeDict.items()):
            if multiStepFeedback.isCanceled():
                break
            newNodesDict = dict()
            newNodesWkbToIdDict = dict()
            intersectionList = intersectionDict.get(drainageId, [])
            intersectionIdList = []
            if intersectionList == []:
                G.add_edge(
                    nodesWkbToIdDict[startEndDict[0]],
                    nodesWkbToIdDict[startEndDict[-1]],
                )
                continue
            for intersectionFeat in intersectionList:
                newNodesWkbToIdDict[intersectionFeat.geometry().asWkb()] = newNodeId
                newNodesDict[newNodeId] = intersectionFeat
                intersectionIdList.append(newNodeId)
                G.add_node(newNodeId, h=intersectionFeat[contourAttr])
                newNodeId += 1

            nodesDict.update(newNodesDict)
            nodesWkbToIdDict.update(newNodesWkbToIdDict)
            list(
                map(
                    addEdgeLambda,
                    graphHandler.pairwise(
                        [
                            nodesWkbToIdDict[startEndDict[0]],
                            *intersectionIdList,
                            nodesWkbToIdDict[startEndDict[-1]],
                        ]
                    ),
                )
            )
            multiStepFeedback.setProgress(current * stepSize)
        return nodesDict, G

    def findContinuityErrorsOnGraph(self, nx, nodesDict, G, contourInterval, feedback):
        flagDict = dict()
        d = dict(G.nodes(data="h", default=None))
        startingNodes, endingNodes = set(), set()
        for node in G.nodes:
            if G.degree(node) != 1:
                continue
            if len(list(G.successors(node))) > 0:
                startingNodes.add(node)
            else:
                endingNodes.add(node)


        def evaluate(startingNode, endingNode):
            flagDict = dict()
            for path in nx.all_simple_paths(G, startingNode, endingNode):
                connectedNodesWithHeight = [
                    (node, d[node]) for node in path if d[node] is not None
                ]
                if len(connectedNodesWithHeight) < 1:
                    continue
                for (node1, h1), (node2, h2) in graphHandler.pairwise(
                    connectedNodesWithHeight
                ):
                    diff = h1 - h2
                    if diff == contourInterval:
                        continue
                    if diff < 0:
                        flagText = self.tr(
                            f"Drainage newtwork going uphill. This network branch has already intercepted countour with height {h2} after intercepting contour with height {h1}."
                        )
                    elif diff == 0:
                        flagText = self.tr(
                            f"Invalid intercection between drainage and contour lines. This network branch has already intercepted twice the countour with height {h2}."
                        )
                    else:
                        flagText = self.tr(
                            f"Drainage network intercepted countour with height {h2} after intercepting contour with height {h1}. Since the contour interval is {contourInterval}, there are missing contours in this region. Check the contours for missing features."
                        )
                    g1 = nodesDict[node1].geometry()
                    g2 = nodesDict[node2].geometry()
                    flagGeom = g1.combine(g2)
                    flagDict[flagGeom.asWkb()] = flagText
            return flagDict

        multiStepFeedback = QgsProcessingMultiStepFeedback(2, feedback)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(
            self.tr(
                "Finding continuity errors on graph: Submitting features to thread..."
            )
        )
        pool = concurrent.futures.ThreadPoolExecutor(os.cpu_count())
        futures = set()
        pairList = list(product(startingNodes, endingNodes))
        stepSize = 100 / len(pairList)
        for current, (startNode, endNode) in enumerate(pairList):
            if multiStepFeedback.isCanceled():
                pool.shutdown(wait=False)
                return flagDict
            futures.add(pool.submit(evaluate, startNode, endNode))
            multiStepFeedback.setProgress(current * stepSize)
        multiStepFeedback.setCurrentStep(0)
        multiStepFeedback.setProgressText(
            self.tr("Finding continuity errors on graph: Evaluating results...")
        )
        for current, future in enumerate(concurrent.futures.as_completed(futures)):
            if multiStepFeedback.isCanceled():
                pool.shutdown(wait=False)
                return flagDict
            result = future.result()
            if result is None:
                continue
            flagDict.update(result)
            multiStepFeedback.setProgress(current * stepSize)
        return flagDict

    def findMissingErrorsOnGraphConsideringRamificationsAndConfluences(
        self, nodesDict, G, feedback
    ):
        flagDict = dict()
        processedNodes = set()
        G = G.copy()
        d = dict(G.nodes(data="h", default=None))
        G = graphHandler.removeFirstOrderEmptyNodes(G, d)
        G = graphHandler.removeSecondOrderEmptyNodes(G, d)
        nodesToVisit = set(
            node for node in G.nodes if G.degree(node) == 1 and len(list(G.successors(node))) > 0
        )
        currentStep = 0
        while nodesToVisit:
            newNodesToVisit = set()
            for node in nodesToVisit:
                if feedback.isCanceled():
                    return flagDict
                if G.degree(node) == 1:
                    if d[node] is None:
                        h = next((d[i] for i in graphHandler.fetch_connected_nodes(G, node, max_degree=2) if d[i] is not None), None)
                        if h is None:
                            continue
                        d[node] = h
                    newNodesToVisit = newNodesToVisit.union(G.successors(node))
                    continue
                if G.degree(node) == 2:
                    if d[node] is None:
                        pred = list(G.predecessors(node))[0]
                        d[node] = d[pred] if d[pred] is not None else next(d[i] for i in graphHandler.fetch_connected_nodes(G, node, max_degree=2) if d[i] is not None)
                    newNodesToVisit = newNodesToVisit.union(G.successors(node))
                    continue
                succ = list(G.successors(node))
                pred = list(G.predecessors(node))
                n1, n2 = succ if len(pred) == 1 else pred
                h1, h2 = d[n1], d[n2]
                processedNodes.add(node)
                if h1 == h2:
                    d[node] = h1
                    newNodesToVisit = newNodesToVisit.union(G.successors(node))
                    continue
                if h1 is None or h2 is None:
                    continue
                flagText = self.tr(
                    f"Drainage encounter with different known height values: {h1} and {h2}."
                )
                flagGeom = nodesDict[node].geometry()
                flagDict[flagGeom.asWkb()] = flagText
            nodesToVisit = newNodesToVisit
        return flagDict

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
