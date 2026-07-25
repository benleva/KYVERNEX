from __future__ import annotations

import pytest

from kyvernex.plugin_adapter import InProcessAdapterError, InProcessCallableAdapter
from kyvernex.plugin_runtime import KyvernexPluginRuntime


def governed_request(request_id: str = "adapter-1") -> dict:
    return {
        "request_id": request_id,
        "operation": "governed.execute",
        "input": {"value": 7},
        "context": {},
        "requested_capabilities": ["governed.execute"],
        "authorization": {
            "principal": "host-principal",
            "grants": ["governed.execute"],
        },
        "limits": {"timeout_seconds": 10, "max_output_bytes": 4096},
    }


def test_adapter_declares_defensive_deterministic_capabilities():
    adapter = InProcessCallableAdapter(lambda request, authority: {}, capabilities={"governed.execute"})
    first = adapter.capabilities()
    first.add("ambient.admin")
    assert adapter.capabilities() == {"governed.execute"}


def test_runtime_authorizes_before_callable_is_invoked():
    calls = []

    def handler(request, authority):
        calls.append((dict(request), dict(authority)))
        return {"value": request["input"]["value"], "principal": authority["principal"]}

    adapter = InProcessCallableAdapter(handler, capabilities={"governed.execute"})
    runtime = KyvernexPluginRuntime(kyvernex_version="1.1.0", instance_id="adapter-runtime")
    runtime.initialize({"allowed_capabilities": ["governed.execute"]}, adapter)
    runtime.validate()

    response = runtime.execute(governed_request())

    assert response["status"] == "SUCCEEDED"
    assert response["result"] == {"value": 7, "principal": "host-principal"}
    assert len(calls) == 1


def test_blocked_request_never_reaches_callable():
    calls = []
    adapter = InProcessCallableAdapter(lambda request, authority: calls.append(1), capabilities={"governed.execute"})
    runtime = KyvernexPluginRuntime(kyvernex_version="1.1.0")
    runtime.initialize({"allowed_capabilities": ["governed.execute"]}, adapter)
    runtime.validate()
    request = governed_request("adapter-blocked")
    request["authorization"]["grants"] = []

    response = runtime.execute(request)

    assert response["status"] == "BLOCKED"
    assert calls == []


def test_non_json_result_becomes_structured_failed_response():
    adapter = InProcessCallableAdapter(lambda request, authority: {1, 2}, capabilities={"governed.execute"})
    runtime = KyvernexPluginRuntime(kyvernex_version="1.1.0")
    runtime.initialize({"allowed_capabilities": ["governed.execute"]}, adapter)
    runtime.validate()

    response = runtime.execute(governed_request("adapter-json"))

    assert response["status"] == "FAILED"
    assert response["error"]["code"] == "EXECUTION_FAILED"


def test_health_is_bounded_and_shutdown_is_idempotent():
    adapter = InProcessCallableAdapter(lambda request, authority: {}, capabilities=set())
    assert adapter.health() == {
        "status": "HEALTHY",
        "adapter_id": "kyvernex.adapter.in_process_callable",
        "adapter_version": "1.0.0",
        "invocation_count": 0,
    }

    adapter.shutdown()
    adapter.shutdown()

    assert adapter.health()["status"] == "SHUTDOWN"
    with pytest.raises(InProcessAdapterError):
        adapter.invoke({}, {})


def test_adapter_rejects_invalid_construction_and_inputs():
    with pytest.raises(TypeError):
        InProcessCallableAdapter(None, capabilities=set())
    with pytest.raises(TypeError):
        InProcessCallableAdapter(lambda request, authority: {}, capabilities=["governed.execute"])

    adapter = InProcessCallableAdapter(lambda request, authority: {}, capabilities=set())
    with pytest.raises(InProcessAdapterError):
        adapter.invoke([], {})
