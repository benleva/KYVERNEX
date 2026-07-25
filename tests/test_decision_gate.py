from kyvernex import (
    CognitiveConfidenceEngine,
    CognitiveDecisionExplainer,
    CognitiveDecisionGate,
    CognitiveGraph,
    CognitiveObject,
    DecisionDisposition,
    DecisionPolicy,
    JsonAuditTrace,
    SessionMemory,
)


def _gate(tmp_path, *, confidence: float, policy: DecisionPolicy | None = None):
    memory = SessionMemory()
    graph = CognitiveGraph()
    obj = CognitiveObject(
        original_content="decision",
        source="test",
        metadata={"confidence": confidence},
    )
    memory.store("s1", obj)
    trace = JsonAuditTrace(tmp_path / "audit.json")
    explainer = CognitiveDecisionExplainer(
        memory=memory,
        graph=graph,
        confidence_engine=CognitiveConfidenceEngine(memory=memory, graph=graph),
        audit_trace=trace,
    )
    return obj, CognitiveDecisionGate(explainer=explainer, policy=policy, audit_sink=trace), trace


def test_high_confidence_is_approved_with_reservation_when_dossier_has_reservations(tmp_path):
    obj, gate, trace = _gate(tmp_path, confidence=0.95)

    decision = gate.evaluate(session_id="s1", object_id=obj.object_id)

    assert decision.disposition is DecisionDisposition.APPROVED_WITH_RESERVATION
    assert trace.count(session_id="s1") == 1


def test_low_confidence_requires_manual_review(tmp_path):
    obj, gate, _ = _gate(tmp_path, confidence=0.20)

    decision = gate.evaluate(session_id="s1", object_id=obj.object_id)

    assert decision.disposition is DecisionDisposition.MANUAL_REVIEW
    assert "CONFIDENZA_INSUFFICIENTE" in decision.reasons


def test_verified_audit_policy_blocks_empty_unverified_dossier(tmp_path):
    obj, gate, _ = _gate(
        tmp_path,
        confidence=0.99,
        policy=DecisionPolicy(require_verified_audit=True),
    )

    decision = gate.evaluate(session_id="s1", object_id=obj.object_id)

    assert decision.disposition is DecisionDisposition.BLOCKED
    assert "AUDIT_NON_VERIFICATO" in decision.reasons


def test_invalid_thresholds_are_rejected():
    try:
        DecisionPolicy(approval_threshold=0.5, reservation_threshold=0.7)
    except ValueError as exc:
        assert str(exc) == "SOGLIE_DECISIONE_NON_VALIDE"
    else:
        raise AssertionError("expected ValueError")
