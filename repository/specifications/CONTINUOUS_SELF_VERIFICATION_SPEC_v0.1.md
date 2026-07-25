# CONTINUOUS SELF-VERIFICATION SPEC v0.1

## Purpose
Implement M3-W003 as the release-facing controller that accepts current targeted-test and complete-suite evidence, prevents advancement without complete verification and never fabricates a source-code defect from missing infrastructure evidence.

## Milestone work item
- ID: `M3-W003`
- Title: `Continuous self-verification controller`
- Milestone: `M3`
- Dependency: `M3-W002`

## Required inputs
- governed work-item identifier;
- targeted-test output and execution outcome;
- complete-suite output and execution outcome.

## Decisions
- `VERIFIED`: targeted and complete current executions both succeed and contain no parsed failures;
- `REPAIR_REQUIRED`: either current execution contains explicit test-failure evidence;
- `EXECUTION_BLOCKED`: verification is incomplete or unavailable without supported code-failure evidence.

## Required artifacts
- `SELF_VERIFICATION.json`;
- `SELF_VERIFICATION_SUMMARY.md` in CI.

## Integration requirements
1. Run M3-W003 targeted tests before the complete suite.
2. Evaluate both current outcomes through the controller.
3. Advance ADE only after both outcomes succeed.
4. Persist the controller result with the remaining KGO evidence.
5. Fail the governed workflow when either verification boundary does not succeed.

## Definition of Done
- controller implementation committed;
- public API exported;
- unit tests cover verified, repair, infrastructure-blocked and invalid-input paths;
- GitHub Actions integrates targeted and complete verification;
- specification and update record committed;
- project status synchronized;
- fresh complete CI evidence succeeds.
