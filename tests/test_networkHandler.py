# -*- coding: utf-8 -*-
import math
import pytest
pytestmark = pytest.mark.unit


from qgis.core import (
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsVectorLayer,
    QgsWkbTypes,
)

from DsgTools.core.GeometricTools.networkHandler import NetworkHandler


@pytest.fixture
def handler():
    return NetworkHandler()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def make_line_layer(wkt_list=None):
    lyr = QgsVectorLayer("LineString?crs=EPSG:4326", "lines", "memory")
    if wkt_list:
        pr = lyr.dataProvider()
        feats = [QgsFeature() for _ in wkt_list]
        for feat, wkt in zip(feats, wkt_list):
            feat.setGeometry(QgsGeometry.fromWkt(wkt))
        pr.addFeatures(feats)
        lyr.updateExtents()
    return lyr


def make_point_layer(wkt_list=None):
    lyr = QgsVectorLayer("Point?crs=EPSG:4326", "points", "memory")
    if wkt_list:
        pr = lyr.dataProvider()
        feats = [QgsFeature() for _ in wkt_list]
        for feat, wkt in zip(feats, wkt_list):
            feat.setGeometry(QgsGeometry.fromWkt(wkt))
        pr.addFeatures(feats)
        lyr.updateExtents()
    return lyr


# ---------------------------------------------------------------------------
# identifyAllNodes
# ---------------------------------------------------------------------------
class TestNetworkIdentifyAllNodes:
    def test_two_connected_lines_share_node(self, handler):
        lyr = make_line_layer(["LINESTRING(0 0, 1 1)", "LINESTRING(1 1, 2 2)"])
        node_dict = handler.identifyAllNodes(lyr)
        shared = QgsPointXY(1.0, 1.0)
        assert shared in node_dict

    def test_isolated_line_start_and_end(self, handler):
        lyr = make_line_layer(["LINESTRING(3 4, 5 6)"])
        node_dict = handler.identifyAllNodes(lyr)
        assert QgsPointXY(3.0, 4.0) in node_dict
        assert QgsPointXY(5.0, 6.0) in node_dict

    def test_empty_layer_returns_empty_dict(self, handler):
        lyr = make_line_layer()
        node_dict = handler.identifyAllNodes(lyr)
        assert node_dict == {}

    def test_start_end_assignments(self, handler):
        lyr = make_line_layer(["LINESTRING(0 0, 1 1)"])
        node_dict = handler.identifyAllNodes(lyr)
        start = QgsPointXY(0.0, 0.0)
        end = QgsPointXY(1.0, 1.0)
        assert len(node_dict[start]["start"]) == 1
        assert len(node_dict[end]["end"]) == 1

    def test_three_lines_star_node(self, handler):
        lyr = make_line_layer(
            [
                "LINESTRING(0 0, 1 1)",
                "LINESTRING(2 0, 1 1)",
                "LINESTRING(1 1, 1 3)",
            ]
        )
        node_dict = handler.identifyAllNodes(lyr)
        junction = QgsPointXY(1.0, 1.0)
        assert junction in node_dict
        total_lines = len(node_dict[junction]["start"]) + len(
            node_dict[junction]["end"]
        )
        assert total_lines == 3


# ---------------------------------------------------------------------------
# nodeOnFrame
# ---------------------------------------------------------------------------
class TestNodeOnFrame:
    def test_node_on_frame_within_radius(self, handler):
        node = QgsPointXY(0.0, 0.0)
        frame_contour = QgsGeometry.fromWkt("LINESTRING(-1 0, 1 0)")
        assert handler.nodeOnFrame(node, [frame_contour], searchRadius=0.5)

    def test_node_far_from_frame(self, handler):
        node = QgsPointXY(10.0, 10.0)
        frame_contour = QgsGeometry.fromWkt("LINESTRING(0 0, 1 0)")
        assert not handler.nodeOnFrame(node, [frame_contour], searchRadius=0.1)

    def test_node_on_any_frame_returns_true(self, handler):
        node = QgsPointXY(5.0, 0.0)
        far_frame = QgsGeometry.fromWkt("LINESTRING(0 100, 10 100)")
        near_frame = QgsGeometry.fromWkt("LINESTRING(0 0, 10 0)")
        assert handler.nodeOnFrame(node, [far_frame, near_frame], searchRadius=0.5)

    def test_empty_frame_list_returns_false(self, handler):
        node = QgsPointXY(0.0, 0.0)
        assert not handler.nodeOnFrame(node, [], searchRadius=1.0)


# ---------------------------------------------------------------------------
# nodeIsWaterSink / nodeIsSpillway (None-guard)
# ---------------------------------------------------------------------------
class TestNodeNoneLayerGuards:
    def test_water_sink_none_layer_returns_false(self, handler):
        node = QgsPointXY(0.0, 0.0)
        assert not handler.nodeIsWaterSink(node, None, searchRadius=1.0)

    def test_spillway_none_layer_returns_false(self, handler):
        node = QgsPointXY(0.0, 0.0)
        assert not handler.nodeIsSpillway(node, None, searchRadius=1.0)

    def test_water_sink_with_point_at_same_location(self, handler):
        lyr = make_point_layer(["POINT(0 0)"])
        node = QgsPointXY(0.0, 0.0)
        assert handler.nodeIsWaterSink(node, lyr, searchRadius=0.001)

    def test_water_sink_with_point_far_away(self, handler):
        lyr = make_point_layer(["POINT(100 100)"])
        node = QgsPointXY(0.0, 0.0)
        assert not handler.nodeIsWaterSink(node, lyr, searchRadius=0.001)


# ---------------------------------------------------------------------------
# nodeNextToWaterBodies
# ---------------------------------------------------------------------------
class TestNodeNextToWaterBodies:
    def test_no_water_body_layers_returns_false(self, handler):
        node = QgsPointXY(0.0, 0.0)
        assert not handler.nodeNextToWaterBodies(node, [], searchRadius=1.0)

    def test_polygon_water_body_intersected(self, handler):
        lyr = QgsVectorLayer("Polygon?crs=EPSG:4326", "water", "memory")
        pr = lyr.dataProvider()
        feat = QgsFeature()
        feat.setGeometry(
            QgsGeometry.fromWkt("POLYGON((-1 -1, 1 -1, 1 1, -1 1, -1 -1))")
        )
        pr.addFeatures([feat])
        lyr.updateExtents()
        node = QgsPointXY(0.0, 0.0)
        assert handler.nodeNextToWaterBodies(node, [lyr], searchRadius=0.01)

    def test_point_geometry_layers_ignored(self, handler):
        lyr = make_point_layer(["POINT(0 0)"])
        node = QgsPointXY(0.0, 0.0)
        assert not handler.nodeNextToWaterBodies(node, [lyr], searchRadius=1.0)


# ---------------------------------------------------------------------------
# getFirstNode / getLastNode on NetworkHandler
# ---------------------------------------------------------------------------
class TestNetworkNodeExtraction:
    def test_first_node_single_line(self, handler):
        lyr = make_line_layer(["LINESTRING(1 2, 3 4, 5 6)"])
        feat = next(lyr.getFeatures())
        node = handler.getFirstNode(lyr, feat, geomType=1)
        assert math.isclose(node.x(), 1.0)
        assert math.isclose(node.y(), 2.0)

    def test_last_node_single_line(self, handler):
        lyr = make_line_layer(["LINESTRING(1 2, 3 4, 5 6)"])
        feat = next(lyr.getFeatures())
        node = handler.getLastNode(lyr, feat, geomType=1)
        assert math.isclose(node.x(), 5.0)
        assert math.isclose(node.y(), 6.0)
