from __future__ import annotations

import pytest

from kyvernex import (
    CognitiveGraph,
    CognitiveObject,
    DeletionPolicy,
    InterProcessFileLock,
    ProcessLockError,
    ProcessSafeMultiTransactionDeletionCoordinator,
    SessionMemory,
)


def test_file_lock_rejects_second_holder_until_release(tmp_path):
    path = tmp_path / "journal.lock"
    first = InterProcessFileLock(path, timeout=0.1, poll_interval=0.01)
    second = InterProcessFileLock(path, timeout=0.05, poll_interval=0.01)

    first.acquire()
    try:
        with pytest.raises(ProcessLockError, match="PROCESS_LOCK_TIMEOUT"):
            second.acquire()
    finally:
        first.release()

    second.acquire()
    second.release()


def test_process_safe_coordinator_completes_cascade_deletion(tmp_path):
    memory = SessionMemory()
    graph = CognitiveGraph()
    left = CognitiveObject(original_content="left", source="test")
    right = CognitiveObject(original_content="right", source="test")
    memory.store("s", left)
    memory.store("s", right)
    graph.connect(
        session_id="s",
        source_object_id=left.object_id,
        target_object_id=right.object_id,
        relation_type="DERIVA_DA",
    )
    coordinator = ProcessSafeMultiTransactionDeletionCoordinator(
        memory=memory,
        graph=graph,
        journal_directory=tmp_path,
    )

    result = coordinator.delete(
        session_id="s",
        object_id=left.object_id,
        policy=DeletionPolicy.CASCADE,
    )

    assert result.object_id == left.object_id
    assert memory.get("s", left.object_id) is None
    assert graph.count("s") == 0
    assert coordinator.pending_transactions() == ()
    assert coordinator.process_lock_path.name == ".kyvernex-deletion.lock"


def test_invalid_lock_configuration_is_rejected(tmp_path):
    with pytest.raises(ValueError, match="LOCK_TIMEOUT_NEGATIVO"):
        InterProcessFileLock(tmp_path / "lock", timeout=-1)
    with pytest.raises(ValueError, match="LOCK_POLL_INTERVAL_NON_VALIDO"):
        InterProcessFileLock(tmp_path / "lock", poll_interval=0)
