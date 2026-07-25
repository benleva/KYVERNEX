from __future__ import annotations

import pytest

from kyvernex import (
    AuditEvent,
    CognitiveGraph,
    CognitiveObject,
    CognitiveRelation,
    KyvernexUnitOfWork,
    RelationType,
    SessionMemory,
    UnitOfWorkCommitError,
    UnitOfWorkState,
)


class RecordingAuditSink:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def append(self, event: AuditEvent) -> None:
        self.events.append(event)

    def append_many(self, events: object) -> None:
        self.events.extend(events)  # type: ignore[arg-type]


class FailingAuditSink:
    def append(self, event: AuditEvent) -> None:
        raise RuntimeError("AUDIT_NON_DISPONIBILE")

    def append_many(self, events: object) -> None:
        raise RuntimeError("AUDIT_NON_DISPONIBILE")


def test_commit_coordinates_memory_graph_and_audit() -> None:
    memory = SessionMemory()
    graph = CognitiveGraph()
    sink = RecordingAuditSink()
    first = CognitiveObject(original_content="A", source="test")
    second = CognitiveObject(original_content="B", source="test")
    relation = CognitiveRelation(
        session_id="session-1",
        source_object_id=first.object_id,
        target_object_id=second.object_id,
        relation_type=RelationType.SUPPORTS,
    )

    transaction = KyvernexUnitOfWork(
        session_id="session-1",
        memory=memory,
        graph=graph,
        audit_sink=sink,
    )
    transaction.begin()
    transaction.stage_object(first)
    transaction.stage_object(second)
    transaction.stage_relation(relation)
    transaction.stage_audit(
        AuditEvent.create(
            session_id="session-1",
            component="TEST",
            event_type="OPERAZIONE_PREPARATA",
        )
    )

    result = transaction.commit()

    assert result.state is UnitOfWorkState.COMMITTED
    assert memory.count("session-1") == 2
    assert graph.count("session-1") == 1
    assert len(sink.events) == 2
    assert sink.events[-1].event_type == "TRANSAZIONE_CONFERMATA"


def test_audit_failure_rolls_back_memory_and_graph() -> None:
    memory = SessionMemory()
    graph = CognitiveGraph()
    first = CognitiveObject(original_content="A", source="test")
    second = CognitiveObject(original_content="B", source="test")
    relation = CognitiveRelation(
        session_id="session-2",
        source_object_id=first.object_id,
        target_object_id=second.object_id,
        relation_type=RelationType.DERIVED_FROM,
    )
    transaction = KyvernexUnitOfWork(
        session_id="session-2",
        memory=memory,
        graph=graph,
        audit_sink=FailingAuditSink(),
    )
    transaction.begin()
    transaction.stage_object(first)
    transaction.stage_object(second)
    transaction.stage_relation(relation)

    with pytest.raises(UnitOfWorkCommitError):
        transaction.commit()

    assert transaction.state is UnitOfWorkState.FAILED
    assert memory.count("session-2") == 0
    assert graph.count("session-2") == 0


def test_relation_requires_existing_or_staged_endpoints() -> None:
    transaction = KyvernexUnitOfWork(
        session_id="session-3",
        memory=SessionMemory(),
        graph=CognitiveGraph(),
    )
    transaction.begin()
    relation = CognitiveRelation(
        session_id="session-3",
        source_object_id="missing-a",
        target_object_id="missing-b",
        relation_type=RelationType.REFERENCES,
    )

    with pytest.raises(RuntimeError, match="INTEGRITA_REFERENZIALE_NON_SODDISFATTA"):
        transaction.stage_relation(relation)


def test_context_manager_commits_active_transaction() -> None:
    memory = SessionMemory()
    graph = CognitiveGraph()
    obj = CognitiveObject(original_content="context", source="test")

    with KyvernexUnitOfWork(session_id="session-4", memory=memory, graph=graph) as transaction:
        transaction.stage_object(obj)

    assert transaction.state is UnitOfWorkState.COMMITTED
    assert memory.get("session-4", obj.object_id) is not None
