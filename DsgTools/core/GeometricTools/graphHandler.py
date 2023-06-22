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
import itertools
import operator
import concurrent.futures
from functools import reduce
from collections import defaultdict, Counter
from itertools import tee
import os
from typing import Dict, Iterable, List, Optional, Tuple
from itertools import chain
from itertools import product
from itertools import starmap
from functools import partial

from qgis.core import QgsGeometry, QgsFeature, QgsProcessingMultiStepFeedback, QgsVectorLayer, QgsFeedback


def fetch_connected_nodes(G, node: int, max_degree: int, feedback: Optional[QgsFeedback] = None) -> List[int]:
    """
    Fetch nodes connected to a given node within a maximum degree limit using a non-recursive approach.

    Args:
        G: The input graph.
        node: The starting node from which to fetch connected nodes.
        max_degree: The maximum degree allowed for connected nodes.
        feedback: An optional QgsFeedback object to provide feedback during processing.

    Returns:
        A list of nodes connected to the starting node within the maximum degree limit.

    Note:
        The function uses a non-recursive approach with a stack to traverse the graph and fetch nodes connected to the
        starting node. It only considers nodes with a degree less than or equal to the specified max_degree.

        If the feedback parameter is provided and the feedback object indicates cancellation,
        the function will stop the traversal and return the list of nodes found so far.

    """
    seen = [node]
    stack = [node]

    while stack:
        current_node = stack.pop()

        if feedback is not None and feedback.isCanceled():
            break

        for neighbor in G.neighbors(current_node):
            if G.degree(neighbor) <= max_degree and neighbor not in seen:
                seen.append(neighbor)
                stack.append(neighbor)

    return seen


def pairwise(iterable: Iterable) -> Iterable:
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def flipLine(edgeDict: dict, edgeId: int) -> QgsFeature:
    """
    Flip the direction of a line feature and return a new QgsFeature.

    Args:
        edgeDict: A dictionary mapping edge feature IDs to QgsFeature objects.
        edgeId: An integer representing the ID of the edge feature to flip.

    Returns:
        A new QgsFeature object representing the flipped line feature.

    Note:
        The function retrieves the edge feature with the given ID from the edgeDict.
        It then reverses the geometry of the line feature and creates a new QgsFeature
        object with the reversed geometry. The new QgsFeature object is returned.

        The function assumes that the edge feature with the provided ID exists in the edgeDict.

    """
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


def buildAuxStructures(
    nx,
    nodesLayer: QgsVectorLayer,
    edgesLayer: QgsVectorLayer,
    feedback: Optional[QgsFeedback]=None,
    directed: Optional[bool]=False,
    useWkt: Optional[bool]=False,
    computeNodeLayerIdDict: Optional[bool]=False,
) -> Tuple:
    """
    Build auxiliary data structures for network analysis.

    Args:
        nx: NetworkX library instance or module.
        nodesLayer: A QgsVectorLayer representing nodes in the network.
        edgesLayer: A QgsVectorLayer representing edges in the network.
        feedback: An optional QgsFeedback object to provide feedback during processing.
        directed: An optional boolean flag indicating whether the network is directed. 
                  Default is False (undirected network).
        useWkt: An optional boolean flag indicating whether to use Well-Known Text (WKT) 
                representation for node geometries. Default is False (use WKB representation).

    Returns:
        A tuple containing the following auxiliary data structures:
        - nodeDict: A dictionary mapping node geometry to an auxiliary ID.
        - nodeIdDict: A dictionary mapping auxiliary ID to node geometry.
        - edgeDict: A dictionary mapping edge feature ID to edge feature.
        - hashDict: A dictionary mapping node feature ID and vertex position to node geometry.
        - networkBidirectionalGraph: A NetworkX graph representing the network.

    Note:
        The function builds the auxiliary data structures by iterating over the nodesLayer and edgesLayer.
        It assigns unique IDs to nodes, maps node geometries to IDs, and stores edge features and node geometries
        in corresponding dictionaries. It also constructs a bidirectional graph representation of the network
        using the provided NetworkX library or module.

        The feedback argument can be used to monitor the progress of the function if a QgsFeedback object is provided.

        By default, the function uses the Well-Known Binary (WKB) representation for node geometries.
        If the useWkt parameter is set to True, the function will use Well-Known Text (WKT) representation instead.

    """
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
    nodeLayerIdDict = dict()
    for current, nodeFeat in enumerate(nodesLayer.getFeatures()):
        if multiStepFeedback is not None and multiStepFeedback.isCanceled():
            break
        geom = nodeFeat.geometry()
        geomKey = geom.asWkb() if not useWkt else geom.asWkt()
        if geomKey not in nodeDict:
            nodeDict[geomKey] = auxId
            nodeIdDict[auxId] = geomKey
            auxId += 1
        nodeLayerIdDict[nodeFeat.id()] = auxId
        hashDict[nodeFeat["featid"]][nodeFeat["vertex_pos"]] = geomKey
        if multiStepFeedback is not None:
            multiStepFeedback.setProgress(current * stepSize)

    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(2)
    networkBidirectionalGraph = buildGraph(
        nx, hashDict, nodeDict, feedback=multiStepFeedback, directed=directed
    )
    return (nodeDict, nodeIdDict, edgeDict, hashDict, networkBidirectionalGraph) \
        if not computeNodeLayerIdDict else (nodeDict, nodeIdDict, edgeDict, hashDict, networkBidirectionalGraph, nodeLayerIdDict)


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
    return G_copy

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
    """
    Remove second-order empty nodes from the graph.

    Args:
        G: The input graph to modify.
        d: A dictionary mapping nodes to values. Used to check if a node is empty (value is None).

    Returns:
        A modified copy of the input graph with second-order empty nodes removed.

    Note:
        Second-order empty nodes are nodes in the graph that have a degree of 2 and their corresponding value in
        the dictionary 'd' is None. The function iteratively removes these nodes and connects their predecessors
        and successors to maintain the graph connectivity. It returns a modified copy of the input graph without
        the second-order empty nodes.

    """
    G_copy = G.copy()
    nodesToRemove = set(
        node for node in G_copy.nodes if G_copy.degree(node) == 2 and d[node] is None
    )
    while nodesToRemove:
        for node in nodesToRemove:
            predList = list(G_copy.predecessors(node))
            pred = predList[0] if len(predList) > 0 else None
            sucList = list(G_copy.successors(node))
            suc = sucList[0] if len(sucList) > 0 else None
            if pred is not None and suc is not None:
                G_copy.add_edge(pred, suc)
            G_copy.remove_node(node)
        nodesToRemove = set(
            node for node in G_copy.nodes if G_copy.degree(node) == 2 and d[node] is None
        )
    return G_copy

def add_edges_from_connected_nodes(G, DiG, node, reverse=False):
    """
    Add edges from connected nodes to a directed graph.

    Args:
        G (networkx.Graph): The input undirected graph.
        DiG (networkx.DiGraph): The directed graph to which edges will be added.
        node: The target node.
        reverse (bool, optional): Determines the direction of the added edges. Defaults to False.

    Returns:
        tuple: A tuple containing two sets: connectedNodes and nextNodesToVisit.
               - connectedNodes: The nodes connected to the target node.
               - nextNodesToVisit: The nodes that should be visited in the next iteration.

    """
    connectedNodes = fetch_connected_nodes(G, node, max_degree=2)
    for (n1, n2) in pairwise(connectedNodes):
        if (n1, n2) not in G.edges and (n2, n1) not in G.edges:
            continue
        pair = (n1, n2) if not reverse else (n2, n1)
        add_edge_from_graph_to_digraph(G, DiG, *pair)
    lastNodeCandidateList = list(set(G.neighbors(connectedNodes[-1])) - set(connectedNodes))
    if lastNodeCandidateList == []:
        return connectedNodes, set(G.neighbors(n2)) - set(connectedNodes) 
    last_pair = (connectedNodes[-1], list(set(G.neighbors(connectedNodes[-1])) - set(connectedNodes))[0]) if not reverse else (list(set(G.neighbors(connectedNodes[-1])) - set(connectedNodes))[0], connectedNodes[-1])
    add_edge_from_graph_to_digraph(G, DiG, *last_pair)
    nextNodesToVisit = set(G.neighbors(last_pair[-1])) - set(connectedNodes)
    return connectedNodes, nextNodesToVisit

def add_edge_from_graph_to_digraph(G, DiG, n1, n2):
    """
    Add an edge from the undirected graph to the directed graph.

    Args:
        G (networkx.Graph): The input undirected graph.
        DiG (networkx.DiGraph): The directed graph.
        n1: The first node of the edge.
        n2: The second node of the edge.

    """
    DiG.add_edge(n1, n2)
    DiG[n1][n2]["featid"] = G[n1][n2].get("featid", None)

def add_node_to_digraph_according_to_flow(G, DiG, node):
    """
    Add a node to the directed graph based on the flow conditions.

    Args:
        G (networkx.Graph): The input undirected graph.
        DiG (networkx.DiGraph): The directed graph.
        node: The node to be added.

    Returns:
        tuple: A tuple containing two sets: nextNodes and addToVisitedNodes.
               - nextNodes: The nodes connected to the added node that should be visited in the next iteration.
               - addToVisitedNodes: The added node itself, if it becomes fully connected in the directed graph.

    """
    neighbors = set(G.neighbors(node))
    nextNodes = set()
    addToVisitedNodes = set()
    for n in neighbors:
        if n not in DiG.nodes or (node, n) in DiG.edges or (n, node) in DiG.edges:
            continue
        preds = set(DiG.predecessors(n))
        succs = set(DiG.successors(n))
        if (preds == set() and succs == set()):
            continue
        elif G.degree(node) == 2:
            if node in DiG.nodes:
                pair = (node, n) if len(DiG.in_edges(node)) > 0 else (n, node)
            else:
                pair = (n, node) if len(preds) == 0 else (n, node)
            add_edge_from_graph_to_digraph(G, DiG, *pair)
        elif (G.degree(node) == 3 and len(preds | succs) < 2):
            continue
        elif preds != set() and succs == set(): # confluencia
            add_edge_from_graph_to_digraph(G, DiG, n, node)
        else: # ramificacao
            add_edge_from_graph_to_digraph(G, DiG, node, n)
        nextNodes.add(n)
    if node in DiG.nodes and set(DiG.predecessors(node)) | set(DiG.successors(node)) == neighbors:
        addToVisitedNodes.add(node)
    return nextNodes, addToVisitedNodes

def is_flow_invalid(DiG, node):
    preds = len(list(DiG.predecessors(node)))
    succs = len(list(DiG.successors(node)))
    return (preds > 0 and succs == 0) or (preds == 0 and succs > 0)

def buildAuxFlowGraph(nx, G, fixedInNodeSet: set, fixedOutNodeSet: set, constantSinkPointSet: set, feedback: Optional[QgsFeedback]=None):
    """
    Build an auxiliary flow graph from an undirected graph.

    Args:
        nx: The networkx module.
        G (networkx.Graph): The input undirected graph.
        fixedInNodeSet (set): The set of nodes with fixed incoming edges.
        fixedOutNodeSet (set): The set of nodes with fixed outgoing edges.

    Returns:
        networkx.DiGraph: The resulting auxiliary flow graph (directed graph).

    """
    DiG = nx.DiGraph()
    visitedNodes = set()
    nEdges = len(list(G.edges))
    if nEdges == 0:
        return DiG
    multiStepFeedback = QgsProcessingMultiStepFeedback(3, feedback) if feedback is not None else None
    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(0)
    for node in fixedInNodeSet:
        if multiStepFeedback is not None and feedback.isCanceled():
            return DiG
        connectedNodes, nextNodesToVisitFromFixedIn = add_edges_from_connected_nodes(G, DiG, node)
        visitedNodes = visitedNodes.union(set(connectedNodes))
    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(1)
    for node in fixedOutNodeSet:
        if multiStepFeedback is not None and feedback.isCanceled():
            return DiG
        connectedNodes, nextNodesToVisitFromFixedOut = add_edges_from_connected_nodes(G, DiG, node, reverse=True)
        visitedNodes = visitedNodes.union(set(connectedNodes))
    for node in constantSinkPointSet:
        if multiStepFeedback is not None and feedback.isCanceled():
            return DiG
        other = [i for i in list(G.edges(node))[0] if i != node][0]
        add_edge_from_graph_to_digraph(G, DiG, other, node)
        fixedOutNodeSet.add(node)

    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(2)
        remainingEdges = nEdges - len(list(DiG.edges))
        stepSize = 100/remainingEdges
        currentEdge = 0
    for baseNode in fixedOutNodeSet:
        if multiStepFeedback is not None and feedback.isCanceled():
            break
        firstOrderNodes = (i for i in nx.dfs_postorder_nodes(G, baseNode) if G.degree(i) == 1)
        path_list = (nx.all_simple_paths(G, i, baseNode) for i in firstOrderNodes if nx.has_path(G, i, baseNode))
        for node_path in itertools.chain(*path_list):
            if multiStepFeedback is not None and feedback.isCanceled():
                break
            for n0, n1 in pairwise(node_path):
                if (n0, n1) in DiG.edges or (n1, n0) in DiG.edges:
                    continue
                add_edge_from_graph_to_digraph(G, DiG, n0, n1)
                if multiStepFeedback is not None:
                    currentEdge += 1
                    multiStepFeedback.setProgress(currentEdge * stepSize)
    return DiG
