from __future__ import annotations

from dataclasses import replace
from typing import Any
from uuid import uuid4

from .models import (
    AuditEvent,
    CognitiveCategory,
    CognitiveObject,
    CognitiveState,
    ExecutionResult,
    ValidationOutcome,
    ValidationRecord,
)


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
    """First executable subset of CORE-005."""

    def validate(self, obj: CognitiveObject) -> ValidationRecord:
        checks = ["OBJECT_ID", "SOURCE", "ORIGINAL_CONTENT", "CATEGORY", "STATE", "TRACEABILITY"]
        errors: list[str] = []
        reservations: list[str] = []

        if not obj.object_id:
            errors.append("OBJECT_ID_MANCANTE")
        if not obj.source.strip():
            errors.append("ORIGINE_MANCANTE")
        if obj.original_content is None or obj.original_content == "":
            errors.append("CONTENUTO_ORIGINALE_MANCANTE")
        if not obj.transformations:
            reservations.append("NESSUNA_TRASFORMAZIONE_REGISTRATA")
        reservations.extend(obj.limitations)

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
    """Reference Prototype 0.1: acquisition, AET, validation, audit, restitution."""

    def __init__(self) -> None:
        self._aet = AET()
        self._validator = ContinuousValidator()

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
        audit.append(
            AuditEvent.create(
                session_id=session,
                component="CORE-008",
                event_type="RISULTATO_RESTITUITO",
                object_id=obj.object_id,
                details={"validation": validation.outcome.value},
            )
        )

        return ExecutionResult(
            session_id=session,
            cognitive_object=obj,
            validation=validation,
            audit=tuple(audit),
        )
