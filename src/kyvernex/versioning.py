from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from .graph import CognitiveGraph, RelationType
from .memory import SessionMemory
from .models import CognitiveObject


class VersioningError(RuntimeError):
    """Base error for KYVERNEX cognitive object versioning."""


class VersionConflictError(VersioningError):
    """Raised when a version transition is invalid or ambiguous."""


class VersionChangeType(StrEnum):
    CORRECTION = "CORREZIONE"
    ENRICHMENT = "ARRICCHIMENTO"
    RECLASSIFICATION = "RICLASSIFICAZIONE"
    SUPERSESSION = "SOSTITUZIONE"


@dataclass(slots=True, frozen=True)
class VersionTransition:
    session_id: str
    previous_object_id: str
    new_object_id: str
    previous_version: str
    new_version: str
    change_type: VersionChangeType
    reason: str


class CognitiveVersionManager:
    """Creates immutable successors for cognitive objects.

    Existing objects are never overwritten. Every revision is stored as a new
    cognitive object and linked to its predecessor through ``DERIVED_FROM``.
    """

    def __init__(self, *, memory: SessionMemory, graph: CognitiveGraph) -> None:
        self.memory = memory
        self.graph = graph

    def revise(
        self,
        *,
        session_id: str,
        object_id: str,
        change_type: VersionChangeType,
        reason: str,
        content: Any | None = None,
        source: str | None = None,
        category: Any | None = None,
        metadata_updates: dict[str, Any] | None = None,
    ) -> tuple[CognitiveObject, VersionTransition]:
        if not session_id.strip():
            raise ValueError("SESSION_ID_MANCANTE")
        if not reason.strip():
            raise ValueError("MOTIVAZIONE_VERSIONE_MANCANTE")

        previous = self.memory.get(session_id, object_id)
        if previous is None:
            raise VersioningError("OGGETTO_COGNITIVO_NON_TROVATO")

        next_version = self._increment(previous.version)
        metadata = deepcopy(previous.metadata)
        metadata.update(metadata_updates or {})
        metadata.update({
            "previous_object_id": previous.object_id,
            "version_change_type": change_type.value,
            "version_reason": reason,
        })

        successor = CognitiveObject(
            original_content=deepcopy(previous.original_content if content is None else content),
            source=previous.source if source is None else source,
            category=previous.category if category is None else category,
            state=previous.state,
            version=next_version,
            transformations=[*previous.transformations, f"VERSIONE:{change_type.value}"],
            applied_rules=list(previous.applied_rules),
            limitations=list(previous.limitations),
            metadata=metadata,
        )

        self.memory.store(session_id, successor)
        try:
            self.graph.connect(
                session_id=session_id,
                source_object_id=successor.object_id,
                target_object_id=previous.object_id,
                relation_type=RelationType.DERIVED_FROM,
                metadata={"change_type": change_type.value, "reason": reason},
            )
        except Exception:
            self.memory.remove(session_id, successor.object_id)
            raise

        transition = VersionTransition(
            session_id=session_id,
            previous_object_id=previous.object_id,
            new_object_id=successor.object_id,
            previous_version=previous.version,
            new_version=next_version,
            change_type=change_type,
            reason=reason,
        )
        return successor, transition

    def history(self, *, session_id: str, object_id: str) -> tuple[CognitiveObject, ...]:
        current = self.memory.get(session_id, object_id)
        if current is None:
            raise VersioningError("OGGETTO_COGNITIVO_NON_TROVATO")

        chain = [current]
        seen = {current.object_id}
        cursor = current.object_id
        while True:
            predecessors = [
                relation.target_object_id
                for relation in self.graph.outgoing(session_id, cursor)
                if relation.relation_type is RelationType.DERIVED_FROM
            ]
            if not predecessors:
                break
            if len(predecessors) > 1:
                raise VersionConflictError("STORIA_VERSIONE_AMBIGUA")
            cursor = predecessors[0]
            if cursor in seen:
                raise VersionConflictError("CICLO_NELLA_STORIA_VERSIONE")
            predecessor = self.memory.get(session_id, cursor)
            if predecessor is None:
                raise VersionConflictError("PREDECESSORE_VERSIONE_MANCANTE")
            chain.append(predecessor)
            seen.add(cursor)
        return tuple(chain)

    @staticmethod
    def _increment(version: str) -> str:
        parts = version.split(".")
        if len(parts) != 2 or not all(part.isdigit() for part in parts):
            raise VersionConflictError("FORMATO_VERSIONE_NON_VALIDO")
        major, minor = (int(part) for part in parts)
        return f"{major}.{minor + 1}"
