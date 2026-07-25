from pathlib import Path

import pytest

from kyvernex import (
    AuditEvent,
    CognitiveConfidenceEngine,
    CognitiveDecisionExplainer,
    CognitiveGraph,
    CognitiveObject,
    ExplainabilityError,
    JsonAuditTrace,
    RelationType,
    SessionMemory,
)


def test_builds_dossier_with_graph_confidence_and_audit(tmp_path: Path) -> None:
    memory = SessionMemory()
    graph = CognitiveGraph()
    session_id = "session-1"
    source = CognitiveObject(original_content="source", source="test", metadata={"confidence": 0.8})
    decision = CognitiveObject(original_content="decision", source="test", metadata={"confidence": 0.4})
    memory.store(session_id, source)
    memory.store(session_id, decision)
    graph.connect(
        session_id=session_id,
        source_object_id=source.object_id,
        target_object_id=decision.object_id,
        relation_type=RelationType.SUPPORTS,
    )
    trace = JsonAuditTrace(tmp_path / "audit.json")
    trace.append(
        AuditEvent.create(
            session_id=session_id,
            component="TEST",
            event_type="DECISIONE_CREATA",
            object_id=decision.object_id,
        )
    )
    explainer = CognitiveDecisionExplainer(
        memory=memory,
        graph=graph,
        confidence_engine=CognitiveConfidenceEngine(memory=memory, graph=graph),
        audit_trace=trace,
    )

    dossier = explainer.explain(session_id=session_id, object_id=decision.object_id)

    assert dossier.cognitive_object.object_id == decision.object_id
    assert dossier.confidence.propagated_confidence == pytest.approx(0.88)
    assert len(dossier.incoming_relations) == 1
    assert len(dossier.audit_records) == 1
    assert dossier.audit_integrity_verified is True


def test_reports_missing_optional_evidence() -> None:
    memory = SessionMemory()
    graph = CognitiveGraph()
    obj = CognitiveObject(original_content="isolated", source="test")
    memory.store("session-1", obj)
    explainer = CognitiveDecisionExplainer(
        memory=memory,
        graph=graph,
        confidence_engine=CognitiveConfidenceEngine(memory=memory, graph=graph),
    )

    dossier = explainer.explain(session_id="session-1", object_id=obj.object_id)

    assert "AUDIT_TRACE_NON_CONFIGURATO" in dossier.reservations
    assert "NESSUNA_REVISIONE_PRECEDENTE" in dossier.reservations
    assert "OGGETTO_ISOLATO_NEL_GRAFO" in dossier.reservations


def test_rejects_unknown_object() -> None:
    memory = SessionMemory()
    graph = CognitiveGraph()
    explainer = CognitiveDecisionExplainer(
        memory=memory,
        graph=graph,
        confidence_engine=CognitiveConfidenceEngine(memory=memory, graph=graph),
    )

    with pytest.raises(ExplainabilityError, match="OGGETTO_COGNITIVO_NON_TROVATO"):
        explainer.explain(session_id="session-1", object_id="missing")
