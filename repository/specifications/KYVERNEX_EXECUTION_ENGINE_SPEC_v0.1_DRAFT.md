# KYVERNEX EXECUTION ENGINE SPECIFICATION

Status: DRAFT
Version: 0.1
Component: KEX

## 1. Purpose
KEX is the governed execution boundary of KYVERNEX. KGO decides what must be attempted, KPM tracks the governed work, and KEX performs only explicitly authorized external actions while preserving execution evidence.

## 2. Architectural boundary
KEX must not decide project priorities, close milestones, invent test evidence, or bypass KGO/KPM policy. Its responsibilities are limited to validation, execution, result capture and ordered execution.

## 3. Core objects
- `ExecutionRequest`: immutable request identity, command, working directory, purpose, timeout and optional environment.
- `ExecutionPolicy`: allowlisted programs, authorized working roots, environment override rule and maximum timeout.
- `CommandRunner`: injectable execution adapter protocol.
- `SubprocessCommandRunner`: local runner using `shell=False`, captured stdout/stderr and explicit timeout.
- `ExecutionResult`: correlated evidence with status, return code, output and execution location.
- `KyvernexExecutionEngine`: policy gate, history ledger and sequential execution coordinator.

## 4. Mandatory controls
1. Every request has a unique non-empty identifier and declared purpose.
2. The executable must be present in the policy allowlist.
3. The working directory must resolve inside an authorized root.
4. Request timeout must not exceed policy.
5. Environment overrides are denied unless explicitly enabled.
6. Shell execution is never implicit.
7. Returned evidence must correlate to the originating request.
8. Ordered execution stops on the first failure by default.

## 5. Evidence semantics
A result is verified execution evidence only after a runner has actually returned it. File presence, planned commands and committed tests are not test-pass evidence.

## 6. KGO integration contract
KGO may submit execution requests to KEX. KGO must consume the returned result and update checkpoint fields only from real evidence. KEX does not directly mark a Definition of Done complete.

## 7. Security posture
The default architecture is deny-first. Capability is granted through narrow policy, explicit roots and injectable runners. Network access, GitHub writes, CI dispatch and credential use require dedicated adapters and policies in later specifications.

## 8. Definition of Done for v0.1
- implementation committed;
- public API exported;
- unit tests committed for allowlist, root restriction, evidence recording and stop-on-failure;
- specification and update record committed;
- complete test suite and CI verified separately before the feature may be declared DONE.
