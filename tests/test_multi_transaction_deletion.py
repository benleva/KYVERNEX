from __future__ import annotations

import json

import pytest

from kyvernex import (
    CognitiveGraph,
    CognitiveObject,
    DeletionJournalError,
    DeletionPolicy,
    MultiTransactionDeletionCoordinator,
    RelationType,
    SessionMemory,
)


def _store_pair(memory: SessionMemory, session_id: str = "s") -> tuple[CognitiveObject, CognitiveObject]:
    left = CognitiveObject(original_content="left", source="test")
    right = CognitiveObject(original_content="right", source="test")
    memory.store(session_id, left)
    memory.store(session_id, right)
    return left, right


def test_completed_deletion_removes_its_transaction_journal(tmp_path):
    memory = SessionMemory()
    graph = CognitiveGraph()
    left, right = _store_pair(memory)
    graph.connect(
        session_id="s",
        source_object_id=left.object_id,
        target_object_id=right.object_id,
        relation_type=RelationType.DERIVED_FROM,
    )
    coordinator = MultiTransactionDeletionCoordinator(
        memory=memory,
        graph=graph,
        journal_directory=tmp_path,
    )

    coordinator.delete(session_id="s", object_id=left.object_id, policy=DeletionPolicy.CASCADE)

    assert coordinator.pending_transactions() == ()
    assert memory.get("s", left.object_id) is None
    assert graph.count("s") == 0


def test_recovery_restores_relations_when_object_still_exists(tmp_path):
    memory = SessionMemory()
    graph = CognitiveGraph()
    left, right = _store_pair(memory)
    relation = graph.connect(
        session_id="s",
        source_object_id=left.object_id,
        target_object_id=right.object_id,
        relation_type=RelationType.DERIVED_FROM,
    )
    graph.remove(relation.relation_id, session_id="s")
    transaction_id = "tx-rollback"
    payload = {
        "format_version": "0.2",
        "transaction_id": transaction_id,
        "state": "PREPARED",
        "session_id": "s",
        "object_id": left.object_id,
        "policy": "CASCADE",
        "relations": [{
            "relation_id": relation.relation_id,
            "source_object_id": relation.source_object_id,
            "target_object_id": relation.target_object_id,
            "relation_type": relation.relation_type.value,
            "metadata": {},
        }],
    }
    (tmp_path / f"deletion-{transaction_id}.json").write_text(json.dumps(payload), encoding="utf-8")

    coordinator = MultiTransactionDeletionCoordinator(
        memory=memory,
        graph=graph,
        journal_directory=tmp_path,
        recover_on_startup=False,
    )
    batch = coordinator.recover_all()

    assert batch.recovered[0].action == "ROLLBACK_RELATIONS_RESTORED"
    assert graph.count("s") == 1
    assert coordinator.pending_transactions() == ()


def test_recovery_processes_multiple_independent_journals(tmp_path):
    memory = SessionMemory()
    graph = CognitiveGraph()
    first, second = _store_pair(memory)
    memory.remove("s", first.object_id)
    memory.remove("s", second.object_id)

    for transaction_id, object_id in (("tx-a", first.object_id), ("tx-b", second.object_id)):
        payload = {
            "format_version": "0.2",
            "transaction_id": transaction_id,
            "state": "MEMORY_APPLIED",
            "session_id": "s",
            "object_id": object_id,
            "policy": "CASCADE",
            "relations": [],
        }
        (tmp_path / f"deletion-{transaction_id}.json").write_text(json.dumps(payload), encoding="utf-8")

    coordinator = MultiTransactionDeletionCoordinator(
        memory=memory,
        graph=graph,
        journal_directory=tmp_path,
        recover_on_startup=False,
    )
    batch = coordinator.recover_all()

    assert len(batch.recovered) == 2
    assert {item.action for item in batch.recovered} == {"COMMIT_ORPHAN_RELATIONS_REMOVED"}
    assert coordinator.pending_transactions() == ()


def test_filename_transaction_mismatch_is_rejected(tmp_path):
    payload = {
        "format_version": "0.2",
        "transaction_id": "different-id",
        "state": "PREPARED",
        "session_id": "s",
        "object_id": "o",
        "policy": "CASCADE",
        "relations": [],
    }
    (tmp_path / "deletion-file-id.json").write_text(json.dumps(payload), encoding="utf-8")
    coordinator = MultiTransactionDeletionCoordinator(
        memory=SessionMemory(),
        graph=CognitiveGraph(),
        journal_directory=tmp_path,
        recover_on_startup=False,
    )

    with pytest.raises(DeletionJournalError, match="DELETION_JOURNAL_FILENAME_MISMATCH"):
        coordinator.recover_all()


def test_continue_on_error_reports_corrupt_journal_and_recovers_valid_one(tmp_path):
    (tmp_path / "deletion-bad.json").write_text("not-json", encoding="utf-8")
    payload = {
        "format_version": "0.2",
        "transaction_id": "good",
        "state": "MEMORY_APPLIED",
        "session_id": "s",
        "object_id": "gone",
        "policy": "CASCADE",
        "relations": [],
    }
    (tmp_path / "deletion-good.json").write_text(json.dumps(payload), encoding="utf-8")
    coordinator = MultiTransactionDeletionCoordinator(
        memory=SessionMemory(),
        graph=CognitiveGraph(),
        journal_directory=tmp_path,
        recover_on_startup=False,
    )

    batch = coordinator.recover_all(continue_on_error=True)

    assert len(batch.recovered) == 1
    assert batch.failed_journals == ("deletion-bad.json",)
