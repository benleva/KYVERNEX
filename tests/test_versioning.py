import pytest

from kyvernex import (
    CognitiveGraph,
    CognitiveObject,
    CognitiveVersionManager,
    RelationType,
    SessionMemory,
    VersionChangeType,
    VersionConflictError,
    VersioningError,
)


def build_manager():
    memory = SessionMemory()
    graph = CognitiveGraph()
    return memory, graph, CognitiveVersionManager(memory=memory, graph=graph)


def test_revision_creates_immutable_successor_and_relation():
    memory, graph, manager = build_manager()
    original = CognitiveObject(original_content="dato iniziale", source="utente")
    memory.store("s1", original)

    successor, transition = manager.revise(
        session_id="s1",
        object_id=original.object_id,
        change_type=VersionChangeType.CORRECTION,
        reason="correzione documentata",
        content="dato corretto",
    )

    assert successor.object_id != original.object_id
    assert successor.version == "0.2"
    assert memory.get("s1", original.object_id).original_content == "dato iniziale"
    assert memory.get("s1", successor.object_id).original_content == "dato corretto"
    assert transition.previous_object_id == original.object_id
    relations = graph.outgoing("s1", successor.object_id)
    assert len(relations) == 1
    assert relations[0].relation_type is RelationType.DERIVED_FROM
    assert relations[0].target_object_id == original.object_id


def test_history_returns_newest_to_oldest():
    memory, _, manager = build_manager()
    first = CognitiveObject(original_content="v1", source="utente")
    memory.store("s1", first)
    second, _ = manager.revise(
        session_id="s1",
        object_id=first.object_id,
        change_type=VersionChangeType.ENRICHMENT,
        reason="seconda versione",
        content="v2",
    )
    third, _ = manager.revise(
        session_id="s1",
        object_id=second.object_id,
        change_type=VersionChangeType.SUPERSESSION,
        reason="terza versione",
        content="v3",
    )

    assert [item.original_content for item in manager.history(session_id="s1", object_id=third.object_id)] == ["v3", "v2", "v1"]


def test_invalid_version_format_is_rejected_without_writes():
    memory, graph, manager = build_manager()
    original = CognitiveObject(original_content="dato", source="utente", version="alpha")
    memory.store("s1", original)

    with pytest.raises(VersionConflictError, match="FORMATO_VERSIONE_NON_VALIDO"):
        manager.revise(
            session_id="s1",
            object_id=original.object_id,
            change_type=VersionChangeType.CORRECTION,
            reason="test",
        )

    assert memory.count("s1") == 1
    assert graph.count("s1") == 0


def test_missing_object_is_rejected():
    _, _, manager = build_manager()
    with pytest.raises(VersioningError, match="OGGETTO_COGNITIVO_NON_TROVATO"):
        manager.revise(
            session_id="s1",
            object_id="missing",
            change_type=VersionChangeType.CORRECTION,
            reason="test",
        )
