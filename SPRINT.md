# KYVERNEX SPRINT

## Completed M6 sprints

- S004 — Freeze the plugin contract: `DONE`
- S005 — Implement the core plugin runtime: `DONE`, verified at `691c769`
- S006 — Govern host contracts: `DONE`, verified at `83ce3a3`
- S007 — Fail-closed plugin configuration: `DONE`, verified at `a8e7f36`

## Sprint S008 — Minimum reference adapter

- Milestone: `M6 — KYVERNEX Plugin Runtime`
- Status: `ACTIVE`
- KPM cycle: `KPM-CYCLE-018`
- KGO cycle: `KGO-CYCLE-029`
- Target version: `1.2.0`
- Scope lock: `repository/specifications/M6_SCOPE_LOCK.md`

### Sprint goal
Complete exactly one minimal in-process adapter that wraps a host-supplied Python callable and proves the governed plugin path without introducing external integrations or a broader adapter framework.

### Sprint backlog

| ID | Task | Priority | Story points | Status |
|---|---|---:|---:|---|
| M6-W004 | Implement one bounded in-process callable adapter | P0 | 3 | IN_PROGRESS |

### Allowed implementation

The adapter may only:

- receive a Python callable in its constructor;
- expose an explicit capability set;
- invoke the callable after runtime authorization;
- return a JSON-serializable result;
- report `HEALTHY` or `SHUTDOWN`;
- shut down idempotently.

### Forbidden implementation

The adapter must not:

- access the network, filesystem, subprocesses, repositories or environment variables;
- load modules or plugins dynamically;
- contact external services;
- decide governance or authorization;
- create background work;
- add a second adapter type;
- introduce a registry, marketplace, SDK family or remote protocol.

### Definition of Sprint Done

S008 is complete only when:

1. one concrete callable adapter exists;
2. the adapter conforms to the frozen host protocol;
3. unauthorized requests still never reach the callable;
4. non-JSON results fail with a governed adapter error;
5. health and idempotent shutdown are tested;
6. targeted and complete repository tests are green.

### Continuation decision
After S008, proceed directly to M6-W006 integration tests. Reject any feature proposal that does not move the single clean-install plugin path toward its smoke test.
