from __future__ import annotations

from dataclasses import dataclass

from .adapters import AIAdapter, AdapterExecutionError, AdapterRequest, AdapterResponse
from .core import KyvernexEngine
from .graph import CognitiveGraph
from .models import AuditEvent, ExecutionResult, ValidationOutcome
from .response_governance import GovernedResponse, ResponseGovernor


@dataclass(slots=True, frozen=True)
class GovernedExecutionResult:
    governance: ExecutionResult
    adapter_response: AdapterResponse | None
    adapter_audit: tuple[AuditEvent, ...]
    blocked: bool
    error: str | None = None
    response_governance: GovernedResponse | None = None


class KyvernexOrchestrator:
    """Runs governance before and after a controlled AI-adapter invocation."""

    def __init__(
        self,
        adapter: AIAdapter,
        *,
        engine: KyvernexEngine | None = None,
        graph: CognitiveGraph | None = None,
    ) -> None:
        self._adapter = adapter
        self._engine = engine or KyvernexEngine()
        self._graph = graph or CognitiveGraph()
        self._response_governor = ResponseGovernor(
            memory=self._engine.memory,
            graph=self._graph,
        )

    @property
    def adapter(self) -> AIAdapter:
        return self._adapter

    @property
    def engine(self) -> KyvernexEngine:
        return self._engine

    @property
    def graph(self) -> CognitiveGraph:
        return self._graph

    def execute(
        self,
        content: object,
        *,
        source: str,
        session_id: str | None = None,
    ) -> GovernedExecutionResult:
        governance = self._engine.execute(content, source=source, session_id=session_id)
        obj = governance.cognitive_object
        audit: list[AuditEvent] = []

        if governance.validation.outcome in {
            ValidationOutcome.INCOMPLETE,
            ValidationOutcome.INCOMPATIBLE,
            ValidationOutcome.REJECTED,
            ValidationOutcome.ERROR,
        }:
            audit.append(
                AuditEvent.create(
                    session_id=governance.session_id,
                    component="AI_ADAPTER_GATE",
                    event_type="INVOCAZIONE_BLOCCATA",
                    object_id=obj.object_id,
                    details={"validation": governance.validation.outcome.value},
                )
            )
            return GovernedExecutionResult(
                governance=governance,
                adapter_response=None,
                adapter_audit=tuple(audit),
                blocked=True,
                error="ADAPTER_INVOCATION_BLOCKED_BY_GOVERNANCE",
            )

        request = AdapterRequest(
            session_id=governance.session_id,
            object_id=obj.object_id,
            content=obj.original_content,
            source=obj.source,
            metadata={
                "category": obj.category.value,
                "state": obj.state.value,
                "applied_rules": list(obj.applied_rules),
                "validation": governance.validation.outcome.value,
            },
        )
        audit.append(
            AuditEvent.create(
                session_id=governance.session_id,
                component="AI_ADAPTER_GATE",
                event_type="RICHIESTA_ADAPTER_PREPARATA",
                object_id=obj.object_id,
                details={"adapter": self._adapter.name},
            )
        )

        try:
            response = self._adapter.invoke(request)
        except AdapterExecutionError as exc:
            audit.append(
                AuditEvent.create(
                    session_id=governance.session_id,
                    component="AI_ADAPTER",
                    event_type="ADAPTER_ERRORE_CONTROLLATO",
                    object_id=obj.object_id,
                    details={"adapter": self._adapter.name, "error": str(exc)},
                )
            )
            return GovernedExecutionResult(
                governance=governance,
                adapter_response=None,
                adapter_audit=tuple(audit),
                blocked=False,
                error=str(exc),
            )
        except Exception as exc:  # defensive boundary for third-party adapters
            audit.append(
                AuditEvent.create(
                    session_id=governance.session_id,
                    component="AI_ADAPTER",
                    event_type="ADAPTER_ERRORE_IMPREVISTO",
                    object_id=obj.object_id,
                    details={"adapter": self._adapter.name, "error_type": type(exc).__name__},
                )
            )
            return GovernedExecutionResult(
                governance=governance,
                adapter_response=None,
                adapter_audit=tuple(audit),
                blocked=False,
                error="ADAPTER_UNEXPECTED_ERROR",
            )

        audit.append(
            AuditEvent.create(
                session_id=governance.session_id,
                component="AI_ADAPTER",
                event_type="RISPOSTA_ADAPTER_RICEVUTA",
                object_id=obj.object_id,
                details={
                    "adapter": response.adapter_name,
                    "model": response.model,
                },
            )
        )

        governed_response = self._response_governor.govern(
            response,
            session_id=governance.session_id,
            parent_object_id=obj.object_id,
        )
        audit.extend(governed_response.audit)

        return GovernedExecutionResult(
            governance=governance,
            adapter_response=response,
            adapter_audit=tuple(audit),
            blocked=False,
            response_governance=governed_response,
        )
