# -*- coding: utf-8 -*-
import pytest
from pathlib import Path
from unittest.mock import MagicMock

pytestmark = pytest.mark.unit

from qgis.core import QgsProcessingFeedback

from DsgTools.core.DSGToolsWorkflow.workflowItem import (
    DSGToolsWorkflowItem,
    ExecutionStatus,
    FlagSettings,
    Metadata,
    ModelExecutionOutput,
    ModelSource,
    load_from_json,
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
def flag_settings_halt():
    return FlagSettings(
        onFlagsRaised="halt",
        modelCanHaveFalsePositiveFlags=False,
        loadOutput=False,
        flagLayerNames=[],
    )


@pytest.fixture
def model_source(simple_model_xml):
    return ModelSource(type="xml", data=simple_model_xml)


@pytest.fixture
def workflow_item(model_source, flag_settings_halt):
    return DSGToolsWorkflowItem(
        displayName="Test Item",
        flags=flag_settings_halt,
        pauseAfterExecution=False,
        source=model_source,
        metadata=Metadata(originalName="test_model"),
        tooltip="Test tooltip",
    )


# ---------------------------------------------------------------------------
# ExecutionStatus
# ---------------------------------------------------------------------------
class TestExecutionStatus:
    def test_all_values_are_strings(self):
        for status in ExecutionStatus:
            assert isinstance(status, str)

    def test_initial_value(self):
        assert ExecutionStatus.INITIAL == "initial"

    def test_running_value(self):
        assert ExecutionStatus.RUNNING == "running"

    def test_failed_value(self):
        assert ExecutionStatus.FAILED == "failed"

    def test_canceled_value(self):
        assert ExecutionStatus.CANCELED == "canceled"

    def test_finished_value(self):
        assert ExecutionStatus.FINISHED == "finished"

    def test_finished_with_flags_value(self):
        assert ExecutionStatus.FINISHED_WITH_FLAGS == "finished with flags"

    def test_paused_before_running_value(self):
        assert ExecutionStatus.PAUSED_BEFORE_RUNNING == "paused before running"

    def test_ignore_flags_value(self):
        assert ExecutionStatus.IGNORE_FLAGS == "ignore flags"

    def test_can_construct_from_string(self):
        assert ExecutionStatus("initial") is ExecutionStatus.INITIAL

    def test_all_eight_members_exist(self):
        assert len(ExecutionStatus) == 8


# ---------------------------------------------------------------------------
# FlagSettings
# ---------------------------------------------------------------------------
class TestFlagSettings:
    @pytest.mark.parametrize("value", ["halt", "warn", "ignore"])
    def test_valid_on_flags_raised(self, value):
        fs = FlagSettings(
            onFlagsRaised=value,
            modelCanHaveFalsePositiveFlags=False,
            loadOutput=False,
            flagLayerNames=[],
        )
        assert fs.onFlagsRaised == value

    def test_invalid_on_flags_raised_raises_value_error(self):
        with pytest.raises(ValueError):
            FlagSettings(
                onFlagsRaised="stop",
                modelCanHaveFalsePositiveFlags=False,
                loadOutput=False,
                flagLayerNames=[],
            )

    def test_empty_string_raises_value_error(self):
        with pytest.raises(ValueError):
            FlagSettings(
                onFlagsRaised="",
                modelCanHaveFalsePositiveFlags=False,
                loadOutput=False,
                flagLayerNames=[],
            )

    def test_flag_layer_names_stored(self):
        fs = FlagSettings(
            onFlagsRaised="halt",
            modelCanHaveFalsePositiveFlags=True,
            loadOutput=True,
            flagLayerNames=["flags_a", "flags_b"],
        )
        assert fs.flagLayerNames == ["flags_a", "flags_b"]

    def test_model_can_have_false_positive_flags_true(self):
        fs = FlagSettings(
            onFlagsRaised="warn",
            modelCanHaveFalsePositiveFlags=True,
            loadOutput=False,
            flagLayerNames=[],
        )
        assert fs.modelCanHaveFalsePositiveFlags is True

    def test_load_output_field(self):
        fs = FlagSettings(
            onFlagsRaised="ignore",
            modelCanHaveFalsePositiveFlags=False,
            loadOutput=True,
            flagLayerNames=[],
        )
        assert fs.loadOutput is True


# ---------------------------------------------------------------------------
# ModelExecutionOutput
# ---------------------------------------------------------------------------
class TestModelExecutionOutput:
    def test_default_status_is_initial(self):
        out = ModelExecutionOutput()
        assert out.status == ExecutionStatus.INITIAL

    def test_status_coerced_from_string(self):
        out = ModelExecutionOutput(status="finished")
        assert out.status == ExecutionStatus.FINISHED

    def test_status_coerced_canceled_from_string(self):
        out = ModelExecutionOutput(status="canceled")
        assert out.status == ExecutionStatus.CANCELED

    def test_default_execution_time_is_zero(self):
        out = ModelExecutionOutput()
        assert out.executionTime == 0.0

    def test_default_execution_message_is_empty(self):
        out = ModelExecutionOutput()
        assert out.executionMessage == ""

    def test_as_dict_contains_expected_keys(self):
        out = ModelExecutionOutput()
        d = out.as_dict()
        assert {"executionTime", "executionMessage", "status", "result"} <= set(d)

    def test_as_dict_status_matches(self):
        out = ModelExecutionOutput(status=ExecutionStatus.FINISHED)
        assert out.as_dict()["status"] == ExecutionStatus.FINISHED

    def test_as_dict_execution_time_matches(self):
        out = ModelExecutionOutput(executionTime=3.14)
        assert out.as_dict()["executionTime"] == 3.14

    def test_as_dict_empty_result_gives_empty_dict(self):
        out = ModelExecutionOutput()
        assert out.as_dict()["result"] == {}


# ---------------------------------------------------------------------------
# DSGToolsWorkflowItem — initial state
# ---------------------------------------------------------------------------
class TestDSGToolsWorkflowItemInitialState:
    def test_initial_status_is_initial(self, workflow_item):
        assert workflow_item.getStatus() == ExecutionStatus.INITIAL

    def test_display_name_stored(self, workflow_item):
        assert workflow_item.displayName == "Test Item"

    def test_current_task_is_none_initially(self, workflow_item):
        assert workflow_item.currentTask is None

    def test_get_flag_names_empty(self, workflow_item):
        assert workflow_item.getFlagNames() == []

    def test_flags_can_have_false_positive_false(self, workflow_item):
        assert workflow_item.flagsCanHaveFalsePositiveResults() is False

    def test_get_description_returns_tooltip(self, workflow_item):
        assert workflow_item.getDescription() == "Test tooltip"

    def test_get_description_returns_string(self, workflow_item):
        assert isinstance(workflow_item.getDescription(), str)

    def test_load_output_false(self, workflow_item):
        assert workflow_item.loadOutput() is False

    def test_model_is_set(self, workflow_item):
        assert workflow_item.model is not None


# ---------------------------------------------------------------------------
# DSGToolsWorkflowItem — flag names
# ---------------------------------------------------------------------------
class TestDSGToolsWorkflowItemFlagNames:
    def test_flag_names_from_settings(self, model_source):
        fs = FlagSettings(
            onFlagsRaised="warn",
            modelCanHaveFalsePositiveFlags=True,
            loadOutput=False,
            flagLayerNames=["layer_a", "layer_b"],
        )
        item = DSGToolsWorkflowItem(
            displayName="Item",
            flags=fs,
            pauseAfterExecution=False,
            source=model_source,
            metadata=Metadata(originalName="test"),
            tooltip="tip",
        )
        assert item.getFlagNames() == ["layer_a", "layer_b"]

    def test_flags_can_have_false_positive_true(self, model_source):
        fs = FlagSettings(
            onFlagsRaised="warn",
            modelCanHaveFalsePositiveFlags=True,
            loadOutput=False,
            flagLayerNames=[],
        )
        item = DSGToolsWorkflowItem(
            displayName="Item",
            flags=fs,
            pauseAfterExecution=False,
            source=model_source,
            metadata=Metadata(originalName="test"),
            tooltip="tip",
        )
        assert item.flagsCanHaveFalsePositiveResults() is True


# ---------------------------------------------------------------------------
# DSGToolsWorkflowItem — status transitions
# ---------------------------------------------------------------------------
class TestDSGToolsWorkflowItemStatusTransitions:
    def test_change_status_to_running(self, workflow_item):
        workflow_item.changeCurrentStatus(ExecutionStatus.RUNNING, "started")
        assert workflow_item.getStatus() == ExecutionStatus.RUNNING

    def test_change_status_to_failed(self, workflow_item):
        workflow_item.changeCurrentStatus(ExecutionStatus.FAILED, "error")
        assert workflow_item.getStatus() == ExecutionStatus.FAILED

    def test_change_status_accepts_string_value(self, workflow_item):
        workflow_item.changeCurrentStatus("finished", "done")
        assert workflow_item.getStatus() == ExecutionStatus.FINISHED

    def test_change_status_updates_execution_message(self, workflow_item):
        workflow_item.changeCurrentStatus(ExecutionStatus.RUNNING, "my message")
        assert workflow_item.executionOutput.executionMessage == "my message"

    def test_change_status_updates_execution_time(self, workflow_item):
        workflow_item.changeCurrentStatus(
            ExecutionStatus.FINISHED, "done", executionTime=3.14
        )
        assert workflow_item.executionOutput.executionTime == 3.14

    def test_change_status_without_time_leaves_time_unchanged(self, workflow_item):
        workflow_item.changeCurrentStatus(ExecutionStatus.RUNNING)
        assert workflow_item.executionOutput.executionTime == 0.0

    def test_pause_before_running_sets_paused_status(self, workflow_item):
        workflow_item.pauseBeforeRunning()
        assert workflow_item.getStatus() == ExecutionStatus.PAUSED_BEFORE_RUNNING

    def test_cancel_with_no_task_is_a_no_op(self, workflow_item):
        # cancelCurrentTask returns early when currentTask is None
        workflow_item.cancelCurrentTask()
        assert workflow_item.getStatus() == ExecutionStatus.INITIAL

    def test_cancel_with_task_sets_canceled_status(self, workflow_item):
        workflow_item.currentTask = MagicMock()
        workflow_item.cancelCurrentTask()
        assert workflow_item.getStatus() == ExecutionStatus.CANCELED

    def test_cancel_clears_current_task(self, workflow_item):
        workflow_item.currentTask = MagicMock()
        workflow_item.cancelCurrentTask()
        assert workflow_item.currentTask is None


# ---------------------------------------------------------------------------
# DSGToolsWorkflowItem — ignore flags toggle
# ---------------------------------------------------------------------------
class TestDSGToolsWorkflowItemIgnoreFlags:
    def test_no_op_when_false_positive_not_allowed(self, workflow_item):
        workflow_item.changeCurrentStatus(ExecutionStatus.FINISHED_WITH_FLAGS)
        workflow_item.setCurrentStateToIgnoreFlags()
        assert workflow_item.getStatus() == ExecutionStatus.FINISHED_WITH_FLAGS

    def test_toggles_to_ignore_when_false_positive_allowed(self, model_source):
        fs = FlagSettings(
            onFlagsRaised="warn",
            modelCanHaveFalsePositiveFlags=True,
            loadOutput=False,
            flagLayerNames=[],
        )
        item = DSGToolsWorkflowItem(
            displayName="Item",
            flags=fs,
            pauseAfterExecution=False,
            source=model_source,
            metadata=Metadata(originalName="test"),
            tooltip="tip",
        )
        item.changeCurrentStatus(ExecutionStatus.FINISHED_WITH_FLAGS)
        item.setCurrentStateToIgnoreFlags()
        assert item.getStatus() == ExecutionStatus.IGNORE_FLAGS

    def test_toggles_back_to_finished_with_flags(self, model_source):
        fs = FlagSettings(
            onFlagsRaised="warn",
            modelCanHaveFalsePositiveFlags=True,
            loadOutput=False,
            flagLayerNames=[],
        )
        item = DSGToolsWorkflowItem(
            displayName="Item",
            flags=fs,
            pauseAfterExecution=False,
            source=model_source,
            metadata=Metadata(originalName="test"),
            tooltip="tip",
        )
        item.changeCurrentStatus(ExecutionStatus.IGNORE_FLAGS)
        item.setCurrentStateToIgnoreFlags()
        assert item.getStatus() == ExecutionStatus.FINISHED_WITH_FLAGS


# ---------------------------------------------------------------------------
# DSGToolsWorkflowItem — reset
# ---------------------------------------------------------------------------
class TestDSGToolsWorkflowItemReset:
    def test_reset_returns_to_initial_status(self, workflow_item):
        workflow_item.changeCurrentStatus(ExecutionStatus.FAILED, "error")
        workflow_item.resetItem()
        assert workflow_item.getStatus() == ExecutionStatus.INITIAL

    def test_reset_clears_execution_message(self, workflow_item):
        workflow_item.changeCurrentStatus(ExecutionStatus.FAILED, "some error")
        workflow_item.resetItem()
        assert workflow_item.executionOutput.executionMessage == ""

    def test_reset_clears_current_task(self, workflow_item):
        workflow_item.currentTask = MagicMock()
        workflow_item.resetItem()
        assert workflow_item.currentTask is None

    def test_reset_reloads_model(self, workflow_item):
        original_model = workflow_item.model
        workflow_item.resetItem()
        assert workflow_item.model is not None
        assert workflow_item.model is not original_model


# ---------------------------------------------------------------------------
# DSGToolsWorkflowItem — serialization
# ---------------------------------------------------------------------------
class TestDSGToolsWorkflowItemSerialization:
    def test_set_status_from_dict_sets_status(self, workflow_item):
        data = {
            "result": {},
            "executionTime": 1.5,
            "executionMessage": "done",
            "status": "finished",
        }
        workflow_item.setStatusFromDict(data)
        assert workflow_item.getStatus() == ExecutionStatus.FINISHED

    def test_set_status_from_dict_sets_execution_time(self, workflow_item):
        data = {
            "result": {},
            "executionTime": 2.5,
            "executionMessage": "done",
            "status": "finished",
        }
        workflow_item.setStatusFromDict(data)
        assert workflow_item.executionOutput.executionTime == 2.5

    def test_execution_status_as_dict_has_status_key(self, workflow_item):
        d = workflow_item.executionStatusAsDict()
        assert "status" in d

    def test_execution_status_as_dict_status_is_initial(self, workflow_item):
        d = workflow_item.executionStatusAsDict()
        assert d["status"] == ExecutionStatus.INITIAL

    def test_execution_status_as_dict_after_status_change(self, workflow_item):
        workflow_item.changeCurrentStatus(ExecutionStatus.FINISHED, "ok")
        d = workflow_item.executionStatusAsDict()
        assert d["status"] == ExecutionStatus.FINISHED

    def test_as_dict_contains_display_name(self, workflow_item):
        d = workflow_item.as_dict()
        assert d["displayName"] == "Test Item"

    def test_as_dict_contains_flags(self, workflow_item):
        d = workflow_item.as_dict()
        assert "flags" in d
        assert d["flags"]["onFlagsRaised"] == "halt"

    def test_as_dict_contains_source(self, workflow_item):
        d = workflow_item.as_dict()
        assert "source" in d
        assert d["source"]["type"] == "xml"


# ---------------------------------------------------------------------------
# load_from_json
# ---------------------------------------------------------------------------
class TestLoadFromJson:
    def _item_dict(self, xml):
        return {
            "displayName": "Test",
            "flags": {
                "onFlagsRaised": "halt",
                "modelCanHaveFalsePositiveFlags": False,
                "loadOutput": False,
                "flagLayerNames": [],
            },
            "pauseAfterExecution": False,
            "source": {"type": "xml", "data": xml},
            "metadata": {"originalName": "test"},
            "tooltip": "tip",
        }

    def test_returns_workflow_item_instance(self, simple_model_xml):
        item = load_from_json(self._item_dict(simple_model_xml))
        assert isinstance(item, DSGToolsWorkflowItem)

    def test_display_name_preserved(self, simple_model_xml):
        item = load_from_json(self._item_dict(simple_model_xml))
        assert item.displayName == "Test"

    def test_flags_on_flags_raised_preserved(self, simple_model_xml):
        item = load_from_json(self._item_dict(simple_model_xml))
        assert item.flags.onFlagsRaised == "halt"

    def test_pause_after_execution_preserved(self, simple_model_xml):
        d = self._item_dict(simple_model_xml)
        d["pauseAfterExecution"] = True
        item = load_from_json(d)
        assert item.pauseAfterExecution is True

    def test_flag_layer_names_preserved(self, simple_model_xml):
        d = self._item_dict(simple_model_xml)
        d["flags"]["flagLayerNames"] = ["lyr_a"]
        item = load_from_json(d)
        assert item.getFlagNames() == ["lyr_a"]

    def test_metadata_original_name_preserved(self, simple_model_xml):
        item = load_from_json(self._item_dict(simple_model_xml))
        assert item.metadata.originalName == "test"

    def test_initial_status_after_load(self, simple_model_xml):
        item = load_from_json(self._item_dict(simple_model_xml))
        assert item.getStatus() == ExecutionStatus.INITIAL

    def test_invalid_flags_raises_value_error(self, simple_model_xml):
        d = self._item_dict(simple_model_xml)
        d["flags"]["onFlagsRaised"] = "invalid"
        with pytest.raises(ValueError):
            load_from_json(d)
