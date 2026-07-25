from kyvernex import CognitiveCategory, CognitiveState, EchoAdapter, KyvernexOrchestrator


def test_adapter_response_becomes_linked_cognitive_object() -> None:
    orchestrator = KyvernexOrchestrator(EchoAdapter(prefix="RISPOSTA"))

    result = orchestrator.execute("domanda", source="test-suite", session_id="session-response")

    assert result.blocked is False
    assert result.response_governance is not None
    response_obj = result.response_governance.cognitive_object
    input_obj = result.governance.cognitive_object

    assert response_obj.category == CognitiveCategory.RESULT
    assert response_obj.state == CognitiveState.VALIDATED
    assert response_obj.object_id != input_obj.object_id
    assert response_obj.metadata["derived_from_object_id"] == input_obj.object_id
    assert response_obj.original_content == "RISPOSTA: domanda"


def test_input_and_response_are_both_stored_in_same_session() -> None:
    orchestrator = KyvernexOrchestrator(EchoAdapter())

    result = orchestrator.execute("contenuto", source="test-suite", session_id="session-memory")

    assert result.response_governance is not None
    stored = orchestrator.engine.memory.list("session-memory")
    assert len(stored) == 2
    assert {obj.object_id for obj in stored} == {
        result.governance.cognitive_object.object_id,
        result.response_governance.cognitive_object.object_id,
    }


def test_governed_response_audit_contains_lineage_and_memory_events() -> None:
    orchestrator = KyvernexOrchestrator(EchoAdapter())

    result = orchestrator.execute("contenuto", source="test-suite")

    event_types = [event.event_type for event in result.adapter_audit]
    assert "RISPOSTA_TRASFORMATA_IN_OGGETTO" in event_types
    assert "RISPOSTA_VALIDATA" in event_types
    assert "RISPOSTA_AI_MEMORIZZATA" in event_types
