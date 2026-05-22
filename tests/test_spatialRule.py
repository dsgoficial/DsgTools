# -*- coding: utf-8 -*-
"""
Tests for SpatialRule (DsgTools/core/GeometricTools/spatialRelationsHandler.py).

SpatialRule is a pure-Python wrapper that validates and stores spatial rule
attributes. These tests exercise its validation and property-setting logic
with no database or canvas dependency.
"""
import pytest
pytestmark = pytest.mark.unit


from DsgTools.core.GeometricTools.spatialRelationsHandler import SpatialRule


@pytest.fixture
def rule():
    return SpatialRule(checkLoadedLayer=False)


# ---------------------------------------------------------------------------
# Rule name
# ---------------------------------------------------------------------------
class TestRuleName:
    def test_validate_valid_name(self, rule):
        assert rule.validateRuleName("my rule")

    def test_validate_empty_string_is_invalid(self, rule):
        assert not rule.validateRuleName("")

    def test_validate_non_string_is_invalid(self, rule):
        assert not rule.validateRuleName(123)
        assert not rule.validateRuleName(None)

    def test_set_valid_name(self, rule):
        assert rule.setRuleName("flood")
        assert rule.ruleName() == "flood"

    def test_set_invalid_name_does_not_update(self, rule):
        rule.setRuleName("original")
        rule.setRuleName("")
        assert rule.ruleName() == "original"

    def test_rule_name_is_valid_after_set(self, rule):
        rule.setRuleName("valid")
        assert rule.ruleNameIsValid()

    def test_rule_name_invalid_before_set(self, rule):
        assert not rule.ruleNameIsValid()


# ---------------------------------------------------------------------------
# Layer names
# ---------------------------------------------------------------------------
class TestLayerNames:
    def test_validate_non_empty_string(self, rule):
        assert rule.validateLayerName("some_layer", checkLoaded=False)

    def test_validate_empty_string_is_invalid(self, rule):
        assert not rule.validateLayerName("", checkLoaded=False)

    def test_set_layer_a_valid(self, rule):
        assert rule.setLayerA("roads", checkLoaded=False)
        assert rule.layerA() == "roads"

    def test_set_layer_a_empty_does_not_update(self, rule):
        rule.setLayerA("original", checkLoaded=False)
        rule.setLayerA("", checkLoaded=False)
        assert rule.layerA() == "original"

    def test_layer_a_valid_after_set(self, rule):
        rule.setLayerA("rivers", checkLoaded=False)
        assert rule.layerAIsValid(checkLoaded=False)

    def test_layer_b_independent_from_a(self, rule):
        rule.setLayerA("layer_a", checkLoaded=False)
        rule.setLayerB("layer_b", checkLoaded=False)
        assert rule.layerA() == "layer_a"
        assert rule.layerB() == "layer_b"

    def test_layer_b_starts_empty(self, rule):
        assert rule.layerB() == ""


# ---------------------------------------------------------------------------
# Filter expressions
# ---------------------------------------------------------------------------
class TestFilterExpressions:
    def test_empty_filter_is_valid(self, rule):
        assert rule.validateFilterExpression("")

    def test_valid_qgis_expression(self, rule):
        assert rule.validateFilterExpression('"field" = 1')

    def test_invalid_expression_is_rejected(self, rule):
        assert not rule.validateFilterExpression("(((unclosed")

    def test_set_filter_a_valid(self, rule):
        assert rule.setFilterA("")
        assert rule.filterA() == ""

    def test_set_filter_a_valid_expression(self, rule):
        assert rule.setFilterA('"type" = 1')
        assert rule.filterA() == '"type" = 1'

    def test_set_filter_a_invalid_does_not_update(self, rule):
        rule.setFilterA('"type" = 1')
        rule.setFilterA("(((")
        assert rule.filterA() == '"type" = 1'

    def test_filter_a_and_b_independent(self, rule):
        rule.setFilterA('"a" = 1')
        rule.setFilterB('"b" = 2')
        assert rule.filterA() == '"a" = 1'
        assert rule.filterB() == '"b" = 2'


# ---------------------------------------------------------------------------
# DE-9IM usage flag
# ---------------------------------------------------------------------------
class TestDE9IM:
    def test_default_use_de9im_is_false(self, rule):
        assert not rule.useDE9IM()

    def test_set_use_de9im_true(self, rule):
        rule.setUseDE9IM(True)
        assert rule.useDE9IM()

    def test_set_use_de9im_false(self, rule):
        rule.setUseDE9IM(True)
        rule.setUseDE9IM(False)
        assert not rule.useDE9IM()

    def test_non_bool_is_rejected(self, rule):
        result = rule.setUseDE9IM("yes")
        assert not result
        assert not rule.useDE9IM()


# ---------------------------------------------------------------------------
# Cardinality
# ---------------------------------------------------------------------------
class TestCardinality:
    def test_validate_standard_cardinality(self, rule):
        # cardinality follows pattern "min..max"
        assert rule.validateCardinality("1..1")

    def test_cardinality_starts_empty(self, rule):
        assert rule.cardinality() == ""

    def test_set_valid_cardinality(self, rule):
        rule.setCardinality("1..1")
        assert rule.cardinality() == "1..1"


# ---------------------------------------------------------------------------
# asDict / validate / isValid
# ---------------------------------------------------------------------------
class TestAsDictAndIsValid:
    def test_as_dict_returns_dict(self, rule):
        assert isinstance(rule.asDict(), dict)

    def test_fully_configured_rule_is_valid(self, rule):
        from DsgTools.core.GeometricTools.spatialRelationsHandler import (
            SpatialRelationsHandler,
        )
        predicates = SpatialRelationsHandler().availablePredicates()
        rule.setRuleName("test_rule")
        rule.setLayerA("layer_a", checkLoaded=False)
        rule.setLayerB("layer_b", checkLoaded=False)
        rule.setFilterA("")
        rule.setFilterB("")
        rule.setPredicateEnum(next(iter(predicates)))
        rule.setCardinality("1..1")
        assert rule.isValid()

    def test_rule_without_name_is_invalid(self, rule):
        rule.setLayerA("a", checkLoaded=False)
        rule.setLayerB("b", checkLoaded=False)
        assert not rule.ruleNameIsValid()

    def test_rule_without_layers_is_invalid(self, rule):
        rule.setRuleName("incomplete")
        assert not rule.layerAIsValid()
        assert not rule.layerBIsValid()


# ---------------------------------------------------------------------------
# Constructor keyword shortcuts
# ---------------------------------------------------------------------------
class TestConstructorShortcuts:
    def test_name_set_via_constructor(self):
        rule = SpatialRule(name="my_rule", checkLoadedLayer=False)
        assert rule.ruleName() == "my_rule"

    def test_layer_a_set_via_constructor(self):
        rule = SpatialRule(layer_a="roads", checkLoadedLayer=False)
        assert rule.layerA() == "roads"

    def test_filter_a_set_via_constructor(self):
        rule = SpatialRule(filter_a='"x" = 1', checkLoadedLayer=False)
        assert rule.filterA() == '"x" = 1'

    def test_use_de9im_set_via_constructor(self):
        rule = SpatialRule(useDE9IM=True, checkLoadedLayer=False)
        assert rule.useDE9IM()
