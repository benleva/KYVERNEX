# KYVERNEX BACKLOG

## Baseline status
- Stable published release: `1.1.0`
- Published stable tag: `v1.1.0`
- Active milestone: `M6 — KYVERNEX Plugin Runtime`
- Active sprint: `S008 — Reference host adapter`
- Target version: `1.2.0`

## Completed milestones
- M2 — Governance consolidation: `DONE`
- M3 — Autonomous Development: `DONE`
- M4 — Governed post-release evolution: `DONE`
- M5 — Promote 1.1 release candidate to stable: `DONE`

## Active milestone

| Work item | Capability | Priority | Story points | Status | Dependencies |
|---|---|---:|---:|---|---|
| M6-W001 | Freeze plugin contract and authority boundaries | P0 | 5 | DONE | stable baseline |
| M6-W002 | Core runtime and lifecycle state machine | P0 | 8 | DONE | M6-W001 |
| M6-W003 | Governed host request, response and error contracts | P0 | 8 | DONE | M6-W002 |
| M6-W004 | Host adapter boundary and reference in-process adapter | P1 | 8 | IN_PROGRESS | M6-W003 |
| M6-W005 | Configuration loading, validation and fail-closed defaults | P0 | 5 | DONE | M6-W002 |
| M6-W006 | Security-boundary and lifecycle integration tests | P0 | 8 | BACKLOG | M6-W003, M6-W004, M6-W005 |
| M6-W007 | Installable example, documentation and package entry point | P1 | 5 | BACKLOG | M6-W006 |
| M6-W008 | Complete verification, build, clean install and smoke test | P0 | 8 | BACKLOG | M6-W007 |
| M6-W009 | Prepare first `1.2.0` prerelease evidence | P1 | 3 | BACKLOG | M6-W008 |

Progress: `4/9` work items and `26/58` story points.

## Verified evidence

### M6-W001
Frozen contract and schema are stored under `repository/specifications/`.

### M6-W002
Lifecycle runtime verified green on commit `691c769`.

### M6-W003
Governed host contracts verified green on commit `83ce3a3`.

### M6-W005
Fail-closed configuration verified green on commit `a8e7f36` after correcting a stale historical test assertion. Test Suite, Reference Prototype Tests, KGO v3 and Pages are green. No filesystem, network, process or repository authority expansion was introduced.

## Current work item
M6-W004 must provide:

- an explicit adapter protocol implementation;
- a bounded reference in-process adapter;
- deterministic capability declaration;
- health reporting;
- invocation only after runtime authorization;
- result validation;
- idempotent shutdown;
- no governance-policy decision inside the adapter;
- no authority expansion from request content, environment variables or ambient host privileges.

## Release states
- `v1.1.0`: stable Latest and immutable;
- `v1.1.0-rc.1`: historical prerelease;
- `v1.0.0`: historical stable;
- `1.2.0`: development target, not released.

## Continuation policy
Complete M6-W004 before activating M6-W006. Stop for current verification failure, adapter authority expansion, contract contradiction, unresolved P0 security boundary, external publication boundary or milestone completion.