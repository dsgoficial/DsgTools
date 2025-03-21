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
from enum import Enum
from itertools import tee
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple
from qgis.PyQt.QtCore import QByteArray
from itertools import chain
from itertools import product
from itertools import combinations

from qgis.core import (
    QgsGeometry,
    QgsFeature,
    QgsProcessingMultiStepFeedback,
    QgsVectorLayer,
    QgsFeedback,
    QgsProcessingContext,
    QgsWkbTypes,
    QgsPointXY,
)

from DsgTools.core.DSGToolsProcessingAlgs.algRunner import AlgRunner


class GraphType(Enum):
    GRAPH = 0
    DIGRAPH = 1
    MULTIGRAPH = 2
    MULTIDIGRAPH = 3


def fetch_connected_nodes(
    G, node: int, max_degree: int, feedback: Optional[QgsFeedback] = None
) -> List[int]:
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


def buildGraph(
    nx: Any,
    hashDict: Dict[int, List[QByteArray]],
    nodeDict: Dict[QByteArray, int],
    feedback: Optional[QgsFeedback] = None,
    graphType: GraphType = 0,
    add_inside_river_attribute: bool = True,
) -> Any:
    """
    Build a graph from hash dictionary and node dictionary.

    Args:
        nx: NetworkX library instance or module.
        hashDict: A dictionary mapping edge ID to a list with the wkbs of the first and the last nodes of the edge.
        nodeDict: A dictionary mapping node geometry to an auxiliary ID.
        feedback: An optional object for providing feedback during processing.
        directed: A boolean flag indicating whether the graph is directed.
                  Default is False (undirected graph).

    Returns:
        The constructed graph object.

    Notes:
        This function iterates over the hash dictionary and adds edges to the graph based on node geometry mappings.
        The graph can be either undirected or directed based on the value of the 'directed' parameter.
        The optional 'feedback' object can be used to monitor the progress of the function.

    """
    graphType = GraphType.GRAPH if graphType == 0 else graphType
    graphDict = {
        GraphType.GRAPH: nx.Graph,
        GraphType.DIGRAPH: nx.DiGraph,
        GraphType.MULTIGRAPH: nx.MultiGraph,
        GraphType.MULTIDIGRAPH: nx.MultiDiGraph,
    }
    graphObject = graphDict.get(graphType, None)
    if graphObject is None:
        raise NotImplementedError("Invalid graph type")
    G = graphObject()
    progressStep = 100 / len(hashDict)
    for current, (edgeId, (wkb_1, wkb_2)) in enumerate(hashDict.items()):
        if feedback is not None and feedback.isCanceled():
            break
        if wkb_1 == [] or wkb_2 == []:
            continue
        if add_inside_river_attribute:
            G.add_edge(
                nodeDict[wkb_1], nodeDict[wkb_2], featid=edgeId, inside_river=False
            )
        else:
            G.add_edge(nodeDict[wkb_1], nodeDict[wkb_2], featid=edgeId)
        if feedback is not None:
            feedback.setProgress(current * progressStep)
    return G


def buildAuxStructures(
    nx: Any,
    nodesLayer: QgsVectorLayer,
    edgesLayer: QgsVectorLayer,
    feedback: Optional[QgsFeedback] = None,
    graphType: Optional[GraphType] = 0,
    useWkt: Optional[bool] = False,
    computeNodeLayerIdDict: Optional[bool] = False,
    addEdgeLength: Optional[bool] = False,
) -> Tuple[
    Dict[QByteArray, int],
    Dict[int, QByteArray],
    Dict[int, QgsFeature],
    Dict[int, Dict[int, QByteArray]],
    Any,
]:
    """
    Build auxiliary data structures for network analysis.

    Args:
        nx: A NetworkX library instance or module.
        nodesLayer: A QgsVectorLayer representing the nodes in the network.
        edgesLayer: A QgsVectorLayer representing the edges in the network.
        feedback: An optional QgsFeedback object to provide feedback during processing.
        graphType: An optional enum flag indicating whether the network is directed.
                  Default is GraphType.GRAPH = 0 (undirected network).
        useWkt: An optional boolean flag indicating whether to use Well-Known Text (WKT)
                representation for node geometries. Default is False (use WKB representation).
        computeNodeLayerIdDict: An optional boolean flag indicating whether to compute
                                a dictionary mapping node layer ID to auxiliary ID.
                                Default is False.
        addEdgeLength: An optional boolean flag that adds the segment length to the graph.
    Returns:
        A tuple containing the following auxiliary data structures:
        - nodeDict: A dictionary mapping node geometry to an auxiliary ID.
        - nodeIdDict: A dictionary mapping auxiliary ID to node geometry.
        - edgeDict: A dictionary mapping edge feature ID to edge feature.
        - hashDict: A dictionary mapping node feature ID and vertex position to node geometry.
        - networkBidirectionalGraph: A NetworkX graph representing the network.

    Notes:
        This function builds auxiliary data structures by iterating over the nodesLayer and edgesLayer.
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
    hashDict = defaultdict(lambda: [[], []])
    nodeLayerIdDict = dict()
    if nodeCount == 0:
        G = nx.Graph()
        return (
            (nodeDict, nodeIdDict, edgeDict, hashDict, G)
            if not computeNodeLayerIdDict
            else (
                nodeDict,
                nodeIdDict,
                edgeDict,
                hashDict,
                G,
                nodeLayerIdDict,
            )
        )
    stepSize = 100 / nodeCount
    auxId = 0
    for current, nodeFeat in enumerate(nodesLayer.getFeatures()):
        if multiStepFeedback is not None and multiStepFeedback.isCanceled():
            break
        geom = nodeFeat.geometry()
        geomKey = geom.asWkb() if not useWkt else geom.asWkt()
        if geomKey not in nodeDict:
            nodeDict[geomKey] = auxId
            nodeIdDict[auxId] = geomKey
            auxId += 1
        if computeNodeLayerIdDict:
            nodeLayerIdDict[nodeFeat["nfeatid"]] = geomKey
        hashDict[nodeFeat["featid"]][nodeFeat["vertex_pos"]] = geomKey
        if multiStepFeedback is not None:
            multiStepFeedback.setProgress(current * stepSize)

    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(2)
    G = buildGraph(
        nx, hashDict, nodeDict, feedback=multiStepFeedback, graphType=graphType
    )
    if addEdgeLength:
        for edge in G.edges:
            a, b, *c = edge
            if multiStepFeedback is not None and multiStepFeedback.isCanceled():
                break
            featid = G[a][b]["featid"] if c == [] else G[a][b][c[0]]["featid"]
            if featid not in edgeDict:
                continue
            geom = edgeDict[featid].geometry()
            if c == []:
                G[a][b]["length"] = geom.length()
            else:
                G[a][b][c[0]]["length"] = geom.length()

    return (
        (nodeDict, nodeIdDict, edgeDict, hashDict, G)
        if not computeNodeLayerIdDict
        else (
            nodeDict,
            nodeIdDict,
            edgeDict,
            hashDict,
            G,
            nodeLayerIdDict,
        )
    )


def buildDirectionalGraphFromIdList(
    nx: Any,
    G: Any,
    nodeDict: Dict[QByteArray, int],
    hashDict: Dict[int, Dict[int, List[int]]],
    idSet: Set[int],
    feedback: Optional[QgsFeedback] = None,
) -> Any:
    DiG = nx.DiGraph()
    nFeats = len(idSet)
    if nFeats == 0:
        return DiG
    if feedback is not None:
        stepSize = 100 / nFeats
    for current, featid in enumerate(idSet):
        if feedback is not None and feedback.isCanceled():
            return DiG
        n0 = nodeDict[hashDict[featid][0]]
        n1 = nodeDict[hashDict[featid][-1]]
        add_edge_from_graph_to_digraph(G, DiG, n0, n1)
        if feedback is not None:
            feedback.setProgress(current * stepSize)
    return DiG


def evaluateStreamOrder(G: Any, feedback: Optional[QgsFeedback] = None) -> Any:
    """
    Evaluate stream order for the given graph.

    Args:
        G: The input graph object.
        feedback: An optional object for providing feedback during processing.

    Returns:
        The graph object with stream order assigned to edges.

    Notes:
        This function evaluates the stream order for the edges in the graph.
        The stream order represents the hierarchical position of the edge in the stream network.
        The optional 'feedback' object can be used to monitor the progress of the function.
    """
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
            node
            for node in G_copy.nodes
            if G_copy.degree(node) == 2 and d[node] is None
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
        if (n1, n2) in DiG.edges or (n2, n1) in DiG.edges:
            continue
        pair = (n1, n2) if not reverse else (n2, n1)
        add_edge_from_graph_to_digraph(G, DiG, *pair)
    lastNodeCandidateList = list(
        set(G.neighbors(connectedNodes[-1])) - set(connectedNodes)
    )
    if lastNodeCandidateList == []:
        return connectedNodes, set(G.neighbors(n2)) - set(connectedNodes)
    last_pair = (
        (
            connectedNodes[-1],
            list(set(G.neighbors(connectedNodes[-1])) - set(connectedNodes))[0],
        )
        if not reverse
        else (
            list(set(G.neighbors(connectedNodes[-1])) - set(connectedNodes))[0],
            connectedNodes[-1],
        )
    )
    if last_pair not in DiG.edges and tuple(reversed(last_pair)) not in DiG.edges:
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
    DiG[n1][n2]["inside_river"] = G[n1][n2].get("inside_river", False)


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
        if preds == set() and succs == set():
            continue
        elif G.degree(node) == 2:
            if node in DiG.nodes:
                pair = (node, n) if len(DiG.in_edges(node)) > 0 else (n, node)
            else:
                pair = (n, node) if len(preds) == 0 else (n, node)
            add_edge_from_graph_to_digraph(G, DiG, *pair)
        elif G.degree(node) == 3 and len(preds | succs) < 2:
            continue
        elif preds != set() and succs == set():  # confluencia
            add_edge_from_graph_to_digraph(G, DiG, n, node)
        else:  # ramificacao
            add_edge_from_graph_to_digraph(G, DiG, node, n)
        nextNodes.add(n)
    if (
        node in DiG.nodes
        and set(DiG.predecessors(node)) | set(DiG.successors(node)) == neighbors
    ):
        addToVisitedNodes.add(node)
    return nextNodes, addToVisitedNodes


def is_flow_invalid(DiG, node: int) -> bool:
    """
    Check if the flow is invalid for a given node in a directed graph.

    Args:
        DiG: The directed graph object.
        node: The node for which to check the flow validity.

    Returns:
        A boolean indicating whether the flow is invalid for the specified node.

    Notes:
        This function checks the flow validity for a given node in a directed graph.
        It returns True if the node has predecessors but no successors, or if it has successors but no predecessors.
        Otherwise, it returns False indicating that the flow is valid for the node.
    """
    preds = len(list(DiG.predecessors(node)))
    succs = len(list(DiG.successors(node)))
    return (preds > 0 and succs == 0) or (preds == 0 and succs > 0)


def flip_edge(DiG, edge: Tuple):
    start, end = edge
    attrDict = DiG[start][end]
    DiG.remove_edge(*edge)
    DiG.add_edge(end, start, **attrDict)


def buildAuxFlowGraph(
    nx,
    G,
    fixedInNodeSet: Set[int],
    fixedOutNodeSet: Set[int],
    nodeIdDict: Dict[int, QByteArray],
    constantSinkPointSet: Optional[Set[int]] = None,
    DiG: Optional[Any] = None,
    feedback: Optional[QgsFeedback] = None,
):
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
    # fixedInNodeSetFromDiG = set()
    # for node in fixedInNodeSet:
    #     if node not in DiG.nodes:
    #         fixedInNodeSetFromDiG.add(node)
    #         continue
    #     nodesToAdd = set(i for i in nx.dfs_preorder_nodes(DiG, node) if DiG[i] is None)
    #     fixedInNodeSetFromDiG = fixedInNodeSetFromDiG.union(nodesToAdd)
    DiG = nx.DiGraph() if DiG is None else DiG
    visitedNodes = set()
    nEdges = len(list(G.edges))
    constantSinkPointSet = (
        set() if constantSinkPointSet is None else constantSinkPointSet
    )
    if nEdges == 0:
        return DiG
    multiStepFeedback = (
        QgsProcessingMultiStepFeedback(5, feedback) if feedback is not None else None
    )
    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(0)
    for node in fixedInNodeSet:
        if multiStepFeedback is not None and feedback.isCanceled():
            return DiG
        connectedNodes, nextNodesToVisitFromFixedIn = add_edges_from_connected_nodes(
            G, DiG, node
        )
        visitedNodes = visitedNodes.union(set(connectedNodes))
    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(1)
    for node in fixedOutNodeSet:
        if multiStepFeedback is not None and feedback.isCanceled():
            return DiG
        connectedNodes, nextNodesToVisitFromFixedOut = add_edges_from_connected_nodes(
            G, DiG, node, reverse=True
        )
        visitedNodes = visitedNodes.union(set(connectedNodes))
    for node in constantSinkPointSet:
        if multiStepFeedback is not None and feedback.isCanceled():
            return DiG
        connectedNodesToConstant = fetch_connected_nodes(G, node, max_degree=2)
        if node not in connectedNodesToConstant:
            connectedNodesToConstant.insert(0, node)
        for n0, n1 in pairwise(reversed(connectedNodesToConstant)):
            if (n0, n1) not in G.edges or (n1, n0) not in G.edges:
                continue
            add_edge_from_graph_to_digraph(G, DiG, n0, n1)
        fixedOutNodeSet.add(node)

    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(2)
        remainingEdges = nEdges - len(list(DiG.edges))
        stepSize = 100 / remainingEdges
        currentEdge = 0

    def distance(start, end):
        startGeom, endGeom = QgsGeometry(), QgsGeometry()
        startGeom.fromWkb(nodeIdDict[start])
        endGeom.fromWkb(nodeIdDict[end])
        return startGeom.distance(endGeom)

    pairList = sorted(
        (
            (start, end)
            for start, end in product(fixedInNodeSet, fixedOutNodeSet)
            if nx.has_path(G, start, end)
        ),
        key=lambda x: (
            any(
                DiG[a][b]["inside_river"]
                for (a, b) in chain(DiG.in_edges(x[0]), DiG.out_edges(x[0]))
            ),
            distance(x[0], x[1]),
        ),
        reverse=True,
    )
    for (start, end) in pairList:
        if multiStepFeedback is not None and feedback.isCanceled():
            break
        for n0, n1 in pairwise(nx.astar_path(G, start, end, weight="length")):
            if multiStepFeedback is not None and feedback.isCanceled():
                break
            if (n0, n1) in DiG.edges or (n1, n0) in DiG.edges:
                continue
            add_edge_from_graph_to_digraph(G, DiG, n0, n1)
            if DiG.degree(n0) == G.degree(n0) and is_flow_invalid(DiG, n0):
                flip_edge(DiG, (n0, n1))
            if multiStepFeedback is not None:
                currentEdge += 1
                multiStepFeedback.setProgress(currentEdge * stepSize)
    remainingEdges = nEdges - len(list(DiG.edges))
    if remainingEdges == 0:
        return DiG
    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(3)
        stepSize = 100 / remainingEdges
        currentEdge = 0
    for baseNode in fixedOutNodeSet:
        if multiStepFeedback is not None and feedback.isCanceled():
            break
        firstOrderNodes = (
            i for i in nx.dfs_postorder_nodes(G, baseNode) if G.degree(i) == 1
        )
        path_list = (
            nx.astar_path(G, i, baseNode, weight="length")
            for i in firstOrderNodes
            if nx.has_path(G, i, baseNode)
        )
        for node_path in path_list:
            if multiStepFeedback is not None and feedback.isCanceled():
                break
            for n0, n1 in pairwise(node_path):
                if multiStepFeedback is not None and feedback.isCanceled():
                    break
                if (n0, n1) in DiG.edges or (n1, n0) in DiG.edges:
                    continue
                add_edge_from_graph_to_digraph(G, DiG, n0, n1)
                if multiStepFeedback is not None:
                    currentEdge += 1
                    multiStepFeedback.setProgress(currentEdge * stepSize)
    remainingEdges = nEdges - len(list(DiG.edges))
    if remainingEdges == 0:
        return DiG
    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(4)
        remainingEdges = nEdges - len(list(DiG.edges))
        stepSize = 100 / remainingEdges
        currentEdge = 0
    for (a, b) in G.edges:
        if ((a, b) in DiG.edges and DiG[a][b]["featid"] == G[a][b]["featid"]) or (
            (b, a) in DiG.edges and DiG[b][a]["featid"] == G[b][a]["featid"]
        ):
            continue
        add_edge_from_graph_to_digraph(G, DiG, a, b)
        if (
            is_flow_invalid(DiG, a)
            and set(nx.dfs_postorder_nodes(DiG, a)).intersection(fixedOutNodeSet)
            == set()
        ) or (
            is_flow_invalid(DiG, b)
            and set(nx.dfs_postorder_nodes(DiG, b)).intersection(fixedOutNodeSet)
            == set()
        ):
            flip_edge(DiG, (a, b))
    return DiG


def find_mergeable_edges_on_graph(
    nx,
    G,
    nodeIdDict,
    allowClosedLines: bool = False,
    feedback: Optional[QgsFeedback] = None,
):
    """
    Find mergeable edges in a graph.

    This function analyzes a graph to identify mergeable edges. Mergeable edges are pairs of edges
    that share common nodes with degree 2. The function returns a dictionary where keys are sets of nodes that
    can be merged, and values are sets of mergeable edge pairs.

    Parameters:
    - nx (module): NetworkX library.
    - G (nx.Graph): The input graph to analyze.
    - nodeIdDict (Dict[int, QByteArray]): Dictionary mapping node IDs to QByteArray objects.
    - feedback (Optional[QgsFeedback]): A QgsFeedback object for providing user feedback during
      processing. If provided and canceled, the function will terminate early.

    Returns:
    - Dict[Set[Hashable], Set[Tuple[Hashable, Hashable]]]: A dictionary where keys are sets of nodes
      that can be merged, and values are sets of frozenset pairs representing mergeable edges.

    Example:
    ```python
    G = nx.Graph()
    G.add_edges_from([
        (1, 2), (3, 2),
        (2, 4), (4, 5), (2, 18), (18, 6),
        (7, 6), (7, 17), (17, 8),
        (8, 9), (8, 13),
        (9, 10),
        (11, 10),
        (12, 10),
        (13, 14),
        (15, 13), (15, 16),
    ])
    nodeIdDict = {1: b'\x00', 2: b'\x01', 3: b'\x02', 4: b'\x03', 5: b'\x04', 6: b'\x05', 7: b'\x06', 8: b'\x07', 9: b'\x08', 10: b'\x09', 11: b'\x0a', 12: b'\x0b', 13: b'\x0c', 14: b'\x0d', 15: b'\x0e', 16: b'\x0f', 17: b'\x10', 18: b'\x11'}
    mergeable_edges = find_mergeable_edges_on_graph(nx, G, nodeIdDict)
    ```

    In the example above, `mergeable_edges` may contain:
    ```python
    {
        frozenset({4, 5}): nx.MultiGraph{(4, 5), (2, 4)},
        frozenset({17, 18, 6, 7}): {(8, 17), (18, 2), (6, 7), (17, 7), (18, 6)},
        frozenset({16, 15}): {(13, 15), (16, 15)},
        frozenset({9}): {(8, 9), (9, 10)}
    }
    ```
    """
    outputGraphDict = defaultdict(lambda: nx.MultiGraph())
    degree2nodes = (i for i in G.nodes if G.degree(i) == 2)
    if feedback is not None and feedback.isCanceled():
        return outputGraphDict
    candidatesSetofFrozenSets = set(
        frozenset(fetch_connected_nodes(G, n, 2)) for n in degree2nodes
    )
    if feedback is not None and feedback.isCanceled():
        return outputGraphDict
    nSteps = len(candidatesSetofFrozenSets)
    if nSteps == 0:
        return outputGraphDict
    if feedback is not None:
        stepSize = 100 / nSteps
    for current, candidateSet in enumerate(candidatesSetofFrozenSets):
        if feedback is not None and feedback.isCanceled():
            break
        for node in candidateSet:
            for edge in G.edges(node):
                n0, n1 = edge
                if "featid" in G[n0][n1]:
                    featid = G[n0][n1]["featid"]
                    if (
                        n0 in outputGraphDict[candidateSet]
                        and n1 in outputGraphDict[candidateSet][n0]
                        and p in outputGraphDict[candidateSet][n0][n1]
                        and outputGraphDict[candidateSet][n0][n1]["featid"] == featid
                    ):
                        continue
                    outputGraphDict[candidateSet].add_edge(
                        n0,
                        n1,
                        featid=featid,
                        length=G[n0][n1][p]["length"]
                        if "length" in G[n0][n1][p]
                        else 1,
                    )
                    continue
                for p in G[n0][n1].keys():
                    if (
                        n0 in outputGraphDict[candidateSet]
                        and n1 in outputGraphDict[candidateSet][n0]
                        and p in outputGraphDict[candidateSet][n0][n1]
                        and outputGraphDict[candidateSet][n0][n1][p]["featid"]
                        == G[n0][n1][p]["featid"]
                    ):
                        continue
                    outputGraphDict[candidateSet].add_edge(
                        n0,
                        n1,
                        featid=G[n0][n1][p]["featid"],
                        length=G[n0][n1][p]["length"]
                        if "length" in G[n0][n1][p]
                        else 1,
                    )
        if feedback is not None:
            feedback.setProgress(current * stepSize)
    keysToPop = set()
    auxDict = defaultdict(lambda: nx.MultiGraph())

    def distance(start, end):
        startGeom, endGeom = QgsGeometry(), QgsGeometry()
        startGeom.fromWkb(nodeIdDict[start])
        endGeom.fromWkb(nodeIdDict[end])
        return startGeom.distance(endGeom)

    for keySet, graph in outputGraphDict.items():
        nodeWithMaxDegree = max(graph.nodes, key=lambda x: graph.degree(x))
        candidateNodes = list(
            filter(
                lambda x: x != nodeWithMaxDegree
                and graph.degree(x) > 1
                and nx.has_path(graph, x, nodeWithMaxDegree),
                graph.nodes,
            )
        )
        nCandidates = len(candidateNodes)
        if nCandidates == 0:
            continue
        elif nCandidates == 1:
            furthestNode = candidateNodes[0]
            if allowClosedLines:
                continue
        else:
            furthestNode = max(
                candidateNodes, key=lambda x: distance(nodeWithMaxDegree, x)
            )
        path_list = list(nx.all_simple_paths(graph, nodeWithMaxDegree, furthestNode))
        if len(path_list) == 1:
            continue
        keysToPop.add(keySet)
        for path in path_list:
            newKey = frozenset(path)
            dictToUpdate = (
                auxDict[newKey]
                if newKey not in outputGraphDict
                else outputGraphDict[newKey]
            )
            for n0, n1 in nx.utils.pairwise(path):
                for p in G[n0][n1].keys():
                    dictToUpdate.add_edge(
                        n0,
                        n1,
                        featid=G[n0][n1][p]["featid"],
                        length=G[n0][n1][p]["length"]
                        if "length" in G[n0][n1][p]
                        else 1,
                    )
    if len(keysToPop) == 0:
        return outputGraphDict
    for k in keysToPop:
        outputGraphDict.pop(k)
    outputGraphDict.update(auxDict)
    return outputGraphDict


def filter_mergeable_graphs_using_attibutes(
    nx,
    G,
    featDict: Dict[int, QgsFeature],
    nodeIdDict: Dict[int, QByteArray],
    attributeNameList: List[str],
    isMulti: bool,
    allowClosedLines: bool = False,
    constraintNodeIds: Set[int] = None,
) -> Tuple[Set[int], Set[int]]:
    """Filters mergeable graphs based on specified attributes, with constraint nodes as break points.

    Args:
        nx (module): NetworkX library.
        G (nx.MultiDiGraph): MultiDigraph to filter.
        featDict (Dict[int, QgsFeature]): Dictionary mapping feature IDs to QgsFeature objects.
        nodeIdDict (Dict[int, QByteArray]): Dictionary mapping node IDs to QByteArray objects.
        attributeNameList (List[str]): List of attribute names to consider for filtering.
        isMulti (bool): Flag indicating whether the graph is a multi-type graph.
        allowClosedLines (bool, optional): Flag to allow closed lines in output. Defaults to False.
        constraintNodeIds (Set[int], optional): Set of node IDs that should act as break points. Defaults to None.

    Returns:
        Tuple[Set[QgsFeature], Set[int]]: Tuple containing sets of features to update and IDs to delete.
    """

    constraintNodeIds = set() if constraintNodeIds is None else constraintNodeIds
    auxDict = defaultdict(lambda: nx.MultiGraph())
    featureSetToUpdate, deleteIdSet = set(), set()

    # Group edges by attribute values
    for n0, n1, p in G.edges:
        featid = G[n0][n1][p]["featid"]
        feat = featDict[featid]
        attrTuple = tuple(feat[i] for i in attributeNameList)
        auxDict[attrTuple].add_edge(n0, n1, featid=featid)

    # Process each attribute group
    for attrTuple, auxGraph in auxDict.items():
        # Get mergeable edge groups
        mergeable_groups = find_mergeable_edges_on_graph(
            nx, auxGraph, nodeIdDict, allowClosedLines=allowClosedLines
        )

        # Process each mergeable group
        for nodeSet, mergeableG in mergeable_groups.items():
            if not allowClosedLines and len(mergeableG.edges) < 2:
                continue

            # Check if there are constraint nodes in this group
            local_constraint_nodes = (
                nodeSet.intersection(constraintNodeIds) if constraintNodeIds else set()
            )

            if not local_constraint_nodes:
                # No constraint nodes, perform normal merging while preserving direction
                edge_feat_ids = []
                for n0, n1, p in mergeableG.edges:
                    edge_feat_ids.append(mergeableG[n0][n1][p]["featid"])

                if not edge_feat_ids:
                    continue

                # Use first edge as reference
                idToKeep = edge_feat_ids[0]
                idsToDelete = set(edge_feat_ids[1:])

                # Get the initial geometry
                outputFeat = featDict[idToKeep]
                merged_geom = outputFeat.geometry()

                for id in idsToDelete:
                    geom_to_merge = featDict[id].geometry()

                    # Get start and end points of both geometries using vertices()
                    merged_vertices = list(merged_geom.vertices())
                    merged_start = QgsPointXY(merged_vertices[0])
                    merged_end = QgsPointXY(merged_vertices[-1])

                    to_merge_vertices = list(geom_to_merge.vertices())
                    to_merge_start = QgsPointXY(to_merge_vertices[0])
                    to_merge_end = QgsPointXY(to_merge_vertices[-1])

                    # Calculate distances between endpoints
                    d_end_start = merged_end.distance(to_merge_start)
                    d_end_end = merged_end.distance(to_merge_end)
                    d_start_start = merged_start.distance(to_merge_start)
                    d_start_end = merged_start.distance(to_merge_end)

                    # Choose the best connection strategy to preserve direction
                    if d_end_start < d_end_end and d_end_start < d_start_start:
                        # Append directly - no reversal needed
                        merged_geom = merged_geom.combine(geom_to_merge).mergeLines()
                    elif d_start_end < d_end_end and d_start_end < d_start_start:
                        # Prepend directly - no reversal needed
                        merged_geom = geom_to_merge.combine(merged_geom).mergeLines()
                    else:
                        # We need to reverse the geometry being merged
                        line = geom_to_merge.constGet().clone()
                        reversed_line = line.reversed()
                        geom_to_merge = QgsGeometry(reversed_line)

                        # Recalculate vertices after reversal
                        to_merge_vertices = list(geom_to_merge.vertices())
                        to_merge_start = QgsPointXY(to_merge_vertices[0])

                        # Determine which end to connect to
                        if merged_end.distance(to_merge_start) < merged_start.distance(
                            to_merge_start
                        ):
                            # Append the reversed geometry
                            merged_geom = merged_geom.combine(
                                geom_to_merge
                            ).mergeLines()
                        else:
                            # Prepend the reversed geometry
                            merged_geom = geom_to_merge.combine(
                                merged_geom
                            ).mergeLines()

                    deleteIdSet.add(id)

                if isMulti:
                    merged_geom.convertToMultiType()

                outputFeat.setGeometry(merged_geom)
                featureSetToUpdate.add(outputFeat)
            else:
                # With constraint nodes, split paths at these nodes

                # Find endpoints (degree 1) and add constraint nodes
                endpoints = set(
                    n for n in mergeableG.nodes if mergeableG.degree(n) == 1
                )
                path_endpoints = endpoints.union(local_constraint_nodes)

                # If we have no endpoints (e.g., a closed ring), use constraint nodes
                if not path_endpoints:
                    path_endpoints = local_constraint_nodes

                # Skip if not enough endpoints
                if len(path_endpoints) < 2:
                    continue

                # Process each possible path between endpoints
                endpoint_pairs = list(combinations(path_endpoints, 2))
                processed_segments = set()  # Track processed segments

                for start, end in endpoint_pairs:
                    try:
                        # Find path between these endpoints
                        path = nx.shortest_path(mergeableG, start, end)

                        # Check for internal constraint nodes
                        internal_constraints = set(path[1:-1]).intersection(
                            local_constraint_nodes
                        )

                        if internal_constraints:
                            # Split path at constraint nodes
                            break_points = (
                                [0]
                                + sorted([path.index(n) for n in internal_constraints])
                                + [len(path) - 1]
                            )

                            # Process each segment between break points
                            for i in range(len(break_points) - 1):
                                start_idx = break_points[i]
                                end_idx = break_points[i + 1]

                                # Get the subpath
                                segment = path[start_idx : end_idx + 1]
                                segment_key = frozenset(segment)

                                # Skip if already processed or too short
                                if (
                                    segment_key in processed_segments
                                    or len(segment) < 3
                                ):
                                    continue
                                processed_segments.add(segment_key)

                                # Get edges in this segment
                                segment_edges = []
                                for j in range(len(segment) - 1):
                                    n0, n1 = segment[j], segment[j + 1]
                                    for p in mergeableG[n0][n1]:
                                        segment_edges.append(
                                            mergeableG[n0][n1][p]["featid"]
                                        )

                                # Skip if only one edge
                                if len(segment_edges) <= 1:
                                    continue

                                # Use first edge as reference for merging
                                idToKeep = segment_edges[0]
                                segment_ids_to_delete = set(segment_edges[1:])

                                # Start with reference geometry
                                outputFeat = featDict[idToKeep]
                                merged_geom = outputFeat.geometry()

                                # Merge each additional geometry while preserving direction
                                for id in segment_ids_to_delete:
                                    geom_to_merge = featDict[id].geometry()

                                    # Get vertices of both geometries
                                    merged_vertices = list(merged_geom.vertices())
                                    merged_start = QgsPointXY(merged_vertices[0])
                                    merged_end = QgsPointXY(merged_vertices[-1])

                                    to_merge_vertices = list(geom_to_merge.vertices())
                                    to_merge_start = QgsPointXY(to_merge_vertices[0])
                                    to_merge_end = QgsPointXY(to_merge_vertices[-1])

                                    # Calculate distances between endpoints
                                    d_end_start = merged_end.distance(to_merge_start)
                                    d_end_end = merged_end.distance(to_merge_end)
                                    d_start_start = merged_start.distance(
                                        to_merge_start
                                    )
                                    d_start_end = merged_start.distance(to_merge_end)

                                    # Choose connection strategy based on endpoint distances
                                    if (
                                        d_end_start < d_end_end
                                        and d_end_start < d_start_start
                                    ):
                                        # Append directly
                                        merged_geom = merged_geom.combine(
                                            geom_to_merge
                                        ).mergeLines()
                                    elif (
                                        d_start_end < d_end_end
                                        and d_start_end < d_start_start
                                    ):
                                        # Prepend directly
                                        merged_geom = geom_to_merge.combine(
                                            merged_geom
                                        ).mergeLines()
                                    else:
                                        # Reverse and then connect
                                        line = geom_to_merge.constGet().clone()
                                        reversed_line = line.reversed()
                                        geom_to_merge = QgsGeometry(reversed_line)

                                        # Recalculate after reversal
                                        to_merge_vertices = list(
                                            geom_to_merge.vertices()
                                        )
                                        to_merge_start = QgsPointXY(
                                            to_merge_vertices[0]
                                        )

                                        # Determine which end to connect to
                                        if merged_end.distance(
                                            to_merge_start
                                        ) < merged_start.distance(to_merge_start):
                                            merged_geom = merged_geom.combine(
                                                geom_to_merge
                                            ).mergeLines()
                                        else:
                                            merged_geom = geom_to_merge.combine(
                                                merged_geom
                                            ).mergeLines()

                                    deleteIdSet.add(id)

                                if isMulti:
                                    merged_geom.convertToMultiType()

                                outputFeat.setGeometry(merged_geom)
                                featureSetToUpdate.add(outputFeat)
                        else:
                            # No internal constraints, process whole path
                            segment_key = frozenset(path)

                            # Skip if already processed
                            if segment_key in processed_segments:
                                continue
                            processed_segments.add(segment_key)

                            # Get edges in this path
                            path_edges = []
                            for i in range(len(path) - 1):
                                n0, n1 = path[i], path[i + 1]
                                for p in mergeableG[n0][n1]:
                                    path_edges.append(mergeableG[n0][n1][p]["featid"])

                            # Skip if only one edge
                            if len(path_edges) <= 1:
                                continue

                            # Merge the path edges
                            idToKeep = path_edges[0]
                            path_ids_to_delete = set(path_edges[1:])

                            outputFeat = featDict[idToKeep]
                            merged_geom = outputFeat.geometry()

                            for id in path_ids_to_delete:
                                geom_to_merge = featDict[id].geometry()

                                # Get vertices
                                merged_vertices = list(merged_geom.vertices())
                                merged_start = QgsPointXY(merged_vertices[0])
                                merged_end = QgsPointXY(merged_vertices[-1])

                                to_merge_vertices = list(geom_to_merge.vertices())
                                to_merge_start = QgsPointXY(to_merge_vertices[0])
                                to_merge_end = QgsPointXY(to_merge_vertices[-1])

                                # Calculate endpoint distances
                                d_end_start = merged_end.distance(to_merge_start)
                                d_end_end = merged_end.distance(to_merge_end)
                                d_start_start = merged_start.distance(to_merge_start)
                                d_start_end = merged_start.distance(to_merge_end)

                                # Choose connection strategy
                                if (
                                    d_end_start < d_end_end
                                    and d_end_start < d_start_start
                                ):
                                    # Append directly
                                    merged_geom = merged_geom.combine(
                                        geom_to_merge
                                    ).mergeLines()
                                elif (
                                    d_start_end < d_end_end
                                    and d_start_end < d_start_start
                                ):
                                    # Prepend directly
                                    merged_geom = geom_to_merge.combine(
                                        merged_geom
                                    ).mergeLines()
                                else:
                                    # Reverse and then connect
                                    line = geom_to_merge.constGet().clone()
                                    reversed_line = line.reversed()
                                    geom_to_merge = QgsGeometry(reversed_line)

                                    # Recalculate
                                    to_merge_vertices = list(geom_to_merge.vertices())
                                    to_merge_start = QgsPointXY(to_merge_vertices[0])

                                    # Choose connection point
                                    if merged_end.distance(
                                        to_merge_start
                                    ) < merged_start.distance(to_merge_start):
                                        merged_geom = merged_geom.combine(
                                            geom_to_merge
                                        ).mergeLines()
                                    else:
                                        merged_geom = geom_to_merge.combine(
                                            merged_geom
                                        ).mergeLines()

                                deleteIdSet.add(id)

                            if isMulti:
                                merged_geom.convertToMultiType()

                            outputFeat.setGeometry(merged_geom)
                            featureSetToUpdate.add(outputFeat)

                    except nx.NetworkXNoPath:
                        # No path between endpoints
                        continue

    return featureSetToUpdate, deleteIdSet


def identify_unmerged_edges_on_graph(
    nx,
    G,
    featDict: Dict[int, QgsFeature],
    nodeIdDict: Dict[int, QByteArray],
    filterPointSet: Set[QByteArray],
    filterLineLayer: QgsVectorLayer,
    attributeNameList: List[str],
) -> Set[int]:
    auxDict = defaultdict(lambda: nx.MultiGraph())
    outputIdSet = set()
    for n0, n1, p in G.edges:
        featid = G[n0][n1][p]["featid"]
        feat = featDict[featid]
        attrTuple = tuple(feat[i] for i in attributeNameList)
        auxDict[attrTuple].add_edge(n0, n1, featid=featid)
    for auxGraph in auxDict.values():
        for idSet, mergeableG in find_mergeable_edges_on_graph(
            nx, auxGraph, nodeIdDict
        ).items():
            if len(mergeableG.edges) < 2:
                continue
            candidatePointSet = idSet - filterPointSet
            if candidatePointSet == set():
                continue
            for nodeId in candidatePointSet:
                if nodeId in outputIdSet or mergeableG.degree(nodeId) != 2:
                    continue
                if filterLineLayer is not None:
                    geom = QgsGeometry()
                    geom.fromWkb(nodeIdDict[nodeId])
                    buffer = geom.buffer(1e-6, -1)
                    geomBB = buffer.boundingBox()
                    if any(
                        f.geometry().intersects(geom)
                        for f in filterLineLayer.getFeatures(geomBB)
                    ):
                        continue
                outputIdSet.add(nodeId)
    return outputIdSet


def buildAuxLayersPriorGraphBuilding(
    networkLayer,
    context=None,
    geographicBoundsLayer=None,
    feedback=None,
    clipOnGeographicBounds=False,
    idFieldName=None,
):
    algRunner = AlgRunner()
    nSteps = 6 if geographicBoundsLayer is not None else 4
    multiStepFeedback = (
        QgsProcessingMultiStepFeedback(nSteps, feedback)
        if feedback is not None
        else None
    )
    context = QgsProcessingContext() if context is None else context
    currentStep = 0
    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(currentStep)
    localCache = algRunner.runCreateFieldWithExpression(
        inputLyr=networkLayer,
        expression="$id",
        fieldName="featid" if idFieldName is None else idFieldName,
        fieldType=1,
        context=context,
        feedback=multiStepFeedback,
    )
    currentStep += 1
    if geographicBoundsLayer is not None:
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        algRunner.runCreateSpatialIndex(
            inputLyr=localCache,
            context=context,
            feedback=multiStepFeedback,
            is_child_algorithm=True,
        )
        currentStep += 1
        if multiStepFeedback is not None:
            multiStepFeedback.setCurrentStep(currentStep)
        localCache = (
            algRunner.runExtractByLocation(
                inputLyr=localCache,
                intersectLyr=geographicBoundsLayer,
                context=context,
                feedback=multiStepFeedback,
            )
            if not clipOnGeographicBounds
            else algRunner.runClip(
                inputLayer=localCache,
                overlayLayer=geographicBoundsLayer,
                context=context,
                feedback=multiStepFeedback,
            )
        )
        currentStep += 1
    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(currentStep)
    algRunner.runCreateSpatialIndex(
        inputLyr=localCache,
        context=context,
        feedback=multiStepFeedback,
        is_child_algorithm=True,
    )
    currentStep += 1
    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(currentStep)
    nodesLayer = algRunner.runExtractSpecificVertices(
        inputLyr=localCache,
        vertices="0,-1",
        context=context,
        feedback=multiStepFeedback,
    )
    currentStep += 1
    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(currentStep)
    nodesLayer = algRunner.runCreateFieldWithExpression(
        inputLyr=nodesLayer,
        expression="$id",
        fieldName="nfeatid" if idFieldName is None else f"n{idFieldName}",
        fieldType=1,
        context=context,
        feedback=multiStepFeedback,
    )
    return localCache, nodesLayer


def getInAndOutNodesOnGeographicBounds(
    nodeDict: Dict[QByteArray, int],
    nodesLayer: QgsVectorLayer,
    geographicBoundsLayer: QgsVectorLayer,
    context: Optional[QgsProcessingContext] = None,
    feedback: Optional[QgsFeedback] = None,
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
    multiStepFeedback = (
        QgsProcessingMultiStepFeedback(3, feedback) if feedback is not None else None
    )
    context = context if context is not None else QgsProcessingContext()
    algRunner = AlgRunner()
    currentStep = 0
    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(currentStep)
    algRunner.runCreateSpatialIndex(
        inputLyr=nodesLayer,
        context=context,
        feedback=multiStepFeedback,
        is_child_algorithm=True,
    )
    currentStep += 1
    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(currentStep)
    nodesOutsideGeographicBounds = algRunner.runExtractByLocation(
        inputLyr=nodesLayer,
        intersectLyr=geographicBoundsLayer,
        predicate=[AlgRunner.Disjoint],
        context=context,
        feedback=multiStepFeedback,
    )
    currentStep += 1
    if multiStepFeedback is not None:
        multiStepFeedback.setCurrentStep(currentStep)
    fixedInNodeSet, fixedOutNodeSet = set(), set()
    nFeats = nodesOutsideGeographicBounds.featureCount()
    if nFeats == 0:
        return fixedInNodeSet, fixedOutNodeSet
    stepSize = 100 / nFeats
    for current, nodeFeat in enumerate(nodesOutsideGeographicBounds.getFeatures()):
        if multiStepFeedback is not None and multiStepFeedback.isCanceled():
            break
        selectedSet = fixedInNodeSet if nodeFeat["vertex_pos"] == 0 else fixedOutNodeSet
        geom = nodeFeat.geometry()
        selectedSet.add(nodeDict[geom.asWkb()])
        if multiStepFeedback is not None:
            multiStepFeedback.setProgress(current * stepSize)
    return fixedInNodeSet, fixedOutNodeSet


def find_constraint_points(
    nodesLayer: QgsVectorLayer,
    constraintLayer: QgsVectorLayer,
    nodeDict: Dict[QByteArray, int],
    nodeLayerIdDict: Dict[int, Dict[int, QByteArray]],
    useBuffer: bool = True,
    context: Optional[QgsProcessingContext] = None,
    feedback: Optional[QgsFeedback] = None,
) -> Set[int]:
    multiStepFeedback = (
        QgsProcessingMultiStepFeedback(3, feedback) if feedback is not None else None
    )
    context = context if context is not None else QgsProcessingContext()
    algRunner = AlgRunner()
    constraintSet = set()
    layerToRelate = (
        algRunner.runBuffer(
            inputLayer=constraintLayer,
            distance=1e-6,
            context=context,
            is_child_algorithm=True,
        )
        if constraintLayer.geometryType() != QgsWkbTypes.PointGeometry and useBuffer
        else constraintLayer
    )
    predicate = (
        AlgRunner.Intersects
        if constraintLayer.geometryType() != QgsWkbTypes.PointGeometry
        else AlgRunner.Equals
    )
    selectedNodesFromOcean = algRunner.runExtractByLocation(
        inputLyr=nodesLayer,
        intersectLyr=layerToRelate,
        context=context,
        predicate=[predicate],
        feedback=multiStepFeedback,
    )
    for feat in selectedNodesFromOcean.getFeatures():
        if multiStepFeedback is not None and multiStepFeedback.isCanceled():
            break
        constraintSet.add(nodeDict[nodeLayerIdDict[feat["nfeatid"]]])
    return constraintSet


def generalize_edges_according_to_degrees(
    G,
    constraintSet: Set[int],
    threshold: float,
    feedback: Optional[QgsFeedback] = None,
):
    G_copy = G.copy()
    pairsToRemove = find_smaller_first_order_path_with_length_smaller_than_threshold(
        G=G_copy, constraintSet=constraintSet, threshold=threshold, feedback=feedback
    )
    while pairsToRemove is not None:
        if feedback is not None and feedback.isCanceled():
            break
        for n0, n1 in pairsToRemove:
            G_copy.remove_edge(n0, n1)
        pairsToRemove = (
            find_smaller_first_order_path_with_length_smaller_than_threshold(
                G=G_copy,
                constraintSet=constraintSet,
                threshold=threshold,
                feedback=feedback,
            )
        )
    return G_copy


def find_smaller_first_order_path_with_length_smaller_than_threshold(
    G, constraintSet: Set[int], threshold: float, feedback: Optional[QgsFeedback] = None
) -> frozenset[frozenset]:
    total_length_dict = dict()
    edges_to_remove_dict = dict()
    for node in set(
        node for node in G.nodes if G.degree(node) == 1 and node not in constraintSet
    ):
        if feedback is not None and feedback.isCanceled():
            return None
        connectedNodes = fetch_connected_nodes(G, node, 2)
        if set(connectedNodes).intersection(constraintSet):
            continue
        pairs = frozenset(
            [frozenset([a, b]) for i in connectedNodes for a, b in G.edges(i)]
        )
        total_length = sum(G[a][b]["length"] for a, b in pairs)
        if total_length >= threshold:
            continue
        edges_to_remove_dict[node] = pairs
        total_length_dict[node] = total_length
    if len(total_length_dict) == 0:
        return None
    smaller_path_node = min(
        total_length_dict.keys(), key=lambda x: total_length_dict[x]
    )
    return edges_to_remove_dict[smaller_path_node]


def find_small_closed_line_groups(
    nx,
    G,
    minLength: float,
    lengthField: Optional[str] = "length",
    idField: Optional[str] = "featid",
    feedback: Optional[QgsFeedback] = None,
) -> set:
    idsToRemove = set()
    loopList = list(nx.simple_cycles(G))
    nLoops = len(loopList)
    if nLoops == 0:
        return idsToRemove
    stepSize = 100 / nLoops
    for current, loop in enumerate(loopList):
        if feedback is not None and feedback.isCanceled():
            break
        pairs = set(pairwise(loop))
        pairs.add((loop[-1], loop[0]))
        currentLen = sum(map(lambda x: G[x[0]][x[1]][0][lengthField], pairs))
        if currentLen > minLength:
            continue
        for pair in pairs:
            idsToRemove.add(G[pair[0]][pair[1]][0][idField])
        if feedback is not None:
            feedback.setProgress(current * stepSize)
    return idsToRemove


def connectedEdgesFeatIds(
    G: Any,
    featid: int,
    feedback: Optional[QgsFeedback] = None,
) -> Set[int]:
    """
    Find edges connected to the edge with the given featid.

    Args:
        G: The graph object (can be Graph, DiGraph, MultiGraph, or MultiDiGraph).
        featid: The feature ID to find connected edges for.
        feedback: An optional QgsFeedback object to provide feedback during processing.

    Returns:
        A set of feature IDs for edges connected to the edge with the given featid.
    """
    # Determine if the graph is a multigraph
    is_multigraph = hasattr(G, "is_multigraph") and G.is_multigraph()

    # Find the nodes of the edge with the given featid
    edge_nodes = set()

    # Iterate through all edges to find the one with the matching featid
    if is_multigraph:
        for u, v, key in G.edges(keys=True):
            if feedback is not None and feedback.isCanceled():
                return set()
            if G[u][v][key].get("featid") == featid:
                edge_nodes.add(u)
                edge_nodes.add(v)
    else:
        for u, v in G.edges():
            if feedback is not None and feedback.isCanceled():
                return set()
            if G[u][v].get("featid") == featid:
                edge_nodes.add(u)
                edge_nodes.add(v)

    if not edge_nodes:
        # No edge found with the given featid
        return set()

    # Get all connected featids
    connected_featids = set()

    # Process all edges connected to the nodes of the edge with the given featid
    for node in edge_nodes:
        if is_multigraph:
            for u, v, key in G.edges(node, keys=True):
                if feedback is not None and feedback.isCanceled():
                    return connected_featids
                connected_featid = G[u][v][key].get("featid")
                if connected_featid is not None and connected_featid != featid:
                    connected_featids.add(connected_featid)
        else:
            for u, v in G.edges(node):
                if feedback is not None and feedback.isCanceled():
                    return connected_featids
                connected_featid = G[u][v].get("featid")
                if connected_featid is not None and connected_featid != featid:
                    connected_featids.add(connected_featid)

    return connected_featids
