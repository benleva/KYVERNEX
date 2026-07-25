import json

import pytest

from kyvernex import (
    JsonSessionMemory,
    KyvernexEngine,
    PersistenceFormatError,
)


def test_objects_survive_memory_restart(tmp_path) -> None:
    path = tmp_path / "memory.json"
    first_memory = JsonSessionMemory(path)
    engine = KyvernexEngine(memory=first_memory)

    result = engine.execute("dato persistente", source="test-suite", session_id="session-a")

    second_memory = JsonSessionMemory(path)
    recovered = second_memory.get("session-a", result.cognitive_object.object_id)

    assert recovered is not None
    assert recovered.original_content == "dato persistente"
    assert recovered.source == "test-suite"
    assert second_memory.count("session-a") == 1


def test_sessions_remain_isolated_after_reload(tmp_path) -> None:
    path = tmp_path / "memory.json"
    memory = JsonSessionMemory(path)
    engine = KyvernexEngine(memory=memory)

    first = engine.execute("uno", source="test-suite", session_id="session-a")
    second = engine.execute("due", source="test-suite", session_id="session-b")

    reloaded = JsonSessionMemory(path)

    assert reloaded.get("session-a", first.cognitive_object.object_id) is not None
    assert reloaded.get("session-a", second.cognitive_object.object_id) is None
    assert reloaded.get("session-b", second.cognitive_object.object_id) is not None


def test_clear_is_persisted(tmp_path) -> None:
    path = tmp_path / "memory.json"
    memory = JsonSessionMemory(path)
    engine = KyvernexEngine(memory=memory)
    engine.execute("uno", source="test-suite", session_id="session-a")

    assert memory.clear("session-a") == 1
    assert JsonSessionMemory(path).count("session-a") == 0


def test_invalid_json_is_rejected_without_silent_reset(tmp_path) -> None:
    path = tmp_path / "memory.json"
    path.write_text("{broken", encoding="utf-8")

    with pytest.raises(PersistenceFormatError, match="FILE_MEMORIA_NON_VALIDO"):
        JsonSessionMemory(path)


def test_unsupported_format_version_is_rejected(tmp_path) -> None:
    path = tmp_path / "memory.json"
    path.write_text(
        json.dumps({"format_version": "999", "sessions": {}}),
        encoding="utf-8",
    )

    with pytest.raises(PersistenceFormatError, match="VERSIONE_FORMATO_MEMORIA_NON_SUPPORTATA"):
        JsonSessionMemory(path)
