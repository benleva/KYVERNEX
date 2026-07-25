# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Active milestone: **M6 — KYVERNEX Plugin Runtime**
- Active sprint: **S008 — Minimum reference adapter**
- Governance mode: **AUTONOMOUS, SCOPE-LOCKED**
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
- M6-W004 minimum reference in-process callable adapter: `IN_PROGRESS`

M6-W004 is limited to one adapter wrapping one host-supplied Python callable. It may not access network, filesystem, subprocesses, repositories, environment variables or external services by itself. It may not decide policy or authorization.

## Remaining direct path
1. M6-W004: one bounded callable adapter;
2. M6-W006: focused lifecycle and authority integration tests;
3. M6-W007: one minimal installable example and package entry point;
4. M6-W008: complete suite, build, clean install and smoke test;
5. M6-W009: prerelease evidence for `1.2.0`.

No additional feature work may be inserted into M6.

## Explicit exclusions
Remote adapters, ChatGPT or browser integrations, plugin discovery, marketplace, databases, queues, background workers, dashboards, authentication systems, billing, secret vaults, arbitrary tool execution, GitHub mutation, multiple SDKs, independent implementation and conformance certification are outside M6.

## Continuation rule
Every change must move the single in-process plugin path measurably closer to clean-install smoke verification. Stop on scope expansion, test failure, authority expansion, contract contradiction, external publication boundary or milestone completion.
