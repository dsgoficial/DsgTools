# -*- coding: utf-8 -*-
import pytest
pytestmark = pytest.mark.unit

from qgis.core import (
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsSpatialIndex,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QVariant

from DsgTools.core.GeometricTools.featureHandler import FeatureHandler


@pytest.fixture
def handler():
    return FeatureHandler(iface=None)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def make_layer(geom_type_wkt, fields=None):
    """Creates an in-memory layer, optionally with extra fields."""
    lyr = QgsVectorLayer(f"{geom_type_wkt}?crs=EPSG:4326", "test", "memory")
    if fields:
        pr = lyr.dataProvider()
        pr.addAttributes(fields)
        lyr.updateFields()
    return lyr


def add_features(lyr, wkt_list):
    pr = lyr.dataProvider()
    feats = []
    for wkt in wkt_list:
        feat = QgsFeature(lyr.fields())
        feat.setGeometry(QgsGeometry.fromWkt(wkt))
        feats.append(feat)
    pr.addFeatures(feats)
    lyr.updateExtents()


# ---------------------------------------------------------------------------
# newFeature
# ---------------------------------------------------------------------------
class TestNewFeature:
    def test_returns_qgsfeature(self, handler):
        feat = handler.newFeature()
        assert isinstance(feat, QgsFeature)

    def test_with_geometry(self, handler):
        geom = QgsGeometry.fromWkt("POINT(1 2)")
        feat = handler.newFeature(geom=geom)
        assert not feat.geometry().isEmpty()

    def test_with_fields_and_attributes(self, handler):
        lyr = make_layer("Point", [QgsField("name", QVariant.String)])
        fields = lyr.fields()
        feat = handler.newFeature(fields=fields, attributeMap={"name": "test"})
        assert feat["name"] == "test"

    def test_no_geom_is_empty(self, handler):
        feat = handler.newFeature()
        assert feat.geometry() is None or feat.geometry().isEmpty()

    def test_with_fields_no_attributes(self, handler):
        lyr = make_layer("Point", [QgsField("x", QVariant.Int)])
        fields = lyr.fields()
        feat = handler.newFeature(fields=fields)
        assert isinstance(feat, QgsFeature)


# ---------------------------------------------------------------------------
# createFeatureFromLayer
# ---------------------------------------------------------------------------
class TestCreateFeatureFromLayer:
    def test_creates_feature_with_layer_fields(self, handler):
        lyr = make_layer("Point", [QgsField("id", QVariant.Int)])
        feat = handler.createFeatureFromLayer(lyr)
        assert isinstance(feat, QgsFeature)

    def test_sets_geometry(self, handler):
        lyr = make_layer("Point")
        geom = QgsGeometry.fromWkt("POINT(3 4)")
        feat = handler.createFeatureFromLayer(lyr, geom=geom)
        assert not feat.geometry().isEmpty()

    def test_sets_attributes(self, handler):
        lyr = make_layer("Point", [QgsField("name", QVariant.String)])
        feat = handler.createFeatureFromLayer(lyr, attributes={"name": "hello"})
        assert feat["name"] == "hello"

    def test_uses_provided_fields_over_layer(self, handler):
        lyr = make_layer("Point", [QgsField("a", QVariant.Int)])
        custom_fields = QgsFields()
        custom_fields.append(QgsField("b", QVariant.String))
        feat = handler.createFeatureFromLayer(lyr, fields=custom_fields)
        assert feat.fields().count() == 1
        assert feat.fields().at(0).name() == "b"


# ---------------------------------------------------------------------------
# buildSpatialIndexAndIdDict
# ---------------------------------------------------------------------------
class TestBuildSpatialIndexAndIdDict:
    def test_returns_spatial_index_and_dict(self, handler):
        lyr = make_layer("Point")
        add_features(lyr, ["POINT(0 0)", "POINT(1 1)", "POINT(2 2)"])
        idx, id_dict = handler.buildSpatialIndexAndIdDict(lyr)
        assert isinstance(idx, QgsSpatialIndex)
        assert isinstance(id_dict, dict)

    def test_all_features_in_dict(self, handler):
        lyr = make_layer("Point")
        add_features(lyr, ["POINT(0 0)", "POINT(1 1)", "POINT(2 2)"])
        _, id_dict = handler.buildSpatialIndexAndIdDict(lyr)
        assert len(id_dict) == lyr.featureCount()

    def test_empty_layer_returns_empty_dict(self, handler):
        lyr = make_layer("Point")
        _, id_dict = handler.buildSpatialIndexAndIdDict(lyr)
        assert id_dict == {}

    def test_spatial_index_finds_nearby_feature(self, handler):
        lyr = make_layer("Point")
        add_features(lyr, ["POINT(0 0)", "POINT(10 10)"])
        idx, id_dict = handler.buildSpatialIndexAndIdDict(lyr)
        from qgis.core import QgsRectangle
        results = idx.intersects(QgsRectangle(-1, -1, 1, 1))
        assert len(results) == 1
        assert id_dict[results[0]].geometry().asPoint().x() == pytest.approx(0.0)

    def test_dict_values_are_features(self, handler):
        lyr = make_layer("Point")
        add_features(lyr, ["POINT(5 5)"])
        _, id_dict = handler.buildSpatialIndexAndIdDict(lyr)
        for feat in id_dict.values():
            assert isinstance(feat, QgsFeature)


# ---------------------------------------------------------------------------
# getFeatureOuterShellAndHoles
# ---------------------------------------------------------------------------
class TestGetFeatureOuterShellAndHoles:
    def test_polygon_without_holes(self, handler):
        lyr = make_layer("Polygon")
        add_features(lyr, ["POLYGON((0 0, 4 0, 4 4, 0 4, 0 0))"])
        feat = next(lyr.getFeatures())
        shells, holes = handler.getFeatureOuterShellAndHoles(feat, isMulti=False)
        assert len(shells) == 1
        assert len(holes) == 0

    def test_polygon_with_hole(self, handler):
        lyr = make_layer("Polygon")
        add_features(
            lyr,
            ["POLYGON((0 0, 4 0, 4 4, 0 4, 0 0),(1 1, 2 1, 2 2, 1 2, 1 1))"],
        )
        feat = next(lyr.getFeatures())
        shells, holes = handler.getFeatureOuterShellAndHoles(feat, isMulti=False)
        assert len(shells) == 1
        assert len(holes) == 1

    def test_shells_are_features(self, handler):
        lyr = make_layer("Polygon")
        add_features(lyr, ["POLYGON((0 0, 4 0, 4 4, 0 4, 0 0))"])
        feat = next(lyr.getFeatures())
        shells, _ = handler.getFeatureOuterShellAndHoles(feat, isMulti=False)
        assert all(isinstance(s, QgsFeature) for s in shells)

    def test_holes_are_features(self, handler):
        lyr = make_layer("Polygon")
        add_features(
            lyr,
            ["POLYGON((0 0, 4 0, 4 4, 0 4, 0 0),(1 1, 2 1, 2 2, 1 2, 1 1))"],
        )
        feat = next(lyr.getFeatures())
        _, holes = handler.getFeatureOuterShellAndHoles(feat, isMulti=False)
        assert all(isinstance(h, QgsFeature) for h in holes)

    def test_multipolygon_without_holes(self, handler):
        lyr = make_layer("MultiPolygon")
        add_features(
            lyr,
            ["MULTIPOLYGON(((0 0,1 0,1 1,0 1,0 0)),((2 2,3 2,3 3,2 3,2 2)))"],
        )
        feat = next(lyr.getFeatures())
        shells, holes = handler.getFeatureOuterShellAndHoles(feat, isMulti=True)
        assert len(shells) == 2
        assert len(holes) == 0


# ---------------------------------------------------------------------------
# createFeaturesWithAttributeDict
# ---------------------------------------------------------------------------
class TestCreateFeaturesWithAttributeDict:
    def test_creates_one_feature_per_geometry(self, handler):
        lyr = make_layer("Polygon", [QgsField("type", QVariant.String)])
        geom_list = [
            QgsGeometry.fromWkt("POLYGON((0 0,1 0,1 1,0 1,0 0))"),
            QgsGeometry.fromWkt("POLYGON((2 2,3 2,3 3,2 3,2 2))"),
        ]
        original = QgsFeature(lyr.fields())
        attr_dict = {"type": "area"}
        result = handler.createFeaturesWithAttributeDict(
            geom_list, original, attr_dict, lyr
        )
        assert len(result) == 2

    def test_features_have_correct_attributes(self, handler):
        lyr = make_layer("Point", [QgsField("label", QVariant.String)])
        geom_list = [QgsGeometry.fromWkt("POINT(0 0)")]
        original = QgsFeature(lyr.fields())
        result = handler.createFeaturesWithAttributeDict(
            geom_list, original, {"label": "test"}, lyr
        )
        assert result[0]["label"] == "test"

    def test_features_have_geometries(self, handler):
        lyr = make_layer("Point")
        geom = QgsGeometry.fromWkt("POINT(5 5)")
        original = QgsFeature(lyr.fields())
        result = handler.createFeaturesWithAttributeDict([geom], original, {}, lyr)
        assert not result[0].geometry().isEmpty()
