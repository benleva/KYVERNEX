from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from threading import RLock
from typing import Any
from uuid import uuid4


class RelationType(StrEnum):
    DERIVED_FROM = "DERIVA_DA"
    TRANSFORMS = "TRASFORMA"
    DEPENDS_ON = "DIPENDE_DA"
    SUPPORTS = "SUPPORTA"
    CONTRADICTS = "CONTRADDICE"
    REFERENCES = "RIFERISCE"


@dataclass(slots=True, frozen=True)
class CognitiveRelation:
    session_id: str
    source_object_id: str
    target_object_id: str
    relation_type: RelationType
    relation_id: str = field(default_factory=lambda: str(uuid4()))
    metadata: dict[str, Any] = field(default_factory=dict)


class RelationConflictError(RuntimeError):
    """Raised when an identical relation already exists in a session."""


class CognitiveGraph:
    """Thread-safe directed relation graph isolated by KYVERNEX session id."""

    def __init__(self) -> None:
        self._relations: dict[str, dict[str, CognitiveRelation]] = {}
        self._lock = RLock()

    def add(self, relation: CognitiveRelation) -> None:
        if not relation.session_id.strip():
            raise ValueError("SESSION_ID_MANCANTE")
        if not relation.source_object_id or not relation.target_object_id:
            raise ValueError("ESTREMI_RELAZIONE_MANCANTI")
        if relation.source_object_id == relation.target_object_id:
            raise ValueError("AUTO_RELAZIONE_NON_AMMESSA")

        with self._lock:
            session = self._relations.setdefault(relation.session_id, {})
            duplicate = any(
                existing.source_object_id == relation.source_object_id
                and existing.target_object_id == relation.target_object_id
                and existing.relation_type == relation.relation_type
                for existing in session.values()
            )
            if duplicate:
                raise RelationConflictError("RELAZIONE_GIA_PRESENTE_NELLA_SESSIONE")
            session[relation.relation_id] = relation

    def connect(
        self,
        *,
        session_id: str,
        source_object_id: str,
        target_object_id: str,
        relation_type: RelationType,
        metadata: dict[str, Any] | None = None,
    ) -> CognitiveRelation:
        relation = CognitiveRelation(
            session_id=session_id,
            source_object_id=source_object_id,
            target_object_id=target_object_id,
            relation_type=relation_type,
            metadata=dict(metadata or {}),
        )
        self.add(relation)
        return relation

    def list(self, session_id: str) -> tuple[CognitiveRelation, ...]:
        with self._lock:
            return tuple(self._relations.get(session_id, {}).values())

    def outgoing(self, session_id: str, object_id: str) -> tuple[CognitiveRelation, ...]:
        return tuple(
            relation
            for relation in self.list(session_id)
            if relation.source_object_id == object_id
        )

    def incoming(self, session_id: str, object_id: str) -> tuple[CognitiveRelation, ...]:
        return tuple(
            relation
            for relation in self.list(session_id)
            if relation.target_object_id == object_id
        )

    def related_object_ids(self, session_id: str, object_id: str) -> tuple[str, ...]:
        related: list[str] = []
        for relation in self.list(session_id):
            if relation.source_object_id == object_id:
                related.append(relation.target_object_id)
            elif relation.target_object_id == object_id:
                related.append(relation.source_object_id)
        return tuple(dict.fromkeys(related))

    def count(self, session_id: str) -> int:
        with self._lock:
            return len(self._relations.get(session_id, {}))

    def clear(self, session_id: str) -> int:
        with self._lock:
            removed = len(self._relations.get(session_id, {}))
            self._relations.pop(session_id, None)
            return removed
