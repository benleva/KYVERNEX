# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Active milestone: `M6 — KYVERNEX Plugin Runtime`
- Active sprint: `S008 — Minimum reference adapter`
- Target version: `1.2.0`
- Scope lock: `repository/specifications/M6_SCOPE_LOCK.md`

## M6 work items

| Work item | Deliverable | Priority | Story points | Status | Dependencies |
|---|---|---:|---:|---|---|
| M6-W001 | Frozen plugin contract and authority boundaries | P0 | 5 | DONE | stable baseline |
| M6-W002 | Core runtime and lifecycle state machine | P0 | 8 | DONE | M6-W001 |
| M6-W003 | Governed request, response and error contracts | P0 | 8 | DONE | M6-W002 |
| M6-W004 | One bounded in-process callable adapter | P0 | 3 | IN_PROGRESS | M6-W003, M6-W005 |
| M6-W005 | Immutable fail-closed configuration | P0 | 5 | DONE | M6-W002 |
| M6-W006 | Focused lifecycle and authority integration tests | P0 | 5 | BACKLOG | M6-W004 |
| M6-W007 | One minimal example and package entry point | P0 | 3 | BACKLOG | M6-W006 |
| M6-W008 | Complete suite, build, clean install and smoke test | P0 | 5 | BACKLOG | M6-W007 |
| M6-W009 | Prepare `1.2.0` prerelease evidence | P1 | 2 | BACKLOG | M6-W008 |

Revised total after scope lock: `44` story points.
Completed: `26/44` story points and `4/9` work items.

## M6-W004 acceptance boundary
M6-W004 is complete only when one adapter:

- wraps one explicitly supplied Python callable;
- exposes an explicit immutable capability set;
- receives only runtime-authorized requests;
- reads no environment variables;
- performs no built-in network, filesystem, subprocess, repository or publication operation;
- makes no governance decision;
- validates that its result is JSON-serializable;
- reports simple health;
- shuts down idempotently.

No second adapter or remote protocol is permitted.

## Remaining path to done
After M6-W004, KPM/KGO may execute only M6-W006, M6-W007, M6-W008 and M6-W009 in that order. New feature work is prohibited inside M6.

## Out of scope
Remote integrations, platform-specific plugins, dynamic discovery, marketplace, persistence, queues, workers, dashboards, authentication, billing, secret storage, arbitrary tool execution, GitHub mutation, additional SDKs, independent implementation and conformance certification.

## Stop policy
Stop immediately on scope growth, current verification failure, authority expansion, contract contradiction, external publication boundary or milestone completion.
