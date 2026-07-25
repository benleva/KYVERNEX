from dataclasses import replace

import pytest

from kyvernex import CognitiveObject, MemoryConflictError, SessionMemory


def test_memory_is_isolated_by_session() -> None:
    memory = SessionMemory()
    first = CognitiveObject(original_content="uno", source="test")
    second = CognitiveObject(original_content="due", source="test")

    memory.store("session-a", first)
    memory.store("session-b", second)

    assert memory.get("session-a", first.object_id) is not None
    assert memory.get("session-a", second.object_id) is None
    assert memory.count("session-a") == 1
    assert memory.count("session-b") == 1


def test_memory_returns_defensive_copies() -> None:
    memory = SessionMemory()
    original = CognitiveObject(original_content="immutabile", source="test")
    memory.store("session-a", original)

    retrieved = memory.get("session-a", original.object_id)
    assert retrieved is not None
    retrieved.limitations.append("MUTAZIONE_ESTERNA")

    stored_again = memory.get("session-a", original.object_id)
    assert stored_again is not None
    assert "MUTAZIONE_ESTERNA" not in stored_again.limitations


def test_duplicate_object_id_is_rejected_inside_same_session() -> None:
    memory = SessionMemory()
    original = CognitiveObject(original_content="uno", source="test")
    duplicate = replace(original, original_content="due")

    memory.store("session-a", original)
    with pytest.raises(MemoryConflictError, match="OBJECT_ID_GIA_PRESENTE"):
        memory.store("session-a", duplicate)


def test_same_object_id_can_exist_in_different_sessions() -> None:
    memory = SessionMemory()
    obj = CognitiveObject(original_content="uno", source="test")

    memory.store("session-a", obj)
    memory.store("session-b", obj)

    assert memory.count("session-a") == 1
    assert memory.count("session-b") == 1


def test_clear_removes_only_selected_session() -> None:
    memory = SessionMemory()
    memory.store("session-a", CognitiveObject(original_content="uno", source="test"))
    memory.store("session-b", CognitiveObject(original_content="due", source="test"))

    assert memory.clear("session-a") == 1
    assert memory.count("session-a") == 0
    assert memory.count("session-b") == 1
