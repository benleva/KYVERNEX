# KYVERNEX BACKLOG

## Baseline status

- Stable published release: `1.0.0`
- Published stable tag: `v1.0.0`
- Published prerelease: `1.1.0rc1`
- Published prerelease tag: `v1.1.0-rc.1`
- Stable promotion candidate: `1.1.0`
- Active milestone: `M5 — Promote 1.1 release candidate to stable`
- Active sprint: `S003 — Verify and publish stable 1.1.0`
- Maintenance line: `1.0.x`

## Completed milestones

### M2 — Governance consolidation
Status: `DONE`

### M3 — Autonomous Development
Status: `DONE`

### M4 — Governed post-release evolution
Status: `DONE`

Completion: `7/7`, `100%`.

## Active milestone

### M5 — Promote 1.1 release candidate to stable

Status: `ACTIVE`
Target: `1.1.0`
Scope: release promotion only; no new functional capability.

| Work item | Capability | Priority | Status | Dependencies |
|---|---|---:|---|---|
| M5-W001 | Synchronize package, public API, CI and stable release materials to `1.1.0`; obtain fresh verification | P0 | IN_VERIFICATION | Published and verified `v1.1.0-rc.1` |
| M5-W002 | Record green evidence and prepare immutable stable tag and GitHub Release | P0 | BACKLOG | M5-W001 |
| M5-W003 | Publish `v1.1.0`, mark it Latest and close M5/S003 | P0 | EXTERNAL_BOUNDARY | M5-W002 |

## Current evidence gate

The repository is synchronized to package and public API version `1.1.0`. The current workflow must verify:

1. targeted governance tests;
2. complete repository suite;
3. source and wheel builds;
4. clean wheel installation;
5. installed package and public API version `1.1.0`;
6. installed `kyvernex-governance` behavior.

No stable tag or Release publication is claimed before that evidence is green.

## Release states

- `v1.0.0`: published stable release and current Latest;
- `v1.1.0-rc.1`: published immutable prerelease, not Latest;
- `v1.1.0`: not yet tagged or published.

## Continuation policy

KPM/KGO continue automatically through verification and release-material synchronization. They stop for current failure evidence or at the external tag and GitHub Release publication boundary.
