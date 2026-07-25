# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Active milestone: **M6 — KYVERNEX Plugin Runtime**
- Active sprint: **S008 — Minimum reference adapter**
- Governance mode: **AUTONOMOUS, SCOPE-LOCKED VERIFICATION**
- KPM cycle: `KPM-CYCLE-018`
- KGO cycle: `KGO-CYCLE-029`
- Target version: `1.2.0`
- Canonical scope lock: `repository/specifications/M6_SCOPE_LOCK.md`

## Product objective
Deliver one installable Python in-process plugin path:

```text
Python host -> KyvernexPluginRuntime -> governed decision -> bounded callable adapter -> structured response
```

M6 is not a general integration platform. It ends after this path is installable, demonstrated and verified.

## Completed work
- M6-W001 plugin contract: `DONE`
- M6-W002 core runtime: `DONE`
- M6-W003 governed host contracts: `DONE`
- M6-W005 fail-closed configuration: `DONE`

Verified green baselines:
- lifecycle runtime: `691c769`;
- host contracts: `83ce3a3`;
- configuration boundary: `a8e7f36`.

## Active work
- M6-W004 minimum reference in-process callable adapter: `IN_VERIFICATION`

Repository evidence:
- `src/kyvernex/plugin_adapter.py` implements the single permitted adapter;
- `tests/test_plugin_adapter.py` covers capability immutability, runtime authorization, blocked execution, JSON result validation, bounded health and idempotent shutdown;
- `src/kyvernex/__init__.py` exposes the adapter as part of the package API.

The adapter wraps one host-supplied Python callable. It contains no network, filesystem, subprocess, repository, environment, discovery or governance-policy operation.

## M6-W004 verification gate
Close M6-W004 only when current CI confirms:
1. targeted adapter tests are green;
2. the complete repository suite is green;
3. blocked requests never invoke the callable;
4. no second adapter or ambient authority was introduced.

## Remaining direct path
1. M6-W006: focused lifecycle and authority integration tests;
2. M6-W007: one minimal installable example and package entry point;
3. M6-W008: complete suite, build, clean install and smoke test;
4. M6-W009: prerelease evidence for `1.2.0`.

No additional feature work may be inserted into M6.

## Explicit exclusions
Remote adapters, ChatGPT or browser integrations, plugin discovery, marketplace, databases, queues, background workers, dashboards, authentication systems, billing, secret vaults, arbitrary tool execution, GitHub mutation, multiple SDKs, independent implementation and conformance certification are outside M6.

## Continuation rule
Read CI evidence for the exact M6-W004 final state. On green, close M6-W004 and proceed directly to M6-W006. On failure, record and repair only the minimum adapter path.