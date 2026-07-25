# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Active milestone: `M6 — KYVERNEX Plugin Runtime`
- Active sprint: `S009 — Focused plugin integration verification`
- Target version: `1.2.0`
- Scope lock: `repository/specifications/M6_SCOPE_LOCK.md`

## M6 work items

| Work item | Deliverable | Priority | Story points | Status | Dependencies |
|---|---|---:|---:|---|---|
| M6-W001 | Frozen plugin contract and authority boundaries | P0 | 5 | DONE | stable baseline |
| M6-W002 | Core runtime and lifecycle state machine | P0 | 8 | DONE | M6-W001 |
| M6-W003 | Governed request, response and error contracts | P0 | 8 | DONE | M6-W002 |
| M6-W004 | One bounded in-process callable adapter | P0 | 3 | DONE | M6-W003, M6-W005 |
| M6-W005 | Immutable fail-closed configuration | P0 | 5 | DONE | M6-W002 |
| M6-W006 | Focused lifecycle and authority integration tests | P0 | 5 | IN_PROGRESS | M6-W004 |
| M6-W007 | One minimal example and package entry point | P0 | 3 | BACKLOG | M6-W006 |
| M6-W008 | Complete suite, build, clean install and smoke test | P0 | 5 | BACKLOG | M6-W007 |
| M6-W009 | Prepare `1.2.0` prerelease evidence | P1 | 2 | BACKLOG | M6-W008 |

Revised total after scope lock: `44` story points.
Completed: `29/44` story points and `5/9` work items.

## Verified evidence
- M6-W002 lifecycle runtime: green on `691c769`;
- M6-W003 governed contracts: green on `83ce3a3`;
- M6-W005 fail-closed configuration: green on `a8e7f36`;
- M6-W004 minimum callable adapter: green on `b138134` for Test Suite, KGO v3, Reference Prototype Tests and Pages.

## M6-W006 acceptance boundary
M6-W006 may add tests only. It must verify the existing chain:

```text
host callable -> InProcessCallableAdapter -> KyvernexPluginRuntime -> governed response
```

Required tests:
- authorized execution succeeds through the full path;
- blocked execution never invokes the callable;
- zero-authority defaults remain present;
- configured capability intersection is enforced;
- invalid result and callable failure produce governed failure behavior;
- lifecycle and shutdown remain deterministic and terminal;
- no network, filesystem, process, repository, environment or discovery authority is introduced.

M6-W006 must not add a new adapter, transport, host platform, service or runtime capability.

## Remaining path to done
After M6-W006, execute only M6-W007, M6-W008 and M6-W009 in that order. New feature work is prohibited inside M6.

## Stop policy
Stop immediately on scope growth, current verification failure, authority expansion, contract contradiction, external publication boundary or milestone completion.
