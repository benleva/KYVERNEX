# KYVERNEX SPRINT

## Sprint S004 — Freeze the plugin contract

- Milestone: `M6 — KYVERNEX Plugin Runtime`
- Status: `DONE`
- KPM cycle: `KPM-CYCLE-013`
- KGO cycle: `KGO-CYCLE-024`
- Target version: `1.2.0`
- Stable baseline: `v1.1.0`
- Sprint goal: define and freeze the host-facing plugin contract, lifecycle, structured schemas and authority boundaries before runtime implementation begins.

### Completed backlog

| ID | Task | Priority | Story points | Status |
|---|---|---:|---:|---|
| M6-W001 | Freeze the plugin contract, lifecycle, schemas and authority boundaries | P0 | 5 | DONE |

Completion: `1/1` tasks, `5/5` story points, `100%`.

### Closure evidence

- normative contract stored at `repository/specifications/M6_PLUGIN_RUNTIME_CONTRACT.md`;
- machine-readable envelopes stored at `repository/specifications/m6-plugin-contract.schema.json`;
- lifecycle states and transitions are explicit;
- request, response, error and configuration fields are defined;
- unknown fields and ambiguous authority fail closed;
- adapter boundary is implementation-neutral;
- planning, authorization, execution and evidence are distinct;
- runtime acceptance tests are derivable from the specification;
- no runtime implementation was claimed during contract freeze.

## Sprint S005 — Implement the core plugin runtime

- Milestone: `M6 — KYVERNEX Plugin Runtime`
- Status: `ACTIVE`
- KPM cycle: `KPM-CYCLE-014`
- KGO cycle: `KGO-CYCLE-025`
- Target version: `1.2.0`
- Stable baseline: `v1.1.0`
- Contract version: `KYVERNEX-M6-PLUGIN-CONTRACT 1.0.0`
- Sprint goal: implement the deterministic in-process runtime skeleton and lifecycle state machine without yet claiming complete host contracts, adapters or production verification.

### Sprint backlog

| ID | Task | Priority | Story points | Status | Dependencies |
|---|---|---:|---:|---|---|
| M6-W002 | Implement the core plugin runtime and lifecycle state machine | P0 | 8 | IN_PROGRESS | M6-W001 |

### Definition of Sprint Done

S005 is complete only when:

- a public plugin runtime class exists;
- all six frozen lifecycle states exist;
- allowed transitions succeed deterministically;
- forbidden transitions fail with a governed lifecycle error;
- `status()` is non-mutating;
- shutdown is terminal and adapter shutdown side effects occur at most once;
- only one execution may be active per instance;
- targeted lifecycle tests pass;
- complete-suite regression evidence is recorded before M6-W002 closes.

## Continuation decision

KPM and KGO continue with M6-W002. Stop on contract contradiction, current test failure or unresolved P0 authority ambiguity.