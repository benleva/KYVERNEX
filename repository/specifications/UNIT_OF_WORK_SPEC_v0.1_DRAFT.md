# KYVERNEX Unit of Work Specification v0.1 DRAFT

## Status

Draft implementation specification.

## Purpose

`KyvernexUnitOfWork` coordinates staged writes to session memory, the cognitive graph and the configured audit sink. The objective is to prevent partially-applied cognitive writes inside one process when a commit operation fails.

## Scope

Version 0.1 coordinates creation of:

- cognitive objects in `SessionMemory`;
- cognitive relations in `CognitiveGraph`;
- audit batches through `AuditSink`.

Deletion transactions remain governed by the existing deletion coordinators and journals.

## Transaction states

- `NUOVA`
- `ATTIVA`
- `CONFERMATA`
- `ANNULLATA`
- `FALLITA`

Only an active transaction may stage data or commit.

## Commit order

1. Store staged cognitive objects.
2. Add staged cognitive relations.
3. Persist staged audit events plus `TRANSAZIONE_CONFERMATA`.
4. Mark the transaction as committed.

## Validation rules

- The session id must be present.
- Object ids must be unique within the transaction and absent from session memory.
- Relation ids must be unique within the transaction.
- A relation must belong to the transaction session.
- Both relation endpoints must already exist in memory or be staged in the same transaction.
- Audit events must belong to the transaction session.

## Failure behavior

If memory, graph or audit persistence fails, applied graph relations and memory objects are removed in reverse order. The transaction enters `FALLITA` and raises `UnitOfWorkCommitError`.

Rollback errors are included in the raised error and are never silently discarded.

## Audit atomicity limitation

The coordinator assumes that `AuditSink.append_many()` is atomic from the caller's perspective. If an external sink persists only part of a batch and then raises, KYVERNEX can roll back memory and graph state but cannot erase the already-persisted external audit records.

## Concurrency and durability limitations

Version 0.1 is process-local and uses `RLock`. It is not a distributed transaction manager and does not provide crash-safe recovery. Durable multi-resource transactions require a later journaled implementation.

## Compliance expectations

An implementation conforming to this draft must:

- stage changes before commit;
- reject invalid state transitions;
- validate relation referential integrity;
- reverse applied memory and graph writes after commit failure;
- expose the final transaction state;
- report rollback failure explicitly.
