from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4


class CognitiveCategory(StrEnum):
    ENTITY = "ENTITA_COGNITIVA"
    DATA = "DATO"
    FACT = "FATTO"
    HYPOTHESIS = "IPOTESI"
    DEDUCTION = "DEDUZIONE"
    OPINION = "OPINIONE"
    RULE = "REGOLA"
    AXIOM = "ASSIOMA"
    META_RULE = "META_REGOLA"
    RELATION = "RELAZIONE"
    TRANSFORMATION = "TRASFORMAZIONE"
    RESULT = "RISULTATO"
    SOURCE = "FONTE_ORIGINE"
    STATE = "STATO_COGNITIVO"
    VALIDATION = "VALIDAZIONE"
    ERROR = "ERRORE"


class CognitiveState(StrEnum):
    ACQUIRED = "ACQUISITO"
    NORMALIZED = "NORMALIZZATO"
    PROCESSED = "ELABORATO"
    VALIDATED = "VALIDATO"
    CONSOLIDATED = "CONSOLIDATO"


class ValidationOutcome(StrEnum):
    VALIDATED = "VALIDATO"
    VALIDATED_WITH_RESERVATION = "VALIDATO_CON_RISERVA"
    NOT_VERIFIABLE = "NON_VERIFICABILE"
    INCOMPLETE = "INCOMPLETO"
    INCOMPATIBLE = "INCOMPATIBILE"
    REJECTED = "RIFIUTATO"
    ERROR = "ERRORE"


@dataclass(slots=True)
class CognitiveObject:
    original_content: Any
    source: str
    category: CognitiveCategory = CognitiveCategory.DATA
    state: CognitiveState = CognitiveState.ACQUIRED
    object_id: str = field(default_factory=lambda: str(uuid4()))
    version: str = "0.1"
    transformations: list[str] = field(default_factory=list)
    applied_rules: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class ValidationRecord:
    outcome: ValidationOutcome
    checks: tuple[str, ...]
    errors: tuple[str, ...] = ()
    reservations: tuple[str, ...] = ()


@dataclass(slots=True, frozen=True)
class AuditEvent:
    session_id: str
    operation_id: str
    component: str
    event_type: str
    timestamp: str
    object_id: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        session_id: str,
        component: str,
        event_type: str,
        object_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> "AuditEvent":
        return cls(
            session_id=session_id,
            operation_id=str(uuid4()),
            component=component,
            event_type=event_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            object_id=object_id,
            details=details or {},
        )


@dataclass(slots=True, frozen=True)
class ExecutionResult:
    session_id: str
    cognitive_object: CognitiveObject
    validation: ValidationRecord
    audit: tuple[AuditEvent, ...]
