from __future__ import annotations

from dataclasses import dataclass, replace

from .adapters import AdapterResponse
from .core import ContinuousValidator
from .memory import SessionMemory
from .models import (
    AuditEvent,
    CognitiveCategory,
    CognitiveObject,
    CognitiveState,
    ValidationOutcome,
    ValidationRecord,
)
from .rules import RuleEngine


@dataclass(slots=True, frozen=True)
class GovernedResponse:
    cognitive_object: CognitiveObject
    validation: ValidationRecord
    audit: tuple[AuditEvent, ...]


class ResponseGovernor:
    """Converts an adapter response into a linked and governed cognitive object."""

    def __init__(
        self,
        *,
        memory: SessionMemory,
        rule_engine: RuleEngine | None = None,
    ) -> None:
        self._memory = memory
        self._rule_engine = rule_engine or RuleEngine()
        self._validator = ContinuousValidator(self._rule_engine)

    def govern(
        self,
        response: AdapterResponse,
        *,
        session_id: str,
        parent_object_id: str,
    ) -> GovernedResponse:
        obj = CognitiveObject(
            original_content=response.content,
            source=f"AI_ADAPTER:{response.adapter_name}:{response.model}",
            category=CognitiveCategory.RESULT,
            state=CognitiveState.NORMALIZED,
            transformations=[
                "AI_RESPONSE:ACQUISIZIONE_CONTROLLATA",
                "AI_RESPONSE:COLLEGAMENTO_ORIGINE",
            ],
            metadata={
                "derived_from_object_id": parent_object_id,
                "adapter_name": response.adapter_name,
                "model": response.model,
                "adapter_metadata": dict(response.metadata),
            },
        )

        audit: list[AuditEvent] = [
            AuditEvent.create(
                session_id=session_id,
                component="RESPONSE_GOVERNANCE",
                event_type="RISPOSTA_TRASFORMATA_IN_OGGETTO",
                object_id=obj.object_id,
                details={"derived_from_object_id": parent_object_id},
            )
        ]

        rule_results = self._rule_engine.evaluate(obj)
        obj.applied_rules.extend(result.rule_id for result in rule_results)
        validation = self._validator.validate(obj)
        if validation.outcome == ValidationOutcome.VALIDATED:
            obj = replace(obj, state=CognitiveState.VALIDATED)

        audit.append(
            AuditEvent.create(
                session_id=session_id,
                component="RESPONSE_GOVERNANCE",
                event_type="RISPOSTA_VALIDATA",
                object_id=obj.object_id,
                details={
                    "outcome": validation.outcome.value,
                    "derived_from_object_id": parent_object_id,
                },
            )
        )

        self._memory.store(session_id, obj)
        audit.append(
            AuditEvent.create(
                session_id=session_id,
                component="MEMORY",
                event_type="RISPOSTA_AI_MEMORIZZATA",
                object_id=obj.object_id,
                details={
                    "derived_from_object_id": parent_object_id,
                    "session_object_count": self._memory.count(session_id),
                },
            )
        )

        return GovernedResponse(
            cognitive_object=obj,
            validation=validation,
            audit=tuple(audit),
        )
