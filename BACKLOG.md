# KYVERNEX BACKLOG

## Baseline status

- Stable release: `1.0.0`
- Published stable tag: `v1.0.0`
- Verified release candidate: `1.1.0rc1`
- Planned prerelease tag: `v1.1.0-rc.1`
- Active milestone: none
- Active sprint: none
- Maintenance line: `1.0.x`

## Completed milestones

### M2 — Governance consolidation
Status: `DONE`

### M3 — Autonomous Development
Status: `DONE`

| Work item | Capability | Status |
|---|---|---|
| M3-W001 | Autonomous task scheduler | DONE |
| M3-W002 | Specification-to-change manifest | DONE |
| M3-W003 | Continuous self-verification controller | DONE |
| M3-W004 | Safe isolated commit manager | DONE |
| M3-W005 | Evidence-based rollback controller | DONE |
| M3-W006 | Execution performance clock and improvement metrics | DONE |

### M4 — Governed post-release evolution
Status: `DONE`
Target: `1.1.0`
Selected capability: `KPM/KGO autonomous control CLI`

| Work item | Capability | Priority | Status | Dependencies |
|---|---|---:|---|---|
| M4-W001 | Synchronize the autonomous control plane with the published 1.0 baseline | P0 | DONE | None |
| M4-W002 | Produce an evidence-backed inventory of post-release capability gaps | P0 | DONE | M4-W001 |
| M4-W003 | Rank validated gaps and select the first dependency-valid 1.1 capability | P0 | DONE | M4-W002 |
| M4-W004 | Write the frozen specification and change manifest for the autonomous control CLI | P1 | DONE | M4-W003 |
| M4-W005 | Implement the selected capability within the authorized boundary | P1 | DONE | M4-W004 |
| M4-W006 | Run targeted and complete verification, build and clean installation | P0 | DONE | M4-W005 |
| M4-W007 | Synchronize documentation and prepare the 1.1 release candidate | P1 | DONE | M4-W006 |

Completion: `7/7`, `100%`.

## Release states

### Release 1.0
Status: `DONE`

Release `KYVERNEX 1.0.0` is verified, tagged, published and marked Latest.

### Release Candidate 1.1.0rc1
Status: `VERIFIED_AWAITING_PUBLICATION`

Passed gates:

- package and public API versions synchronized to `1.1.0rc1`;
- targeted M4 tests green;
- complete repository suite green;
- source and wheel builds green;
- clean wheel installation green;
- installed `kyvernex-governance` smoke test green;
- KGO v3 current-evidence workflow green on commit `807def6`;
- release notes present.

## Open backlog

No implementation work item is active.

Remaining external release action:

1. create tag `v1.1.0-rc.1`;
2. publish `KYVERNEX 1.1.0-rc.1` as a GitHub prerelease;
3. do not mark it Latest;
4. preserve `v1.0.0` as the stable release.

New feature work requires a separately authorized milestone. Observations do not become active work automatically.
