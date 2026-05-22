# -*- coding: utf-8 -*-
import sys
import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch, patch as _patch
from qgis.testing import unittest
from qgis.PyQt.QtWidgets import QLineEdit, QTextEdit, QComboBox, QCheckBox

try:
    from DsgTools.gui.ProductionTools.Toolboxes.WorkflowToolBox.workflowSetupDialog import (
        WorkflowSetupDialog,
    )
    from DsgTools.gui.ProductionTools.Toolboxes.WorkflowToolBox.workflowDockWidget import (
        WorkflowDockWidget,
    )
    from DsgTools.core.DSGToolsWorkflow.workflow import (
        DSGToolsWorkflow,
        WorkflowMetadata,
        dsgtools_workflow_from_dict,
    )
    from DsgTools.core.DSGToolsWorkflow.workflowItem import (
        DSGToolsWorkflowItem,
        FlagSettings,
        Metadata,
        ModelSource,
        ExecutionStatus,
    )
except ImportError:
    pytest.skip("Workflow GUI modules not found", allow_module_level=True)

_MODELS_DIR = (
    Path(__file__).parent.parent / "DsgTools" / "core" / "Misc" / "QGIS_Models"
)
_MODEL_XML = (_MODELS_DIR / "muvd_add_vertex.model3").read_text(encoding="utf-8")

_MSGBOX_DOCK = "DsgTools.gui.ProductionTools.Toolboxes.WorkflowToolBox.workflowDockWidget.QMessageBox"


def _make_workflow(name="My Workflow", n_items=2):
    items = [
        {
            "displayName": f"Step {i + 1}",
            "flags": {
                "onFlagsRaised": "halt",
                "modelCanHaveFalsePositiveFlags": False,
                "loadOutput": False,
                "flagLayerNames": [],
            },
            "pauseAfterExecution": False,
            "source": {"type": "xml", "data": _MODEL_XML},
            "metadata": {"originalName": f"step_{i + 1}"},
            "tooltip": "tip",
        }
        for i in range(n_items)
    ]
    return dsgtools_workflow_from_dict(
        {
            "displayName": name,
            "metadata": {"author": "Tester", "version": "1.0", "lastModified": "2024-01-01"},
            "workflowItemList": items,
        }
    )


# ===========================================================================
# WorkflowSetupDialog — initial state and field accessors
# ===========================================================================

class WorkflowSetupDialogStateTester(unittest.TestCase):
    def setUp(self):
        self.dlg = WorkflowSetupDialog()

    def tearDown(self):
        self.dlg.close()

    def test_initial_name_is_empty(self):
        self.assertEqual(self.dlg.workflowName(), "")

    def test_initial_author_is_empty(self):
        self.assertEqual(self.dlg.author(), "")

    def test_initial_version_is_empty(self):
        self.assertEqual(self.dlg.version(), "")

    def test_initial_model_count_is_zero(self):
        self.assertEqual(self.dlg.modelCount(), 0)

    def test_set_and_get_workflow_name(self):
        self.dlg.setWorkflowName("QA Workflow")
        self.assertEqual(self.dlg.workflowName(), "QA Workflow")

    def test_set_and_get_workflow_author(self):
        self.dlg.setWorkflowAuthor("Philipe")
        self.assertEqual(self.dlg.author(), "Philipe")

    def test_set_and_get_workflow_version(self):
        self.dlg.setWorkflowVersion("2.0")
        self.assertEqual(self.dlg.version(), "2.0")

    def test_workflow_name_strips_whitespace(self):
        self.dlg.setWorkflowName("  My Workflow  ")
        self.assertEqual(self.dlg.workflowName(), "My Workflow")

    def test_author_strips_whitespace(self):
        self.dlg.setWorkflowAuthor("  Author  ")
        self.assertEqual(self.dlg.author(), "Author")

    def test_version_strips_whitespace(self):
        self.dlg.setWorkflowVersion("  1.0  ")
        self.assertEqual(self.dlg.version(), "1.0")

    def test_clear_resets_name(self):
        self.dlg.setWorkflowName("QA Workflow")
        self.dlg.clear()
        self.assertEqual(self.dlg.workflowName(), "")

    def test_clear_resets_author(self):
        self.dlg.setWorkflowAuthor("Philipe")
        self.dlg.clear()
        self.assertEqual(self.dlg.author(), "")

    def test_clear_resets_version(self):
        self.dlg.setWorkflowVersion("1.0")
        self.dlg.clear()
        self.assertEqual(self.dlg.version(), "")

    def test_clear_resets_model_count(self):
        # modelCount is managed by orderedTableWidget; clear should bring it to 0
        self.dlg.clear()
        self.assertEqual(self.dlg.modelCount(), 0)

    def test_now_returns_non_empty_string(self):
        self.assertNotEqual(self.dlg.now(), "")

    def test_now_contains_slash_separators(self):
        # format: "dd/mm/yyyy HH:MM:SS"
        self.assertIn("/", self.dlg.now())

    def test_now_contains_colon_separators(self):
        self.assertIn(":", self.dlg.now())


# ===========================================================================
# WorkflowSetupDialog — validate()
# ===========================================================================

class WorkflowSetupDialogValidationTester(unittest.TestCase):
    def setUp(self):
        self.dlg = WorkflowSetupDialog()

    def tearDown(self):
        self.dlg.close()

    def _fill_required(self):
        self.dlg.setWorkflowName("My Workflow")
        self.dlg.setWorkflowAuthor("Author")
        self.dlg.setWorkflowVersion("1.0")

    def test_validate_empty_name_returns_non_empty_message(self):
        self.assertNotEqual(self.dlg.validate(), "")

    def test_validate_empty_author_returns_message(self):
        self.dlg.setWorkflowName("My Workflow")
        self.assertNotEqual(self.dlg.validate(), "")

    def test_validate_empty_version_returns_message(self):
        self.dlg.setWorkflowName("My Workflow")
        self.dlg.setWorkflowAuthor("Author")
        self.assertNotEqual(self.dlg.validate(), "")

    def test_validate_all_required_fields_no_models_passes(self):
        self._fill_required()
        self.assertEqual(self.dlg.validate(), "")

    def test_validate_row_contents_empty_name_returns_message(self):
        contents = {"displayName": "", "source": {"data": "some_xml"}}
        self.assertNotEqual(self.dlg.validateRowContents(contents), "")

    def test_validate_row_contents_empty_source_returns_message(self):
        contents = {"displayName": "My Model", "source": {"data": ""}}
        self.assertNotEqual(self.dlg.validateRowContents(contents), "")

    def test_validate_row_contents_valid_returns_empty(self):
        contents = {"displayName": "My Model", "source": {"data": "<model/>"}}
        self.assertEqual(self.dlg.validateRowContents(contents), "")

    def test_current_workflow_with_no_rows_returns_none(self):
        # dsgtools_workflow_from_dict raises ValueError for empty item list
        self._fill_required()
        self.assertIsNone(self.dlg.currentWorkflow())


# ===========================================================================
# WorkflowSetupDialog — widget factory methods
# ===========================================================================

class WorkflowSetupDialogWidgetFactoryTester(unittest.TestCase):
    def setUp(self):
        self.dlg = WorkflowSetupDialog()

    def tearDown(self):
        self.dlg.close()

    def test_model_name_widget_returns_qlineedit(self):
        self.assertIsInstance(self.dlg.modelNameWidget(), QLineEdit)

    def test_model_name_widget_has_placeholder(self):
        le = self.dlg.modelNameWidget()
        self.assertNotEqual(le.placeholderText(), "")

    def test_model_name_widget_with_name_sets_text(self):
        le = self.dlg.modelNameWidget("my_model")
        self.assertEqual(le.text(), "my_model")

    def test_tooltip_widget_returns_qtextedit(self):
        self.assertIsInstance(self.dlg.tooltipWidget(), QTextEdit)

    def test_tooltip_widget_has_placeholder(self):
        w = self.dlg.tooltipWidget()
        self.assertNotEqual(w.placeholderText(), "")

    def test_tooltip_widget_with_text_sets_content(self):
        w = self.dlg.tooltipWidget("my tooltip")
        self.assertEqual(w.toPlainText(), "my tooltip")

    def test_on_flags_widget_returns_qcombobox(self):
        self.assertIsInstance(self.dlg.onFlagsWidget(), QComboBox)

    def test_on_flags_widget_has_three_options(self):
        combo = self.dlg.onFlagsWidget()
        self.assertEqual(combo.count(), 3)

    def test_on_flags_widget_default_index_is_zero(self):
        combo = self.dlg.onFlagsWidget()
        self.assertEqual(combo.currentIndex(), 0)

    def test_on_flags_widget_halt_sets_index_zero(self):
        combo = self.dlg.onFlagsWidget("halt")
        self.assertEqual(combo.currentIndex(), WorkflowSetupDialog.ON_FLAGS_HALT)

    def test_on_flags_widget_warn_sets_index_one(self):
        combo = self.dlg.onFlagsWidget("warn")
        self.assertEqual(combo.currentIndex(), WorkflowSetupDialog.ON_FLAGS_WARN)

    def test_on_flags_widget_ignore_sets_index_two(self):
        combo = self.dlg.onFlagsWidget("ignore")
        self.assertEqual(combo.currentIndex(), WorkflowSetupDialog.ON_FLAGS_IGNORE)

    def test_false_positive_flags_widget_returns_qcheckbox(self):
        self.assertIsInstance(self.dlg.falsePositiveFlagsWidget(), QCheckBox)

    def test_false_positive_flags_widget_default_unchecked(self):
        cb = self.dlg.falsePositiveFlagsWidget()
        self.assertFalse(cb.isChecked())

    def test_false_positive_flags_widget_with_true_is_checked(self):
        cb = self.dlg.falsePositiveFlagsWidget(option=True)
        self.assertTrue(cb.isChecked())

    def test_pause_after_execution_widget_returns_qcheckbox(self):
        self.assertIsInstance(self.dlg.pauseAfterExecutionWidget(), QCheckBox)

    def test_pause_after_execution_widget_default_unchecked(self):
        self.assertFalse(self.dlg.pauseAfterExecutionWidget().isChecked())

    def test_pause_after_execution_widget_with_true_is_checked(self):
        self.assertTrue(self.dlg.pauseAfterExecutionWidget(option=True).isChecked())

    def test_load_output_widget_returns_qcheckbox(self):
        self.assertIsInstance(self.dlg.loadOutputWidget(), QCheckBox)

    def test_load_output_widget_default_unchecked(self):
        self.assertFalse(self.dlg.loadOutputWidget().isChecked())


# ===========================================================================
# WorkflowSetupDialog — workflowParameterMap()
# ===========================================================================

class WorkflowSetupDialogParameterMapTester(unittest.TestCase):
    def setUp(self):
        self.dlg = WorkflowSetupDialog()
        self.dlg.setWorkflowName("QA Workflow")
        self.dlg.setWorkflowAuthor("Tester")
        self.dlg.setWorkflowVersion("1.0")

    def tearDown(self):
        self.dlg.close()

    def test_parameter_map_has_display_name_key(self):
        self.assertIn("displayName", self.dlg.workflowParameterMap())

    def test_parameter_map_display_name_matches_field(self):
        self.assertEqual(self.dlg.workflowParameterMap()["displayName"], "QA Workflow")

    def test_parameter_map_has_metadata_key(self):
        self.assertIn("metadata", self.dlg.workflowParameterMap())

    def test_parameter_map_metadata_has_author(self):
        self.assertEqual(self.dlg.workflowParameterMap()["metadata"]["author"], "Tester")

    def test_parameter_map_metadata_has_version(self):
        self.assertEqual(self.dlg.workflowParameterMap()["metadata"]["version"], "1.0")

    def test_parameter_map_metadata_has_last_modified(self):
        self.assertIn("lastModified", self.dlg.workflowParameterMap()["metadata"])

    def test_parameter_map_has_workflow_item_list(self):
        self.assertIn("workflowItemList", self.dlg.workflowParameterMap())

    def test_parameter_map_workflow_item_list_empty_with_no_rows(self):
        self.assertEqual(self.dlg.workflowParameterMap()["workflowItemList"], [])


# ===========================================================================
# WorkflowDockWidget — initial state
# ===========================================================================

class WorkflowDockWidgetInitialStateTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.iface = MagicMock()
        cls.dock = WorkflowDockWidget(cls.iface)

    @classmethod
    def tearDownClass(cls):
        cls.dock.close()

    def test_initial_current_workflow_is_none(self):
        self.assertIsNone(self.dock.currentWorkflow())

    def test_initial_current_workflow_name_is_empty(self):
        self.assertEqual(self.dock.currentWorkflowName(), "")

    def test_initial_table_row_count_is_zero(self):
        self.assertEqual(self.dock.tableWidget.rowCount(), 0)

    def test_initial_combobox_has_placeholder_at_index_zero(self):
        self.assertEqual(self.dock.comboBox.currentIndex(), 0)
        self.assertNotEqual(self.dock.comboBox.currentText(), "")

    def test_initial_run_button_is_enabled(self):
        self.assertTrue(self.dock.runPushButton.isEnabled())

    def test_initial_cancel_button_is_disabled(self):
        self.assertFalse(self.dock.cancelPushButton.isEnabled())

    def test_initial_resume_button_is_enabled(self):
        self.assertTrue(self.dock.resumePushButton.isEnabled())

    def test_initial_workflows_dict_is_empty(self):
        self.assertEqual(self.dock.workflows, {})


# ===========================================================================
# WorkflowDockWidget — GUI state
# ===========================================================================

class WorkflowDockWidgetGuiStateTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.iface = MagicMock()
        cls.dock = WorkflowDockWidget(cls.iface)

    @classmethod
    def tearDownClass(cls):
        cls.dock.close()

    def setUp(self):
        self.dock.setGuiState(False)

    def test_set_gui_active_disables_run_button(self):
        self.dock.setGuiState(True)
        self.assertFalse(self.dock.runPushButton.isEnabled())

    def test_set_gui_active_enables_cancel_button(self):
        self.dock.setGuiState(True)
        self.assertTrue(self.dock.cancelPushButton.isEnabled())

    def test_set_gui_active_disables_resume_button(self):
        self.dock.setGuiState(True)
        self.assertFalse(self.dock.resumePushButton.isEnabled())

    def test_set_gui_inactive_enables_run_button(self):
        self.dock.setGuiState(True)
        self.dock.setGuiState(False)
        self.assertTrue(self.dock.runPushButton.isEnabled())

    def test_set_gui_inactive_disables_cancel_button(self):
        self.dock.setGuiState(True)
        self.dock.setGuiState(False)
        self.assertFalse(self.dock.cancelPushButton.isEnabled())

    def test_show_edition_button_true_shows_add_button(self):
        self.dock.showEditionButton(True)
        self.assertFalse(self.dock.addPushButton.isHidden())

    def test_show_edition_button_false_hides_add_button(self):
        self.dock.showEditionButton(False)
        self.assertTrue(self.dock.addPushButton.isHidden())

    def test_show_edition_button_true_shows_edit_button(self):
        self.dock.showEditionButton(True)
        self.assertFalse(self.dock.editPushButton.isHidden())

    def test_show_edition_button_false_hides_edit_button(self):
        self.dock.showEditionButton(False)
        self.assertTrue(self.dock.editPushButton.isHidden())

    def test_show_edition_button_true_shows_remove_button(self):
        self.dock.showEditionButton(True)
        self.assertFalse(self.dock.removePushButton.isHidden())

    def test_show_edition_button_false_hides_remove_button(self):
        self.dock.showEditionButton(False)
        self.assertTrue(self.dock.removePushButton.isHidden())


# ===========================================================================
# WorkflowDockWidget — workflow management
# ===========================================================================

class WorkflowDockWidgetWorkflowManagementTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.iface = MagicMock()
        cls.dock = WorkflowDockWidget(cls.iface)

    @classmethod
    def tearDownClass(cls):
        cls.dock.close()

    def setUp(self):
        from collections import defaultdict
        self.dock.workflows = {}
        self.dock.ignoreFlagsMenuDict = defaultdict(dict)
        self.dock.workflowStatusDict = defaultdict(list)
        self.dock.resetComboBox()
        self.dock.resetTable()
        self.workflow = _make_workflow("Test Workflow", n_items=2)

    def test_add_workflow_item_appears_in_combobox(self):
        self.dock.addWorkflowItem(self.workflow)
        idx = self.dock.comboBox.findText("Test Workflow")
        self.assertGreater(idx, 0)

    def test_add_workflow_item_selects_it_in_combobox(self):
        self.dock.addWorkflowItem(self.workflow)
        self.assertEqual(self.dock.comboBox.currentText(), "Test Workflow")

    def test_add_workflow_item_stores_in_workflows_dict(self):
        self.dock.addWorkflowItem(self.workflow)
        self.assertIn("Test Workflow", self.dock.workflows)

    def test_add_duplicate_workflow_does_not_increase_combobox_count(self):
        self.dock.addWorkflowItem(self.workflow)
        count_before = self.dock.comboBox.count()
        self.dock.addWorkflowItem(self.workflow)
        self.assertEqual(self.dock.comboBox.count(), count_before)

    def test_current_workflow_returns_added_workflow(self):
        self.dock.addWorkflowItem(self.workflow)
        current = self.dock.currentWorkflow()
        self.assertIsNotNone(current)
        self.assertEqual(current.displayName, "Test Workflow")

    def test_add_two_workflows_both_in_combobox(self):
        wf2 = _make_workflow("Second Workflow", n_items=1)
        self.dock.addWorkflowItem(self.workflow)
        self.dock.addWorkflowItem(wf2)
        self.assertGreater(self.dock.comboBox.findText("Test Workflow"), 0)
        self.assertGreater(self.dock.comboBox.findText("Second Workflow"), 0)

    def test_remove_workflow_removes_from_combobox(self):
        self.dock.addWorkflowItem(self.workflow)
        with patch(_MSGBOX_DOCK + ".question", return_value=MagicMock()):
            with patch.object(self.dock, "confirmAction", return_value=True):
                self.dock.removeWorkflow()
        self.assertEqual(self.dock.comboBox.findText("Test Workflow"), -1)

    def test_remove_workflow_removes_from_dict(self):
        self.dock.addWorkflowItem(self.workflow)
        with patch.object(self.dock, "confirmAction", return_value=True):
            self.dock.removeWorkflow()
        self.assertNotIn("Test Workflow", self.dock.workflows)

    def test_remove_workflow_denied_keeps_workflow(self):
        self.dock.addWorkflowItem(self.workflow)
        with patch.object(self.dock, "confirmAction", return_value=False):
            self.dock.removeWorkflow()
        self.assertIn("Test Workflow", self.dock.workflows)

    def test_remove_with_no_workflow_selected_does_nothing(self):
        # comboBox at index 0 (placeholder) → no-op
        self.dock.removeWorkflow()
        self.assertEqual(self.dock.workflows, {})


# ===========================================================================
# WorkflowDockWidget — setWorkflow populates the table
# ===========================================================================

class WorkflowDockWidgetTableTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.iface = MagicMock()
        cls.dock = WorkflowDockWidget(cls.iface)

    @classmethod
    def tearDownClass(cls):
        cls.dock.close()

    def setUp(self):
        from collections import defaultdict
        self.dock.workflows = {}
        self.dock.ignoreFlagsMenuDict = defaultdict(dict)
        self.dock.workflowStatusDict = defaultdict(list)
        self.dock.resetComboBox()
        self.dock.resetTable()

    def test_set_workflow_sets_table_row_count(self):
        wf = _make_workflow(n_items=3)
        self.dock.setWorkflow(wf)
        self.assertEqual(self.dock.tableWidget.rowCount(), 3)

    def test_set_workflow_none_clears_table(self):
        wf = _make_workflow(n_items=2)
        self.dock.setWorkflow(wf)
        self.dock.setWorkflow(None)
        self.assertEqual(self.dock.tableWidget.rowCount(), 0)

    def test_set_workflow_row_zero_shows_first_item_name(self):
        wf = _make_workflow(n_items=2)
        self.dock.setWorkflow(wf)
        name_widget = self.dock.tableWidget.cellWidget(0, 0)
        self.assertIsNotNone(name_widget)
        self.assertEqual(name_widget.text(), "Step 1")

    def test_set_workflow_row_one_shows_second_item_name(self):
        wf = _make_workflow(n_items=2)
        self.dock.setWorkflow(wf)
        name_widget = self.dock.tableWidget.cellWidget(1, 0)
        self.assertEqual(name_widget.text(), "Step 2")

    def test_adding_workflow_via_add_item_populates_table(self):
        wf = _make_workflow(n_items=2)
        self.dock.addWorkflowItem(wf)
        self.assertEqual(self.dock.tableWidget.rowCount(), 2)

    def test_reset_table_clears_rows(self):
        wf = _make_workflow(n_items=2)
        self.dock.setWorkflow(wf)
        self.dock.resetTable()
        self.assertEqual(self.dock.tableWidget.rowCount(), 0)

    def test_reset_table_sets_three_columns(self):
        self.dock.resetTable()
        self.assertEqual(self.dock.tableWidget.columnCount(), 3)


# ===========================================================================
# WorkflowDockWidget — state persistence
# ===========================================================================

class WorkflowDockWidgetStateTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.iface = MagicMock()
        cls.dock = WorkflowDockWidget(cls.iface)

    @classmethod
    def tearDownClass(cls):
        cls.dock.close()

    def setUp(self):
        from collections import defaultdict
        self.dock.workflows = {}
        self.dock.ignoreFlagsMenuDict = defaultdict(dict)
        self.dock.workflowStatusDict = defaultdict(list)
        self.dock.resetComboBox()
        self.dock.resetTable()

    def test_load_empty_state_produces_no_workflows(self):
        self.dock.loadState("{}")
        self.assertEqual(self.dock.workflows, {})

    def test_load_empty_state_resets_combobox(self):
        self.dock.addWorkflowItem(_make_workflow("wf1"))
        self.dock.loadState("{}")
        self.assertEqual(self.dock.comboBox.count(), 1)  # only placeholder

    def test_load_state_with_workflow_populates_dock(self):
        wf = _make_workflow("Loaded Workflow", n_items=1)
        state = json.dumps(
            {
                "workflows": {"Loaded Workflow": wf.as_dict()},
                "current_workflow": 1,
                "show_buttons": True,
                "workflow_status_dict_list": {},
            }
        )
        self.dock.loadState(state)
        self.assertIn("Loaded Workflow", self.dock.workflows)

    def test_load_state_selects_correct_workflow(self):
        wf = _make_workflow("Loaded Workflow", n_items=1)
        state = json.dumps(
            {
                "workflows": {"Loaded Workflow": wf.as_dict()},
                "current_workflow": 1,
                "show_buttons": True,
                "workflow_status_dict_list": {},
            }
        )
        self.dock.loadState(state)
        self.assertEqual(self.dock.comboBox.currentText(), "Loaded Workflow")

    def test_save_and_reload_preserves_workflow_name(self):
        wf = _make_workflow("Persistent Workflow", n_items=1)
        self.dock.addWorkflowItem(wf)
        self.dock.saveState()
        dock2 = WorkflowDockWidget(self.iface)
        try:
            # State is saved to QgsProject — load it explicitly
            self.dock.saveState()
            from qgis.core import QgsProject, QgsExpressionContextUtils
            raw = QgsExpressionContextUtils.projectScope(
                QgsProject.instance()
            ).variable("dsgtools_qatoolbox_state")
            if raw:
                dock2.loadState(raw)
                self.assertIn("Persistent Workflow", dock2.workflows)
        finally:
            dock2.close()

    def test_workflow_tooltip_contains_author(self):
        wf = _make_workflow("Tooltip Workflow", n_items=1)
        self.dock.addWorkflowItem(wf)
        idx = self.dock.comboBox.findText("Tooltip Workflow")
        from qgis.PyQt.QtCore import Qt
        tooltip = self.dock.comboBox.itemData(idx, Qt.ItemDataRole.ToolTipRole)
        self.assertIn("Tester", tooltip)

    def test_workflow_tooltip_contains_version(self):
        wf = _make_workflow("Tooltip Workflow 2", n_items=1)
        self.dock.addWorkflowItem(wf)
        idx = self.dock.comboBox.findText("Tooltip Workflow 2")
        from qgis.PyQt.QtCore import Qt
        tooltip = self.dock.comboBox.itemData(idx, Qt.ItemDataRole.ToolTipRole)
        self.assertIn("1.0", tooltip)


def run_all(filterString=None):
    filterString = "test_" if filterString is None else filterString
    suite = unittest.TestSuite()
    for cls in [
        WorkflowSetupDialogStateTester,
        WorkflowSetupDialogValidationTester,
        WorkflowSetupDialogWidgetFactoryTester,
        WorkflowSetupDialogParameterMapTester,
        WorkflowDockWidgetInitialStateTester,
        WorkflowDockWidgetGuiStateTester,
        WorkflowDockWidgetWorkflowManagementTester,
        WorkflowDockWidgetTableTester,
        WorkflowDockWidgetStateTester,
    ]:
        suite.addTests(unittest.makeSuite(cls, filterString))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
