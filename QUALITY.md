# KYVERNEX QUALITY BASELINE

## Current stable baseline

KYVERNEX `1.1.0` is the verified and published stable baseline under immutable tag `v1.1.0` and is marked Latest.

Preserved historical releases:

- `v1.1.0-rc.1`: immutable prerelease record;
- `v1.0.0`: immutable previous stable release.

## Verified stable 1.1.0 evidence

- targeted governance tests: passed;
- complete repository suite: passed;
- source and wheel builds: passed;
- clean wheel installation: passed;
- installed package and public API version: `1.1.0`;
- installed `kyvernex-governance` smoke test: passed;
- KGO v3 governed result enforcement: passed;
- stable-promotion commit `56bd8da`: green in the user-observed GitHub Actions page;
- GitHub Release `KYVERNEX 1.1.0`: published and marked Latest.

## Verified governance capability

Selected M4 capability: `KPM/KGO autonomous control CLI`.

Verified controls:

- deterministic `start`, `status`, `advance` and `resume` commands;
- fail-closed malformed-plan and unknown-dependency handling;
- closed-milestone validation;
- existing-checkpoint overwrite prevention;
- active-item advancement prevention;
- governed exit codes;
- invalid input and policy error handling;
- no unsupported test, CI, repository-write or release claim;
- write boundary limited to the supplied checkpoint path;
- installed-wheel console-script smoke verification.

## Release quality state

| Area | State |
|---|---|
| M4 specification and manifest | VERIFIED |
| Governance CLI implementation | VERIFIED |
| M5 stable promotion | COMPLETE |
| Targeted tests | GREEN |
| Complete suite | GREEN |
| Source and wheel builds | GREEN |
| Clean installation | GREEN |
| Installed CLI smoke test | GREEN |
| Package version | `1.1.0` |
| Public API version | `1.1.0` |
| Stable tag | `v1.1.0` |
| Stable GitHub Release | PUBLISHED / LATEST |
| Active technical blocker | NONE |
| Open governed blocker issues | NONE |

## Completion metrics

| Area | Result |
|---|---:|
| M4 work items | 7/7 DONE |
| S002 story points | 37/37 DONE |
| M5 work items | 3/3 DONE |
| S003 | DONE |
| Stable 1.1.0 technical gates | Complete |
| Stable 1.1.0 publication | Complete |

## Issue reconciliation

Historical KGO blocker issues `#1`, `#2`, `#3` and stale verified-evidence issue `#4` are closed as completed. Their audit history is preserved. Current green evidence takes precedence over the historical failure snapshots that created those records.

## Quality controls

- Current commit evidence takes precedence over historical workflow results.
- Correctness evidence cannot be replaced by performance measurements.
- Rollback requires explicit current failure evidence and authorization.
- The governance CLI cannot mutate Git refs, source files, branches, issues or releases.
- Published tags remain immutable historical records.
- The proprietary license notice remains in force; independent legal review remains recommended.
- New work requires a documented defect, verified release feedback, authorized maintenance or a separately approved milestone.

## Current quality decision

`KYVERNEX 1.1.0` satisfies the stable release quality gate. It is implemented, verified, tagged, published and marked Latest. KPM/KGO remain in safe stop with no active blocker or authorized backlog item.