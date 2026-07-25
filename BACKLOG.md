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
Selected capability: `KPM/KGO autonomous control CLI`

| Work item | Capability | Priority | Status | Dependencies |
|---|---|---:|---|---|
| M4-W001 | Synchronize the autonomous control plane with the published 1.0 baseline | P0 | DONE | None |
| M4-W002 | Produce an evidence-backed inventory of post-release capability gaps | P0 | DONE | M4-W001 |
| M4-W003 | Rank validated gaps and select the first dependency-valid 1.1 capability | P0 | DONE | M4-W002 |
| M4-W004 | Write the frozen specification and change manifest for the autonomous control CLI | P1 | DONE | M4-W003 |
| M4-W005 | Implement the selected capability within the authorized boundary | P1 | TEST | M4-W004 |
| M4-W006 | Run targeted and complete verification, build and clean installation | P0 | IN_DEVELOPMENT | M4-W005 |
| M4-W007 | Synchronize documentation and prepare the 1.1 release candidate | P1 | BACKLOG | M4-W006 |

## Current evidence state

The governance CLI implementation, console-script metadata, deterministic tests and CI integration are committed. A fresh GitHub Actions run must verify:

1. targeted M4 tests;
2. complete repository suite;
3. source and wheel builds;
4. clean wheel installation;
5. installed `kyvernex-governance start` behavior.

No successful result is claimed before that run completes.

## Continuation policy

KPM selects the next dependency-valid item by priority. KGO advances only from current repository evidence. It must stop for a documented blocker, failed verification, missing authorization or completed milestone.