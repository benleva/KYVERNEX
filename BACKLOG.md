# KYVERNEX BACKLOG

## Baseline status

- Stable published release: `1.0.0`
- Published stable tag: `v1.0.0`
- Published prerelease: `1.1.0rc1`
- Published prerelease tag: `v1.1.0-rc.1`
- Verified stable promotion candidate: `1.1.0`
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

Status: `ACTIVE_AT_PUBLICATION_BOUNDARY`
Target: `1.1.0`
Scope: release promotion only; no new functional capability.

| Work item | Capability | Priority | Status | Dependencies |
|---|---|---:|---|---|
| M5-W001 | Synchronize package, public API, CI and stable release materials to `1.1.0`; obtain fresh verification | P0 | DONE | Published and verified `v1.1.0-rc.1` |
| M5-W002 | Record green evidence and prepare immutable stable tag and GitHub Release | P0 | DONE | M5-W001 |
| M5-W003 | Publish `v1.1.0`, mark it Latest and close M5/S003 | P0 | EXTERNAL_BOUNDARY | M5-W002 |

## Verified evidence

The final stable-promotion state on commit `56bd8da` is green for:

1. targeted governance tests;
2. complete repository suite;
3. source and wheel builds;
4. clean wheel installation;
5. installed package and public API version `1.1.0`;
6. installed `kyvernex-governance` behavior;
7. KGO v3 governed result enforcement.

## Release states

- `v1.0.0`: published stable release and current Latest;
- `v1.1.0-rc.1`: published immutable prerelease, not Latest;
- `v1.1.0`: verified and ready to be tagged and published as the new stable Latest release.

## Remaining external action

1. create tag `v1.1.0` from `main`;
2. publish GitHub Release `KYVERNEX 1.1.0`;
3. use `RELEASE_NOTES_1.1.0.md` as the release body;
4. do not mark it as a prerelease;
5. mark it as Latest;
6. preserve `v1.0.0` and `v1.1.0-rc.1` as immutable historical releases.

## Continuation policy

After publication, close M5 and S003 and return KPM/KGO to safe stop. On publication failure, preserve all existing tags and record the blocker before retrying.