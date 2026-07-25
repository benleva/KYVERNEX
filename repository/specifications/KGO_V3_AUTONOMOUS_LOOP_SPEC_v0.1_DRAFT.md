# KGO v3 Autonomous Loop Specification v0.1 DRAFT

## Purpose
KGO v3 is the closed-loop governance state machine for KYVERNEX. It decides from the current execution evidence whether to continue, repair, or complete the governed scope.

## Governing principle
Historical failed runs are immutable evidence of earlier commits and must not be reopened as current defects. Absence of supported failure evidence is not evidence of a code failure.

## Inputs
- previous persisted `KGO_STATE.json`;
- current pytest output;
- current CI outcome;
- current commit identifier;
- current work item;
- optional milestone-complete signal.

## Decisions
- `CONTINUE`: current CI succeeds, or no supported code failure is present;
- `REPAIR`: current output contains explicit test-failure evidence;
- `COMPLETE`: the governed milestone is complete.

## Persistent artifacts
- `KGO_STATE.json` stores the latest loop state;
- `KGO_V3_LOOP.json` stores the complete decision and parsed evidence;
- `KGO_V3_SUMMARY.md` provides the human-readable run summary.

## Safety and momentum rules
1. Only current-run evidence may open a repair cycle.
2. Historical red runs remain historical and do not block a later verified commit.
3. A successful CI outcome advances the loop even if a human-readable parser does not recover positive test counts.
4. A non-success outcome without test-failure evidence is recorded as an execution condition, not fabricated as a source-code defect.
5. Completion closes the governed scope under the anti-infinite rule.

## Boundaries
KGO v3 selects the next governance decision. Semantic code generation, repository writes, branch creation, merge, and external platform actions remain subject to the authorized executor and repository permissions.

## Verification
Unit tests shall cover successful continuation, evidence-based repair, non-fabrication of blockers, milestone completion, state persistence, and workflow integration.
