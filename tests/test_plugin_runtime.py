from __future__ import annotations

import pytest

from kyvernex.plugin_runtime import KyvernexPluginRuntime, PluginRuntimeError, PluginState


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


def valid_request(request_id="r-1", *, grants=None, requested=None):
    return {
        "request_id": request_id,
        "operation": "governed.execute",
        "input": {"value": 1},
        "context": {},
        "requested_capabilities": requested or ["governed.execute"],
        "authorization": {
            "principal": "principal-1",
            "grants": grants if grants is not None else ["governed.execute"],
        },
        "limits": {
            "timeout_seconds": 10,
            "max_output_bytes": 4096,
        },
    }


def build_ready_runtime(adapter=None):
    runtime = KyvernexPluginRuntime(kyvernex_version="1.1.0", instance_id="instance-1")
    adapter = adapter or RecordingAdapter()
    runtime.initialize(
        {
            "plugin_api_version": "1.0.0",
            "allowed_capabilities": ["governed.execute", "network.access"],
            "limits": {"timeout_seconds": 30, "max_output_bytes": 8192},
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


def test_authorized_execute_returns_structured_success_response():
    runtime, adapter = build_ready_runtime()
    response = runtime.execute(valid_request())
    assert response["status"] == "SUCCEEDED"
    assert response["request_id"] == "r-1"
    assert response["result"] == {"accepted": True, "request_id": "r-1"}
    assert response["error"] is None
    assert response["decision"]["authorized"] is True
    assert response["evidence"]["execution_id"]
    assert response["plugin"]["plugin_id"] == "kyvernex.plugin.runtime"
    assert runtime.state is PluginState.READY
    assert adapter.invocations[0][1]["principal"] == "principal-1"


def test_missing_explicit_grant_returns_blocked_without_adapter_invocation():
    runtime, adapter = build_ready_runtime()
    response = runtime.execute(valid_request("r-blocked", grants=[]))
    assert response["status"] == "BLOCKED"
    assert response["result"] is None
    assert response["error"]["code"] == "AUTHORIZATION_REQUIRED"
    assert response["decision"]["authorized"] is False
    assert response["evidence"]["execution_id"] is None
    assert adapter.invocations == []
    assert runtime.state is PluginState.READY


def test_unnegotiated_capability_is_blocked():
    runtime, adapter = build_ready_runtime()
    response = runtime.execute(
        valid_request(
            "r-capability",
            grants=["governed.execute", "filesystem.read"],
            requested=["governed.execute", "filesystem.read"],
        )
    )
    assert response["status"] == "BLOCKED"
    assert response["error"]["code"] == "CAPABILITY_NOT_NEGOTIATED"
    assert adapter.invocations == []


def test_execution_failure_returns_structured_failed_response():
    runtime, _ = build_ready_runtime(FailingAdapter())
    response = runtime.execute(valid_request("r-failed"))
    assert response["status"] == "FAILED"
    assert response["result"] is None
    assert response["error"]["code"] == "EXECUTION_FAILED"
    assert response["decision"]["authorized"] is True
    assert runtime.state is PluginState.READY


def test_duplicate_request_id_is_rejected_even_after_blocked_outcome():
    runtime, _ = build_ready_runtime()
    runtime.execute(valid_request("r-duplicate", grants=[]))
    with pytest.raises(PluginRuntimeError) as error:
        runtime.execute(valid_request("r-duplicate"))
    assert error.value.code == "DUPLICATE_REQUEST_ID"


def test_unknown_request_field_is_rejected_before_execution():
    runtime, adapter = build_ready_runtime()
    request = valid_request("r-unknown")
    request["ambient_authority"] = True
    with pytest.raises(PluginRuntimeError) as error:
        runtime.execute(request)
    assert error.value.code == "REQUEST_SCHEMA_INVALID"
    assert adapter.invocations == []


def test_limits_cannot_exceed_configured_maximums():
    runtime, adapter = build_ready_runtime()
    request = valid_request("r-limit")
    request["limits"]["timeout_seconds"] = 31
    with pytest.raises(PluginRuntimeError) as error:
        runtime.execute(request)
    assert error.value.code == "REQUEST_SCHEMA_INVALID"
    assert adapter.invocations == []


def test_execute_before_ready_fails_closed():
    runtime = KyvernexPluginRuntime(kyvernex_version="1.1.0")
    with pytest.raises(PluginRuntimeError) as error:
        runtime.execute(valid_request("r-not-ready"))
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
        "filesystem": {"read_roots": (), "write_roots": ()},
        "network": {"enabled": False, "allowed_hosts": ()},
        "process": {"enabled": False, "allowed_commands": ()},
        "repository": "FORBIDDEN",
    }
    assert "config" not in status
