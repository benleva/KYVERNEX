# KYVERNEX QUALITY BASELINE

## Stable baseline

KYVERNEX `1.0.0` remains the verified and published stable baseline under immutable tag `v1.0.0`.

Verified Release 1.0 evidence:

- M3 targeted tests: passed;
- complete repository suite: passed;
- source and wheel builds: passed;
- clean wheel installation: passed;
- installed package and public API version: `1.0.0`;
- GitHub Actions run `#58`: green;
- GitHub Release `KYVERNEX 1.0.0`: published and marked Latest.

## Active M4 quality gate

Selected capability: `KPM/KGO autonomous control CLI`.

Implemented controls:

- deterministic `start`, `status`, `advance` and `resume` commands;
- fail-closed malformed-plan and unknown-dependency handling;
- closed-milestone validation;
- existing-checkpoint overwrite prevention;
- active-item advancement prevention;
- blocked-state exit code `2`;
- no unsupported test, CI, repository-write or release claim;
- write boundary limited to the supplied checkpoint path;
- installed-wheel console-script smoke test integrated into CI.

## Current evidence status

| Area | State |
|---|---|
| M4 specification and manifest | PRESENT |
| CLI implementation | PRESENT |
| Targeted tests | PRESENT, FRESH CI PENDING |
| Complete suite | FRESH CI PENDING |
| Source and wheel builds | FRESH CI PENDING |
| Clean installation | FRESH CI PENDING |
| Installed CLI smoke test | FRESH CI PENDING |
| Active documented blocker | NONE BEFORE CI RESULT |

No M4 verification success is claimed until a fresh GitHub Actions run completes.

## Quality controls

- Current commit evidence takes precedence over historical workflow results.
- Correctness evidence cannot be replaced by performance measurements.
- Rollback requires explicit current failure evidence and authorization.
- The CLI cannot mutate Git refs, source files, branches, issues or releases.
- The proprietary license notice remains in force; independent legal review remains recommended.

## Current quality decision

`M4-W005` is implemented and under verification. KGO must stop and record evidence if the current workflow fails; it may advance to release-candidate synchronization only after all M4 gates are green.