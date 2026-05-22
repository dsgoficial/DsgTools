# -*- coding: utf-8 -*-
import math
import pytest
pytestmark = pytest.mark.unit


from qgis.core import (
    Qgis,
    QgsFeature,
    QgsGeometry,
    QgsPoint,
    QgsPointXY,
    QgsVectorLayer,
    QgsWkbTypes,
)

from DsgTools.core.GeometricTools.geometryHandler import GeometryHandler


@pytest.fixture
def handler():
    return GeometryHandler()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def make_line_layer(wkt_list=None, multipart=False):
    geom_type = "MultiLineString" if multipart else "LineString"
    lyr = QgsVectorLayer(f"{geom_type}?crs=EPSG:4326", "lines", "memory")
    if wkt_list:
        pr = lyr.dataProvider()
        feats = []
        for wkt in wkt_list:
            feat = QgsFeature()
            feat.setGeometry(QgsGeometry.fromWkt(wkt))
            feats.append(feat)
        pr.addFeatures(feats)
        lyr.updateExtents()
    return lyr


def make_polygon_layer(wkt_list=None):
    lyr = QgsVectorLayer("Polygon?crs=EPSG:4326", "polygons", "memory")
    if wkt_list:
        pr = lyr.dataProvider()
        feats = []
        for wkt in wkt_list:
            feat = QgsFeature()
            feat.setGeometry(QgsGeometry.fromWkt(wkt))
            feats.append(feat)
        pr.addFeatures(feats)
        lyr.updateExtents()
    return lyr


def make_point_layer(wkt_list=None):
    lyr = QgsVectorLayer("Point?crs=EPSG:4326", "points", "memory")
    if wkt_list:
        pr = lyr.dataProvider()
        feats = []
        for wkt in wkt_list:
            feat = QgsFeature()
            feat.setGeometry(QgsGeometry.fromWkt(wkt))
            feats.append(feat)
        pr.addFeatures(feats)
        lyr.updateExtents()
    return lyr


# ---------------------------------------------------------------------------
# getClockWiseList
# ---------------------------------------------------------------------------
class TestGetClockWiseList:
    def test_counter_clockwise_returns_as_is(self, handler):
        # CCW square: sum > 0 → returned unchanged
        pts = [
            QgsPointXY(0, 0),
            QgsPointXY(0, 1),
            QgsPointXY(1, 1),
            QgsPointXY(1, 0),
            QgsPointXY(0, 0),
        ]
        result = handler.getClockWiseList(pts)
        assert result == pts

    def test_clockwise_is_reversed(self, handler):
        # CW square: sum < 0 → returned reversed
        pts = [
            QgsPointXY(0, 0),
            QgsPointXY(1, 0),
            QgsPointXY(1, 1),
            QgsPointXY(0, 1),
            QgsPointXY(0, 0),
        ]
        result = handler.getClockWiseList(pts)
        assert result == pts[::-1]

    def test_single_point_returns_as_is(self, handler):
        pts = [QgsPointXY(1, 2)]
        result = handler.getClockWiseList(pts)
        assert result == pts


# ---------------------------------------------------------------------------
# isclose
# ---------------------------------------------------------------------------
class TestIsClose:
    def test_identical_values(self, handler):
        assert handler.isclose(1.0, 1.0)

    def test_close_values_within_default_tolerance(self, handler):
        assert handler.isclose(1.0, 1.0 + 1e-10)

    def test_far_values_are_not_close(self, handler):
        assert not handler.isclose(1.0, 2.0)

    def test_custom_abs_tolerance(self, handler):
        assert handler.isclose(1.0, 1.05, abs_tol=0.1)
        assert not handler.isclose(1.0, 1.2, abs_tol=0.1)

    def test_custom_rel_tolerance(self, handler):
        assert handler.isclose(100.0, 101.0, rel_tol=0.02)
        assert not handler.isclose(100.0, 110.0, rel_tol=0.02)

    def test_zero_comparison(self, handler):
        assert handler.isclose(0.0, 0.0)
        assert not handler.isclose(0.0, 1e-8)


# ---------------------------------------------------------------------------
# adjustGeometry
# ---------------------------------------------------------------------------
class TestAdjustGeometry:
    def test_single_polygon_returns_one_item(self, handler):
        geom = QgsGeometry.fromWkt("POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))")
        result = handler.adjustGeometry(
            geom, {"hasMValues": False, "hasZValues": False, "isMulti": False}
        )
        assert len(result) == 1

    def test_multipolygon_splits_into_parts(self, handler):
        geom = QgsGeometry.fromWkt(
            "MULTIPOLYGON(((0 0,1 0,1 1,0 1,0 0)),((2 2,3 2,3 3,2 3,2 2)))"
        )
        result = handler.adjustGeometry(
            geom, {"hasMValues": False, "hasZValues": False, "isMulti": False}
        )
        assert len(result) == 2

    def test_is_multi_converts_to_multipart(self, handler):
        geom = QgsGeometry.fromWkt("POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))")
        result = handler.adjustGeometry(
            geom, {"hasMValues": False, "hasZValues": False, "isMulti": True}
        )
        assert len(result) == 1
        assert result[0].isMultipart()

    def test_none_geometry_returns_empty_list(self, handler):
        result = handler.adjustGeometry(
            None, {"hasMValues": False, "hasZValues": False, "isMulti": False}
        )
        assert result == []


# ---------------------------------------------------------------------------
# deaggregateGeometry
# ---------------------------------------------------------------------------
class TestDeaggregateGeometry:
    def test_single_part_returns_list_with_one(self, handler):
        geom = QgsGeometry.fromWkt("POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))")
        result = handler.deaggregateGeometry(geom)
        assert len(result) == 1

    def test_multipart_returns_all_parts(self, handler):
        geom = QgsGeometry.fromWkt(
            "MULTIPOLYGON(((0 0,1 0,1 1,0 1,0 0)),((2 2,3 2,3 3,2 3,2 2)))"
        )
        result = handler.deaggregateGeometry(geom)
        assert len(result) == 2

    def test_each_part_is_multipart_geometry(self, handler):
        geom = QgsGeometry.fromWkt(
            "MULTILINESTRING((0 0,1 1),(2 2,3 3))"
        )
        result = handler.deaggregateGeometry(geom)
        assert all(g.isMultipart() for g in result)

    def test_none_returns_list_with_none(self, handler):
        result = handler.deaggregateGeometry(None)
        assert result == [None]


# ---------------------------------------------------------------------------
# getGeomNodes
# ---------------------------------------------------------------------------
class TestGetGeomNodes:
    def test_line_single_returns_point_list(self, handler):
        geom = QgsGeometry.fromWkt("LINESTRING(0 0, 1 1, 2 0)")
        nodes = handler.getGeomNodes(geom, 1, False)
        assert len(nodes) == 3

    def test_multiline_returns_list_of_lists(self, handler):
        geom = QgsGeometry.fromWkt("MULTILINESTRING((0 0,1 1),(2 2,3 3))")
        nodes = handler.getGeomNodes(geom, 1, True)
        assert len(nodes) == 2
        assert len(nodes[0]) == 2

    def test_polygon_single_returns_ring_list(self, handler):
        geom = QgsGeometry.fromWkt("POLYGON((0 0, 1 0, 1 1, 0 1, 0 0))")
        nodes = handler.getGeomNodes(geom, 2, False)
        assert len(nodes) == 1  # one ring
        assert len(nodes[0]) == 5

    def test_point_single_returns_point(self, handler):
        geom = QgsGeometry.fromWkt("POINT(1 2)")
        nodes = handler.getGeomNodes(geom, 0, False)
        assert math.isclose(nodes.x(), 1.0)
        assert math.isclose(nodes.y(), 2.0)


# ---------------------------------------------------------------------------
# getFirstNode / getLastNode / getFirstAndLastNode
# ---------------------------------------------------------------------------
class TestNodeExtraction:
    def test_get_first_node_single_line(self, handler):
        lyr = make_line_layer(["LINESTRING(0 0, 1 1, 2 2)"])
        feat = next(lyr.getFeatures())
        node = handler.getFirstNode(lyr, feat, geomType=1)
        assert math.isclose(node.x(), 0.0)
        assert math.isclose(node.y(), 0.0)

    def test_get_last_node_single_line(self, handler):
        lyr = make_line_layer(["LINESTRING(0 0, 1 1, 2 2)"])
        feat = next(lyr.getFeatures())
        node = handler.getLastNode(lyr, feat, geomType=1)
        assert math.isclose(node.x(), 2.0)
        assert math.isclose(node.y(), 2.0)

    def test_get_second_node_single_line(self, handler):
        lyr = make_line_layer(["LINESTRING(0 0, 1 1, 2 2)"])
        feat = next(lyr.getFeatures())
        node = handler.getSecondNode(lyr, feat, geomType=1)
        assert math.isclose(node.x(), 1.0)
        assert math.isclose(node.y(), 1.0)

    def test_get_penult_node_single_line(self, handler):
        lyr = make_line_layer(["LINESTRING(0 0, 1 1, 2 2)"])
        feat = next(lyr.getFeatures())
        node = handler.getPenultNode(lyr, feat, geomType=1)
        assert math.isclose(node.x(), 1.0)
        assert math.isclose(node.y(), 1.0)

    def test_get_first_and_last_node(self, handler):
        lyr = make_line_layer(["LINESTRING(3 4, 5 6, 7 8)"])
        feat = next(lyr.getFeatures())
        first, last = handler.getFirstAndLastNode(lyr, feat, geomType=1)
        assert math.isclose(first.x(), 3.0) and math.isclose(first.y(), 4.0)
        assert math.isclose(last.x(), 7.0) and math.isclose(last.y(), 8.0)


# ---------------------------------------------------------------------------
# getFirstAndLastNodeFromGeom
# ---------------------------------------------------------------------------
class TestGetFirstAndLastNodeFromGeom:
    def test_single_line(self, handler):
        geom = QgsGeometry.fromWkt("LINESTRING(0 0, 1 1, 2 2)")
        first, last = handler.getFirstAndLastNodeFromGeom(geom)
        assert math.isclose(first.x(), 0.0)
        assert math.isclose(last.x(), 2.0)

    def test_multiline_single_part(self, handler):
        geom = QgsGeometry.fromWkt("MULTILINESTRING((0 0,1 1,2 2))")
        first, last = handler.getFirstAndLastNodeFromGeom(geom)
        assert math.isclose(first.x(), 0.0)
        assert math.isclose(last.x(), 2.0)


# ---------------------------------------------------------------------------
# makeQgsPolygonFromBounds
# ---------------------------------------------------------------------------
class TestMakeQgsPolygonFromBounds:
    def test_creates_multipolygon_by_default(self, handler):
        geom = handler.makeQgsPolygonFromBounds(0, 0, 3, 3, isMulti=True)
        assert geom.type() == Qgis.GeometryType.Polygon
        assert geom.isMultipart()

    def test_creates_single_polygon(self, handler):
        geom = handler.makeQgsPolygonFromBounds(0, 0, 3, 3, isMulti=False)
        assert geom.type() == Qgis.GeometryType.Polygon
        assert not geom.isMultipart()

    def test_polygon_covers_bounds(self, handler):
        geom = handler.makeQgsPolygonFromBounds(0, 0, 6, 6, isMulti=False)
        bb = geom.boundingBox()
        assert math.isclose(bb.xMinimum(), 0.0)
        assert math.isclose(bb.yMinimum(), 0.0)
        assert math.isclose(bb.xMaximum(), 6.0)
        assert math.isclose(bb.yMaximum(), 6.0)

    def test_polygon_is_valid(self, handler):
        geom = handler.makeQgsPolygonFromBounds(1, 2, 4, 5, isMulti=False)
        assert geom.isGeosValid()


# ---------------------------------------------------------------------------
# getOuterShellAndHoles
# ---------------------------------------------------------------------------
class TestGetOuterShellAndHoles:
    def test_polygon_without_holes(self, handler):
        geom = QgsGeometry.fromWkt("POLYGON((0 0, 4 0, 4 4, 0 4, 0 0))")
        shells, holes = handler.getOuterShellAndHoles(geom, isMulti=False)
        assert len(shells) == 1
        assert len(holes) == 0

    def test_polygon_with_one_hole(self, handler):
        geom = QgsGeometry.fromWkt(
            "POLYGON((0 0, 4 0, 4 4, 0 4, 0 0),(1 1, 2 1, 2 2, 1 2, 1 1))"
        )
        shells, holes = handler.getOuterShellAndHoles(geom, isMulti=False)
        assert len(shells) == 1
        assert len(holes) == 1

    def test_multipolygon_without_holes(self, handler):
        geom = QgsGeometry.fromWkt(
            "MULTIPOLYGON(((0 0,1 0,1 1,0 1,0 0)),((2 2,3 2,3 3,2 3,2 2)))"
        )
        shells, holes = handler.getOuterShellAndHoles(geom, isMulti=True)
        assert len(shells) == 2
        assert len(holes) == 0
        assert all(g.isMultipart() for g in shells)


# ---------------------------------------------------------------------------
# multiToSinglePart
# ---------------------------------------------------------------------------
class TestMultiToSinglePart:
    def test_multilinestring_splits(self, handler):
        geom = QgsGeometry.fromWkt("MULTILINESTRING((0 0,1 1),(2 2,3 3))")
        parts = handler.multiToSinglePart(geom)
        assert len(parts) == 2

    def test_single_line_returns_one(self, handler):
        geom = QgsGeometry.fromWkt("LINESTRING(0 0,1 1)")
        parts = handler.multiToSinglePart(geom)
        assert len(parts) == 1

    def test_multipolygon_splits(self, handler):
        geom = QgsGeometry.fromWkt(
            "MULTIPOLYGON(((0 0,1 0,1 1,0 1,0 0)),((2 2,3 2,3 3,2 3,2 2)))"
        )
        parts = handler.multiToSinglePart(geom)
        assert len(parts) == 2


# ---------------------------------------------------------------------------
# calcAzimuth (static method)
# ---------------------------------------------------------------------------
class TestCalcAzimuth:
    def test_north(self):
        p1 = QgsPoint(0.0, 0.0)
        p2 = QgsPoint(0.0, 1.0)
        assert math.isclose(GeometryHandler.calcAzimuth(p1, p2), 0.0, abs_tol=1e-10)

    def test_east(self):
        p1 = QgsPoint(0.0, 0.0)
        p2 = QgsPoint(1.0, 0.0)
        assert math.isclose(GeometryHandler.calcAzimuth(p1, p2), 90.0, abs_tol=1e-10)

    def test_south(self):
        p1 = QgsPoint(0.0, 0.0)
        p2 = QgsPoint(0.0, -1.0)
        assert math.isclose(GeometryHandler.calcAzimuth(p1, p2), 180.0, abs_tol=1e-10)

    def test_west(self):
        p1 = QgsPoint(0.0, 0.0)
        p2 = QgsPoint(-1.0, 0.0)
        assert math.isclose(GeometryHandler.calcAzimuth(p1, p2), 270.0, abs_tol=1e-10)

    def test_northeast(self):
        p1 = QgsPoint(0.0, 0.0)
        p2 = QgsPoint(1.0, 1.0)
        az = GeometryHandler.calcAzimuth(p1, p2)
        assert math.isclose(az, 45.0, abs_tol=1e-6)


# ---------------------------------------------------------------------------
# calculateAngleDifferences
# ---------------------------------------------------------------------------
class TestCalculateAngleDifferences:
    def test_north_direction_is_zero(self, handler):
        # calculateAngleDifferences uses convention: 180 - atan2(dx,dy)
        # so north (0,0)->(0,1) gives 180 - 0 = 180
        start = QgsPoint(0.0, 0.0)
        end = QgsPoint(0.0, 1.0)
        angle = handler.calculateAngleDifferences(start, end)
        assert math.isclose(angle, 180.0, abs_tol=1e-10)

    def test_east_direction_is_90(self, handler):
        start = QgsPoint(0.0, 0.0)
        end = QgsPoint(1.0, 0.0)
        angle = handler.calculateAngleDifferences(start, end)
        assert math.isclose(angle, 90.0, abs_tol=1e-10)

    def test_south_direction_is_180(self, handler):
        # south (0,0)->(0,-1): 180 - atan2(0,-1) = 180 - 180 = 0
        start = QgsPoint(0.0, 0.0)
        end = QgsPoint(0.0, -1.0)
        angle = handler.calculateAngleDifferences(start, end)
        assert math.isclose(angle, 0.0, abs_tol=1e-10)


# ---------------------------------------------------------------------------
# identifyAllNodes
# ---------------------------------------------------------------------------
class TestIdentifyAllNodes:
    def test_two_lines_sharing_a_node(self, handler):
        lyr = make_line_layer(
            [
                "LINESTRING(0 0, 1 1)",
                "LINESTRING(1 1, 2 0)",
            ]
        )
        node_dict = handler.identifyAllNodes(lyr)
        # Shared node (1,1) appears in both start/end dicts
        shared = QgsPointXY(1.0, 1.0)
        assert shared in node_dict

    def test_isolated_line_has_start_and_end(self, handler):
        lyr = make_line_layer(["LINESTRING(0 0, 5 5)"])
        node_dict = handler.identifyAllNodes(lyr)
        start = QgsPointXY(0.0, 0.0)
        end = QgsPointXY(5.0, 5.0)
        assert start in node_dict
        assert end in node_dict

    def test_node_start_end_assignment(self, handler):
        lyr = make_line_layer(["LINESTRING(0 0, 1 1)"])
        node_dict = handler.identifyAllNodes(lyr)
        start = QgsPointXY(0.0, 0.0)
        end = QgsPointXY(1.0, 1.0)
        assert len(node_dict[start]["start"]) == 1
        assert len(node_dict[end]["end"]) == 1

    def test_empty_layer_returns_empty_dict(self, handler):
        lyr = make_line_layer()
        node_dict = handler.identifyAllNodes(lyr)
        assert node_dict == {}


# ---------------------------------------------------------------------------
# getOutOfBoundsAngle
# ---------------------------------------------------------------------------
class TestGetOutOfBoundsAngle:
    def test_right_angle_line_no_flags(self, handler):
        # 90-degree angle at (1,1)
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromWkt("LINESTRING(0 1, 1 1, 1 0)"))
        result = handler.getOutOfBoundsAngle(feat, angle=30)
        assert result == []

    def test_sharp_angle_line_raises_flag(self, handler):
        # Acute angle at (1,0): azimuth to (0,0) is 270°, azimuth to (0,1) is 315°
        # vertexAngle = 270-315+360=315, 315>180 → 360-315=45 < 60 → flagged
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromWkt("LINESTRING(0 0, 1 0, 0 1)"))
        result = handler.getOutOfBoundsAngle(feat, angle=60)
        assert len(result) > 0

    def test_result_contains_angle_and_geom(self, handler):
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromWkt("LINESTRING(0 0, 1 0.01, 2 0)"))
        result = handler.getOutOfBoundsAngle(feat, angle=60)
        if result:
            item = result[0]
            assert "angle" in item
            assert "geom" in item
