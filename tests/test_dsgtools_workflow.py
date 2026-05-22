# -*- coding: utf-8 -*-
import json
import pytest
from pathlib import Path
from unittest.mock import MagicMock

pytestmark = pytest.mark.unit

from DsgTools.core.DSGToolsWorkflow.workflowItem import (
    DSGToolsWorkflowItem,
    ExecutionStatus,
    FlagSettings,
    Metadata,
    ModelSource,
)
from DsgTools.core.DSGToolsWorkflow.workflow import (
    DSGToolsWorkflow,
    WorkflowMetadata,
    dsgtools_workflow_from_dict,
    dsgtools_workflow_from_json,
)

MODELS_DIR = (
    Path(__file__).parent.parent / "DsgTools" / "core" / "Misc" / "QGIS_Models"
)


# ---------------------------------------------------------------------------
# Patch iface so clearOutputs() doesn't crash in headless tests
# ---------------------------------------------------------------------------
@pytest.fixture(autouse=True)
def _patch_iface(monkeypatch):
    mock_iface = MagicMock()
    import DsgTools.core.DSGToolsWorkflow.workflowItem as _wi

    monkeypatch.setattr(_wi, "iface", mock_iface)
    return mock_iface


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def simple_model_xml():
    model_path = MODELS_DIR / "muvd_add_vertex.model3"
    return model_path.read_text(encoding="utf-8")


@pytest.fixture
def workflow_metadata():
    return WorkflowMetadata(author="Tester", version="1.0", lastModified="2024-01-01")


@pytest.fixture
def make_item(simple_model_xml):
    def _make(display_name="Step", pause_after=False, on_flags_raised="halt"):
        flags = FlagSettings(
            onFlagsRaised=on_flags_raised,
            modelCanHaveFalsePositiveFlags=False,
            loadOutput=False,
            flagLayerNames=[],
        )
        return DSGToolsWorkflowItem(
            displayName=display_name,
            flags=flags,
            pauseAfterExecution=pause_after,
            source=ModelSource(type="xml", data=simple_model_xml),
            metadata=Metadata(originalName=display_name),
            tooltip="tip",
        )

    return _make


@pytest.fixture
def single_item_workflow(make_item, workflow_metadata):
    return DSGToolsWorkflow(
        displayName="Single Step Workflow",
        metadata=workflow_metadata,
        workflowItemList=[make_item("Step 1")],
    )


@pytest.fixture
def three_item_workflow(make_item, workflow_metadata):
    return DSGToolsWorkflow(
        displayName="Three Step Workflow",
        metadata=workflow_metadata,
        workflowItemList=[
            make_item("Step 1"),
            make_item("Step 2"),
            make_item("Step 3"),
        ],
    )


def _workflow_dict(simple_model_xml, n_items=1, display_name="My Workflow"):
    return {
        "displayName": display_name,
        "metadata": {
            "author": "Author",
            "version": "1.0",
            "lastModified": "2024-01-01",
        },
        "workflowItemList": [
            {
                "displayName": f"Step {i + 1}",
                "flags": {
                    "onFlagsRaised": "halt",
                    "modelCanHaveFalsePositiveFlags": False,
                    "loadOutput": False,
                    "flagLayerNames": [],
                },
                "pauseAfterExecution": False,
                "source": {"type": "xml", "data": simple_model_xml},
                "metadata": {"originalName": f"step_{i + 1}"},
                "tooltip": "tip",
            }
            for i in range(n_items)
        ],
    }


# ---------------------------------------------------------------------------
# WorkflowMetadata
# ---------------------------------------------------------------------------
class TestWorkflowMetadata:
    def test_stores_author(self, workflow_metadata):
        assert workflow_metadata.author == "Tester"

    def test_stores_version(self, workflow_metadata):
        assert workflow_metadata.version == "1.0"

    def test_stores_last_modified(self, workflow_metadata):
        assert workflow_metadata.lastModified == "2024-01-01"


# ---------------------------------------------------------------------------
# DSGToolsWorkflow — navigation
# ---------------------------------------------------------------------------
class TestDSGToolsWorkflowNavigation:
    def test_initial_step_index_is_zero(self, three_item_workflow):
        assert three_item_workflow.getCurrentWorkflowStepIndex() == 0

    def test_get_current_workflow_item_is_first(self, three_item_workflow):
        assert three_item_workflow.getCurrentWorkflowItem().displayName == "Step 1"

    def test_get_next_workflow_step_from_start(self, three_item_workflow):
        assert three_item_workflow.getNextWorkflowStep() == 1

    def test_get_next_workflow_item_from_start(self, three_item_workflow):
        item = three_item_workflow.getNextWorkflowItem()
        assert item.displayName == "Step 2"

    def test_get_next_step_at_last_item_returns_none(self, three_item_workflow):
        three_item_workflow.setCurrentWorkflowItem(2)
        assert three_item_workflow.getNextWorkflowStep() is None

    def test_get_next_item_at_last_returns_none(self, three_item_workflow):
        three_item_workflow.setCurrentWorkflowItem(2)
        assert three_item_workflow.getNextWorkflowItem() is None

    def test_set_current_workflow_item_changes_index(self, three_item_workflow):
        three_item_workflow.setCurrentWorkflowItem(2)
        assert three_item_workflow.getCurrentWorkflowStepIndex() == 2

    def test_set_current_out_of_bounds_is_ignored(self, three_item_workflow):
        three_item_workflow.setCurrentWorkflowItem(99)
        assert three_item_workflow.getCurrentWorkflowStepIndex() == 0

    def test_set_current_negative_is_ignored(self, three_item_workflow):
        three_item_workflow.setCurrentWorkflowItem(-1)
        assert three_item_workflow.getCurrentWorkflowStepIndex() == 0

    def test_get_workflow_item_from_valid_index(self, three_item_workflow):
        item = three_item_workflow.getWorkflowItemFromIndex(1)
        assert item.displayName == "Step 2"

    def test_get_workflow_item_from_first_index(self, three_item_workflow):
        item = three_item_workflow.getWorkflowItemFromIndex(0)
        assert item.displayName == "Step 1"

    def test_get_workflow_item_from_last_index(self, three_item_workflow):
        item = three_item_workflow.getWorkflowItemFromIndex(2)
        assert item.displayName == "Step 3"

    def test_get_workflow_item_from_out_of_bounds_returns_none(
        self, three_item_workflow
    ):
        assert three_item_workflow.getWorkflowItemFromIndex(99) is None

    def test_get_workflow_item_from_negative_index_returns_none(
        self, three_item_workflow
    ):
        assert three_item_workflow.getWorkflowItemFromIndex(-1) is None

    def test_get_workflow_item_from_name_exists(self, three_item_workflow):
        item = three_item_workflow.getWorklowItemFromName("Step 3")
        assert item is not None
        assert item.displayName == "Step 3"

    def test_get_workflow_item_from_name_not_found_returns_none(
        self, three_item_workflow
    ):
        assert three_item_workflow.getWorklowItemFromName("Nonexistent") is None

    def test_single_item_next_step_is_none(self, single_item_workflow):
        assert single_item_workflow.getNextWorkflowStep() is None

    def test_single_item_next_item_is_none(self, single_item_workflow):
        assert single_item_workflow.getNextWorkflowItem() is None


# ---------------------------------------------------------------------------
# DSGToolsWorkflow — status
# ---------------------------------------------------------------------------
class TestDSGToolsWorkflowStatus:
    def test_current_item_status_is_initial(self, three_item_workflow):
        assert three_item_workflow.getCurrentWorkflowItemStatus() == ExecutionStatus.INITIAL

    def test_get_status_list_length_matches_item_count(self, three_item_workflow):
        assert len(three_item_workflow.getStatusList()) == 3

    def test_get_status_list_has_required_keys(self, three_item_workflow):
        for entry in three_item_workflow.getStatusList():
            assert "workflowItem" in entry
            assert "execution_status" in entry

    def test_get_status_list_display_names_in_order(self, three_item_workflow):
        names = [e["workflowItem"] for e in three_item_workflow.getStatusList()]
        assert names == ["Step 1", "Step 2", "Step 3"]

    def test_get_status_list_all_initial(self, three_item_workflow):
        for entry in three_item_workflow.getStatusList():
            assert entry["execution_status"]["status"] == ExecutionStatus.INITIAL

    def test_status_list_reflects_item_state_change(self, three_item_workflow):
        three_item_workflow.workflowItemList[1].changeCurrentStatus(
            ExecutionStatus.FINISHED
        )
        status_list = three_item_workflow.getStatusList()
        assert status_list[1]["execution_status"]["status"] == ExecutionStatus.FINISHED


# ---------------------------------------------------------------------------
# DSGToolsWorkflow — reset
# ---------------------------------------------------------------------------
class TestDSGToolsWorkflowReset:
    def test_reset_from_zero_all_items_initial(self, three_item_workflow):
        three_item_workflow.resetWorkflowItems(startIdx=0)
        for entry in three_item_workflow.getStatusList():
            assert entry["execution_status"]["status"] == ExecutionStatus.INITIAL

    def test_reset_sets_current_step_to_start_idx(self, three_item_workflow):
        three_item_workflow.workflowItemList[2].changeCurrentStatus(
            ExecutionStatus.FAILED
        )
        three_item_workflow.resetWorkflowItems(startIdx=2)
        assert three_item_workflow.getCurrentWorkflowStepIndex() == 2

    def test_partial_reset_preserves_items_before_start_idx(
        self, three_item_workflow
    ):
        three_item_workflow.workflowItemList[0].changeCurrentStatus(
            ExecutionStatus.FINISHED
        )
        three_item_workflow.workflowItemList[1].changeCurrentStatus(
            ExecutionStatus.FAILED
        )
        three_item_workflow.resetWorkflowItems(startIdx=1)
        assert (
            three_item_workflow.workflowItemList[0].getStatus()
            == ExecutionStatus.FINISHED
        )

    def test_partial_reset_resets_items_at_and_after_start_idx(
        self, three_item_workflow
    ):
        three_item_workflow.workflowItemList[1].changeCurrentStatus(
            ExecutionStatus.FAILED
        )
        three_item_workflow.workflowItemList[2].changeCurrentStatus(
            ExecutionStatus.FAILED
        )
        three_item_workflow.resetWorkflowItems(startIdx=1)
        assert (
            three_item_workflow.workflowItemList[1].getStatus()
            == ExecutionStatus.INITIAL
        )
        assert (
            three_item_workflow.workflowItemList[2].getStatus()
            == ExecutionStatus.INITIAL
        )

    def test_reset_skips_already_initial_items(self, three_item_workflow):
        # All items start as INITIAL; resetItem should not be called on them,
        # so the model reference should stay the same.
        original_model = three_item_workflow.workflowItemList[0].model
        three_item_workflow.resetWorkflowItems(startIdx=0)
        assert three_item_workflow.workflowItemList[0].model is original_model


# ---------------------------------------------------------------------------
# DSGToolsWorkflow — serialization
# ---------------------------------------------------------------------------
class TestDSGToolsWorkflowSerialization:
    def test_as_dict_has_display_name(self, three_item_workflow):
        d = three_item_workflow.as_dict()
        assert d["displayName"] == "Three Step Workflow"

    def test_as_dict_has_metadata_author(self, three_item_workflow):
        assert three_item_workflow.as_dict()["metadata"]["author"] == "Tester"

    def test_as_dict_has_metadata_version(self, three_item_workflow):
        assert three_item_workflow.as_dict()["metadata"]["version"] == "1.0"

    def test_as_dict_workflow_item_list_length(self, three_item_workflow):
        assert len(three_item_workflow.as_dict()["workflowItemList"]) == 3

    def test_as_dict_item_display_names_in_order(self, three_item_workflow):
        names = [
            item["displayName"]
            for item in three_item_workflow.as_dict()["workflowItemList"]
        ]
        assert names == ["Step 1", "Step 2", "Step 3"]

    def test_export_returns_true(self, three_item_workflow, tmp_path):
        output_file = str(tmp_path / "workflow.json")
        assert three_item_workflow.export(output_file) is True

    def test_export_creates_file(self, three_item_workflow, tmp_path):
        output_file = str(tmp_path / "workflow.json")
        three_item_workflow.export(output_file)
        assert Path(output_file).exists()

    def test_export_produces_valid_json(self, three_item_workflow, tmp_path):
        output_file = str(tmp_path / "workflow.json")
        three_item_workflow.export(output_file)
        with open(output_file, encoding="utf-8") as f:
            data = json.load(f)
        assert data["displayName"] == "Three Step Workflow"

    def test_export_json_contains_correct_item_count(
        self, three_item_workflow, tmp_path
    ):
        output_file = str(tmp_path / "workflow.json")
        three_item_workflow.export(output_file)
        with open(output_file, encoding="utf-8") as f:
            data = json.load(f)
        assert len(data["workflowItemList"]) == 3


# ---------------------------------------------------------------------------
# dsgtools_workflow_from_dict
# ---------------------------------------------------------------------------
class TestDsgToolsWorkflowFromDict:
    def test_returns_workflow_instance(self, simple_model_xml):
        d = _workflow_dict(simple_model_xml)
        assert isinstance(dsgtools_workflow_from_dict(d), DSGToolsWorkflow)

    def test_display_name_preserved(self, simple_model_xml):
        d = _workflow_dict(simple_model_xml, display_name="My Workflow")
        wf = dsgtools_workflow_from_dict(d)
        assert wf.displayName == "My Workflow"

    def test_metadata_author_preserved(self, simple_model_xml):
        d = _workflow_dict(simple_model_xml)
        assert dsgtools_workflow_from_dict(d).metadata.author == "Author"

    def test_metadata_version_preserved(self, simple_model_xml):
        d = _workflow_dict(simple_model_xml)
        assert dsgtools_workflow_from_dict(d).metadata.version == "1.0"

    def test_item_count_preserved(self, simple_model_xml):
        d = _workflow_dict(simple_model_xml, n_items=2)
        assert len(dsgtools_workflow_from_dict(d).workflowItemList) == 2

    def test_item_display_names_in_order(self, simple_model_xml):
        d = _workflow_dict(simple_model_xml, n_items=3)
        wf = dsgtools_workflow_from_dict(d)
        names = [item.displayName for item in wf.workflowItemList]
        assert names == ["Step 1", "Step 2", "Step 3"]

    def test_initial_step_index_is_zero(self, simple_model_xml):
        d = _workflow_dict(simple_model_xml)
        wf = dsgtools_workflow_from_dict(d)
        assert wf.getCurrentWorkflowStepIndex() == 0

    def test_missing_display_name_raises_value_error(self, simple_model_xml):
        d = _workflow_dict(simple_model_xml)
        d.pop("displayName")
        with pytest.raises(ValueError):
            dsgtools_workflow_from_dict(d)

    def test_missing_author_raises_value_error(self, simple_model_xml):
        d = _workflow_dict(simple_model_xml)
        d["metadata"].pop("author")
        with pytest.raises(ValueError):
            dsgtools_workflow_from_dict(d)

    def test_empty_item_list_raises_value_error(self, simple_model_xml):
        d = _workflow_dict(simple_model_xml)
        d["workflowItemList"] = []
        with pytest.raises(ValueError):
            dsgtools_workflow_from_dict(d)

    def test_missing_item_list_raises_value_error(self, simple_model_xml):
        d = _workflow_dict(simple_model_xml)
        d.pop("workflowItemList")
        with pytest.raises(ValueError):
            dsgtools_workflow_from_dict(d)


# ---------------------------------------------------------------------------
# Round-trip: export → dsgtools_workflow_from_json
# ---------------------------------------------------------------------------
class TestWorkflowRoundTrip:
    def test_round_trip_display_name(self, three_item_workflow, tmp_path):
        path = str(tmp_path / "workflow.json")
        three_item_workflow.export(path)
        reloaded = dsgtools_workflow_from_json(path)
        assert reloaded.displayName == three_item_workflow.displayName

    def test_round_trip_item_count(self, three_item_workflow, tmp_path):
        path = str(tmp_path / "workflow.json")
        three_item_workflow.export(path)
        reloaded = dsgtools_workflow_from_json(path)
        assert len(reloaded.workflowItemList) == len(three_item_workflow.workflowItemList)

    def test_round_trip_item_names(self, three_item_workflow, tmp_path):
        path = str(tmp_path / "workflow.json")
        three_item_workflow.export(path)
        reloaded = dsgtools_workflow_from_json(path)
        original_names = [i.displayName for i in three_item_workflow.workflowItemList]
        reloaded_names = [i.displayName for i in reloaded.workflowItemList]
        assert reloaded_names == original_names

    def test_round_trip_metadata_author(self, three_item_workflow, tmp_path):
        path = str(tmp_path / "workflow.json")
        three_item_workflow.export(path)
        reloaded = dsgtools_workflow_from_json(path)
        assert reloaded.metadata.author == three_item_workflow.metadata.author

    def test_round_trip_items_start_in_initial_state(
        self, three_item_workflow, tmp_path
    ):
        path = str(tmp_path / "workflow.json")
        three_item_workflow.export(path)
        reloaded = dsgtools_workflow_from_json(path)
        for item in reloaded.workflowItemList:
            assert item.getStatus() == ExecutionStatus.INITIAL
