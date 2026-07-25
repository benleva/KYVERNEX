# Evidence-based Rollback Controller Specification v0.1

## Work item
`M3-W005`

## Purpose
Authorize a rollback only when current verification evidence supports it and the approved isolated changeset has not changed.

## Boundary
The controller produces a deterministic commit-level rollback plan. It does not execute git commands, call GitHub, rewrite repository history, or widen KGO/KPM scope.

## Inputs
- current `SelfVerificationResult`;
- failed commit identifier;
- restore commit identifier;
- approved isolated changeset fingerprint;
- current changeset fingerprint;
- explicit executor authorization.

## Decisions
- `NOT_REQUIRED`: targeted and complete verification succeeded;
- `ROLLBACK_APPROVED`: current supported test-failure evidence exists;
- `EXECUTION_BLOCKED`: verification evidence is incomplete and cannot justify rollback.

## Safety controls
- explicit authorization is mandatory by default;
- failed and restore commits are mandatory and must differ;
- approved and current changeset fingerprints must match;
- only `CURRENT_TEST_FAILURE_EVIDENCE` can authorize rollback under the default policy;
- unknown verification states are rejected;
- the result is sealed with a deterministic SHA-256 evidence fingerprint.

## Execution boundary
`command_hint` is advisory evidence for an authorized executor. The controller itself performs no repository mutation.

## Definition of Done
- controller implementation present;
- public API exported;
- deterministic decision tests present;
- mutation, authorization, and incomplete-evidence tests present;
- workflow runs targeted rollback tests before the complete suite;
- project status synchronized;
- fresh complete CI evidence successful.
