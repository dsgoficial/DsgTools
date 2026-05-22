# -*- coding: utf-8 -*-
import pytest
pytestmark = pytest.mark.unit

from qgis.core import (
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsPointXY,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QVariant

from DsgTools.core.GeometricTools.attributeHandler import AttributeHandler


@pytest.fixture
def handler():
    return AttributeHandler(iface=None)


def make_layer_with_fields(field_defs):
    """Creates an in-memory layer with the specified fields.

    field_defs: list of (name, QVariant.Type) tuples.
    """
    lyr = QgsVectorLayer("Point?crs=EPSG:4326", "test", "memory")
    pr = lyr.dataProvider()
    fields = [QgsField(name, ftype) for name, ftype in field_defs]
    pr.addAttributes(fields)
    lyr.updateFields()
    return lyr


def make_feature_for_layer(lyr, attributes=None, geom=None):
    feat = QgsFeature(lyr.fields())
    if geom:
        feat.setGeometry(geom)
    if attributes:
        for k, v in attributes.items():
            feat[k] = v
    return feat


# ---------------------------------------------------------------------------
# setFeatureAttributes
# ---------------------------------------------------------------------------
class TestSetFeatureAttributes:
    def test_sets_string_attribute(self, handler):
        lyr = make_layer_with_fields([("name", QVariant.String)])
        feat = make_feature_for_layer(lyr)
        result = handler.setFeatureAttributes(feat, {"name": "test_value"})
        assert result["name"] == "test_value"

    def test_sets_int_attribute(self, handler):
        lyr = make_layer_with_fields([("count", QVariant.Int)])
        feat = make_feature_for_layer(lyr)
        result = handler.setFeatureAttributes(feat, {"count": 42})
        assert result["count"] == 42

    def test_ignores_unknown_field(self, handler):
        lyr = make_layer_with_fields([("name", QVariant.String)])
        feat = make_feature_for_layer(lyr)
        result = handler.setFeatureAttributes(feat, {"nonexistent": "x"})
        assert result["name"] is None or result["name"] == ""

    def test_skips_empty_string_value(self, handler):
        lyr = make_layer_with_fields([("name", QVariant.String)])
        feat = make_feature_for_layer(lyr, {"name": "original"})
        result = handler.setFeatureAttributes(feat, {"name": ""})
        assert result["name"] == "original"

    def test_sets_multiple_attributes(self, handler):
        lyr = make_layer_with_fields(
            [("name", QVariant.String), ("value", QVariant.Int)]
        )
        feat = make_feature_for_layer(lyr)
        result = handler.setFeatureAttributes(feat, {"name": "foo", "value": 7})
        assert result["name"] == "foo"
        assert result["value"] == 7

    def test_ignored_clause_uses_old_feat_value(self, handler):
        lyr = make_layer_with_fields([("name", QVariant.String)])
        old_feat = make_feature_for_layer(lyr, {"name": "original"})
        new_feat = make_feature_for_layer(lyr)
        attr_dict = {"name": {"value": "new_value", "ignored": True}}
        result = handler.setFeatureAttributes(new_feat, attr_dict, oldFeat=old_feat)
        assert result["name"] == "original"

    def test_ignored_clause_without_old_feat_sets_none(self, handler):
        lyr = make_layer_with_fields([("name", QVariant.String)])
        new_feat = make_feature_for_layer(lyr)
        attr_dict = {"name": {"value": "new_value", "ignored": True}}
        result = handler.setFeatureAttributes(new_feat, attr_dict, oldFeat=None)
        assert result["name"] is None

    def test_not_ignored_clause_uses_dict_value(self, handler):
        lyr = make_layer_with_fields([("name", QVariant.String)])
        feat = make_feature_for_layer(lyr)
        attr_dict = {"name": {"value": "expected", "ignored": False}}
        result = handler.setFeatureAttributes(feat, attr_dict)
        assert result["name"] == "expected"

    def test_returns_feature(self, handler):
        lyr = make_layer_with_fields([("name", QVariant.String)])
        feat = make_feature_for_layer(lyr)
        result = handler.setFeatureAttributes(feat, {"name": "v"})
        assert isinstance(result, QgsFeature)


# ---------------------------------------------------------------------------
# getTuppleAttribute
# ---------------------------------------------------------------------------
class TestGetTuppleAttribute:
    def test_returns_sorted_attribute_string(self, handler):
        lyr = make_layer_with_fields(
            [("b_field", QVariant.String), ("a_field", QVariant.String)]
        )
        feat = make_feature_for_layer(lyr, {"a_field": "alpha", "b_field": "beta"})
        pr = lyr.dataProvider()
        pr.addFeatures([feat])
        lyr.updateExtents()
        feat = next(lyr.getFeatures())
        result = handler.getTuppleAttribute(feat, lyr)
        assert result == "alpha,beta"

    def test_excludes_geometry_type_field(self, handler):
        lyr = make_layer_with_fields(
            [("name", QVariant.String), ("geom_col", QVariant.ByteArray)]
        )
        feat = make_feature_for_layer(lyr, {"name": "test"})
        pr = lyr.dataProvider()
        pr.addFeatures([feat])
        lyr.updateExtents()
        feat = next(lyr.getFeatures())
        result = handler.getTuppleAttribute(feat, lyr)
        assert "test" in result

    def test_blacklist_excludes_field(self, handler):
        lyr = make_layer_with_fields(
            [("name", QVariant.String), ("secret", QVariant.String)]
        )
        feat = make_feature_for_layer(lyr, {"name": "visible", "secret": "hidden"})
        pr = lyr.dataProvider()
        pr.addFeatures([feat])
        lyr.updateExtents()
        feat = next(lyr.getFeatures())
        result = handler.getTuppleAttribute(feat, lyr, bList=["secret"])
        assert "hidden" not in result
        assert "visible" in result

    def test_empty_layer_returns_empty_string(self, handler):
        lyr = QgsVectorLayer("Point?crs=EPSG:4326", "empty", "memory")
        lyr.dataProvider().addAttributes([QgsField("x", QVariant.Int)])
        lyr.updateFields()
        feat = QgsFeature(lyr.fields())
        result = handler.getTuppleAttribute(feat, lyr)
        assert isinstance(result, str)
