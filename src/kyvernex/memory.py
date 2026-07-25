from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from threading import RLock

from .models import CognitiveObject


class MemoryConflictError(RuntimeError):
    """Raised when an object identifier is reused inside the same session."""


class SessionMemory:
    """Thread-safe, process-local memory isolated by KYVERNEX session id.

    Objects are copied on write and read so callers cannot mutate the stored
    state without an explicit new store operation.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, dict[str, CognitiveObject]] = defaultdict(dict)
        self._lock = RLock()

    def store(self, session_id: str, obj: CognitiveObject) -> None:
        if not session_id.strip():
            raise ValueError("SESSION_ID_MANCANTE")
        if not obj.object_id:
            raise ValueError("OBJECT_ID_MANCANTE")

        with self._lock:
            session = self._sessions[session_id]
            if obj.object_id in session:
                raise MemoryConflictError("OBJECT_ID_GIA_PRESENTE_NELLA_SESSIONE")
            session[obj.object_id] = deepcopy(obj)

    def get(self, session_id: str, object_id: str) -> CognitiveObject | None:
        with self._lock:
            obj = self._sessions.get(session_id, {}).get(object_id)
            return deepcopy(obj) if obj is not None else None

    def list(self, session_id: str) -> tuple[CognitiveObject, ...]:
        with self._lock:
            objects = self._sessions.get(session_id, {}).values()
            return tuple(deepcopy(obj) for obj in objects)

    def count(self, session_id: str) -> int:
        with self._lock:
            return len(self._sessions.get(session_id, {}))

    def clear(self, session_id: str) -> int:
        with self._lock:
            removed = len(self._sessions.get(session_id, {}))
            self._sessions.pop(session_id, None)
            return removed
