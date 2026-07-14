# -*- coding: utf-8 -*-
"""Tests for the edge-XOR coverage validator."""

import sys

from qgis.core import (
    QgsFeature,
    QgsGeometry,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingUtils,
    QgsVectorLayer,
)
from qgis.testing import start_app, unittest

from DsgTools.core.DSGToolsProcessingAlgs.Algs.ValidationAlgs.identifyGapsAndOverlapsInCoverageAlgorithm import (
    IdentifyGapsAndOverlapsInCoverageAlgorithm,
    canonical_segment_key,
)


APP = start_app()


def polygon_layer(name, wkts):
    layer = QgsVectorLayer("Polygon?crs=EPSG:31983", name, "memory")
    features = []
    for wkt in wkts:
        feature = QgsFeature()
        feature.setGeometry(QgsGeometry.fromWkt(wkt))
        features.append(feature)
    layer.dataProvider().addFeatures(features)
    layer.updateExtents()
    return layer


class IdentifyCoverageEdgeXorTest(unittest.TestCase):
    def run_algorithm(self, coverage_layers, frame_layer):
        algorithm = IdentifyGapsAndOverlapsInCoverageAlgorithm()
        algorithm.initAlgorithm()
        context = QgsProcessingContext()
        results, successful = algorithm.run(
            {
                algorithm.INPUTLAYERS: coverage_layers,
                algorithm.FRAMELAYER: frame_layer,
                algorithm.SELECTED: False,
                algorithm.GRID_SIZE: 0.000001,
                algorithm.MIN_AREA: 0.0,
                algorithm.FLAGS: "memory:",
                algorithm.NODE_FLAGS: "memory:",
            },
            context,
            QgsProcessingFeedback(),
        )
        self.assertTrue(successful)
        return {
            key: QgsProcessingUtils.mapLayerFromString(layer_id, context)
            for key, layer_id in results.items()
        }

    def test_canonical_segment_key_ignores_orientation_only(self):
        forward = canonical_segment_key(
            QgsGeometry.fromWkt("POINT (0 0)").asPoint(),
            QgsGeometry.fromWkt("POINT (10 0)").asPoint(),
            0.000001,
        )
        reverse = canonical_segment_key(
            QgsGeometry.fromWkt("POINT (10 0)").asPoint(),
            QgsGeometry.fromWkt("POINT (0 0)").asPoint(),
            0.000001,
        )
        split_a = canonical_segment_key(
            QgsGeometry.fromWkt("POINT (0 0)").asPoint(),
            QgsGeometry.fromWkt("POINT (5 0)").asPoint(),
            0.000001,
        )
        self.assertEqual(forward, reverse)
        self.assertNotEqual(forward, split_a)

    def test_perfect_coverage_has_no_flags(self):
        coverage = polygon_layer(
            "coverage",
            [
                "POLYGON ((0 0, 5 0, 5 10, 0 10, 0 0))",
                "POLYGON ((5 0, 10 0, 10 10, 5 10, 5 0))",
            ],
        )
        frame = polygon_layer(
            "frame", ["POLYGON ((0 0, 5 0, 10 0, 10 10, 5 10, 0 10, 0 0))"]
        )
        output = self.run_algorithm([coverage], frame)
        self.assertEqual(output["FLAGS"].featureCount(), 0)
        self.assertEqual(output["NODE_FLAGS"].featureCount(), 0)

    def test_gap_is_reported_as_polygon(self):
        coverage = polygon_layer(
            "coverage",
            [
                "POLYGON ((0 0, 4 0, 4 10, 0 10, 0 0))",
                "POLYGON ((6 0, 10 0, 10 10, 6 10, 6 0))",
            ],
        )
        frame = polygon_layer(
            "frame",
            ["POLYGON ((0 0, 4 0, 6 0, 10 0, 10 10, 6 10, 4 10, 0 10, 0 0))"],
        )
        output = self.run_algorithm([coverage], frame)
        flags = list(output["FLAGS"].getFeatures())
        self.assertEqual(len(flags), 1)
        self.assertTrue(flags[0]["reason"].startswith("COVERFAIL_GAP"))
        self.assertAlmostEqual(flags[0].geometry().area(), 20.0, places=6)

    def test_overlap_is_reported_as_polygon(self):
        coverage = polygon_layer(
            "coverage",
            [
                "POLYGON ((0 0, 6 0, 6 10, 0 10, 0 0))",
                "POLYGON ((4 0, 10 0, 10 10, 4 10, 4 0))",
            ],
        )
        frame = polygon_layer(
            "frame",
            ["POLYGON ((0 0, 4 0, 6 0, 10 0, 10 10, 6 10, 4 10, 0 10, 0 0))"],
        )
        output = self.run_algorithm([coverage], frame)
        flags = list(output["FLAGS"].getFeatures())
        self.assertEqual(len(flags), 1)
        self.assertTrue(flags[0]["reason"].startswith("COVERFAIL_OVERLAP"))
        self.assertAlmostEqual(flags[0].geometry().area(), 20.0, places=6)

    def test_intermediate_node_on_one_side_is_reported(self):
        left = polygon_layer(
            "left", ["POLYGON ((0 0, 5 0, 5 5, 5 10, 0 10, 0 0))"]
        )
        right = polygon_layer(
            "right", ["POLYGON ((5 0, 10 0, 10 10, 5 10, 5 0))"]
        )
        frame = polygon_layer(
            "frame", ["POLYGON ((0 0, 5 0, 10 0, 10 10, 5 10, 0 10, 0 0))"]
        )
        output = self.run_algorithm([left, right], frame)
        node_flags = list(output["NODE_FLAGS"].getFeatures())
        self.assertEqual(len(node_flags), 1)
        self.assertTrue(node_flags[0]["reason"].startswith("EDGE_NODE_MISMATCH"))
        point = node_flags[0].geometry().asPoint()
        self.assertAlmostEqual(point.x(), 5.0, places=6)
        self.assertAlmostEqual(point.y(), 5.0, places=6)

    def test_matching_intermediate_nodes_are_valid(self):
        left = polygon_layer(
            "left", ["POLYGON ((0 0, 5 0, 5 5, 5 10, 0 10, 0 0))"]
        )
        right = polygon_layer(
            "right", ["POLYGON ((5 0, 10 0, 10 10, 5 10, 5 5, 5 0))"]
        )
        frame = polygon_layer(
            "frame", ["POLYGON ((0 0, 5 0, 10 0, 10 10, 5 10, 0 10, 0 0))"]
        )
        output = self.run_algorithm([left, right], frame)
        self.assertEqual(output["FLAGS"].featureCount(), 0)
        self.assertEqual(output["NODE_FLAGS"].featureCount(), 0)


def run_all(filterString=None):
    filterString = "test_" if filterString is None else filterString
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(IdentifyCoverageEdgeXorTest, filterString))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
