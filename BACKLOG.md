# KYVERNEX BACKLOG

## Baseline status
- Stable published release: `1.1.0`
- Published stable tag: `v1.1.0`
- Active milestone: `M6 — KYVERNEX Plugin Runtime`
- Active sprint: `S007 — Fail-closed plugin configuration`
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
| M6-W004 | Host adapter boundary and reference in-process adapter | P1 | 8 | BACKLOG | M6-W003 |
| M6-W005 | Configuration loading, validation and fail-closed defaults | P0 | 5 | IN_VERIFICATION | M6-W002 |
| M6-W006 | Security-boundary and lifecycle integration tests | P0 | 8 | BACKLOG | M6-W003, M6-W004, M6-W005 |
| M6-W007 | Installable example, documentation and package entry point | P1 | 5 | BACKLOG | M6-W006 |
| M6-W008 | Complete verification, build, clean install and smoke test | P0 | 8 | BACKLOG | M6-W007 |
| M6-W009 | Prepare first `1.2.0` prerelease evidence | P1 | 3 | BACKLOG | M6-W008 |

Progress remains `3/9` work items and `21/58` story points until M6-W005 receives fresh green evidence.

## M6-W005 implementation
- `src/kyvernex/plugin_config.py` defines immutable validated configuration;
- `src/kyvernex/plugin_runtime.py` consumes only the validated configuration object;
- `tests/test_plugin_config.py` covers defaults, unknown fields, normalized roots, allowlists, wildcard rejection, mandatory audit and lifecycle immutability;
- defaults grant no filesystem, network or process authority;
- repository authority remains forbidden;
- configuration cannot be replaced after initialization.

## Verification gate
Close M6-W005 only after targeted and complete tests are green for the exact final commit and no authority expansion is observed.

## Release states
- `v1.1.0`: stable Latest and immutable;
- `v1.1.0-rc.1`: historical prerelease;
- `v1.0.0`: historical stable;
- `1.2.0`: development target, not released.
