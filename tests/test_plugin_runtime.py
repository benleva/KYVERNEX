from __future__ import annotations

import pytest

from kyvernex.plugin_runtime import (
    KyvernexPluginRuntime,
    PluginRuntimeError,
    PluginState,
)


class RecordingAdapter:
    adapter_id = "test.adapter"
    adapter_version = "1.0.0"

    def __init__(self) -> None:
        self.shutdown_calls = 0
        self.invocations: list[tuple[dict, dict]] = []

    def capabilities(self) -> set[str]:
        return {"governed.execute", "filesystem.read"}

    def invoke(self, request, authority):
        self.invocations.append((dict(request), dict(authority)))
        return {"accepted": True, "request_id": request.get("request_id")}

    def health(self):
        return {"status": "HEALTHY"}

    def shutdown(self) -> None:
        self.shutdown_calls += 1


class FailingAdapter(RecordingAdapter):
    def invoke(self, request, authority):
        raise RuntimeError("host failure")


def build_ready_runtime(adapter=None):
    runtime = KyvernexPluginRuntime(kyvernex_version="1.1.0", instance_id="instance-1")
    adapter = adapter or RecordingAdapter()
    runtime.initialize(
        {
            "plugin_api_version": "1.0.0",
            "allowed_capabilities": ["governed.execute", "network.access"],
        },
        adapter,
    )
    runtime.validate()
    return runtime, adapter


def test_created_initialize_validate_ready_lifecycle():
    runtime = KyvernexPluginRuntime(kyvernex_version="1.1.0", instance_id="instance-1")
    adapter = RecordingAdapter()

    assert runtime.state is PluginState.CREATED
    initialized = runtime.initialize(
        {"plugin_api_version": "1.0.0", "allowed_capabilities": ["governed.execute"]},
        adapter,
    )
    assert initialized["state"] == "INITIALIZED"

    ready = runtime.validate()
    assert ready["state"] == "READY"
    assert ready["capabilities"] == ["governed.execute"]


def test_capabilities_are_intersection_not_union():
    runtime, _ = build_ready_runtime()
    assert runtime.status()["capabilities"] == ["governed.execute"]


def test_execute_transitions_back_to_ready():
    runtime, adapter = build_ready_runtime()

    result = runtime.execute(
        {"request_id": "r-1"},
        authority={"capabilities": ["governed.execute"]},
    )

    assert result == {"accepted": True, "request_id": "r-1"}
    assert runtime.state is PluginState.READY
    assert runtime.status()["last_completed_request_status"] == "SUCCEEDED"
    assert adapter.invocations == [
        (
            {"request_id": "r-1"},
            {"capabilities": ["governed.execute"]},
        )
    ]


def test_execution_failure_returns_runtime_to_ready():
    runtime, _ = build_ready_runtime(FailingAdapter())

    with pytest.raises(PluginRuntimeError) as error:
        runtime.execute({"request_id": "r-2"})

    assert error.value.code == "EXECUTION_FAILED"
    assert runtime.state is PluginState.READY
    assert runtime.status()["last_completed_request_status"] == "FAILED"


def test_execute_before_ready_fails_closed():
    runtime = KyvernexPluginRuntime(kyvernex_version="1.1.0")

    with pytest.raises(PluginRuntimeError) as error:
        runtime.execute({"request_id": "r-3"})

    assert error.value.code == "PLUGIN_NOT_READY"
    assert runtime.state is PluginState.CREATED


def test_forbidden_transition_is_rejected():
    runtime = KyvernexPluginRuntime(kyvernex_version="1.1.0")

    with pytest.raises(PluginRuntimeError) as error:
        runtime.validate()

    assert error.value.code == "INVALID_LIFECYCLE_TRANSITION"
    assert runtime.state is PluginState.CREATED


def test_incompatible_api_is_rejected_without_state_change():
    runtime = KyvernexPluginRuntime(kyvernex_version="1.1.0")

    with pytest.raises(PluginRuntimeError) as error:
        runtime.initialize(
            {"plugin_api_version": "2.0.0", "allowed_capabilities": []},
            RecordingAdapter(),
        )

    assert error.value.code == "INCOMPATIBLE_PLUGIN_API"
    assert runtime.state is PluginState.CREATED


def test_shutdown_is_terminal_and_adapter_shutdown_is_once():
    runtime, adapter = build_ready_runtime()

    first = runtime.shutdown()
    second = runtime.shutdown()

    assert first["state"] == "SHUTDOWN"
    assert second["state"] == "SHUTDOWN"
    assert runtime.state is PluginState.SHUTDOWN
    assert adapter.shutdown_calls == 1

    with pytest.raises(PluginRuntimeError) as error:
        runtime.initialize({}, adapter)
    assert error.value.code == "INVALID_LIFECYCLE_TRANSITION"


def test_status_is_non_mutating_and_reports_zero_default_authority():
    runtime, _ = build_ready_runtime()
    before = runtime.state

    status = runtime.status()

    assert runtime.state is before
    assert status["authority"] == {
        "filesystem": "NONE",
        "network": "DISABLED",
        "process": "DISABLED",
        "repository": "FORBIDDEN",
    }
    assert "config" not in status
