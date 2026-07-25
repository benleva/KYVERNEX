# KYVERNEX BACKLOG

## Baseline status

- Stable release: `1.0.0`
- Published tag: `v1.0.0`
- Active milestone: `M4 — Governed post-release evolution`
- Active sprint: `S002 — Establish the 1.1 evidence baseline`
- Target version: `1.1.0`
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

## Release 1.0

Status: `DONE`

Release `KYVERNEX 1.0.0` is verified, tagged, published and marked Latest.

## Active milestone

### M4 — Governed post-release evolution

Status: `ACTIVE`
Target: `1.1.0`

Goal: allow KPM and KGO to resume autonomous, evidence-bounded progression after Release 1.0 without altering the immutable `v1.0.0` baseline or inventing unsupported features.

| Work item | Capability | Priority | Status | Dependencies |
|---|---|---:|---|---|
| M4-W001 | Synchronize the autonomous control plane with the published 1.0 baseline | P0 | DONE | None |
| M4-W002 | Produce an evidence-backed inventory of post-release capability gaps | P0 | IN_DEVELOPMENT | M4-W001 |
| M4-W003 | Rank validated gaps and select the first dependency-valid 1.1 capability | P0 | READY | M4-W002 |
| M4-W004 | Write the frozen specification and change manifest for the selected capability | P1 | BACKLOG | M4-W003 |
| M4-W005 | Implement the selected capability within the authorized boundary | P1 | BACKLOG | M4-W004 |
| M4-W006 | Run targeted and complete verification, build and clean installation | P0 | BACKLOG | M4-W005 |
| M4-W007 | Synchronize documentation and prepare the 1.1 release candidate | P1 | BACKLOG | M4-W006 |

## Continuation policy

KPM selects the next dependency-valid item by priority. KGO advances only from current repository evidence. It must stop for a documented blocker, missing authorization, failed verification or completed milestone. New observations do not bypass the ordered backlog.