# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Active milestone: **M6 — KYVERNEX Plugin Runtime**
- Completed sprint: **S008 — Minimum reference adapter**
- Active sprint: **S009 — Focused plugin integration verification**
- Governance mode: **AUTONOMOUS, SCOPE-LOCKED**
- KPM cycle: `KPM-CYCLE-019`
- KGO cycle: `KGO-CYCLE-030`
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
- M6-W004 minimum reference in-process callable adapter: `DONE`
- M6-W005 fail-closed configuration: `DONE`

Verified green baselines:
- lifecycle runtime: `691c769`;
- host contracts: `83ce3a3`;
- configuration boundary: `a8e7f36`;
- minimum callable adapter: `b138134`.

User-observed GitHub Actions evidence confirms green results on commit `b138134` for the Test Suite, KGO v3, Reference Prototype Tests and Pages deployment.

## Active work
- M6-W006 focused lifecycle and authority integration tests: `IN_PROGRESS`

M6-W006 is limited to tests of the existing minimum path. It may not add capabilities, adapters, external systems or new product behavior.

Required integration evidence:
1. authorized host request reaches the callable and returns a structured success response;
2. blocked request never reaches the callable;
3. zero-authority defaults remain intact;
4. lifecycle initialize, validate, execute, status and shutdown remains deterministic;
5. shutdown remains terminal and idempotent;
6. no network, filesystem, process, repository or environment authority appears.

## Remaining direct path
1. M6-W006: focused lifecycle and authority integration tests;
2. M6-W007: one minimal installable example and package entry point;
3. M6-W008: complete suite, build, clean install and smoke test;
4. M6-W009: prerelease evidence for `1.2.0`.

No additional feature work may be inserted into M6.

## Continuation rule
Implement only focused end-to-end tests for the frozen minimum plugin path. Stop on scope expansion, current test failure, authority expansion, contract contradiction, external publication boundary or milestone completion.
