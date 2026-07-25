from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from threading import RLock
from typing import Iterable
from uuid import uuid4

from .audit_sink import AuditSink, persist_audit
from .graph import CognitiveGraph, CognitiveRelation
from .memory import SessionMemory
from .models import AuditEvent, CognitiveObject


class UnitOfWorkState(StrEnum):
    NEW = "NUOVA"
    ACTIVE = "ATTIVA"
    COMMITTED = "CONFERMATA"
    ROLLED_BACK = "ANNULLATA"
    FAILED = "FALLITA"


class UnitOfWorkError(RuntimeError):
    """Base error for coordinated KYVERNEX transactions."""


class UnitOfWorkStateError(UnitOfWorkError):
    """Raised when an operation is incompatible with the transaction state."""


class UnitOfWorkCommitError(UnitOfWorkError):
    """Raised when commit fails after rollback has been attempted."""


@dataclass(slots=True, frozen=True)
class UnitOfWorkResult:
    transaction_id: str
    session_id: str
    state: UnitOfWorkState
    stored_object_ids: tuple[str, ...]
    stored_relation_ids: tuple[str, ...]
    audit_event_count: int


class KyvernexUnitOfWork:
    """Coordinates memory, graph and audit writes within one process.

    Objects, relations and audit events are staged until ``commit``. If a
    memory, graph or audit write fails, already-applied memory and graph writes
    are removed in reverse order. Audit sinks are expected to provide an
    atomic ``append_many`` operation; an external sink that partially writes
    before raising cannot be repaired by this process-local coordinator.
    """

    def __init__(
        self,
        *,
        session_id: str,
        memory: SessionMemory,
        graph: CognitiveGraph,
        audit_sink: AuditSink | None = None,
    ) -> None:
        if not session_id.strip():
            raise ValueError("SESSION_ID_MANCANTE")
        self.session_id = session_id
        self.memory = memory
        self.graph = graph
        self.audit_sink = audit_sink
        self.transaction_id = str(uuid4())
        self.state = UnitOfWorkState.NEW
        self._objects: list[CognitiveObject] = []
        self._relations: list[CognitiveRelation] = []
        self._audit: list[AuditEvent] = []
        self._lock = RLock()

    def __enter__(self) -> "KyvernexUnitOfWork":
        self.begin()
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> bool:
        if exc_type is not None:
            self.rollback()
            return False
        if self.state is UnitOfWorkState.ACTIVE:
            self.commit()
        return False

    def begin(self) -> None:
        with self._lock:
            if self.state is not UnitOfWorkState.NEW:
                raise UnitOfWorkStateError("UNIT_OF_WORK_GIA_AVVIATA")
            self.state = UnitOfWorkState.ACTIVE

    def stage_object(self, obj: CognitiveObject) -> None:
        with self._lock:
            self._require_active()
            if any(existing.object_id == obj.object_id for existing in self._objects):
                raise UnitOfWorkError("OBJECT_ID_DUPLICATO_NELLA_TRANSAZIONE")
            if self.memory.get(self.session_id, obj.object_id) is not None:
                raise UnitOfWorkError("OBJECT_ID_GIA_PRESENTE_NELLA_SESSIONE")
            self._objects.append(obj)

    def stage_relation(self, relation: CognitiveRelation) -> None:
        with self._lock:
            self._require_active()
            if relation.session_id != self.session_id:
                raise UnitOfWorkError("SESSIONE_RELAZIONE_INCOMPATIBILE")
            if any(existing.relation_id == relation.relation_id for existing in self._relations):
                raise UnitOfWorkError("RELATION_ID_DUPLICATO_NELLA_TRANSAZIONE")
            available_ids = {obj.object_id for obj in self._objects}
            available_ids.update(obj.object_id for obj in self.memory.list(self.session_id))
            if relation.source_object_id not in available_ids or relation.target_object_id not in available_ids:
                raise UnitOfWorkError("INTEGRITA_REFERENZIALE_NON_SODDISFATTA")
            self._relations.append(relation)

    def stage_audit(self, event: AuditEvent) -> None:
        with self._lock:
            self._require_active()
            if event.session_id != self.session_id:
                raise UnitOfWorkError("SESSIONE_AUDIT_INCOMPATIBILE")
            self._audit.append(event)

    def stage_audit_many(self, events: Iterable[AuditEvent]) -> None:
        for event in events:
            self.stage_audit(event)

    def commit(self) -> UnitOfWorkResult:
        with self._lock:
            self._require_active()
            stored_objects: list[str] = []
            stored_relations: list[str] = []
            commit_event = AuditEvent.create(
                session_id=self.session_id,
                component="UNIT_OF_WORK",
                event_type="TRANSAZIONE_CONFERMATA",
                details={"transaction_id": self.transaction_id},
            )
            audit_batch = (*self._audit, commit_event)
            try:
                for obj in self._objects:
                    self.memory.store(self.session_id, obj)
                    stored_objects.append(obj.object_id)
                for relation in self._relations:
                    self.graph.add(relation)
                    stored_relations.append(relation.relation_id)
                persist_audit(self.audit_sink, audit_batch)
            except Exception as exc:
                rollback_errors = self._rollback_applied(stored_objects, stored_relations)
                self.state = UnitOfWorkState.FAILED
                detail = f"UNIT_OF_WORK_COMMIT_FALLITO: {exc}"
                if rollback_errors:
                    detail += f"; ROLLBACK_INCOMPLETO: {' | '.join(rollback_errors)}"
                raise UnitOfWorkCommitError(detail) from exc

            self.state = UnitOfWorkState.COMMITTED
            return UnitOfWorkResult(
                transaction_id=self.transaction_id,
                session_id=self.session_id,
                state=self.state,
                stored_object_ids=tuple(stored_objects),
                stored_relation_ids=tuple(stored_relations),
                audit_event_count=len(audit_batch) if self.audit_sink is not None else 0,
            )

    def rollback(self) -> UnitOfWorkResult:
        with self._lock:
            if self.state is UnitOfWorkState.COMMITTED:
                raise UnitOfWorkStateError("UNIT_OF_WORK_GIA_CONFERMATA")
            if self.state in {UnitOfWorkState.ROLLED_BACK, UnitOfWorkState.FAILED}:
                return UnitOfWorkResult(
                    transaction_id=self.transaction_id,
                    session_id=self.session_id,
                    state=self.state,
                    stored_object_ids=(),
                    stored_relation_ids=(),
                    audit_event_count=0,
                )
            self._objects.clear()
            self._relations.clear()
            self._audit.clear()
            self.state = UnitOfWorkState.ROLLED_BACK
            return UnitOfWorkResult(
                transaction_id=self.transaction_id,
                session_id=self.session_id,
                state=self.state,
                stored_object_ids=(),
                stored_relation_ids=(),
                audit_event_count=0,
            )

    def _rollback_applied(self, object_ids: list[str], relation_ids: list[str]) -> list[str]:
        errors: list[str] = []
        for relation_id in reversed(relation_ids):
            try:
                self.graph.remove(self.session_id, relation_id)
            except Exception as exc:
                errors.append(f"RELAZIONE {relation_id}: {exc}")
        for object_id in reversed(object_ids):
            try:
                self.memory.remove(self.session_id, object_id)
            except Exception as exc:
                errors.append(f"OGGETTO {object_id}: {exc}")
        return errors

    def _require_active(self) -> None:
        if self.state is not UnitOfWorkState.ACTIVE:
            raise UnitOfWorkStateError("UNIT_OF_WORK_NON_ATTIVA")
