# KGO Integrated Orchestrator Specification v0.1 DRAFT

## Scope

KGO is implemented inside `src/kyvernex/program_manager.py`, together with KPM. It is not a separate package or execution engine.

## Architecture

- KPM governs milestones, work items, dependencies and Definition of Done.
- KGO governs autonomous sequencing, checkpoint persistence and resumption.
- KYVERNEX remains the only execution engine.

## Public types

- `GovernanceMode`
- `GovernanceState`
- `GovernanceCheckpoint`
- `KGOError`
- `KyvernexGovernanceOrchestrator`

## Autonomous lifecycle

1. `start_autonomous()` enables autonomous mode.
2. KGO selects the first open milestone or a requested milestone.
3. `advance()` selects and starts the next dependency-valid work item.
4. `complete_current_item()` accepts verified Definition of Done evidence, closes the item and advances automatically.
5. When no unfinished item remains, KGO closes the milestone.
6. State is persisted after every transition when a checkpoint path is configured.
7. `resume()` restores orchestration metadata from the checkpoint.

## Safety and truthfulness

- KGO never marks a work item DONE without a complete Definition of Done.
- KGO never closes a milestone containing unfinished work.
- Test, CI and commit fields are evidence fields and remain `None` unless explicitly supplied from verified evidence.
- A blocked dependency graph produces `BLOCKED`, not a fabricated completion state.

## Anti-infinite rule

Closed milestones remain immutable through KPM. KGO may only select open milestones whose target version is within its configured release target.

## Platform boundary

Autonomous means no user decision is required between dependency-valid tasks. Runtime continuity still depends on the host environment invoking the orchestrator. Checkpoints provide deterministic resumption across invocations.
