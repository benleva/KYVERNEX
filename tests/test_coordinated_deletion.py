import pytest

from kyvernex import (
    CognitiveDeletionCoordinator,
    CognitiveGraph,
    CognitiveObject,
    DeletionPolicy,
    DeletionRestrictedError,
    RelationType,
    SessionMemory,
)


def build_state():
    memory = SessionMemory()
    graph = CognitiveGraph()
    parent = CognitiveObject(original_content="parent", source="test")
    child = CognitiveObject(original_content="child", source="test")
    memory.store("s1", parent)
    memory.store("s1", child)
    relation = graph.connect(
        session_id="s1",
        source_object_id=child.object_id,
        target_object_id=parent.object_id,
        relation_type=RelationType.DERIVED_FROM,
    )
    return memory, graph, parent, child, relation


def test_restrict_blocks_referenced_object_deletion():
    memory, graph, parent, child, relation = build_state()
    coordinator = CognitiveDeletionCoordinator(memory=memory, graph=graph)

    with pytest.raises(DeletionRestrictedError):
        coordinator.delete(
            session_id="s1",
            object_id=parent.object_id,
            policy=DeletionPolicy.RESTRICT,
        )

    assert memory.get("s1", parent.object_id) is not None
    assert graph.count("s1") == 1


def test_cascade_removes_object_and_linked_relations():
    memory, graph, parent, child, relation = build_state()
    coordinator = CognitiveDeletionCoordinator(memory=memory, graph=graph)

    result = coordinator.delete(
        session_id="s1",
        object_id=parent.object_id,
        policy=DeletionPolicy.CASCADE,
    )

    assert result.removed_object.object_id == parent.object_id
    assert result.removed_relations == (relation,)
    assert memory.get("s1", parent.object_id) is None
    assert memory.get("s1", child.object_id) is not None
    assert graph.count("s1") == 0
    assert [event.event_type for event in result.audit] == [
        "CANCELLAZIONE_PREPARATA",
        "RELAZIONI_COLLEGATE_RIMOSSE",
        "OGGETTO_COGNITIVO_RIMOSSO",
        "CANCELLAZIONE_COMPLETATA",
    ]


def test_unreferenced_object_can_be_deleted_with_restrict():
    memory = SessionMemory()
    graph = CognitiveGraph()
    obj = CognitiveObject(original_content="isolated", source="test")
    memory.store("s1", obj)
    coordinator = CognitiveDeletionCoordinator(memory=memory, graph=graph)

    result = coordinator.delete(session_id="s1", object_id=obj.object_id)

    assert result.removed_relations == ()
    assert memory.get("s1", obj.object_id) is None


def test_missing_object_is_explicit():
    coordinator = CognitiveDeletionCoordinator(memory=SessionMemory(), graph=CognitiveGraph())
    with pytest.raises(KeyError, match="OBJECT_NOT_FOUND"):
        coordinator.delete(session_id="s1", object_id="missing")
