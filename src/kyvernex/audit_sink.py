from __future__ import annotations

from typing import Iterable, Protocol

from .models import AuditEvent


class AuditSink(Protocol):
    """Destination capable of persisting one or more KYVERNEX audit events."""

    def append(self, event: AuditEvent) -> object:
        ...

    def append_many(self, events: Iterable[AuditEvent]) -> object:
        ...


def persist_audit(sink: AuditSink | None, events: Iterable[AuditEvent]) -> None:
    """Persist a completed audit batch when a sink is configured.

    The iterable is materialized exactly once so generators are safe and empty
    batches do not trigger storage writes.
    """

    if sink is None:
        return
    batch = tuple(events)
    if batch:
        sink.append_many(batch)
