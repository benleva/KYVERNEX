# M4 Post-release Capability Gap Inventory v0.1

## Purpose

Identify evidence-backed gaps between the published KYVERNEX 1.0 capabilities and an operational autonomous KPM/KGO continuation path for target version 1.1.0.

## Baseline evidence

- Release `v1.0.0` is published and immutable.
- `KyvernexProgramManager` can rank dependency-valid work items and transition them through governed states.
- `KyvernexGovernanceOrchestrator` can start autonomous mode, advance, save checkpoints and resume from a checkpoint.
- The package entry point `kyvernex` currently runs the cognitive reference engine on a single input.
- No package script currently exposes KPM/KGO start, status, advance or resume operations.
- The historical root checkpoint had to be synchronized manually after Release 1.0.
- Repository search found no explicit TODO, FIXME or NotImplemented marker that would outrank this operational gap.

## Validated gaps

### G1 — No executable KPM/KGO control surface

Severity: P0

The autonomous coordinator exists as a Python API, but there is no supported command-line path to start, inspect, advance or resume it from repository state. This makes autonomous continuation dependent on manual file edits or bespoke Python invocation.

Required outcome:

- deterministic CLI entry point;
- start, status, advance and resume commands;
- explicit checkpoint path;
- machine-readable JSON output;
- non-zero exit codes for blocked or invalid states;
- no repository mutation beyond the authorized checkpoint path.

### G2 — Governance state is duplicated across Markdown and JSON

Severity: P1

`PROJECT_STATUS.md`, `BACKLOG.md`, `SPRINT.md` and `KGO_CHECKPOINT.json` can diverge because no validator checks their active milestone, sprint, cycle and task identifiers.

Required future outcome:

- deterministic consistency check;
- mismatch report;
- no silent correction.

### G3 — Workflow is tied to the completed M3 work-item identity

Severity: P1

The current CI governance workflow records M3-specific identifiers. A future release cycle needs work-item identity supplied from current governed state rather than frozen constants.

Required future outcome:

- current work-item input or checkpoint-derived identity;
- unchanged verification safeguards;
- backward-compatible evidence schema handling.

### G4 — Autonomous progression does not execute semantic implementation

Severity: P2

The orchestrator selects and records work, while repository writes remain an authorized external operation. This is an intentional boundary, not a Release 1.0 defect. Future work may improve executor integration without allowing governance decisions to bypass authorization.

## Ranked result

1. G1 — executable KPM/KGO control surface.
2. G2 — governance-state consistency validator.
3. G3 — dynamic current-work-item CI evidence.
4. G4 — authorized executor integration research.

## Selected 1.1 capability

**G1: KPM/KGO autonomous control CLI**

Selection rationale:

- directly enables the user-authorized request to start and continue KPM/KGO;
- uses already implemented and verified program-manager/orchestrator behavior;
- closes a demonstrated operational gap;
- has bounded scope and can be tested deterministically;
- does not modify the immutable `v1.0.0` release.

## Non-goals

- automatic GitHub tagging or release publication;
- unrestricted repository writes;
- semantic code generation;
- weakening KPM dependencies, Definition of Done or KGO stop conditions;
- changing the published 1.0 baseline.
