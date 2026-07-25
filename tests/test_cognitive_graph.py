import pytest

from kyvernex import (
    CognitiveGraph,
    EchoAdapter,
    KyvernexOrchestrator,
    RelationConflictError,
    RelationType,
)


def test_graph_isolates_sessions_and_supports_queries() -> None:
    graph = CognitiveGraph()
    first = graph.connect(
        session_id="session-a",
        source_object_id="result-1",
        target_object_id="input-1",
        relation_type=RelationType.DERIVED_FROM,
    )
    graph.connect(
        session_id="session-b",
        source_object_id="result-1",
        target_object_id="input-1",
        relation_type=RelationType.DERIVED_FROM,
    )

    assert graph.count("session-a") == 1
    assert graph.count("session-b") == 1
    assert graph.outgoing("session-a", "result-1") == (first,)
    assert graph.incoming("session-a", "input-1") == (first,)
    assert graph.related_object_ids("session-a", "result-1") == ("input-1",)


def test_graph_rejects_duplicate_and_self_relation() -> None:
    graph = CognitiveGraph()
    graph.connect(
        session_id="session-a",
        source_object_id="child",
        target_object_id="parent",
        relation_type=RelationType.DERIVED_FROM,
    )

    with pytest.raises(RelationConflictError):
        graph.connect(
            session_id="session-a",
            source_object_id="child",
            target_object_id="parent",
            relation_type=RelationType.DERIVED_FROM,
        )

    with pytest.raises(ValueError, match="AUTO_RELAZIONE_NON_AMMESSA"):
        graph.connect(
            session_id="session-a",
            source_object_id="same",
            target_object_id="same",
            relation_type=RelationType.REFERENCES,
        )


def test_governed_ai_response_creates_derived_from_relation() -> None:
    orchestrator = KyvernexOrchestrator(EchoAdapter())
    result = orchestrator.execute(
        "Il cielo è blu.",
        source="test-suite",
        session_id="session-graph",
    )

    governed_response = result.response_governance
    assert governed_response is not None
    relation = governed_response.relation
    assert relation.relation_type == RelationType.DERIVED_FROM
    assert relation.source_object_id == governed_response.cognitive_object.object_id
    assert relation.target_object_id == result.governance.cognitive_object.object_id
    assert orchestrator.graph.count("session-graph") == 1
    assert any(
        event.event_type == "RELAZIONE_COGNITIVA_REGISTRATA"
        for event in result.adapter_audit
    )
