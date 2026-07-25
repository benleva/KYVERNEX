from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .graph import CognitiveGraph, CognitiveRelation
from .memory import SessionMemory
from .models import AuditEvent, CognitiveObject


class DeletionPolicy(StrEnum):
    RESTRICT = "RESTRICT"
    CASCADE = "CASCADE"


class DeletionRestrictedError(RuntimeError):
    """Raised when a referenced object cannot be deleted under RESTRICT policy."""


class DeletionTransactionError(RuntimeError):
    """Raised when coordinated deletion fails and rollback is attempted."""


@dataclass(slots=True, frozen=True)
class DeletionResult:
    session_id: str
    object_id: str
    removed_object: CognitiveObject
    removed_relations: tuple[CognitiveRelation, ...]
    policy: DeletionPolicy
    audit: tuple[AuditEvent, ...]


class CognitiveDeletionCoordinator:
    """Coordinates object and relation deletion with restrict or cascade semantics.

    The operation removes graph edges before memory data. If memory removal fails,
    removed edges are restored. This provides process-level rollback semantics;
    cross-file crash atomicity is intentionally not claimed.
    """

    def __init__(self, *, memory: SessionMemory, graph: CognitiveGraph) -> None:
        self._memory = memory
        self._graph = graph

    def delete(
        self,
        *,
        session_id: str,
        object_id: str,
        policy: DeletionPolicy = DeletionPolicy.RESTRICT,
    ) -> DeletionResult:
        obj = self._memory.get(session_id, object_id)
        if obj is None:
            raise KeyError("OBJECT_NOT_FOUND")

        linked = tuple(
            dict.fromkeys(
                (*self._graph.outgoing(session_id, object_id), *self._graph.incoming(session_id, object_id))
            )
        )
        if linked and policy == DeletionPolicy.RESTRICT:
            raise DeletionRestrictedError("OBJECT_HAS_COGNITIVE_RELATIONS")

        audit: list[AuditEvent] = [
            AuditEvent.create(
                session_id=session_id,
                component="DELETION_COORDINATOR",
                event_type="CANCELLAZIONE_PREPARATA",
                object_id=object_id,
                details={"policy": policy.value, "linked_relations": len(linked)},
            )
        ]

        removed_relations: tuple[CognitiveRelation, ...] = ()
        try:
            if policy == DeletionPolicy.CASCADE:
                removed_relations = self._graph.remove_for_object(session_id, object_id)
            removed_object = self._memory.remove(session_id, object_id)
            if removed_object is None:
                raise RuntimeError("OBJECT_DISAPPEARED_DURING_DELETION")
        except Exception as exc:
            rollback_errors: list[str] = []
            for relation in removed_relations:
                try:
                    self._graph.add(relation)
                except Exception as rollback_exc:
                    rollback_errors.append(type(rollback_exc).__name__)
            message = "DELETION_TRANSACTION_FAILED"
            if rollback_errors:
                message += "|ROLLBACK_INCOMPLETE:" + ",".join(rollback_errors)
            raise DeletionTransactionError(message) from exc

        audit.append(
            AuditEvent.create(
                session_id=session_id,
                component="COGNITIVE_GRAPH",
                event_type="RELAZIONI_COLLEGATE_RIMOSSE",
                object_id=object_id,
                details={"removed_relations": len(removed_relations)},
            )
        )
        audit.append(
            AuditEvent.create(
                session_id=session_id,
                component="MEMORY",
                event_type="OGGETTO_COGNITIVO_RIMOSSO",
                object_id=object_id,
                details={"policy": policy.value},
            )
        )
        audit.append(
            AuditEvent.create(
                session_id=session_id,
                component="DELETION_COORDINATOR",
                event_type="CANCELLAZIONE_COMPLETATA",
                object_id=object_id,
                details={"removed_relations": len(removed_relations)},
            )
        )
        return DeletionResult(
            session_id=session_id,
            object_id=object_id,
            removed_object=removed_object,
            removed_relations=removed_relations,
            policy=policy,
            audit=tuple(audit),
        )
