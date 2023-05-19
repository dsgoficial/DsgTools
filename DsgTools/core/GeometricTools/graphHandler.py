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

from collections import defaultdict
from itertools import tee
from typing import Iterable
from itertools import chain
from itertools import product
from itertools import starmap
from functools import partial

from qgis.core import QgsGeometry, QgsFeature, QgsProcessingMultiStepFeedback


def fetch_connected_nodes(G, node, max_degree, seen=None, feedback=None):
    if seen == None:
        seen = [node]
    for neighbor in G.neighbors(node):
        if feedback is not None and feedback.isCanceled():
            break
        if G.degree(neighbor) > max_degree:
            continue
        if neighbor not in seen:
            seen.append(neighbor)
            fetch_connected_nodes(G, neighbor, max_degree, seen)
    return seen


def pairwise(iterable: Iterable) -> Iterable:
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def flipLine(edgeDict: dict, edgeId: int) -> QgsFeature:
    edgeFeat = edgeDict[edgeId]
    edgeGeomAsQgsLine = edgeFeat.geometry().constGet()
    reversedGeom = QgsGeometry(edgeGeomAsQgsLine.reversed())
    newFeat = QgsFeature(edgeFeat)
    newFeat.setGeometry(reversedGeom)
    return newFeat


def buildGraph(nx, hashDict, nodeDict, feedback=None, directed=False):
    G = nx.Graph() if not directed else nx.DiGraph()
    progressStep = 100 / len(hashDict)
    for current, (edgeId, (wkb_1, wkb_2)) in enumerate(hashDict.items()):
        if feedback is not None and feedback.isCanceled():
            break
        G.add_edge(nodeDict[wkb_1], nodeDict[wkb_2])
        G[nodeDict[wkb_1]][nodeDict[wkb_2]]["featid"] = edgeId
        if feedback is not None:
            feedback.setProgress(current * progressStep)
    return G


def buildAuxStructures(nx, nodesLayer, edgesLayer, feedback=None, directed=False):
    multiStepFeedback = (
        QgsProcessingMultiStepFeedback(3, feedback) if feedback is not None else None
    )
    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(0)
    edgeDict = {feat["featid"]: feat for feat in edgesLayer.getFeatures()}
    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(1)
    nodeDict = defaultdict(list)
    nodeIdDict = defaultdict(list)
    nodeCount = nodesLayer.featureCount()
    stepSize = 100 / nodeCount
    auxId = 0
    hashDict = defaultdict(lambda: [[], []])
    for current, nodeFeat in enumerate(nodesLayer.getFeatures()):
        if multiStepFeedback is not None and multiStepFeedback.isCanceled():
            break
        geom = nodeFeat.geometry()
        geomWkb = geom.asWkb()
        if geomWkb not in nodeDict:
            nodeDict[geomWkb] = auxId
            nodeIdDict[auxId] = geomWkb
            auxId += 1
        hashDict[nodeFeat["featid"]][nodeFeat["vertex_pos"]] = geomWkb
        if multiStepFeedback is not None:
            multiStepFeedback.setProgress(current * stepSize)

    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(2)
    networkBidirectionalGraph = buildGraph(
        nx, hashDict, nodeDict, feedback=multiStepFeedback, directed=directed
    )
    return nodeDict, nodeIdDict, edgeDict, hashDict, networkBidirectionalGraph


def evaluateStreamOrder(G, feedback=None):
    G = G.copy()
    firstOrderNodes = set(
        node
        for node in G.nodes
        if G.degree(node) == 1 and len(list(G.successors(node))) > 0
    )
    stepSize = 100 / len(G.edges)
    current = 0
    G_copy = G.copy()
    visitedNodes = set()
    for n0, n1 in G_copy.edges:
        G_copy[n0][n1]["stream_order"] = 0
    while len(firstOrderNodes) > 0:
        if feedback is not None and feedback.isCanceled():
            return G_copy
        for node in firstOrderNodes:
            if node in visitedNodes:
                continue
            connectedNodes = fetch_connected_nodes(G, node, 2)
            pairs = [(a, b) for i in connectedNodes for a, b in G.out_edges(i)]
            predOrderValueList = [
                G_copy[n0][node]["stream_order"] for n0 in G_copy.predecessors(node)
            ]
            startIdx = max(predOrderValueList) + 1 if len(predOrderValueList) > 0 else 1
            for idx, (n0, n1) in enumerate(pairs, start=startIdx):
                current += 1
                if feedback is not None and feedback.isCanceled():
                    return G_copy
                G_copy[n0][n1]["stream_order"] = (
                    idx
                    if G_copy.degree(n0) <= 2
                    else max(
                        [idx]
                        + [
                            G_copy[i][n0]["stream_order"] + 1
                            for i in G_copy.predecessors(n0)
                        ]
                    )
                )
                G.remove_edge(n0, n1)
                succList = list(G_copy.successors(n1))
                if len(succList) > 1:
                    for i in G_copy.successors(n1):
                        G_copy[n1][i]["stream_order"] = idx + 1
                    G.remove_edge(n1, succList[0])
                if feedback is not None:
                    feedback.setProgress(current * stepSize)
            for n in connectedNodes:
                visitedNodes.add(n)
            # visitedNodes.add(node)
        firstOrderNodes = (
            set(
                node
                for node in G.nodes
                if G.degree(node) == 1 and len(list(G.successors(node))) > 0
            )
            - visitedNodes
        )
        # firstOrderNodes = [node for node in G.nodes if G.degree(node) == 1 and node not in visitedNodes]
    return G_copy


# def evaluateStreamOrder(nx, G, feedback=None):
#     G = G.copy()
#     firstOrderNodes = set(node for node in G.nodes if G.degree(node) == 1 and len(list(G.successors(node))) > 0)
#     stepSize = 100 / len(G.edges)
#     current = 0
#     G_copy = G.copy()
#     visitedNodes = set()
#     for n0, n1 in G_copy.edges:
#         G_copy[n0][n1]["stream_order"] = 0
#     roots = (v for v, d in G.in_degree() if d == 0)
#     leaves = (v for v, d in G.out_degree() if d == 0)
#     all_paths = partial(nx.all_simple_paths, G)
#     pathDict = defaultdict(list)
#     for path in sorted(chain.from_iterable(starmap(all_paths, product(roots, leaves))), key=lambda x: len(x), reverse=True):
#         pathDict[path[0]].append(path)


def removeFirstOrderEmptyNodes(G, d):
    """
    Test case:
    G = nx.DiGraph()
    G.add_edges_from(
        [
            (1,2), (3,2), (4,5), (6,5), (7,6),
            (5, 8), (2, 8), (8,9),
            (10,1), (11,10),
            (9, 12), (9, 13),
            (16, 12), (14, 13),
            (12, 15), (13, 15),
            (15, 17)
        ]
    )
    """
    G_copy = G.copy()
    nodesToRemove = set(
        node
        for node in G_copy.nodes
        if G_copy.degree(node) == 1
        and d[node] is None
        and len(list(G_copy.successors(node))) > 0
    )
    while nodesToRemove:
        for node in nodesToRemove:
            G_copy.remove_node(node)
        nodesToRemove = set(
            node
            for node in G_copy.nodes
            if G_copy.degree(node) == 1
            and d[node] is None
            and len(list(G_copy.successors(node))) > 0
        )
    return G_copy


def removeSecondOrderEmptyNodes(G, d):
    G_copy = G.copy()
    nodesToRemove = set(
        node for node in G_copy.nodes if G_copy.degree(node) == 2 and d[node] is None
    )
    while nodesToRemove:
        for node in nodesToRemove:
            pred = list(G_copy.predecessors(node))[0]
            suc = list(G_copy.successors(node))[0]
            G_copy.add_edge(pred, suc)
            G_copy.remove_node(node)
        nodesToRemove = set(
            node for node in G_copy.nodes if G_copy.degree(node) == 2 and d[node] is None
        )
    return G_copy
