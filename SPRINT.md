# KYVERNEX SPRINT

## Sprint S004 — Freeze the plugin contract

- Milestone: `M6 — KYVERNEX Plugin Runtime`
- Status: `ACTIVE`
- KPM cycle: `KPM-CYCLE-013`
- KGO cycle: `KGO-CYCLE-024`
- Target version: `1.2.0`
- Stable baseline: `v1.1.0`
- Sprint goal: define and freeze the host-facing plugin contract, lifecycle, structured schemas and authority boundaries before runtime implementation begins.

## Sprint backlog

| ID | Task | Priority | Story points | Status | Dependencies |
|---|---|---:|---:|---|---|
| M6-W001 | Freeze the plugin contract, lifecycle, schemas and authority boundaries | P0 | 5 | IN_PROGRESS | Stable `v1.1.0` baseline |

Sprint total: `1` task, `5` story points.

## Contract areas to freeze

1. plugin identity and version metadata;
2. lifecycle operations: `initialize`, `validate`, `execute`, `status`, `shutdown`;
3. lifecycle state transitions and forbidden transitions;
4. host request schema;
5. host response schema;
6. governed error schema;
7. configuration schema and fail-closed defaults;
8. host adapter protocol;
9. KPM/KGO/KEX integration points;
10. filesystem, network, process and repository authority boundaries;
11. audit and evidence fields;
12. compatibility and version-negotiation rules.

## Definition of Sprint Done

S004 is complete only when:

- the plugin contract is stored as a versioned repository specification;
- all lifecycle states and transitions are explicit;
- every request, response and error field is defined;
- defaults are fail closed;
- no configuration option can silently increase authority;
- the adapter boundary is explicit and implementation-neutral;
- the specification distinguishes planning, authorization, execution and evidence;
- acceptance tests for the future runtime can be derived from the contract;
- no runtime implementation is claimed before the contract is frozen.

## Closure decision

On completion, close M6-W001 and activate M6-W002. Stop if the specification leaves an unresolved P0 authority or security ambiguity.