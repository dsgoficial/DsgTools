# -*- coding: utf-8 -*-
import sys
import pytest
from qgis.testing import unittest
from qgis.PyQt.QtTest import QTest

try:
    from DsgTools.gui.CustomWidgets.SelectionWidgets.customTableSelector import (
        CustomTableSelector,
    )
except ImportError:
    pytest.skip(
        "customTableSelector module not found", allow_module_level=True
    )

HEADERS = [
    "Category",
    "Layer Name",
    "Geometry\nColumn",
    "Geometry\nType",
    "Layer\nType",
]


def make_item(cat, name, geom="geom", geom_type="MULTIPOLYGON", table_type="TABLE"):
    return {
        "Category": cat,
        "Layer Name": name,
        "Geometry\nColumn": geom,
        "Geometry\nType": geom_type,
        "Layer\nType": table_type,
    }


def _visible_leaf_count(tree_widget):
    root = tree_widget.invisibleRootItem()
    return sum(root.child(i).childCount() for i in range(root.childCount()))


class CustomTableSelectorTester(unittest.TestCase):
    def setUp(self):
        self.sel = CustomTableSelector()
        self.sel.setHeaders(HEADERS)
        self.sel.setFilterColumn([0, 1])

    def tearDown(self):
        self.sel.close()

    # --- Configuration ---

    def test_setTitle_updates_groupbox(self):
        self.sel.setTitle("My Layers")
        self.assertEqual(self.sel.groupBox.title(), "My Layers")

    def test_setHeaders_labels_both_trees(self):
        from_header = self.sel.fromTreeWidget.headerItem()
        to_header = self.sel.toTreeWidget.headerItem()
        for i, label in enumerate(HEADERS):
            self.assertEqual(from_header.text(i), label)
            self.assertEqual(to_header.text(i), label)

    def test_setFilterColumn_list(self):
        self.sel.setFilterColumn([0, 2])
        self.assertEqual(self.sel.filterColumnKeyList, [0, 2])

    def test_setFilterColumn_int(self):
        self.sel.setFilterColumn(1)
        self.assertEqual(self.sel.filterColumnKeyList, [1])

    # --- Initial state ---

    def test_setInitialState_populates_fromLs(self):
        items = [make_item("cat1", "layer1"), make_item("cat2", "layer2")]
        self.sel.setInitialState(items, unique=True)
        self.assertEqual(len(self.sel.fromLs), 2)

    def test_setInitialState_unique_deduplicates(self):
        item = make_item("cat1", "layer1")
        self.sel.setInitialState([item, item], unique=True)
        self.assertEqual(len(self.sel.fromLs), 1)

    def test_setInitialState_non_unique_allows_duplicates(self):
        item = make_item("cat1", "layer1")
        self.sel.setInitialState([item, item], unique=False)
        self.assertEqual(len(self.sel.fromLs), 2)

    def test_setInitialState_empty_list_clears_state(self):
        self.sel.setInitialState([make_item("cat1", "layer1")], unique=True)
        self.sel.setInitialState([], unique=True)
        self.assertEqual(len(self.sel.fromLs), 0)

    def test_items_grouped_by_first_column(self):
        items = [
            make_item("cat1", "layer1"),
            make_item("cat1", "layer2"),
            make_item("cat2", "layer3"),
        ]
        self.sel.setInitialState(items, unique=True)
        root = self.sel.fromTreeWidget.invisibleRootItem()
        self.assertEqual(root.childCount(), 2)

    def test_same_category_items_under_one_parent(self):
        items = [make_item("cat1", "layer1"), make_item("cat1", "layer2")]
        self.sel.setInitialState(items, unique=True)
        root = self.sel.fromTreeWidget.invisibleRootItem()
        self.assertEqual(root.childCount(), 1)
        self.assertEqual(root.child(0).childCount(), 2)

    # --- getSelectedNodes ---

    def test_getSelectedNodes_empty_when_nothing_moved(self):
        self.sel.setInitialState([make_item("cat1", "layer1")], unique=True)
        self.assertEqual(self.sel.getSelectedNodes(), [])

    def test_getSelectedNodes_concatenated_format(self):
        item = make_item("cat1", "layer1", "geom", "MULTIPOLYGON", "TABLE")
        self.sel.setInitialState([item], unique=True)
        self.sel.pushButtonSelectAll.click()
        selected = self.sel.getSelectedNodes()
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0], "cat1,layer1,geom,MULTIPOLYGON,TABLE")

    # --- Select / deselect buttons ---

    def test_select_all_moves_all_items_to_to_tree(self):
        items = [make_item("cat1", "layer1"), make_item("cat1", "layer2")]
        self.sel.setInitialState(items, unique=True)
        self.sel.pushButtonSelectAll.click()
        self.assertEqual(len(self.sel.getSelectedNodes()), 2)
        self.assertEqual(len(self.sel.fromLs), 0)

    def test_deselect_all_moves_all_items_back(self):
        items = [make_item("cat1", "layer1"), make_item("cat1", "layer2")]
        self.sel.setInitialState(items, unique=True)
        self.sel.pushButtonSelectAll.click()
        self.sel.pushButtonDeselectAll.click()
        self.assertEqual(len(self.sel.getSelectedNodes()), 0)
        self.assertEqual(len(self.sel.toLs), 0)

    def test_select_one_moves_only_selected_leaf(self):
        items = [make_item("cat1", "layer1"), make_item("cat1", "layer2")]
        self.sel.setInitialState(items, unique=True)
        root = self.sel.fromTreeWidget.invisibleRootItem()
        root.child(0).child(0).setSelected(True)
        self.sel.pushButtonSelectOne.click()
        self.assertEqual(len(self.sel.getSelectedNodes()), 1)
        self.assertEqual(len(self.sel.fromLs), 1)

    def test_deselect_one_moves_only_selected_leaf_back(self):
        items = [make_item("cat1", "layer1"), make_item("cat1", "layer2")]
        self.sel.setInitialState(items, unique=True)
        self.sel.pushButtonSelectAll.click()
        root = self.sel.toTreeWidget.invisibleRootItem()
        root.child(0).child(0).setSelected(True)
        self.sel.pushButtonDeselectOne.click()
        self.assertEqual(len(self.sel.getSelectedNodes()), 1)

    def test_select_all_then_deselect_all_restores_fromLs(self):
        items = [make_item("cat1", "layer1"), make_item("cat2", "layer2")]
        self.sel.setInitialState(items, unique=True)
        self.sel.pushButtonSelectAll.click()
        self.sel.pushButtonDeselectAll.click()
        # items returned to fromLs; toLs is empty
        self.assertEqual(len(self.sel.fromLs), 2)
        self.assertEqual(self.sel.toLs, [])

    # --- Filter ---

    def test_clearAll_clears_filter_text(self):
        self.sel.filterLineEdit.setText("something")
        self.sel.clearAll()
        self.assertEqual(self.sel.filterLineEdit.text(), "")

    def test_filter_narrows_visible_items_in_from_tree(self):
        items = [
            make_item("cat1", "hidrografia_l"),
            make_item("cat1", "vegetacao_a"),
        ]
        self.sel.setInitialState(items, unique=True)
        QTest.keyClicks(self.sel.filterLineEdit, "hidro")
        self.assertEqual(_visible_leaf_count(self.sel.fromTreeWidget), 1)

    def test_filter_empty_string_restores_all_items(self):
        items = [
            make_item("cat1", "hidrografia_l"),
            make_item("cat1", "vegetacao_a"),
        ]
        self.sel.setInitialState(items, unique=True)
        QTest.keyClicks(self.sel.filterLineEdit, "hidro")
        self.sel.filterLineEdit.clear()
        self.assertEqual(_visible_leaf_count(self.sel.fromTreeWidget), 2)

    def test_filter_by_category_shows_all_items_in_matching_category(self):
        items = [
            make_item("hid", "hidrografia_l"),
            make_item("hid", "hidrografia_a"),
            make_item("veg", "vegetacao_a"),
        ]
        self.sel.setInitialState(items, unique=True)
        QTest.keyClicks(self.sel.filterLineEdit, "hid")
        self.assertEqual(_visible_leaf_count(self.sel.fromTreeWidget), 2)

    def test_filter_no_match_shows_no_items(self):
        items = [
            make_item("cat1", "hidrografia_l"),
            make_item("cat1", "vegetacao_a"),
        ]
        self.sel.setInitialState(items, unique=True)
        QTest.keyClicks(self.sel.filterLineEdit, "zzznomatch")
        # Nothing matches → tree is empty (fromLs is unchanged, only display is filtered)
        self.assertEqual(_visible_leaf_count(self.sel.fromTreeWidget), 0)


def run_all(filterString=None):
    filterString = "test_" if filterString is None else filterString
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(CustomTableSelectorTester, filterString))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
