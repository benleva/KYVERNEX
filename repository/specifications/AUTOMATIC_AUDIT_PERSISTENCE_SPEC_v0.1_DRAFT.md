# AUTOMATIC AUDIT PERSISTENCE SPEC v0.1 DRAFT

## 1. Purpose
Define how executable KYVERNEX components deliver generated `AuditEvent` batches to a persistent audit destination.

## 2. Audit sink contract
An audit sink shall expose:

- `append(event)` for one event;
- `append_many(events)` for an ordered batch.

`JsonAuditTrace` conforms structurally to this contract.

## 3. Ordering
Events shall be appended in the same order in which the producing component returns them. Engine events precede orchestrator adapter events because engine governance completes first.

## 4. Integration points

### 4.1 KyvernexEngine
When configured with an audit sink, the engine shall persist the complete `ExecutionResult.audit` batch before returning the result.

### 4.2 KyvernexOrchestrator
The orchestrator shall persist only `adapter_audit` through the sink already configured on its engine. It shall not append the engine batch again.

### 4.3 CognitiveDeletionCoordinator
When configured with an audit sink, the coordinator shall persist the complete successful `DeletionResult.audit` batch before returning the result.

## 5. Failure behavior
Audit sink failures shall propagate to the caller. The prototype shall not silently discard audit evidence.

## 6. Compatibility
The sink is optional. Absence of a sink preserves previous process-local return behavior.

## 7. Non-goals
This draft does not define:

- ACID atomicity between memory, graph, journal, and audit trace;
- remote or distributed audit delivery;
- signed checkpoints or external notarization;
- automatic persistence of failed operations that do not produce a result batch.

## 8. Verification targets
Tests should verify:

- full engine batch persistence;
- engine plus adapter batch persistence without duplication;
- deletion batch persistence;
- hash-chain validity after automatic persistence.
