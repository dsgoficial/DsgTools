# -*- coding: utf-8 -*-
import sys
import pytest
from unittest.mock import MagicMock, patch
from qgis.testing import unittest
from qgis.PyQt.QtCore import Qt

try:
    from DsgTools.gui.LayerTools.LoadLayersFromServer.loadLayersFromServer import (
        LoadLayersFromServer,
    )
    from DsgTools.gui.CustomWidgets.ConnectionWidgets.ServerConnectionWidgets.customServerConnectionWidget import (
        CustomServerConnectionWidget,
    )
except ImportError:
    pytest.skip(
        "LoadLayersFromServer module not found", allow_module_level=True
    )

_PROGRESS = "DsgTools.gui.LayerTools.LoadLayersFromServer.loadLayersFromServer.ProgressWidget"
_MSGBOX = "DsgTools.gui.LayerTools.LoadLayersFromServer.loadLayersFromServer.QMessageBox"


def _make_db(geom_list):
    db = MagicMock()
    db.getGeomColumnTupleList.return_value = geom_list
    return db


def _make_geom(schema, table, geom="geom", geom_type="MULTIPOLYGON", table_type="TABLE"):
    return (schema, table, geom, geom_type, table_type)


class CustomServerConnectionWidgetTester(unittest.TestCase):
    """Pure-logic tests for CustomServerConnectionWidget helper methods."""

    def setUp(self):
        self.widget = CustomServerConnectionWidget()

    def tearDown(self):
        self.widget.close()

    def test_getDisplayString_edgv213_with_impl(self):
        result = self.widget.getDisplayString("mydb", "2.1.3", 1)
        self.assertEqual(result, "mydb (EDGV 2.1.3 impl. 1)")

    def test_getDisplayString_edgv213_no_impl(self):
        result = self.widget.getDisplayString("mydb", "2.1.3", -1)
        self.assertEqual(result, "mydb (EDGV 2.1.3)")

    def test_getDisplayString_edgv30_with_impl(self):
        result = self.widget.getDisplayString("mydb", "3.0", 2)
        self.assertEqual(result, "mydb (EDGV 3.0 impl. 2)")

    def test_getDisplayString_edgv30pro_no_impl(self):
        result = self.widget.getDisplayString("mydb", "3.0 Pro", -1)
        self.assertEqual(result, "mydb (EDGV 3.0 Pro)")

    def test_getDisplayString_edgv213pro_with_impl(self):
        result = self.widget.getDisplayString("mydb", "2.1.3 Pro", 3)
        self.assertEqual(result, "mydb (EDGV 2.1.3 Pro impl. 3)")

    def test_getDisplayString_non_edgv_shows_unknown_model(self):
        result = self.widget.getDisplayString("mydb", "Non_EDGV", -1)
        self.assertIn("mydb", result)
        self.assertIn("Unknown model", result)

    def test_getDisplayString_unknown_version_no_prefix(self):
        result = self.widget.getDisplayString("mydb", "FTer_2a_Ed", -1)
        self.assertEqual(result, "mydb (FTer_2a_Ed)")

    def test_getDisplayString_unknown_version_with_impl(self):
        result = self.widget.getDisplayString("mydb", "FTer_2a_Ed", 1)
        self.assertEqual(result, "mydb (FTer_2a_Ed impl. 1)")


class LoadLayersLogicTester(unittest.TestCase):
    """Tests for lyrDict construction and error-logging logic."""

    def setUp(self):
        with patch(_PROGRESS):
            self.dlg = LoadLayersFromServer(MagicMock())

    def tearDown(self):
        self.dlg.close()

    def _inject(self, db_name, geom_list):
        self.dlg.customServerConnectionWidget.selectedDbsDict[db_name] = _make_db(
            geom_list
        )

    def _add(self, db_names):
        with patch(_PROGRESS):
            self.dlg.updateLayersFromDbs("added", db_names)

    def _remove(self, db_names):
        with patch(_PROGRESS):
            self.dlg.updateLayersFromDbs("removed", db_names)

    # --- logInternalError ---

    def test_logInternalError_empty_dict_returns_empty_string(self):
        self.assertEqual(self.dlg.logInternalError({}), "")

    def test_logInternalError_with_errors_includes_db_names(self):
        result = self.dlg.logInternalError({"db1": "err1", "db2": "err2"})
        self.assertIn("db1", result)
        self.assertIn("db2", result)

    def test_logInternalError_with_errors_mentions_log(self):
        result = self.dlg.logInternalError({"db1": "err"})
        self.assertIn("qgis log", result.lower())

    def test_logInternalError_empty_has_no_db_names_in_result(self):
        result = self.dlg.logInternalError({})
        self.assertEqual(result, "")

    # --- updateLayersFromDbs: non-EDGV database ---

    def test_non_edgv_db_uses_tablename_as_lyrname(self):
        self._inject("mydb", [_make_geom("public", "hidrografia_l")])
        self._add(["mydb"])
        self.assertIn("public,hidrografia_l,geom,MULTIPOLYGON,TABLE", self.dlg.lyrDict)

    def test_non_edgv_db_uses_schema_as_cat(self):
        self._inject("mydb", [_make_geom("myschema", "layer_a")])
        self._add(["mydb"])
        key = "myschema,layer_a,geom,MULTIPOLYGON,TABLE"
        entry = self.dlg.lyrDict[key]["mydb"]
        self.assertEqual(entry["cat"], "myschema")
        self.assertEqual(entry["lyrName"], "layer_a")

    # --- updateLayersFromDbs: EDGV database ---

    def test_edgv_db_splits_tablename_into_cat_and_lyrname(self):
        self._inject("mydb_EDGV_3.0", [_make_geom("hid", "hid_hidrografia_l")])
        self._add(["mydb_EDGV_3.0"])
        key = "hid,hidrografia_l,geom,MULTIPOLYGON,TABLE"
        self.assertIn(key, self.dlg.lyrDict)
        entry = self.dlg.lyrDict[key]["mydb_EDGV_3.0"]
        self.assertEqual(entry["cat"], "hid")
        self.assertEqual(entry["lyrName"], "hidrografia_l")

    def test_edgv_tablename_no_underscore_falls_back_to_layers_cat(self):
        # tableName with no underscore: lyrName becomes "" → fallback
        self._inject("mydb_EDGV_3.0", [_make_geom("hid", "hidrografia")])
        self._add(["mydb_EDGV_3.0"])
        self.assertIn("layers,hidrografia,geom,MULTIPOLYGON,TABLE", self.dlg.lyrDict)

    def test_muvd_geometry_suffix_falls_back_to_layers_cat(self):
        # MUVD (non-EDGV keyword): lyrName in ["a","p","l"] AND "EDGV" not in dbName → fallback
        self._inject("mydb_MUVD", [_make_geom("hid", "hid_l", geom_type="MULTILINESTRING")])
        self._add(["mydb_MUVD"])
        self.assertIn(
            "layers,hid_l,geom,MULTILINESTRING,TABLE", self.dlg.lyrDict
        )

    def test_edgv_geometry_suffix_does_not_fall_back(self):
        # For EDGV db: lyrName = "l", but "EDGV" IS in dbName → no fallback
        self._inject("mydb_EDGV_3.0", [_make_geom("hid", "hid_l", geom_type="MULTILINESTRING")])
        self._add(["mydb_EDGV_3.0"])
        self.assertIn("hid,l,geom,MULTILINESTRING,TABLE", self.dlg.lyrDict)

    def test_mgcp_db_parses_like_edgv(self):
        self._inject("mydb_MGCP", [_make_geom("veg", "veg_vegetacao_a")])
        self._add(["mydb_MGCP"])
        self.assertIn("veg,vegetacao_a,geom,MULTIPOLYGON,TABLE", self.dlg.lyrDict)

    # --- Multiple DBs ---

    def test_multiple_dbs_share_the_same_key(self):
        geom = [_make_geom("hid", "hid_hidrografia_l")]
        self._inject("db1_EDGV_3.0", geom)
        self._inject("db2_EDGV_3.0", geom)
        self._add(["db1_EDGV_3.0", "db2_EDGV_3.0"])
        key = "hid,hidrografia_l,geom,MULTIPOLYGON,TABLE"
        self.assertIn("db1_EDGV_3.0", self.dlg.lyrDict[key])
        self.assertIn("db2_EDGV_3.0", self.dlg.lyrDict[key])

    def test_lyrdict_stores_full_metadata_per_db(self):
        self._inject("mydb", [_make_geom("public", "hidrografia_l", "wkb_geometry", "POINT", "VIEW")])
        self._add(["mydb"])
        key = "public,hidrografia_l,wkb_geometry,POINT,VIEW"
        entry = self.dlg.lyrDict[key]["mydb"]
        self.assertEqual(entry["tableSchema"], "public")
        self.assertEqual(entry["tableName"], "hidrografia_l")
        self.assertEqual(entry["geom"], "wkb_geometry")
        self.assertEqual(entry["geomType"], "POINT")
        self.assertEqual(entry["tableType"], "VIEW")

    # --- Remove ---

    def test_remove_one_db_preserves_other_db_in_same_key(self):
        geom = [_make_geom("hid", "hid_hidrografia_l")]
        self._inject("db1_EDGV_3.0", geom)
        self._inject("db2_EDGV_3.0", geom)
        self._add(["db1_EDGV_3.0", "db2_EDGV_3.0"])
        self._remove(["db1_EDGV_3.0"])
        key = "hid,hidrografia_l,geom,MULTIPOLYGON,TABLE"
        self.assertNotIn("db1_EDGV_3.0", self.dlg.lyrDict[key])
        self.assertIn("db2_EDGV_3.0", self.dlg.lyrDict[key])

    def test_remove_last_db_deletes_key_from_lyrdict(self):
        self._inject("db1_EDGV_3.0", [_make_geom("hid", "hid_hidrografia_l")])
        self._add(["db1_EDGV_3.0"])
        self._remove(["db1_EDGV_3.0"])
        self.assertNotIn(
            "hid,hidrografia_l,geom,MULTIPOLYGON,TABLE", self.dlg.lyrDict
        )

    def test_remove_db_not_in_dict_is_harmless(self):
        self._inject("db1_EDGV_3.0", [_make_geom("hid", "hid_hidrografia_l")])
        self._add(["db1_EDGV_3.0"])
        # remove a db that was never added — should not raise
        self._remove(["db_nonexistent"])
        self.assertIn(
            "hid,hidrografia_l,geom,MULTIPOLYGON,TABLE", self.dlg.lyrDict
        )

    # --- updateLayersFromDbs populates the selector widget ---

    def test_add_populates_layers_selector(self):
        self._inject("mydb", [_make_geom("public", "layer_a")])
        self._add(["mydb"])
        # fromLs has the item (it wasn't moved to toTree yet)
        self.assertEqual(len(self.dlg.layersCustomSelector.fromLs), 1)

    def test_remove_all_clears_layers_selector(self):
        self._inject("mydb", [_make_geom("public", "layer_a")])
        self._add(["mydb"])
        self._remove(["mydb"])
        self.assertEqual(len(self.dlg.layersCustomSelector.fromLs), 0)

    # --- resetInterface ---

    def test_resetInterface_unchecks_only_with_elements(self):
        self.dlg.checkBoxOnlyWithElements.setCheckState(Qt.CheckState.Checked)
        self.dlg.resetInterface()
        self.assertEqual(
            self.dlg.checkBoxOnlyWithElements.checkState(), Qt.CheckState.Unchecked
        )

    def test_resetInterface_clears_filter_in_selector(self):
        self.dlg.layersCustomSelector.filterLineEdit.setText("something")
        self.dlg.resetInterface()
        self.assertEqual(self.dlg.layersCustomSelector.filterLineEdit.text(), "")

    def test_resetInterface_does_not_affect_unique_load_checkbox(self):
        self.dlg.uniqueLoadCheckBox.setChecked(True)
        self.dlg.resetInterface()
        # uniqueLoadCheckBox is not part of resetInterface — state unchanged
        self.assertTrue(self.dlg.uniqueLoadCheckBox.isChecked())


class LoadLayersDialogTester(unittest.TestCase):
    """Tests for dialog-level signal wiring and UI interaction."""

    def setUp(self):
        with patch(_PROGRESS):
            self.dlg = LoadLayersFromServer(MagicMock())

    def tearDown(self):
        self.dlg.close()

    def test_accepted_with_empty_selection_shows_info_message(self):
        with patch(_MSGBOX) as mock_qmsg:
            self.dlg.on_buttonBox_accepted()
            mock_qmsg.information.assert_called_once()

    def test_accepted_with_empty_selection_does_not_raise(self):
        with patch(_MSGBOX):
            self.dlg.on_buttonBox_accepted()

    def test_resetAll_signal_triggers_resetInterface(self):
        self.dlg.checkBoxOnlyWithElements.setCheckState(Qt.CheckState.Checked)
        self.dlg.customServerConnectionWidget.resetAll.emit()
        self.assertEqual(
            self.dlg.checkBoxOnlyWithElements.checkState(), Qt.CheckState.Unchecked
        )

    def test_dbDictChanged_added_signal_updates_lyrdict(self):
        db_name = "mydb"
        self.dlg.customServerConnectionWidget.selectedDbsDict[db_name] = _make_db(
            [_make_geom("public", "layer_a")]
        )
        with patch(_PROGRESS):
            self.dlg.customServerConnectionWidget.dbDictChanged.emit("added", [db_name])
        self.assertIn("public,layer_a,geom,MULTIPOLYGON,TABLE", self.dlg.lyrDict)

    def test_dbDictChanged_removed_signal_prunes_lyrdict(self):
        db_name = "mydb"
        self.dlg.customServerConnectionWidget.selectedDbsDict[db_name] = _make_db(
            [_make_geom("public", "layer_a")]
        )
        with patch(_PROGRESS):
            self.dlg.customServerConnectionWidget.dbDictChanged.emit("added", [db_name])
        with patch(_PROGRESS):
            self.dlg.customServerConnectionWidget.dbDictChanged.emit("removed", [db_name])
        self.assertNotIn("public,layer_a,geom,MULTIPOLYGON,TABLE", self.dlg.lyrDict)

    def test_tab_change_clears_selector_completely(self):
        # serverConnectionTab.currentChanged → setInitialState(int)
        # Both internal lists and toTreeWidget must be cleared.
        db_name = "mydb"
        self.dlg.customServerConnectionWidget.selectedDbsDict[db_name] = _make_db(
            [_make_geom("public", "layer_a")]
        )
        with patch(_PROGRESS):
            self.dlg.updateLayersFromDbs("added", [db_name])
        self.dlg.layersCustomSelector.pushButtonSelectAll.click()
        self.dlg.customServerConnectionWidget.serverConnectionTab.currentChanged.emit(0)
        self.assertEqual(self.dlg.layersCustomSelector.fromLs, [])
        self.assertEqual(self.dlg.layersCustomSelector.toLs, [])
        self.assertEqual(self.dlg.layersCustomSelector.getSelectedNodes(), [])

    def test_initial_lyrdict_is_empty(self):
        self.assertEqual(self.dlg.lyrDict, {})

    def test_initial_checkbox_state_is_unchecked(self):
        self.assertEqual(
            self.dlg.checkBoxOnlyWithElements.checkState(), Qt.CheckState.Unchecked
        )

    def test_initial_unique_load_is_unchecked(self):
        self.assertFalse(self.dlg.uniqueLoadCheckBox.isChecked())


def run_all(filterString=None):
    filterString = "test_" if filterString is None else filterString
    suite = unittest.TestSuite()
    suite.addTests(
        unittest.makeSuite(CustomServerConnectionWidgetTester, filterString)
    )
    suite.addTests(unittest.makeSuite(LoadLayersLogicTester, filterString))
    suite.addTests(unittest.makeSuite(LoadLayersDialogTester, filterString))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
