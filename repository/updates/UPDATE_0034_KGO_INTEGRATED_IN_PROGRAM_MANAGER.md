# UPDATE 0034 — KGO integrated in Program Manager

## Change

KGO has been implemented in the same Python module as KPM: `src/kyvernex/program_manager.py`.

## Added

- autonomous governance mode and lifecycle states;
- deterministic checkpoint model;
- milestone and task auto-selection;
- automatic advancement after a verified task closure;
- milestone closure through existing KPM safeguards;
- JSON checkpoint persistence and resume support;
- public exports from `kyvernex.__init__`;
- focused KGO tests;
- integrated KGO specification.

## Governance impact

This update does not create a second execution engine. KGO is a governance layer over KPM inside the KYVERNEX module boundary.

## Verification status

Implementation and tests were written and committed. The complete test suite and CI result have not yet been freshly verified by this update.
