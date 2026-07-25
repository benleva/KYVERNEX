import json
from pathlib import Path

from kyvernex import (
    CognitiveObject,
    KyvernexEngine,
    Rule,
    RuleEngine,
    RuleSeverity,
    ValidationOutcome,
    to_primitive,
)


_REQUIRED_ENGINE_AUDIT_EVENTS = {
    "INPUT_ACQUISITO",
    "OGGETTO_NORMALIZZATO",
    "REGOLE_APPLICATE",
    "VALIDAZIONE_COMPLETATA",
    "OGGETTO_MEMORIZZATO",
    "RISULTATO_RESTITUITO",
}


def test_default_rules_are_recorded_in_object_and_audit() -> None:
    result = KyvernexEngine().execute("dato", source="test-suite")

    assert result.cognitive_object.applied_rules == ["ARGUS-R001", "ARGUS-R002", "ARGUS-R003"]
    assert result.audit[2].component == "RULE_ENGINE"
    assert result.validation.outcome == ValidationOutcome.VALIDATED


def test_custom_error_rule_blocks_validation() -> None:
    rule = Rule(
        rule_id="TEST-R001",
        description="Regola di prova sempre falsa.",
        severity=RuleSeverity.ERROR,
        predicate=lambda obj: False,
        failure_message="REGOLA_TEST_FALLITA",
    )
    engine = KyvernexEngine(rule_engine=RuleEngine((rule,)))

    result = engine.execute("dato", source="test-suite")

    assert result.validation.outcome == ValidationOutcome.INCOMPLETE
    assert "REGOLA_TEST_FALLITA" in result.validation.errors
    assert result.cognitive_object.applied_rules == ["TEST-R001"]


def test_rule_exception_is_converted_to_controlled_error() -> None:
    def broken(_: CognitiveObject) -> bool:
        raise RuntimeError("boom")

    rule = Rule(
        rule_id="TEST-R002",
        description="Regola non eseguibile.",
        severity=RuleSeverity.RESERVATION,
        predicate=broken,
        failure_message="NON_USATO",
    )
    result = RuleEngine((rule,)).evaluate(CognitiveObject(original_content="x", source="test"))[0]

    assert result.passed is False
    assert result.severity == RuleSeverity.ERROR
    assert result.message == "REGOLA_NON_ESEGUIBILE:RuntimeError"


def test_execution_result_matches_declared_top_level_schema_contract() -> None:
    schema = json.loads(Path("schemas/execution-result.schema.json").read_text(encoding="utf-8"))
    payload = to_primitive(KyvernexEngine().execute("dato", source="test-suite"))
    event_types = {event["event_type"] for event in payload["audit"]}

    assert set(payload) == set(schema["required"])
    assert set(payload["cognitive_object"]) == set(
        schema["properties"]["cognitive_object"]["required"]
    )
    assert set(payload["validation"]) == set(schema["properties"]["validation"]["required"])
    assert _REQUIRED_ENGINE_AUDIT_EVENTS <= event_types
