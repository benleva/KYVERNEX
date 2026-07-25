from kyvernex import CognitiveState, KyvernexEngine, ValidationOutcome


def test_valid_input_is_preserved_and_validated() -> None:
    engine = KyvernexEngine()
    result = engine.execute("Il cielo è blu.", source="test-suite", session_id="session-1")

    assert result.cognitive_object.original_content == "Il cielo è blu."
    assert result.cognitive_object.source == "test-suite"
    assert result.cognitive_object.state == CognitiveState.VALIDATED
    assert result.validation.outcome == ValidationOutcome.VALIDATED
    assert len(result.audit) == 5
    assert result.audit[0].component == "CORE-001"
    assert result.audit[2].component == "RULE_ENGINE"
    assert result.audit[-1].component == "CORE-008"


def test_missing_source_is_incomplete() -> None:
    engine = KyvernexEngine()
    result = engine.execute("contenuto", source="")

    assert result.validation.outcome == ValidationOutcome.INCOMPLETE
    assert "ORIGINE_MANCANTE" in result.validation.errors


def test_empty_input_is_not_presented_as_valid() -> None:
    engine = KyvernexEngine()
    result = engine.execute("", source="test-suite")

    assert result.validation.outcome == ValidationOutcome.INCOMPLETE
    assert result.cognitive_object.state != CognitiveState.VALIDATED
    assert "CONTENUTO_ORIGINALE_MANCANTE" in result.validation.errors


def test_sessions_are_isolated() -> None:
    engine = KyvernexEngine()
    first = engine.execute("uno", source="test-suite")
    second = engine.execute("due", source="test-suite")

    assert first.session_id != second.session_id
    assert first.cognitive_object.object_id != second.cognitive_object.object_id
