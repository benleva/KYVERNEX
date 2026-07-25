from __future__ import annotations

from dataclasses import replace
from typing import Any
from uuid import uuid4

from .audit_sink import AuditSink, persist_audit
from .memory import SessionMemory
from .models import (
    AuditEvent,
    CognitiveCategory,
    CognitiveObject,
    CognitiveState,
    ExecutionResult,
    ValidationOutcome,
    ValidationRecord,
)
from .rules import RuleEngine, RuleSeverity


class AET:
    """Minimal translator: preserves the original input and declares uncertainty."""

    def translate(self, content: Any, *, source: str) -> CognitiveObject:
        limitations: list[str] = []
        if content is None or content == "":
            limitations.append("INPUT_VUOTO")
        return CognitiveObject(
            original_content=content,
            source=source,
            category=CognitiveCategory.DATA,
            state=CognitiveState.NORMALIZED,
            transformations=["AET:PRESERVAZIONE_ORIGINALE", "AET:NORMALIZZAZIONE_MINIMA"],
            limitations=limitations,
        )


class ContinuousValidator:
    """Executable subset of CORE-005 with deterministic ARGUS rules."""

    def __init__(self, rule_engine: RuleEngine | None = None) -> None:
        self._rule_engine = rule_engine or RuleEngine()

    def validate(self, obj: CognitiveObject) -> ValidationRecord:
        checks = ["OBJECT_ID", "CATEGORY", "STATE", "TRACEABILITY"]
        errors: list[str] = []
        reservations: list[str] = []

        if not obj.object_id:
            errors.append("OBJECT_ID_MANCANTE")

        rule_results = self._rule_engine.evaluate(obj)
        checks.extend(result.rule_id for result in rule_results)
        for result in rule_results:
            if result.passed:
                continue
            if result.severity == RuleSeverity.ERROR:
                errors.append(result.message)
            else:
                reservations.append(result.message)

        reservations.extend(obj.limitations)
        errors = list(dict.fromkeys(errors))
        reservations = list(dict.fromkeys(reservations))

        if errors:
            outcome = ValidationOutcome.INCOMPLETE
        elif reservations:
            outcome = ValidationOutcome.VALIDATED_WITH_RESERVATION
        else:
            outcome = ValidationOutcome.VALIDATED

        return ValidationRecord(
            outcome=outcome,
            checks=tuple(checks),
            errors=tuple(errors),
            reservations=tuple(reservations),
        )


class KyvernexEngine:
    """Reference Prototype 0.1 executable vertical slice."""

    def __init__(
        self,
        rule_engine: RuleEngine | None = None,
        memory: SessionMemory | None = None,
        audit_sink: AuditSink | None = None,
    ) -> None:
        self._aet = AET()
        self._rule_engine = rule_engine or RuleEngine()
        self._validator = ContinuousValidator(self._rule_engine)
        self._memory = memory or SessionMemory()
        self._audit_sink = audit_sink

    @property
    def memory(self) -> SessionMemory:
        return self._memory

    @property
    def audit_sink(self) -> AuditSink | None:
        return self._audit_sink

    def execute(self, content: Any, *, source: str, session_id: str | None = None) -> ExecutionResult:
        session = session_id or str(uuid4())
        audit: list[AuditEvent] = [
            AuditEvent.create(
                session_id=session,
                component="CORE-001",
                event_type="INPUT_ACQUISITO",
                details={"source": source},
            )
        ]

        obj = self._aet.translate(content, source=source)
        audit.append(
            AuditEvent.create(
                session_id=session,
                component="AET",
                event_type="OGGETTO_NORMALIZZATO",
                object_id=obj.object_id,
                details={"category": obj.category.value, "state": obj.state.value},
            )
        )

        rule_results = self._rule_engine.evaluate(obj)
        obj.applied_rules.extend(result.rule_id for result in rule_results)
        audit.append(
            AuditEvent.create(
                session_id=session,
                component="RULE_ENGINE",
                event_type="REGOLE_APPLICATE",
                object_id=obj.object_id,
                details={
                    "results": [
                        {
                            "rule_id": result.rule_id,
                            "passed": result.passed,
                            "severity": result.severity.value,
                            "message": result.message,
                        }
                        for result in rule_results
                    ]
                },
            )
        )

        validation = self._validator.validate(obj)
        if validation.outcome == ValidationOutcome.VALIDATED:
            obj = replace(obj, state=CognitiveState.VALIDATED)

        audit.append(
            AuditEvent.create(
                session_id=session,
                component="CORE-005",
                event_type="VALIDAZIONE_COMPLETATA",
                object_id=obj.object_id,
                details={
                    "outcome": validation.outcome.value,
                    "errors": list(validation.errors),
                    "reservations": list(validation.reservations),
                },
            )
        )

        self._memory.store(session, obj)
        audit.append(
            AuditEvent.create(
                session_id=session,
                component="MEMORY",
                event_type="OGGETTO_MEMORIZZATO",
                object_id=obj.object_id,
                details={"session_object_count": self._memory.count(session)},
            )
        )

        audit.append(
            AuditEvent.create(
                session_id=session,
                component="CORE-008",
                event_type="RISULTATO_RESTITUITO",
                object_id=obj.object_id,
                details={"validation": validation.outcome.value},
            )
        )

        result = ExecutionResult(
            session_id=session,
            cognitive_object=obj,
            validation=validation,
            audit=tuple(audit),
        )
        persist_audit(self._audit_sink, result.audit)
        return result
