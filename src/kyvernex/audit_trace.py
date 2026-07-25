from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from threading import RLock
from typing import Any, Iterable

from .models import AuditEvent


class AuditTraceError(RuntimeError):
    """Raised when the persistent audit trace is malformed or fails integrity checks."""


@dataclass(slots=True, frozen=True)
class AuditTraceRecord:
    sequence: int
    event: AuditEvent
    previous_hash: str
    record_hash: str


class JsonAuditTrace:
    """Append-only, versioned JSON audit ledger with a SHA-256 hash chain."""

    FORMAT_VERSION = "0.1"
    GENESIS_HASH = "0" * 64

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._lock = RLock()
        self._records: list[AuditTraceRecord] = []
        self._load()

    @property
    def path(self) -> Path:
        return self._path

    def append(self, event: AuditEvent) -> AuditTraceRecord:
        return self.append_many((event,))[0]

    def append_many(self, events: Iterable[AuditEvent]) -> tuple[AuditTraceRecord, ...]:
        with self._lock:
            added: list[AuditTraceRecord] = []
            previous_hash = self._records[-1].record_hash if self._records else self.GENESIS_HASH
            next_sequence = len(self._records) + 1
            for event in events:
                self._validate_event(event)
                payload = self._event_payload(event)
                record_hash = self._calculate_hash(next_sequence, payload, previous_hash)
                record = AuditTraceRecord(
                    sequence=next_sequence,
                    event=event,
                    previous_hash=previous_hash,
                    record_hash=record_hash,
                )
                self._records.append(record)
                added.append(record)
                previous_hash = record_hash
                next_sequence += 1
            if added:
                self._persist()
            return tuple(added)

    def list(self, *, session_id: str | None = None) -> tuple[AuditTraceRecord, ...]:
        with self._lock:
            if session_id is None:
                return tuple(self._records)
            return tuple(record for record in self._records if record.event.session_id == session_id)

    def verify(self) -> bool:
        with self._lock:
            previous_hash = self.GENESIS_HASH
            expected_sequence = 1
            for record in self._records:
                if record.sequence != expected_sequence or record.previous_hash != previous_hash:
                    raise AuditTraceError("AUDIT_TRACE_CHAIN_BROKEN")
                calculated = self._calculate_hash(
                    record.sequence,
                    self._event_payload(record.event),
                    record.previous_hash,
                )
                if calculated != record.record_hash:
                    raise AuditTraceError("AUDIT_TRACE_HASH_MISMATCH")
                previous_hash = record.record_hash
                expected_sequence += 1
            return True

    def count(self, *, session_id: str | None = None) -> int:
        return len(self.list(session_id=session_id))

    def _load(self) -> None:
        if not self._path.exists():
            return
        try:
            payload = json.loads(self._path.read_text(encoding="utf-8"))
            if payload.get("format_version") != self.FORMAT_VERSION:
                raise AuditTraceError("AUDIT_TRACE_VERSION_UNSUPPORTED")
            records = payload.get("records")
            if not isinstance(records, list):
                raise AuditTraceError("AUDIT_TRACE_RECORDS_INVALID")
            self._records = [self._decode_record(item) for item in records]
            self.verify()
        except AuditTraceError:
            raise
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise AuditTraceError("AUDIT_TRACE_FILE_INVALID") from exc

    def _persist(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "format_version": self.FORMAT_VERSION,
            "records": [self._encode_record(record) for record in self._records],
        }
        encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
        temporary_path: Path | None = None
        try:
            with NamedTemporaryFile(
                "w",
                encoding="utf-8",
                dir=self._path.parent,
                prefix=f".{self._path.name}.",
                suffix=".tmp",
                delete=False,
            ) as handle:
                handle.write(encoded)
                handle.flush()
                os.fsync(handle.fileno())
                temporary_path = Path(handle.name)
            os.replace(temporary_path, self._path)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()

    @classmethod
    def _calculate_hash(cls, sequence: int, event: dict[str, Any], previous_hash: str) -> str:
        canonical = json.dumps(
            {"sequence": sequence, "event": event, "previous_hash": previous_hash},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(canonical).hexdigest()

    @staticmethod
    def _validate_event(event: AuditEvent) -> None:
        if not event.session_id.strip():
            raise ValueError("AUDIT_SESSION_ID_MANCANTE")
        if not event.operation_id.strip():
            raise ValueError("AUDIT_OPERATION_ID_MANCANTE")
        if not event.component.strip() or not event.event_type.strip():
            raise ValueError("AUDIT_EVENT_DATA_MANCANTI")

    @staticmethod
    def _event_payload(event: AuditEvent) -> dict[str, Any]:
        return {
            "session_id": event.session_id,
            "operation_id": event.operation_id,
            "component": event.component,
            "event_type": event.event_type,
            "timestamp": event.timestamp,
            "object_id": event.object_id,
            "details": event.details,
        }

    @classmethod
    def _encode_record(cls, record: AuditTraceRecord) -> dict[str, Any]:
        return {
            "sequence": record.sequence,
            "event": cls._event_payload(record.event),
            "previous_hash": record.previous_hash,
            "record_hash": record.record_hash,
        }

    @staticmethod
    def _decode_record(raw: dict[str, Any]) -> AuditTraceRecord:
        event_raw = raw["event"]
        event = AuditEvent(
            session_id=event_raw["session_id"],
            operation_id=event_raw["operation_id"],
            component=event_raw["component"],
            event_type=event_raw["event_type"],
            timestamp=event_raw["timestamp"],
            object_id=event_raw.get("object_id"),
            details=dict(event_raw.get("details", {})),
        )
        return AuditTraceRecord(
            sequence=int(raw["sequence"]),
            event=event,
            previous_hash=raw["previous_hash"],
            record_hash=raw["record_hash"],
        )
