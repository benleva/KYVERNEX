import json

import pytest

from kyvernex import (
    CognitiveObject,
    GraphPersistenceFormatError,
    JsonCognitiveGraph,
    ReferentialIntegrityError,
    RelationType,
    SessionMemory,
)


def _memory_with_pair(session_id: str = "session-1") -> tuple[SessionMemory, CognitiveObject, CognitiveObject]:
    memory = SessionMemory()
    source = CognitiveObject(original_content="input", source="test")
    target = CognitiveObject(original_content="output", source="test")
    memory.store(session_id, source)
    memory.store(session_id, target)
    return memory, source, target


def test_graph_survives_reopen(tmp_path) -> None:
    path = tmp_path / "graph.json"
    memory, source, target = _memory_with_pair()
    graph = JsonCognitiveGraph(path, memory=memory)
    relation = graph.connect(
        session_id="session-1",
        source_object_id=target.object_id,
        target_object_id=source.object_id,
        relation_type=RelationType.DERIVED_FROM,
    )

    reopened = JsonCognitiveGraph(path, memory=memory)

    assert reopened.count("session-1") == 1
    assert reopened.list("session-1")[0] == relation


def test_missing_endpoint_is_rejected(tmp_path) -> None:
    memory, source, _ = _memory_with_pair()
    graph = JsonCognitiveGraph(tmp_path / "graph.json", memory=memory)

    with pytest.raises(ReferentialIntegrityError, match="TARGET_OBJECT_NOT_FOUND"):
        graph.connect(
            session_id="session-1",
            source_object_id=source.object_id,
            target_object_id="missing-object",
            relation_type=RelationType.REFERENCES,
        )

    assert graph.count("session-1") == 0


def test_clear_is_persistent(tmp_path) -> None:
    path = tmp_path / "graph.json"
    memory, source, target = _memory_with_pair()
    graph = JsonCognitiveGraph(path, memory=memory)
    graph.connect(
        session_id="session-1",
        source_object_id=source.object_id,
        target_object_id=target.object_id,
        relation_type=RelationType.SUPPORTS,
    )

    assert graph.clear("session-1") == 1
    assert JsonCognitiveGraph(path, memory=memory).count("session-1") == 0


def test_corrupted_graph_is_not_silently_accepted(tmp_path) -> None:
    path = tmp_path / "graph.json"
    path.write_text("{broken", encoding="utf-8")

    with pytest.raises(GraphPersistenceFormatError, match="GRAPH_JSON_NON_VALIDO"):
        JsonCognitiveGraph(path, memory=SessionMemory())


def test_unsupported_format_version_is_rejected(tmp_path) -> None:
    path = tmp_path / "graph.json"
    path.write_text(
        json.dumps({"format_version": "999", "sessions": {}}),
        encoding="utf-8",
    )

    with pytest.raises(GraphPersistenceFormatError, match="GRAPH_FORMAT_VERSION_NON_SUPPORTATA"):
        JsonCognitiveGraph(path, memory=SessionMemory())


def test_persisted_dangling_relation_is_rejected_on_load(tmp_path) -> None:
    path = tmp_path / "graph.json"
    path.write_text(
        json.dumps(
            {
                "format_version": "0.1",
                "sessions": {
                    "session-1": [
                        {
                            "relation_id": "rel-1",
                            "source_object_id": "missing-a",
                            "target_object_id": "missing-b",
                            "relation_type": "DERIVA_DA",
                            "metadata": {},
                        }
                    ]
                },
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(GraphPersistenceFormatError, match="GRAPH_RELATION_DATA_NON_VALIDI"):
        JsonCognitiveGraph(path, memory=SessionMemory())
