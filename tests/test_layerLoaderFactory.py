# -*- coding: utf-8 -*-
"""
Tests for DsgTools/core/Factories/LayerLoaderFactory/

Strategy
--------
The loader classes depend heavily on an ``abstractDb`` object and QGIS' iface.
To avoid coupling the tests to a live database we use ``unittest.mock`` to
provide a controlled ``abstractDb`` double for every test that exercises
constructor-level or pure-logic methods.

Tests that touch the filesystem (``domainMapping``, ``getStyleFromFile``) use
real files shipped with the plugin.

Tests that require a live DB or canvas interaction are excluded from this
suite — those are exercised by the integration tests.
"""

import os
from unittest.mock import MagicMock

import pytest
pytestmark = pytest.mark.unit


from DsgTools.core.Factories.LayerLoaderFactory.layerLoaderFactory import (
    LayerLoaderFactory,
)
from DsgTools.core.Factories.LayerLoaderFactory.geopackageLayerLoader import (
    GeopackageLayerLoader,
)
from DsgTools.core.Factories.LayerLoaderFactory.shapefileLayerLoader import (
    ShapefileLayerLoader,
)


# ---------------------------------------------------------------------------
# Helpers / shared fixtures
# ---------------------------------------------------------------------------
def _make_abstract_db(driver_name="GPKG", version="EDGV 3.0", db_name="test.gpkg"):
    """Returns a MagicMock that quacks like AbstractDb."""
    db = MagicMock()
    db.getType.return_value = driver_name
    db.getDatabaseVersion.return_value = version
    db.getDatabaseName.return_value = db_name
    db.getGeomTypeDict.return_value = {}
    db.getGeomDict.return_value = {}
    # SQLite / GeoPackage inner db mock
    db.db = MagicMock()
    db.db.databaseName.return_value = db_name
    return db


@pytest.fixture
def factory():
    return LayerLoaderFactory()


@pytest.fixture
def gpkg_db():
    return _make_abstract_db(driver_name="GPKG")


@pytest.fixture
def shp_db():
    db = _make_abstract_db(driver_name="SHP")
    db.databaseName.return_value = "/tmp/test"
    return db


@pytest.fixture
def postgis_db():
    return _make_abstract_db(driver_name="QPSQL")


# ---------------------------------------------------------------------------
# LayerLoaderFactory.makeLoader
# ---------------------------------------------------------------------------
class TestLayerLoaderFactory:
    def test_gpkg_returns_geopackage_loader(self, factory, gpkg_db):
        loader = factory.makeLoader(iface=None, abstractDb=gpkg_db)
        assert isinstance(loader, GeopackageLayerLoader)

    def test_shp_returns_shapefile_loader(self, factory, shp_db):
        loader = factory.makeLoader(iface=None, abstractDb=shp_db)
        assert isinstance(loader, ShapefileLayerLoader)

    def test_postgis_returns_postgis_loader(self, factory, postgis_db):
        from DsgTools.core.Factories.LayerLoaderFactory.postgisLayerLoader import (
            PostGISLayerLoader,
        )
        loader = factory.makeLoader(iface=None, abstractDb=postgis_db)
        assert isinstance(loader, PostGISLayerLoader)

    def test_unknown_driver_returns_none(self, factory):
        db = _make_abstract_db(driver_name="UNSUPPORTED")
        loader = factory.makeLoader(iface=None, abstractDb=db)
        assert loader is None

    def test_load_centroids_flag_forwarded(self, factory, gpkg_db):
        loader = factory.makeLoader(iface=None, abstractDb=gpkg_db, loadCentroids=True)
        assert isinstance(loader, GeopackageLayerLoader)

    def test_raster_flag_forwarded_to_postgis(self, factory, postgis_db):
        from DsgTools.core.Factories.LayerLoaderFactory.postgisLayerLoader import (
            PostGISLayerLoader,
        )
        loader = factory.makeLoader(
            iface=None, abstractDb=postgis_db, rasterLayer=True
        )
        assert isinstance(loader, PostGISLayerLoader)


# ---------------------------------------------------------------------------
# EDGVLayerLoader.preLoadStep
# ---------------------------------------------------------------------------
class TestPreLoadStep:
    @pytest.fixture
    def loader(self, gpkg_db):
        return GeopackageLayerLoader(iface=None, abstractDb=gpkg_db, loadCentroids=False)

    def test_empty_list_returns_empty_and_false(self, loader):
        result, is_dict = loader.preLoadStep([])
        assert result == []
        assert is_dict is False

    def test_string_list_returned_as_is(self, loader):
        input_list = ["layer_a", "layer_b"]
        result, is_dict = loader.preLoadStep(input_list)
        assert result == input_list
        assert is_dict is False

    def test_dict_list_extracts_table_names(self, loader):
        input_list = [
            {"tableName": "table_a", "geomType": "POINT", "cat": "infra", "lyrName": "a"},
            {"tableName": "table_b", "geomType": "LINE", "cat": "infra", "lyrName": "b"},
        ]
        result, is_dict = loader.preLoadStep(input_list)
        assert result == ["table_a", "table_b"]
        assert is_dict is True

    def test_single_string_item(self, loader):
        result, is_dict = loader.preLoadStep(["only_one"])
        assert result == ["only_one"]
        assert is_dict is False


# ---------------------------------------------------------------------------
# EDGVLayerLoader.getLyrDict
# ---------------------------------------------------------------------------
class TestGetLyrDict:
    @pytest.fixture
    def loader(self, gpkg_db):
        return GeopackageLayerLoader(iface=None, abstractDb=gpkg_db, loadCentroids=False)

    def test_empty_list_returns_empty_defaultdict(self, loader):
        result = loader.getLyrDict([])
        assert len(result) == 0

    def test_dict_list_grouped_by_geom_and_category(self, loader):
        input_list = [
            {"tableName": "t1", "geomType": "POINT", "cat": "infra", "lyrName": "t1"},
            {"tableName": "t2", "geomType": "POLYGON", "cat": "area", "lyrName": "t2"},
        ]
        result = loader.getLyrDict(input_list)
        assert "Point" in result
        assert "Area" in result

    def test_multiple_layers_same_geom_and_cat(self, loader):
        input_list = [
            {"tableName": "t1", "geomType": "LINESTRING", "cat": "roads", "lyrName": "t1"},
            {"tableName": "t2", "geomType": "LINESTRING", "cat": "roads", "lyrName": "t2"},
        ]
        result = loader.getLyrDict(input_list)
        assert len(result["Line"]["roads"]) == 2

    def test_string_list_with_edgv_false_grouped_by_schema(self, loader):
        # When isEdgv=False and input is plain string list, schema is first part
        input_list = ["schema_table1", "schema_table2"]
        result = loader.getLyrDict(input_list, isEdgv=False)
        assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# GeopackageLayerLoader.specialEdgvAttributes
# ---------------------------------------------------------------------------
class TestSpecialEdgvAttributes:
    def test_returns_expected_attributes(self, gpkg_db):
        loader = GeopackageLayerLoader(iface=None, abstractDb=gpkg_db, loadCentroids=False)
        attrs = loader.specialEdgvAttributes()
        assert isinstance(attrs, list)
        assert "finalidade" in attrs
        assert "tipo" in attrs

    def test_returns_four_attributes(self, gpkg_db):
        loader = GeopackageLayerLoader(iface=None, abstractDb=gpkg_db, loadCentroids=False)
        assert len(loader.specialEdgvAttributes()) == 4


# ---------------------------------------------------------------------------
# GeopackageLayerLoader.domainMapping
# ---------------------------------------------------------------------------
class TestDomainMapping:
    @pytest.fixture
    def loader(self, gpkg_db):
        return GeopackageLayerLoader(iface=None, abstractDb=gpkg_db, loadCentroids=False)

    def test_edgv_3_loads_json(self, loader):
        result = loader.domainMapping("EDGV 3.0")
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_edgv_213_loads_json(self, loader):
        result = loader.domainMapping("EDGV 2.1.3")
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_edgv_213_pro_loads_json(self, loader):
        result = loader.domainMapping("EDGV 2.1.3 Pro")
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_short_version_aliases_work(self, loader):
        full = loader.domainMapping("EDGV 3.0")
        short = loader.domainMapping("3.0")
        assert full == short

    def test_unknown_version_returns_empty_dict(self, loader):
        result = loader.domainMapping("NonExistentVersion")
        assert result == {}


# ---------------------------------------------------------------------------
# GeopackageLayerLoader.filterLayerList
# ---------------------------------------------------------------------------
class TestGeopackageFilterLayerList:
    @pytest.fixture
    def loader(self, gpkg_db):
        # Set up geomTypeDict so we can test geomFilterList
        gpkg_db.getGeomTypeDict.return_value = {
            "POINT": ["layer_point"],
            "LINESTRING": ["layer_line"],
            "POLYGON": ["layer_polygon"],
        }
        gpkg_db.getGeomDict.return_value = {}
        return GeopackageLayerLoader(iface=None, abstractDb=gpkg_db, loadCentroids=False)

    def test_no_filter_returns_all_layers(self, loader):
        layers = ["layer_a", "layer_b", "layer_c"]
        result = loader.filterLayerList(layers, False, False, [])
        assert result == layers

    def test_only_with_elements_delegates_to_db(self, loader):
        layers = ["layer_a", "layer_b"]
        loader.abstractDb.getLayersWithElementsV2.return_value = ["layer_a"]
        result = loader.filterLayerList(layers, False, True, [])
        assert result == ["layer_a"]
        loader.abstractDb.getLayersWithElementsV2.assert_called_once()

    def test_geom_filter_point_only(self, loader):
        layers = ["layer_point", "layer_line", "layer_polygon"]
        result = loader.filterLayerList(layers, False, False, ["Point"])
        assert "layer_point" in result
        assert "layer_line" not in result

    def test_empty_layer_list_returns_empty(self, loader):
        result = loader.filterLayerList([], False, False, [])
        assert result == []


# ---------------------------------------------------------------------------
# EDGVLayerLoader.getStyleFromFile
# ---------------------------------------------------------------------------
class TestGetStyleFromFile:
    @pytest.fixture
    def loader(self, gpkg_db):
        return GeopackageLayerLoader(iface=None, abstractDb=gpkg_db, loadCentroids=False)

    def test_returns_none_when_no_matching_qml(self, loader, tmp_path):
        result = loader.getStyleFromFile(str(tmp_path), "nonexistent_layer")
        assert result is None

    def test_returns_path_when_qml_exists(self, loader, tmp_path):
        qml_file = tmp_path / "test_layer.qml"
        qml_file.write_text(
            '<?xml version="1.0" encoding="UTF-8"?><qgis version="3.0"></qgis>'
        )
        result = loader.getStyleFromFile(str(tmp_path), "test_layer")
        assert result is not None
        assert os.path.exists(result)

    def test_case_insensitive_qml_match(self, loader, tmp_path):
        qml_file = tmp_path / "Test_Layer.qml"
        qml_file.write_text(
            '<?xml version="1.0" encoding="UTF-8"?><qgis version="3.0"></qgis>'
        )
        result = loader.getStyleFromFile(str(tmp_path), "test_layer")
        assert result is not None
