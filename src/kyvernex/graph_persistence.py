from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from .graph import CognitiveGraph, CognitiveRelation, RelationType
from .memory import SessionMemory


class GraphPersistenceFormatError(RuntimeError):
    """Raised when a persisted cognitive graph cannot be safely loaded."""


class ReferentialIntegrityError(RuntimeError):
    """Raised when a relation references an object absent from session memory."""


class JsonCognitiveGraph(CognitiveGraph):
    """Versioned JSON graph with referential integrity against KYVERNEX memory."""

    FORMAT_VERSION = "0.1"

    def __init__(self, path: str | Path, *, memory: SessionMemory) -> None:
        super().__init__()
        self._path = Path(path)
        self._memory = memory
        self._load()

    @property
    def path(self) -> Path:
        return self._path

    def add(self, relation: CognitiveRelation) -> None:
        self._assert_endpoints_exist(relation)
        super().add(relation)
        self._persist()

    def remove(self, session_id: str, relation_id: str) -> CognitiveRelation | None:
        removed = super().remove(session_id, relation_id)
        if removed is not None:
            self._persist()
        return removed

    def remove_for_object(self, session_id: str, object_id: str) -> tuple[CognitiveRelation, ...]:
        removed = super().remove_for_object(session_id, object_id)
        if removed:
            self._persist()
        return removed

    def clear(self, session_id: str) -> int:
        removed = super().clear(session_id)
        if removed:
            self._persist()
        return removed

    def _assert_endpoints_exist(self, relation: CognitiveRelation) -> None:
        source = self._memory.get(relation.session_id, relation.source_object_id)
        target = self._memory.get(relation.session_id, relation.target_object_id)
        missing: list[str] = []
        if source is None:
            missing.append("SOURCE_OBJECT_NOT_FOUND")
        if target is None:
            missing.append("TARGET_OBJECT_NOT_FOUND")
        if missing:
            raise ReferentialIntegrityError("|".join(missing))

    def _load(self) -> None:
        if not self._path.exists():
            return
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise GraphPersistenceFormatError("GRAPH_JSON_NON_VALIDO") from exc
        if payload.get("format_version") != self.FORMAT_VERSION:
            raise GraphPersistenceFormatError("GRAPH_FORMAT_VERSION_NON_SUPPORTATA")
        sessions = payload.get("sessions")
        if not isinstance(sessions, dict):
            raise GraphPersistenceFormatError("GRAPH_SESSIONS_NON_VALIDE")
        try:
            for session_id, relations in sessions.items():
                if not isinstance(relations, list):
                    raise TypeError
                for item in relations:
                    relation = CognitiveRelation(
                        session_id=session_id,
                        source_object_id=item["source_object_id"],
                        target_object_id=item["target_object_id"],
                        relation_type=RelationType(item["relation_type"]),
                        relation_id=item["relation_id"],
                        metadata=dict(item.get("metadata", {})),
                    )
                    self._assert_endpoints_exist(relation)
                    CognitiveGraph.add(self, relation)
        except (KeyError, TypeError, ValueError, ReferentialIntegrityError) as exc:
            raise GraphPersistenceFormatError("GRAPH_RELATION_DATA_NON_VALIDI") from exc

    def _payload(self) -> dict[str, Any]:
        sessions: dict[str, list[dict[str, Any]]] = {}
        for session_id in tuple(self._relations):
            sessions[session_id] = [
                {
                    "relation_id": relation.relation_id,
                    "source_object_id": relation.source_object_id,
                    "target_object_id": relation.target_object_id,
                    "relation_type": relation.relation_type.value,
                    "metadata": dict(relation.metadata),
                }
                for relation in self.list(session_id)
            ]
        return {"format_version": self.FORMAT_VERSION, "sessions": sessions}

    def _persist(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(self._payload(), ensure_ascii=False, indent=2, sort_keys=True)
        temporary_path: Path | None = None
        try:
            with NamedTemporaryFile(
                "w", encoding="utf-8", dir=self._path.parent,
                prefix=f".{self._path.name}.", suffix=".tmp", delete=False,
            ) as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
                temporary_path = Path(handle.name)
            os.replace(temporary_path, self._path)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()
