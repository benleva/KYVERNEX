# KGO CI Backlog Orchestration Specification v0.1 DRAFT

## Purpose
KGO converts test evidence into a deterministic governance state instead of treating CI as a binary pass/fail lamp.

## Inputs
- Complete pytest textual output.
- GitHub commit and workflow metadata.
- Governance mode: `autonomous` or `verify-only`.

## Required outputs
- `KGO_EVIDENCE.json`: immutable CI execution metadata.
- `KGO_BACKLOG.json`: ordered failure inventory.
- `KGO_CHECKPOINT.json`: resumable governance state.
- `KGO_SUMMARY.md`: human-readable report and next governed task.
- GitHub issue creation or update when autonomous mode is blocked.

## Classification policy
- Import and collection failures: `P0 / COLLECTION_OR_IMPORT`.
- Runtime defects, including `TypeError`, `RuntimeError` and `KEXError`: `P0 / RUNTIME_DEFECT`.
- Timeout failures: `P0 / TIMEOUT`.
- Assertion and contract mismatches: `P1 / CONTRACT_MISMATCH`.
- Other failures: `P1 / UNCLASSIFIED_TEST_FAILURE`.

## Selection policy
The next task is selected deterministically by priority, category and pytest node identifier. KGO must never declare verification while the reported failed-test count is greater than zero.

## Stop conditions
The workflow stops with a failed status when test failures remain, but only after preserving evidence, backlog, checkpoint and summary. This is a governed block, not an orchestration crash.

## Autonomous repair boundary
This version analyzes, prioritizes, persists and reports failures. It does not generate or commit source-code patches. Automated patch generation requires a separately authorized coding agent, bounded permissions, branch isolation, review gates and fresh test evidence.
