# KYVERNEX BACKLOG

## Baseline status

- Stable release: `1.0.0`
- Published stable tag: `v1.0.0`
- Published prerelease: `1.1.0rc1`
- Published prerelease tag: `v1.1.0-rc.1`
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
Status: `PUBLISHED_PRERELEASE`

- package and public API versions are `1.1.0rc1`;
- verification gates passed;
- tag `v1.1.0-rc.1` exists;
- GitHub prerelease is published;
- prerelease is not Latest;
- `v1.0.0` remains the stable Latest release.

## Open backlog

No implementation or publication work item is active.

New work requires a documented defect, explicit release-candidate feedback, an approved promotion plan to stable `1.1.0`, or a separately authorized milestone. The anti-infinite rule applies.