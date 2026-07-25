# KYVERNEX BACKLOG

## Baseline status

- Stable published release: `1.1.0`
- Published stable tag: `v1.1.0`
- Previous stable tag: `v1.0.0`
- Published prerelease tag: `v1.1.0-rc.1`
- Active milestone: `M6 — KYVERNEX Plugin Runtime`
- Active sprint: `S006 — Govern host contracts`
- Target version: `1.2.0`
- Maintenance line: `1.1.x`

## Completed milestones

### M2 — Governance consolidation
Status: `DONE`

### M3 — Autonomous Development
Status: `DONE`

### M4 — Governed post-release evolution
Status: `DONE`
Completion: `7/7`, `100%`.

### M5 — Promote 1.1 release candidate to stable
Status: `DONE`
Completion: `3/3`, `100%`.

## Active milestone

### M6 — KYVERNEX Plugin Runtime

Status: `ACTIVE`
Target: `1.2.0`
Scope: build the installable product plugin layer over the existing KYVERNEX engine. The strategic roadmap is unchanged.

| Work item | Capability | Priority | Story points | Status | Dependencies |
|---|---|---:|---:|---|---|
| M6-W001 | Freeze the plugin contract, lifecycle, schemas and authority boundaries | P0 | 5 | DONE | Stable `v1.1.0` baseline |
| M6-W002 | Implement the core plugin runtime and lifecycle state machine | P0 | 8 | DONE | M6-W001 |
| M6-W003 | Implement governed host request, response and error contracts | P0 | 8 | IN_VERIFICATION | M6-W002 |
| M6-W004 | Add host adapter boundary and reference in-process adapter | P1 | 8 | BACKLOG | M6-W003 |
| M6-W005 | Add configuration loading, validation and fail-closed defaults | P0 | 5 | BACKLOG | M6-W002 |
| M6-W006 | Add security-boundary and lifecycle integration tests | P0 | 8 | BACKLOG | M6-W003, M6-W004, M6-W005 |
| M6-W007 | Add installable example, developer documentation and package entry point | P1 | 5 | BACKLOG | M6-W006 |
| M6-W008 | Run complete verification, build, clean installation and plugin smoke test | P0 | 8 | BACKLOG | M6-W007 |
| M6-W009 | Prepare the first `1.2.0` prerelease package and release evidence | P1 | 3 | BACKLOG | M6-W008 |

Progress: `2/9` work items, `13/58` story points. M6-W003 remains open until fresh CI is green.

## M6-W003 current implementation

- `src/kyvernex/plugin_contracts.py` defines immutable request, response, decision, evidence and error envelopes.
- `src/kyvernex/plugin_runtime.py` validates and authorizes requests before adapter invocation.
- `tests/test_plugin_runtime.py` covers success, blocked, failed, duplicate-ID, unknown-field, limit and lifecycle behavior.
- blocked requests do not reach the adapter;
- no ambient filesystem, network, process or repository authority is added.

## Definition of M6 Done

M6 is complete only when:

- the plugin contract and lifecycle are frozen and documented;
- the runtime is installable and importable;
- lifecycle transitions are deterministic and fail closed;
- host requests use structured validated contracts;
- all execution passes through existing governance and KEX boundaries;
- configuration cannot expand authority silently;
- targeted and complete tests are green;
- source and wheel builds succeed;
- clean installation and plugin smoke tests pass;
- release evidence is recorded without unsupported claims.

## Release states

- `v1.1.0`: published stable release and Latest;
- `v1.1.0-rc.1`: preserved immutable prerelease record;
- `v1.0.0`: preserved immutable historical stable release;
- `1.2.0`: active development target, not yet released.

## Continuation policy

Read current CI evidence for M6-W003. On green, close it and activate the next dependency-valid work item. On failure, record the exact failure before repair.
