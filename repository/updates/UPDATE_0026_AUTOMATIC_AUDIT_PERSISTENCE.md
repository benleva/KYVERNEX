# UPDATE_0026 — Automatic Audit Persistence

## Status
DRAFT IMPLEMENTATION — tests added, not yet CI-verified.

## Objective
Connect the persistent Audit Trace to executable KYVERNEX components so completed audit batches are stored automatically instead of requiring manual append calls.

## Changes
- Added `AuditSink` protocol and `persist_audit` helper.
- `KyvernexEngine` accepts an optional `audit_sink` and persists its completed execution audit batch.
- `KyvernexOrchestrator` persists adapter and response-governance audit events through the engine sink.
- `CognitiveDeletionCoordinator` accepts an optional `audit_sink` and persists successful deletion audit events.
- Exported the audit sink API from the package root.
- Added focused tests for engine, orchestrator, and deletion persistence.

## Semantics
Audit persistence occurs after the governed operation has produced its final result. A sink failure is therefore visible to the caller and is not silently ignored. This update does not claim atomicity between domain-state persistence and audit-ledger persistence.

## Compatibility
The sink is optional. Existing constructors and behavior remain valid when no sink is supplied.

## Known limitations
- ResponseGovernor does not own a sink directly; its events are persisted by the orchestrator batch.
- Durable and multi-transaction deletion coordinators do not yet expose an `audit_sink` constructor parameter.
- Domain mutation and audit append are not one ACID transaction.
- Tests are present but not yet confirmed by CI.
