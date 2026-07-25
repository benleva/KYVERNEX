from __future__ import annotations

import json

import pytest

from kyvernex import AuditEvent, AuditTraceError, JsonAuditTrace


def _event(session_id: str = "s", event_type: str = "TEST_EVENT") -> AuditEvent:
    return AuditEvent.create(
        session_id=session_id,
        component="TEST",
        event_type=event_type,
        object_id="object-1",
        details={"value": 1},
    )


def test_append_reload_and_verify(tmp_path):
    path = tmp_path / "audit.json"
    trace = JsonAuditTrace(path)
    first = trace.append(_event(event_type="FIRST"))
    second = trace.append(_event(event_type="SECOND"))

    reopened = JsonAuditTrace(path)

    assert reopened.verify() is True
    assert reopened.count() == 2
    assert first.sequence == 1
    assert second.sequence == 2
    assert second.previous_hash == first.record_hash


def test_append_many_preserves_order_and_session_filter(tmp_path):
    trace = JsonAuditTrace(tmp_path / "audit.json")

    records = trace.append_many((_event("a", "ONE"), _event("b", "TWO"), _event("a", "THREE")))

    assert tuple(record.sequence for record in records) == (1, 2, 3)
    assert trace.count(session_id="a") == 2
    assert tuple(record.event.event_type for record in trace.list(session_id="a")) == ("ONE", "THREE")


def test_tampered_event_is_detected_on_reload(tmp_path):
    path = tmp_path / "audit.json"
    trace = JsonAuditTrace(path)
    trace.append(_event())
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["records"][0]["event"]["details"]["value"] = 999
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(AuditTraceError, match="AUDIT_TRACE_HASH_MISMATCH"):
        JsonAuditTrace(path)


def test_broken_sequence_is_detected(tmp_path):
    path = tmp_path / "audit.json"
    trace = JsonAuditTrace(path)
    trace.append_many((_event(event_type="ONE"), _event(event_type="TWO")))
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["records"][1]["sequence"] = 9
    path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(AuditTraceError, match="AUDIT_TRACE_CHAIN_BROKEN"):
        JsonAuditTrace(path)


def test_unsupported_version_is_rejected(tmp_path):
    path = tmp_path / "audit.json"
    path.write_text(json.dumps({"format_version": "9", "records": []}), encoding="utf-8")

    with pytest.raises(AuditTraceError, match="AUDIT_TRACE_VERSION_UNSUPPORTED"):
        JsonAuditTrace(path)
