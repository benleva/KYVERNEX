import json

import pytest

from kyvernex import (
    CognitiveGraph,
    CognitiveObject,
    DeletionJournalError,
    DeletionPolicy,
    DurableDeletionCoordinator,
    RelationType,
    SessionMemory,
)


def _setup(tmp_path):
    memory = SessionMemory()
    graph = CognitiveGraph()
    first = CognitiveObject(original_content="first", source="test")
    second = CognitiveObject(original_content="second", source="test")
    memory.store("s1", first)
    memory.store("s1", second)
    relation = graph.connect(
        session_id="s1",
        source_object_id=second.object_id,
        target_object_id=first.object_id,
        relation_type=RelationType.DERIVED_FROM,
    )
    coordinator = DurableDeletionCoordinator(
        memory=memory,
        graph=graph,
        journal_path=tmp_path / "deletion-journal.json",
    )
    return memory, graph, coordinator, first, second, relation


def test_successful_cascade_removes_journal(tmp_path):
    memory, graph, coordinator, first, _, _ = _setup(tmp_path)

    result = coordinator.delete(
        session_id="s1",
        object_id=first.object_id,
        policy=DeletionPolicy.CASCADE,
    )

    assert result.removed_object.object_id == first.object_id
    assert memory.get("s1", first.object_id) is None
    assert graph.count("s1") == 0
    assert not coordinator.journal_path.exists()


def test_recovery_restores_relations_when_object_still_exists(tmp_path):
    memory, graph, coordinator, first, second, relation = _setup(tmp_path)
    graph.remove(relation.session_id, relation.relation_id)
    payload = {
        "format_version": coordinator.FORMAT_VERSION,
        "transaction_id": "tx-rollback",
        "state": "PREPARED",
        "session_id": "s1",
        "object_id": first.object_id,
        "policy": "CASCADE",
        "relations": [coordinator._encode_relation(relation)],
    }
    coordinator.journal_path.write_text(json.dumps(payload), encoding="utf-8")

    recovery = coordinator.recover()

    assert recovery is not None
    assert recovery.action == "ROLLBACK_RELATIONS_RESTORED"
    assert graph.related_object_ids("s1", first.object_id) == (second.object_id,)
    assert not coordinator.journal_path.exists()


def test_recovery_completes_deletion_when_object_is_absent(tmp_path):
    memory, graph, coordinator, first, _, relation = _setup(tmp_path)
    memory.remove("s1", first.object_id)
    payload = {
        "format_version": coordinator.FORMAT_VERSION,
        "transaction_id": "tx-commit",
        "state": "MEMORY_APPLIED",
        "session_id": "s1",
        "object_id": first.object_id,
        "policy": "CASCADE",
        "relations": [coordinator._encode_relation(relation)],
    }
    coordinator.journal_path.write_text(json.dumps(payload), encoding="utf-8")

    recovery = coordinator.recover()

    assert recovery is not None
    assert recovery.action == "COMMIT_ORPHAN_RELATIONS_REMOVED"
    assert graph.count("s1") == 0
    assert not coordinator.journal_path.exists()


def test_invalid_journal_is_rejected(tmp_path):
    path = tmp_path / "deletion-journal.json"
    path.write_text("not-json", encoding="utf-8")

    with pytest.raises(DeletionJournalError):
        DurableDeletionCoordinator(
            memory=SessionMemory(),
            graph=CognitiveGraph(),
            journal_path=path,
        )
