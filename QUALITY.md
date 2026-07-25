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

## Verified M4 quality gate

Selected capability: `KPM/KGO autonomous control CLI`.

Verified controls:

- deterministic `start`, `status`, `advance` and `resume` commands;
- fail-closed malformed-plan and unknown-dependency handling;
- closed-milestone validation;
- existing-checkpoint overwrite prevention;
- active-item advancement prevention;
- blocked-state exit code `2`;
- invalid input and policy error handling;
- no unsupported test, CI, repository-write or release claim;
- write boundary limited to the supplied checkpoint path;
- installed-wheel console-script smoke test.

## Release-candidate evidence

| Area | State |
|---|---|
| M4 specification and manifest | VERIFIED |
| CLI implementation | VERIFIED |
| Targeted tests | GREEN |
| Complete suite | GREEN |
| Source and wheel builds | GREEN |
| Clean installation | GREEN |
| Installed CLI smoke test | GREEN |
| Package version | `1.1.0rc1` |
| Public API version | `1.1.0rc1` |
| KGO v3 final candidate workflow | GREEN on commit `807def6` |
| Active technical blocker | NONE |

## Completion metrics

| Area | Result |
|---|---:|
| M4 work items | 7/7 DONE |
| S002 story points | 37/37 DONE |
| Release-candidate technical gates | Complete |
| GitHub prerelease publication | Pending external action |

## Quality controls

- Current commit evidence takes precedence over historical workflow results.
- Correctness evidence cannot be replaced by performance measurements.
- Rollback requires explicit current failure evidence and authorization.
- The CLI cannot mutate Git refs, source files, branches, issues or releases.
- The proprietary license notice remains in force; independent legal review remains recommended.
- `v1.0.0` remains immutable and Latest until a future stable release is explicitly published.

## Current quality decision

`KYVERNEX 1.1.0rc1` satisfies the technical Release Candidate gate. It is authorized for publication as the separate prerelease `v1.1.0-rc.1`, provided it is marked as a prerelease and not as Latest.
