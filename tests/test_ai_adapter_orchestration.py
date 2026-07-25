from kyvernex import (
    EchoAdapter,
    FailingAdapter,
    KyvernexOrchestrator,
    ValidationOutcome,
)


def test_valid_input_reaches_echo_adapter() -> None:
    orchestrator = KyvernexOrchestrator(EchoAdapter(prefix="MODEL"))

    result = orchestrator.execute("Analizza questo input", source="test-suite", session_id="session-ai-1")

    assert result.blocked is False
    assert result.error is None
    assert result.adapter_response is not None
    assert result.adapter_response.content == "MODEL: Analizza questo input"
    assert result.adapter_response.metadata["network_used"] is False
    assert result.adapter_audit[0].component == "AI_ADAPTER_GATE"
    assert any(
        event.event_type == "RISPOSTA_ADAPTER_RICEVUTA"
        for event in result.adapter_audit
    )


def test_invalid_input_is_blocked_before_adapter_invocation() -> None:
    orchestrator = KyvernexOrchestrator(EchoAdapter())

    result = orchestrator.execute("contenuto", source="", session_id="session-ai-2")

    assert result.governance.validation.outcome == ValidationOutcome.INCOMPLETE
    assert result.blocked is True
    assert result.adapter_response is None
    assert result.error == "ADAPTER_INVOCATION_BLOCKED_BY_GOVERNANCE"
    assert result.adapter_audit[-1].event_type == "INVOCAZIONE_BLOCCATA"


def test_controlled_adapter_failure_is_contained_and_audited() -> None:
    orchestrator = KyvernexOrchestrator(FailingAdapter())

    result = orchestrator.execute("input valido", source="test-suite")

    assert result.blocked is False
    assert result.adapter_response is None
    assert result.error == "ADAPTER_EXECUTION_FAILED"
    assert result.adapter_audit[-1].event_type == "ADAPTER_ERRORE_CONTROLLATO"


def test_governance_memory_keeps_original_object_not_adapter_output() -> None:
    orchestrator = KyvernexOrchestrator(EchoAdapter())

    result = orchestrator.execute("originale", source="test-suite", session_id="session-ai-3")
    stored = orchestrator.engine.memory.get("session-ai-3", result.governance.cognitive_object.object_id)

    assert stored is not None
    assert stored.original_content == "originale"
    assert result.adapter_response is not None
    assert stored.original_content != result.adapter_response.content
