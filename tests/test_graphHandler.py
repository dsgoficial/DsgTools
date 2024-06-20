# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DsgTools
                                 A QGIS plugin
 Brazilian Army Cartographic Production Tools
                              -------------------
        begin                : 2023-06-19
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

import sys
import unittest
import networkx as nx
from DsgTools.core.GeometricTools.graphHandler import (
    fetch_connected_nodes,
    buildAuxFlowGraph,
)


class FetchConnectedNodesTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test graph
        edges_list = [
            (1, 2),
            (11, 3),
            (3, 2),
            (2, 4),
            (4, 5),
            (4, 6),
            (5, 7),
            (6, 7),
            (7, 8),
        ]
        self.G = nx.Graph()
        self.DiG = nx.DiGraph()
        self.G.add_edges_from(edges_list)
        self.DiG.add_edges_from(edges_list)

    def test_fetch_connected_nodes_starting_node_11_max_degree_2(self):
        result = fetch_connected_nodes(self.G, 11, 2)
        expected = [11, 3]
        self.assertCountEqual(result, expected)

    def test_fetch_connected_nodes_dig_starting_node_11_max_degree_2(self):
        result = fetch_connected_nodes(self.DiG, 11, 2)
        expected = [11, 3]
        self.assertCountEqual(result, expected)

    def test_fetch_connected_nodes_starting_node_11_max_degree_1(self):
        result = fetch_connected_nodes(self.G, 11, 1)
        expected = [11]
        self.assertCountEqual(result, expected)

    def test_fetch_connected_nodes_starting_node_11_max_degree_3(self):
        result = fetch_connected_nodes(self.G, 11, 3)
        expected = [11, 3, 2, 1, 4, 5, 6, 7, 8]
        self.assertCountEqual(result, expected)

    def test_fetch_connected_nodes_dig_starting_node_11_max_degree_3(self):
        result = fetch_connected_nodes(self.DiG, 11, 3)
        expected = [11, 3, 2, 4, 5, 6, 7, 8]
        self.assertCountEqual(result, expected)


class BuildAuxFlowGraphTestCase(unittest.TestCase):
    @staticmethod
    def graphs_equal(graph1, graph2):
        """Check if graphs are equal.

        Equality here means equal as Python objects (not isomorphism).
        Node, edge and graph data must match.

        Parameters
        ----------
        graph1, graph2 : graph

        Returns
        -------
        bool
            True if graphs are equal, False otherwise.
        """
        return (
            graph1.adj == graph2.adj
            and graph1.nodes == graph2.nodes
            and graph1.graph == graph2.graph
        )

    def test_build_flow_dict_case1(self):
        G = nx.Graph()
        G.add_edges_from(
            [
                (1, 3),
                (2, 3),
                (4, 3),
                (4, 5),
                (19, 4),
                (19, 6),
                (6, 7),
                (8, 6),
                (9, 17),
                (8, 17),
                (10, 12),
                (12, 11),
                (12, 13),
                (13, 8),
                (14, 13),
                (14, 18),
                (18, 15),
                (14, 16),
            ]
        )
        expectedG = nx.DiGraph()
        expectedG.add_edges_from(
            [
                (1, 3),
                (2, 3),
                (3, 4),
                (5, 4),
                (4, 19),
                (19, 6),
                (7, 6),
                (6, 8),
                (9, 17),
                (17, 8),
                (8, 13),
                (10, 12),
                (11, 12),
                (12, 13),
                (13, 14),
                (14, 18),
                (14, 16),
                (18, 15),
            ]
        )
        outputG = buildAuxFlowGraph(nx, G, {1, 9}, {15, 16})
        self.assertEqual(set(expectedG.nodes), set(outputG.nodes))
        self.assertEqual(set(expectedG.edges), set(outputG.edges))
        self.assertEqual(set(expectedG.adj), set(outputG.adj))

    def test_build_flow_dict_case2(self):
        G = nx.Graph()
        G.add_edges_from(
            [
                (1, 2),
                (2, 3),
                (3, 4),
                (4, 6),
                (7, 6),
                (6, 2),
                (4, 5),
            ]
        )
        expectedG = nx.DiGraph()
        expectedG.add_edges_from(
            [
                (1, 2),
                (2, 3),
                (3, 4),
                (2, 6),
                (7, 6),
                (6, 4),
                (4, 5),
            ]
        )
        outputG = buildAuxFlowGraph(nx, G, {1}, {5})
        self.assertEqual(set(expectedG.nodes), set(outputG.nodes))
        self.assertEqual(set(expectedG.edges), set(outputG.edges))
        self.assertEqual(set(expectedG.adj), set(outputG.adj))

    def test_build_flow_dict_case3(self):
        G = nx.Graph()
        G.add_edges_from(
            [
                (1, 3),
                (2, 3),
                (4, 3),
                (4, 5),
                (4, 7),
                (6, 7),
                (8, 7),
                (8, 9),
                (9, 10),
                (10, 14),
                (14, 13),
                (13, 8),  # loop
                (12, 13),
                (12, 11),
                (15, 14),
                (15, 16),
                (17, 10),
                (17, 18),
                (26, 17),
                (26, 25),
                (27, 26),
                (27, 28),
                (27, 29),
                (31, 18),
                (30, 31),
                (31, 32),
                (19, 18),
                (19, 20),
                (34, 19),
                (34, 21),
                (34, 22),
                (22, 23),
                (22, 33),
                (24, 33),
            ]
        )
        expectedG = nx.DiGraph()
        expectedG.add_edges_from(
            [
                (1, 3),
                (2, 3),
                (3, 4),
                (5, 4),
                (4, 7),
                (6, 7),
                (7, 8),
                (8, 9),
                (8, 13),
                (11, 12),
                (12, 13),
                (13, 14),
                (9, 10),
                (14, 10),
                (14, 15),
                (15, 16),
                (10, 17),
                (17, 18),
                (25, 26),
                (26, 27),
                (28, 27),
                (27, 29),
                (17, 18),
                (18, 31),
                (30, 31),
                (31, 32),
                (24, 33),
                (33, 22),
                (23, 22),
                (22, 34),
                (21, 34),
                (34, 19),
                (19, 18),
                (20, 19),
            ]
        )
        outputG = buildAuxFlowGraph(nx, G, {1, 24}, {16, 29, 32})
        self.assertEqual(set(expectedG.nodes), set(outputG.nodes))
        self.assertEqual(set(expectedG.edges), set(outputG.edges))
        self.assertEqual(set(expectedG.adj), set(outputG.adj))

    def test_build_flow_dict_case4(self):
        G = nx.Graph()
        G.add_edges_from(
            [
                (1, 3),
                (2, 3),
                (4, 3),
                (4, 5),
                (19, 4),
                (19, 6),
                (6, 7),
                (8, 6),
                (9, 17),
                (8, 17),
                (10, 12),
                (12, 11),
                (12, 13),
                (13, 8),
                (14, 13),
                (14, 18),
                (18, 15),
                (14, 16),
                (21, 22),
                (22, 20),
                (24, 23),
                (24, 22),
                (24, 25),
                (26, 25),
                (27, 26),
                (28, 26),
                (28, 29),
                (32, 29),
                (30, 29),
                (30, 31),
                (32, 33),
                (33, 34),
                (33, 35),
            ]
        )
        expectedG = nx.DiGraph()
        expectedG.add_edges_from(
            [
                (1, 3),
                (2, 3),
                (3, 4),
                (5, 4),
                (4, 19),
                (19, 6),
                (7, 6),
                (6, 8),
                (9, 17),
                (17, 8),
                (8, 13),
                (10, 12),
                (11, 12),
                (12, 13),
                (13, 14),
                (14, 18),
                (14, 16),
                (18, 15),
                (20, 22),
                (21, 22),
                (22, 24),
                (23, 24),
                (24, 25),
                (25, 26),
                (27, 26),
                (26, 28),
                (28, 29),
                (34, 33),
                (35, 33),
                (33, 32),
                (32, 29),
                (29, 30),
                (30, 31),
            ]
        )
        outputG = buildAuxFlowGraph(nx, G, {1, 9}, {15, 16, 31})
        self.assertEqual(set(expectedG.nodes), set(outputG.nodes))
        self.assertEqual(set(expectedG.edges), set(outputG.edges))
        self.assertEqual(set(expectedG.adj), set(outputG.adj))


def run_all(filterString=None):
    """Default function that is called by the runner if nothing else is specified"""
    filterString = "test_" if filterString is None else filterString
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(FetchConnectedNodesTestCase, filterString))
    suite.addTests(unittest.makeSuite(BuildAuxFlowGraphTestCase, filterString))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
