from __future__ import annotations

import json
import os
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from uuid import uuid4

from .deletion import (
    CognitiveDeletionCoordinator,
    DeletionPolicy,
    DeletionResult,
)
from .graph import CognitiveGraph, CognitiveRelation, RelationType
from .memory import SessionMemory


class DeletionJournalError(RuntimeError):
    """Raised when a durable deletion journal is malformed or unrecoverable."""


class DeletionJournalState(StrEnum):
    PREPARED = "PREPARED"
    GRAPH_APPLIED = "GRAPH_APPLIED"
    MEMORY_APPLIED = "MEMORY_APPLIED"


@dataclass(slots=True, frozen=True)
class RecoveryResult:
    transaction_id: str
    action: str
    session_id: str
    object_id: str


class DurableDeletionCoordinator(CognitiveDeletionCoordinator):
    """Adds a write-ahead journal and deterministic crash recovery to deletion.

    Recovery follows the visible memory state. If the cognitive object still
    exists, removed graph relations are restored. If the object is absent,
    remaining relations are removed and the deletion is completed.
    """

    FORMAT_VERSION = "0.1"

    def __init__(
        self,
        *,
        memory: SessionMemory,
        graph: CognitiveGraph,
        journal_path: str | Path,
        recover_on_startup: bool = True,
    ) -> None:
        super().__init__(memory=memory, graph=graph)
        self._journal_path = Path(journal_path)
        if recover_on_startup:
            self.recover()

    @property
    def journal_path(self) -> Path:
        return self._journal_path

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
        transaction_id = str(uuid4())
        record = {
            "format_version": self.FORMAT_VERSION,
            "transaction_id": transaction_id,
            "state": DeletionJournalState.PREPARED.value,
            "session_id": session_id,
            "object_id": object_id,
            "policy": policy.value,
            "relations": [self._encode_relation(relation) for relation in linked],
        }
        self._write_journal(record)

        try:
            result = super().delete(
                session_id=session_id,
                object_id=object_id,
                policy=policy,
            )
            record["state"] = DeletionJournalState.MEMORY_APPLIED.value
            self._write_journal(record)
            self._remove_journal()
            return result
        except Exception:
            # The base coordinator already attempts process-level rollback. The
            # durable record remains available for startup recovery.
            raise

    def recover(self) -> RecoveryResult | None:
        if not self._journal_path.exists():
            return None
        record = self._read_journal()
        session_id = record["session_id"]
        object_id = record["object_id"]
        transaction_id = record["transaction_id"]
        relations = tuple(self._decode_relation(item, session_id) for item in record["relations"])

        if self._memory.get(session_id, object_id) is not None:
            existing_ids = {relation.relation_id for relation in self._graph.list(session_id)}
            for relation in relations:
                if relation.relation_id not in existing_ids:
                    self._graph.add(relation)
            action = "ROLLBACK_RELATIONS_RESTORED"
        else:
            self._graph.remove_for_object(session_id, object_id)
            action = "COMMIT_ORPHAN_RELATIONS_REMOVED"

        self._remove_journal()
        return RecoveryResult(
            transaction_id=transaction_id,
            action=action,
            session_id=session_id,
            object_id=object_id,
        )

    def _read_journal(self) -> dict[str, Any]:
        try:
            payload = json.loads(self._journal_path.read_text(encoding="utf-8"))
            if payload.get("format_version") != self.FORMAT_VERSION:
                raise DeletionJournalError("DELETION_JOURNAL_VERSION_UNSUPPORTED")
            required = {"transaction_id", "state", "session_id", "object_id", "policy", "relations"}
            if not required.issubset(payload) or not isinstance(payload["relations"], list):
                raise DeletionJournalError("DELETION_JOURNAL_DATA_INVALID")
            DeletionJournalState(payload["state"])
            DeletionPolicy(payload["policy"])
            return payload
        except DeletionJournalError:
            raise
        except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
            raise DeletionJournalError("DELETION_JOURNAL_INVALID") from exc

    def _write_journal(self, payload: dict[str, Any]) -> None:
        self._journal_path.parent.mkdir(parents=True, exist_ok=True)
        encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
        temporary_path: Path | None = None
        try:
            with NamedTemporaryFile(
                "w",
                encoding="utf-8",
                dir=self._journal_path.parent,
                prefix=f".{self._journal_path.name}.",
                suffix=".tmp",
                delete=False,
            ) as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
                temporary_path = Path(handle.name)
            os.replace(temporary_path, self._journal_path)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()

    def _remove_journal(self) -> None:
        try:
            self._journal_path.unlink(missing_ok=True)
        except OSError as exc:
            raise DeletionJournalError("DELETION_JOURNAL_REMOVE_FAILED") from exc

    @staticmethod
    def _encode_relation(relation: CognitiveRelation) -> dict[str, Any]:
        return {
            "relation_id": relation.relation_id,
            "source_object_id": relation.source_object_id,
            "target_object_id": relation.target_object_id,
            "relation_type": relation.relation_type.value,
            "metadata": dict(relation.metadata),
        }

    @staticmethod
    def _decode_relation(raw: dict[str, Any], session_id: str) -> CognitiveRelation:
        try:
            return CognitiveRelation(
                session_id=session_id,
                source_object_id=raw["source_object_id"],
                target_object_id=raw["target_object_id"],
                relation_type=RelationType(raw["relation_type"]),
                relation_id=raw["relation_id"],
                metadata=dict(raw.get("metadata", {})),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise DeletionJournalError("DELETION_JOURNAL_RELATION_INVALID") from exc
