# KPM/KGO Autonomous Control CLI Specification v0.1

## Work item

`M4-W004`

## Objective

Expose the already implemented KPM and KGO orchestration behavior through a deterministic command-line interface suitable for local execution and CI evidence.

## Command

The package shall expose:

```bash
kyvernex-governance <command> --plan <path> --checkpoint <path>
```

Supported commands:

- `start`: construct KPM from the plan, start KGO in autonomous mode and persist the first checkpoint;
- `status`: read and validate the checkpoint without advancing state;
- `advance`: resume the persisted state and select the next dependency-valid action only when no current item is active;
- `resume`: restore the persisted checkpoint and emit its current state without mutation.

## Plan document

The plan is UTF-8 JSON with:

- `target_version`;
- `milestones[]`: `milestone_id`, `title`, `target_version`, `closed`;
- `items[]`: `item_id`, `title`, `milestone_id`, `priority`, `story_points`, `status`, `dependencies`, `done`.

Unknown enum values, missing identifiers, invalid dependencies and malformed JSON must fail closed.

## Checkpoint document

The checkpoint is written only through `KyvernexGovernanceOrchestrator.save_checkpoint` and contains the governed state. The CLI must not claim repository writes, test success, CI success or item completion that are absent from the supplied plan and checkpoint.

## Output

Every successful command writes one JSON object to standard output with stable sorted keys. It includes:

- mode;
- state;
- target version;
- current milestone;
- current item;
- completed milestones;
- completed items;
- blocked items;
- completion percentage;
- cycle;
- verification references when available.

## Exit codes

- `0`: command completed and state is not blocked;
- `2`: governed state is `BLOCKED`;
- `3`: invalid plan, invalid checkpoint or policy error;
- `4`: requested operation is not currently permitted.

## Safety boundaries

- The CLI may read the plan and checkpoint paths.
- It may write only the explicitly supplied checkpoint path.
- It may not edit source files, documentation, Git refs, branches, issues or releases.
- It may not mark a work item complete without a complete Definition of Done already present in the plan.
- It may not reopen a closed milestone.
- It may not bypass dependencies or KGO stop conditions.

## Determinism

Given identical plan and checkpoint inputs, commands must produce the same state transition and equivalent JSON output. Timestamps are not added.

## Tests

Required tests:

1. `start` selects the highest-priority dependency-valid item;
2. `status` does not mutate the checkpoint;
3. malformed plans fail closed;
4. unknown dependencies fail closed;
5. closed milestones reject new work;
6. blocked state returns exit code `2`;
7. output contains no unsupported execution claim;
8. the installed console script reports the package version-compatible control behavior.

## Definition of Done

- specification committed;
- change manifest committed;
- CLI implementation present;
- public console script configured;
- deterministic unit tests present;
- complete suite green;
- package build and clean-wheel installation green;
- README, changelog, backlog, sprint and checkpoint synchronized.

## Non-goals

- semantic implementation generation;
- automatic completion of Definition of Done fields;
- GitHub API mutation;
- automatic tagging or publishing;
- changes to the immutable `v1.0.0` tag.
