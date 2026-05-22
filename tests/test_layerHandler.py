# -*- coding: utf-8 -*-
import math
import pytest
pytestmark = pytest.mark.unit


from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsFeature,
    QgsField,
    QgsGeometry,
    QgsPointXY,
    QgsVectorLayer,
    QgsWkbTypes,
)
from qgis.PyQt.QtCore import QVariant

from DsgTools.core.GeometricTools.layerHandler import LayerHandler


@pytest.fixture
def handler():
    return LayerHandler(iface=None)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def make_layer(wkt_type, crs="EPSG:4326", fields=None):
    lyr = QgsVectorLayer(f"{wkt_type}?crs={crs}", "test", "memory")
    if fields:
        pr = lyr.dataProvider()
        pr.addAttributes(fields)
        lyr.updateFields()
    return lyr


def add_features(lyr, wkt_list, attrs=None):
    pr = lyr.dataProvider()
    feats = []
    for i, wkt in enumerate(wkt_list):
        feat = QgsFeature(lyr.fields())
        feat.setGeometry(QgsGeometry.fromWkt(wkt))
        if attrs and i < len(attrs):
            for k, v in attrs[i].items():
                feat[k] = v
        feats.append(feat)
    pr.addFeatures(feats)
    lyr.updateExtents()


# ---------------------------------------------------------------------------
# getFeatureList
# ---------------------------------------------------------------------------
class TestGetFeatureList:
    def test_returns_all_features_and_size(self, handler):
        lyr = make_layer("Point")
        add_features(lyr, ["POINT(0 0)", "POINT(1 1)", "POINT(2 2)"])
        _, size = handler.getFeatureList(lyr)
        assert size == 3

    def test_return_iterator_false_gives_list(self, handler):
        lyr = make_layer("Point")
        add_features(lyr, ["POINT(0 0)", "POINT(1 1)"])
        feat_list, size = handler.getFeatureList(lyr, returnIterator=False)
        assert isinstance(feat_list, list)
        assert len(feat_list) == 2

    def test_return_size_false_omits_size(self, handler):
        lyr = make_layer("Point")
        add_features(lyr, ["POINT(0 0)"])
        result = handler.getFeatureList(lyr, returnSize=False)
        assert not isinstance(result, tuple)

    def test_only_selected_returns_zero_when_none_selected(self, handler):
        lyr = make_layer("Point")
        add_features(lyr, ["POINT(0 0)", "POINT(1 1)"])
        _, size = handler.getFeatureList(lyr, onlySelected=True)
        assert size == 0

    def test_empty_layer_returns_zero(self, handler):
        lyr = make_layer("Point")
        _, size = handler.getFeatureList(lyr)
        assert size == 0


# ---------------------------------------------------------------------------
# getDestinationParameters
# ---------------------------------------------------------------------------
class TestGetDestinationParameters:
    def test_point_layer_params(self, handler):
        lyr = make_layer("Point")
        params = handler.getDestinationParameters(lyr)
        assert "geomType" in params
        assert "hasMValues" in params
        assert "hasZValues" in params
        assert "isMulti" in params
        assert "crs" in params

    def test_single_point_is_not_multi(self, handler):
        lyr = make_layer("Point")
        params = handler.getDestinationParameters(lyr)
        assert not params["isMulti"]

    def test_multi_line_is_multi(self, handler):
        lyr = make_layer("MultiLineString")
        params = handler.getDestinationParameters(lyr)
        assert params["isMulti"]

    def test_standard_layer_has_no_m_or_z(self, handler):
        lyr = make_layer("Point")
        params = handler.getDestinationParameters(lyr)
        assert not params["hasMValues"]
        assert not params["hasZValues"]

    def test_polygon_geom_type(self, handler):
        lyr = make_layer("Polygon")
        params = handler.getDestinationParameters(lyr)
        assert params["geomType"] is not None


# ---------------------------------------------------------------------------
# getCoordinateTransformer
# ---------------------------------------------------------------------------
class TestGetCoordinateTransformer:
    def test_same_crs_returns_none(self, handler):
        lyr_a = make_layer("Point", crs="EPSG:4326")
        lyr_b = make_layer("Point", crs="EPSG:4326")
        result = handler.getCoordinateTransformer(lyr_a, lyr_b)
        assert result is None

    def test_different_crs_returns_transformer(self, handler):
        lyr_a = make_layer("Point", crs="EPSG:4326")
        lyr_b = make_layer("Point", crs="EPSG:31983")
        result = handler.getCoordinateTransformer(lyr_a, lyr_b)
        assert result is not None


# ---------------------------------------------------------------------------
# createUnifiedVectorLayer
# ---------------------------------------------------------------------------
class TestCreateUnifiedVectorLayer:
    def test_creates_valid_layer(self, handler):
        lyr = handler.createUnifiedVectorLayer(QgsWkbTypes.Point, 4326)
        assert lyr.isValid()

    def test_has_featid_and_layer_fields(self, handler):
        lyr = handler.createUnifiedVectorLayer(QgsWkbTypes.Point, 4326)
        field_names = [f.name() for f in lyr.fields()]
        assert "featid" in field_names
        assert "layer" in field_names

    def test_with_attribute_tuple_has_extra_fields(self, handler):
        lyr = handler.createUnifiedVectorLayer(
            QgsWkbTypes.Point, 4326, attributeTupple=True
        )
        field_names = [f.name() for f in lyr.fields()]
        assert "tupple" in field_names
        assert "blacklist" in field_names

    def test_line_layer_type(self, handler):
        lyr = handler.createUnifiedVectorLayer(QgsWkbTypes.LineString, 4326)
        assert lyr.geometryType() == QgsWkbTypes.GeometryType.LineGeometry


# ---------------------------------------------------------------------------
# getUnifiedVectorFields
# ---------------------------------------------------------------------------
class TestGetUnifiedVectorFields:
    def test_without_tupple_returns_two_fields(self, handler):
        fields = handler.getUnifiedVectorFields(attributeTupple=False)
        names = [f.name() for f in fields]
        assert names == ["featid", "layer"]

    def test_with_tupple_returns_four_fields(self, handler):
        fields = handler.getUnifiedVectorFields(attributeTupple=True)
        names = [f.name() for f in fields]
        assert names == ["featid", "layer", "tupple", "blacklist"]


# ---------------------------------------------------------------------------
# buildInitialAndEndPointDict
# ---------------------------------------------------------------------------
class TestBuildInitialAndEndPointDict:
    def test_single_line_creates_two_entries(self, handler):
        lyr = make_layer("LineString")
        add_features(lyr, ["LINESTRING(0 0, 1 1, 2 2)"])
        result = handler.buildInitialAndEndPointDict(lyr)
        assert len(result) == 2

    def test_two_connected_lines_share_a_node(self, handler):
        lyr = make_layer("LineString")
        add_features(lyr, ["LINESTRING(0 0, 1 1)", "LINESTRING(1 1, 2 2)"])
        result = handler.buildInitialAndEndPointDict(lyr)
        shared = QgsPointXY(1.0, 1.0)
        assert shared in result
        assert len(result[shared]) == 2

    def test_empty_layer_returns_empty_dict(self, handler):
        lyr = make_layer("LineString")
        result = handler.buildInitialAndEndPointDict(
            lyr, recordStepProgress=False
        )
        assert result == {}


# ---------------------------------------------------------------------------
# addFeatToDict / addPointToDict
# ---------------------------------------------------------------------------
class TestAddToDict:
    def test_add_point_to_empty_dict(self, handler):
        d = {}
        pt = QgsPointXY(1.0, 2.0)
        handler.addPointToDict(pt, d, item=99)
        assert pt in d
        assert 99 in d[pt]

    def test_add_point_accumulates_items(self, handler):
        d = {}
        pt = QgsPointXY(1.0, 2.0)
        handler.addPointToDict(pt, d, item=1)
        handler.addPointToDict(pt, d, item=2)
        assert len(d[pt]) == 2

    def test_add_feat_to_dict_adds_both_endpoints(self, handler):
        d = {}
        line = [QgsPointXY(0, 0), QgsPointXY(1, 1), QgsPointXY(2, 2)]
        handler.addFeatToDict(endVerticesDict=d, line=line, item=42)
        assert QgsPointXY(0, 0) in d
        assert QgsPointXY(2, 2) in d


# ---------------------------------------------------------------------------
# searchDuplicatedFeatures
# ---------------------------------------------------------------------------
class TestSearchDuplicatedFeatures:
    def _make_feat_dict(self, wkt, feat_id):
        geom = QgsGeometry.fromWkt(wkt)
        feat = QgsFeature()
        feat.setGeometry(geom)
        return {"geom": geom, "feat": feat, "attrKey": ""}

    def test_identical_geometries_are_duplicates(self, handler):
        wkt = "POINT(1 1)"
        feat_list = [self._make_feat_dict(wkt, i) for i in range(2)]
        result = handler.searchDuplicatedFeatures(feat_list, columns=[])
        assert len(result) > 0

    def test_different_geometries_not_duplicates(self, handler):
        feat_list = [
            self._make_feat_dict("POINT(0 0)", 1),
            self._make_feat_dict("POINT(1 1)", 2),
        ]
        result = handler.searchDuplicatedFeatures(feat_list, columns=[])
        assert len(result) == 0

    def test_empty_list_returns_empty(self, handler):
        result = handler.searchDuplicatedFeatures([], columns=[])
        assert result == {}
