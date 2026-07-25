from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from threading import RLock
from typing import Any
from uuid import uuid4

from .deletion import CognitiveDeletionCoordinator, DeletionPolicy, DeletionResult
from .durable_deletion import DeletionJournalError, DeletionJournalState, RecoveryResult
from .graph import CognitiveGraph, CognitiveRelation, RelationType
from .memory import SessionMemory


@dataclass(slots=True, frozen=True)
class RecoveryBatch:
    recovered: tuple[RecoveryResult, ...]
    failed_journals: tuple[str, ...]


class MultiTransactionDeletionCoordinator(CognitiveDeletionCoordinator):
    """Crash-recoverable deletion using one journal file per transaction.

    Separate journal files prevent concurrent deletions from overwriting one
    another. A process-local lock serializes mutation of memory and graph.
    Cross-process distributed locking is intentionally outside this prototype.
    """

    FORMAT_VERSION = "0.2"

    def __init__(
        self,
        *,
        memory: SessionMemory,
        graph: CognitiveGraph,
        journal_directory: str | Path,
        recover_on_startup: bool = True,
    ) -> None:
        super().__init__(memory=memory, graph=graph)
        self._journal_directory = Path(journal_directory)
        self._transaction_lock = RLock()
        if recover_on_startup:
            self.recover_all()

    @property
    def journal_directory(self) -> Path:
        return self._journal_directory

    def delete(
        self,
        *,
        session_id: str,
        object_id: str,
        policy: DeletionPolicy = DeletionPolicy.RESTRICT,
    ) -> DeletionResult:
        with self._transaction_lock:
            obj = self._memory.get(session_id, object_id)
            if obj is None:
                raise KeyError("OBJECT_NOT_FOUND")

            linked_by_id = {
                relation.relation_id: relation
                for relation in (
                    *self._graph.outgoing(session_id, object_id),
                    *self._graph.incoming(session_id, object_id),
                )
            }
            linked = tuple(linked_by_id.values())
            transaction_id = str(uuid4())
            path = self._journal_path(transaction_id)
            record = {
                "format_version": self.FORMAT_VERSION,
                "transaction_id": transaction_id,
                "state": DeletionJournalState.PREPARED.value,
                "session_id": session_id,
                "object_id": object_id,
                "policy": policy.value,
                "relations": [self._encode_relation(relation) for relation in linked],
            }
            self._write(path, record)
            try:
                result = super().delete(
                    session_id=session_id,
                    object_id=object_id,
                    policy=policy,
                )
                record["state"] = DeletionJournalState.MEMORY_APPLIED.value
                self._write(path, record)
                path.unlink(missing_ok=True)
                return result
            except Exception:
                # Keep the transaction journal for deterministic recovery.
                raise

    def recover_all(self, *, continue_on_error: bool = False) -> RecoveryBatch:
        with self._transaction_lock:
            if not self._journal_directory.exists():
                return RecoveryBatch(recovered=(), failed_journals=())

            recovered: list[RecoveryResult] = []
            failed: list[str] = []
            for path in sorted(self._journal_directory.glob("deletion-*.json")):
                try:
                    recovered.append(self._recover_one(path))
                except DeletionJournalError:
                    failed.append(path.name)
                    if not continue_on_error:
                        raise
            return RecoveryBatch(recovered=tuple(recovered), failed_journals=tuple(failed))

    def pending_transactions(self) -> tuple[str, ...]:
        if not self._journal_directory.exists():
            return ()
        return tuple(path.stem.removeprefix("deletion-") for path in sorted(self._journal_directory.glob("deletion-*.json")))

    def _recover_one(self, path: Path) -> RecoveryResult:
        record = self._read(path)
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

        path.unlink(missing_ok=True)
        return RecoveryResult(
            transaction_id=transaction_id,
            action=action,
            session_id=session_id,
            object_id=object_id,
        )

    def _journal_path(self, transaction_id: str) -> Path:
        return self._journal_directory / f"deletion-{transaction_id}.json"

    def _read(self, path: Path) -> dict[str, Any]:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if payload.get("format_version") != self.FORMAT_VERSION:
                raise DeletionJournalError("DELETION_JOURNAL_VERSION_UNSUPPORTED")
            required = {"transaction_id", "state", "session_id", "object_id", "policy", "relations"}
            if not required.issubset(payload) or not isinstance(payload["relations"], list):
                raise DeletionJournalError("DELETION_JOURNAL_DATA_INVALID")
            if path != self._journal_path(payload["transaction_id"]):
                raise DeletionJournalError("DELETION_JOURNAL_FILENAME_MISMATCH")
            DeletionJournalState(payload["state"])
            DeletionPolicy(payload["policy"])
            return payload
        except DeletionJournalError:
            raise
        except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
            raise DeletionJournalError("DELETION_JOURNAL_INVALID") from exc

    def _write(self, path: Path, payload: dict[str, Any]) -> None:
        self._journal_directory.mkdir(parents=True, exist_ok=True)
        encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
        temporary_path: Path | None = None
        try:
            with NamedTemporaryFile(
                "w",
                encoding="utf-8",
                dir=self._journal_directory,
                prefix=f".{path.name}.",
                suffix=".tmp",
                delete=False,
            ) as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
                temporary_path = Path(handle.name)
            os.replace(temporary_path, path)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()

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
