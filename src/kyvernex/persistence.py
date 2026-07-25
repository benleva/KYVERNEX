from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from threading import RLock
from typing import Any

from .memory import MemoryConflictError
from .models import CognitiveCategory, CognitiveObject, CognitiveState


class PersistenceFormatError(RuntimeError):
    """Raised when the persistent memory file is malformed or incompatible."""


class JsonSessionMemory:
    """Thread-safe session memory persisted as one atomic JSON document.

    The storage format is intentionally simple and versioned. Every mutation is
    written to a temporary file and atomically replaces the previous snapshot.
    """

    FORMAT_VERSION = "1"

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._sessions: dict[str, dict[str, CognitiveObject]] = {}
        self._lock = RLock()
        self._load()

    @property
    def path(self) -> Path:
        return self._path

    def store(self, session_id: str, obj: CognitiveObject) -> None:
        if not session_id.strip():
            raise ValueError("SESSION_ID_MANCANTE")
        if not obj.object_id:
            raise ValueError("OBJECT_ID_MANCANTE")

        with self._lock:
            session = self._sessions.setdefault(session_id, {})
            if obj.object_id in session:
                raise MemoryConflictError("OBJECT_ID_GIA_PRESENTE_NELLA_SESSIONE")
            session[obj.object_id] = deepcopy(obj)
            self._persist()

    def get(self, session_id: str, object_id: str) -> CognitiveObject | None:
        with self._lock:
            obj = self._sessions.get(session_id, {}).get(object_id)
            return deepcopy(obj) if obj is not None else None

    def list(self, session_id: str) -> tuple[CognitiveObject, ...]:
        with self._lock:
            return tuple(deepcopy(obj) for obj in self._sessions.get(session_id, {}).values())

    def count(self, session_id: str) -> int:
        with self._lock:
            return len(self._sessions.get(session_id, {}))

    def clear(self, session_id: str) -> int:
        with self._lock:
            removed = len(self._sessions.get(session_id, {}))
            self._sessions.pop(session_id, None)
            if removed:
                self._persist()
            return removed

    def _load(self) -> None:
        if not self._path.exists():
            return
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
            if payload.get("format_version") != self.FORMAT_VERSION:
                raise PersistenceFormatError("VERSIONE_FORMATO_MEMORIA_NON_SUPPORTATA")
            sessions = payload.get("sessions")
            if not isinstance(sessions, dict):
                raise PersistenceFormatError("FORMATO_SESSIONI_NON_VALIDO")
            self._sessions = {
                session_id: {
                    object_id: self._decode_object(raw)
                    for object_id, raw in objects.items()
                }
                for session_id, objects in sessions.items()
            }
        except PersistenceFormatError:
            raise
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise PersistenceFormatError("FILE_MEMORIA_NON_VALIDO") from exc

    def _persist(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "format_version": self.FORMAT_VERSION,
            "sessions": {
                session_id: {
                    object_id: self._encode_object(obj)
                    for object_id, obj in objects.items()
                }
                for session_id, objects in self._sessions.items()
            },
        }
        temporary = self._path.with_suffix(self._path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        temporary.replace(self._path)

    @staticmethod
    def _encode_object(obj: CognitiveObject) -> dict[str, Any]:
        return {
            "original_content": obj.original_content,
            "source": obj.source,
            "category": obj.category.value,
            "state": obj.state.value,
            "object_id": obj.object_id,
            "version": obj.version,
            "transformations": list(obj.transformations),
            "applied_rules": list(obj.applied_rules),
            "limitations": list(obj.limitations),
            "metadata": obj.metadata,
        }

    @staticmethod
    def _decode_object(raw: dict[str, Any]) -> CognitiveObject:
        return CognitiveObject(
            original_content=raw["original_content"],
            source=raw["source"],
            category=CognitiveCategory(raw["category"]),
            state=CognitiveState(raw["state"]),
            object_id=raw["object_id"],
            version=raw.get("version", "0.1"),
            transformations=list(raw.get("transformations", [])),
            applied_rules=list(raw.get("applied_rules", [])),
            limitations=list(raw.get("limitations", [])),
            metadata=dict(raw.get("metadata", {})),
        )
