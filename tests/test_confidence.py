import pytest

from kyvernex import (
    CognitiveConfidenceEngine,
    CognitiveGraph,
    CognitiveObject,
    ConfidenceCycleError,
    ConfidenceError,
    RelationType,
    SessionMemory,
)


def _store(memory: SessionMemory, session_id: str, confidence: float | None) -> CognitiveObject:
    metadata = {} if confidence is None else {"confidence": confidence}
    obj = CognitiveObject(original_content="x", source="test", metadata=metadata)
    memory.store(session_id, obj)
    return obj


def test_direct_confidence_without_relations() -> None:
    memory = SessionMemory()
    graph = CognitiveGraph()
    obj = _store(memory, "s", 0.8)

    result = CognitiveConfidenceEngine(memory=memory, graph=graph).assess(
        session_id="s", object_id=obj.object_id
    )

    assert result.direct_confidence == pytest.approx(0.8)
    assert result.propagated_confidence == pytest.approx(0.8)
    assert "NESSUNA_EVIDENZA_RELAZIONALE" in result.reservations


def test_support_increases_confidence() -> None:
    memory = SessionMemory()
    graph = CognitiveGraph()
    target = _store(memory, "s", 0.4)
    supporter = _store(memory, "s", 0.5)
    graph.connect(
        session_id="s",
        source_object_id=supporter.object_id,
        target_object_id=target.object_id,
        relation_type=RelationType.SUPPORTS,
    )

    result = CognitiveConfidenceEngine(memory=memory, graph=graph).assess(
        session_id="s", object_id=target.object_id
    )

    assert result.propagated_confidence == pytest.approx(0.7)
    assert result.supporting_object_ids == (supporter.object_id,)


def test_contradiction_reduces_confidence() -> None:
    memory = SessionMemory()
    graph = CognitiveGraph()
    target = _store(memory, "s", 0.8)
    contradiction = _store(memory, "s", 0.5)
    graph.connect(
        session_id="s",
        source_object_id=contradiction.object_id,
        target_object_id=target.object_id,
        relation_type=RelationType.CONTRADICTS,
    )

    result = CognitiveConfidenceEngine(memory=memory, graph=graph).assess(
        session_id="s", object_id=target.object_id
    )

    assert result.propagated_confidence == pytest.approx(0.4)
    assert "CONTRADDIZIONI_PRESENTI" in result.reservations


def test_missing_confidence_uses_default() -> None:
    memory = SessionMemory()
    graph = CognitiveGraph()
    obj = _store(memory, "s", None)

    result = CognitiveConfidenceEngine(
        memory=memory, graph=graph, default_confidence=0.25
    ).assess(session_id="s", object_id=obj.object_id)

    assert result.direct_confidence == pytest.approx(0.25)
    assert "CONFIDENZA_DIRETTA_ASSENTE" in result.reservations


def test_invalid_confidence_is_rejected() -> None:
    memory = SessionMemory()
    graph = CognitiveGraph()
    obj = CognitiveObject(
        original_content="x", source="test", metadata={"confidence": "alta"}
    )
    memory.store("s", obj)

    with pytest.raises(ConfidenceError, match="CONFIDENZA_NON_NUMERICA"):
        CognitiveConfidenceEngine(memory=memory, graph=graph).assess(
            session_id="s", object_id=obj.object_id
        )


def test_cycle_is_detected() -> None:
    memory = SessionMemory()
    graph = CognitiveGraph()
    first = _store(memory, "s", 0.5)
    second = _store(memory, "s", 0.5)
    graph.connect(
        session_id="s",
        source_object_id=first.object_id,
        target_object_id=second.object_id,
        relation_type=RelationType.SUPPORTS,
    )
    graph.connect(
        session_id="s",
        source_object_id=second.object_id,
        target_object_id=first.object_id,
        relation_type=RelationType.SUPPORTS,
    )

    with pytest.raises(ConfidenceCycleError):
        CognitiveConfidenceEngine(memory=memory, graph=graph).assess(
            session_id="s", object_id=first.object_id
        )
