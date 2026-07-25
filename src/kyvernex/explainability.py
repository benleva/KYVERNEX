from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .audit_trace import AuditTraceRecord
from .confidence import CognitiveConfidenceEngine, ConfidenceAssessment
from .graph import CognitiveGraph, CognitiveRelation
from .memory import SessionMemory
from .models import CognitiveObject
from .versioning import CognitiveVersionManager


class ExplainabilityError(RuntimeError):
    """Raised when a cognitive decision dossier cannot be assembled."""


class AuditTraceReader(Protocol):
    def list(self, *, session_id: str | None = None) -> tuple[AuditTraceRecord, ...]:
        ...

    def verify(self) -> bool:
        ...


@dataclass(slots=True, frozen=True)
class CognitiveDecisionDossier:
    session_id: str
    object_id: str
    cognitive_object: CognitiveObject
    version_history: tuple[CognitiveObject, ...]
    incoming_relations: tuple[CognitiveRelation, ...]
    outgoing_relations: tuple[CognitiveRelation, ...]
    confidence: ConfidenceAssessment
    audit_records: tuple[AuditTraceRecord, ...]
    audit_integrity_verified: bool
    reservations: tuple[str, ...]


class CognitiveDecisionExplainer:
    """Builds a deterministic evidence dossier for one cognitive object.

    The dossier consolidates the immutable object snapshot, version lineage,
    graph neighbourhood, propagated confidence and object-specific audit trail.
    It does not generate natural-language justifications and does not infer
    facts that are absent from KYVERNEX memory, graph or audit storage.
    """

    def __init__(
        self,
        *,
        memory: SessionMemory,
        graph: CognitiveGraph,
        confidence_engine: CognitiveConfidenceEngine,
        audit_trace: AuditTraceReader | None = None,
    ) -> None:
        self.memory = memory
        self.graph = graph
        self.confidence_engine = confidence_engine
        self.audit_trace = audit_trace
        self.version_manager = CognitiveVersionManager(memory=memory, graph=graph)

    def explain(self, *, session_id: str, object_id: str) -> CognitiveDecisionDossier:
        if not session_id.strip():
            raise ValueError("SESSION_ID_MANCANTE")
        if not object_id.strip():
            raise ValueError("OBJECT_ID_MANCANTE")

        obj = self.memory.get(session_id, object_id)
        if obj is None:
            raise ExplainabilityError("OGGETTO_COGNITIVO_NON_TROVATO")

        history = self.version_manager.history(session_id=session_id, object_id=object_id)
        incoming = self.graph.incoming(session_id, object_id)
        outgoing = self.graph.outgoing(session_id, object_id)
        confidence = self.confidence_engine.assess(session_id=session_id, object_id=object_id)

        audit_records: tuple[AuditTraceRecord, ...] = ()
        audit_verified = False
        reservations = list(confidence.reservations)
        if self.audit_trace is None:
            reservations.append("AUDIT_TRACE_NON_CONFIGURATO")
        else:
            audit_verified = self.audit_trace.verify()
            audit_records = tuple(
                record
                for record in self.audit_trace.list(session_id=session_id)
                if record.event.object_id == object_id
            )
            if not audit_records:
                reservations.append("AUDIT_OGGETTO_ASSENTE")

        if len(history) == 1:
            reservations.append("NESSUNA_REVISIONE_PRECEDENTE")
        if not incoming and not outgoing:
            reservations.append("OGGETTO_ISOLATO_NEL_GRAFO")

        return CognitiveDecisionDossier(
            session_id=session_id,
            object_id=object_id,
            cognitive_object=obj,
            version_history=history,
            incoming_relations=incoming,
            outgoing_relations=outgoing,
            confidence=confidence,
            audit_records=audit_records,
            audit_integrity_verified=audit_verified,
            reservations=tuple(dict.fromkeys(reservations)),
        )
