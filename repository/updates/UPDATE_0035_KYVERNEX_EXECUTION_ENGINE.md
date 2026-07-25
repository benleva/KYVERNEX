# UPDATE 0035 — KYVERNEX EXECUTION ENGINE

## Change
Introduced KEX as `src/kyvernex/execution_engine.py`, the governed execution boundary beneath KGO and KPM.

## Added
- `ExecutionRequest`
- `ExecutionResult`
- `ExecutionStatus`
- `ExecutionPolicy`
- `CommandRunner`
- `SubprocessCommandRunner`
- `KyvernexExecutionEngine`
- `KEXError`
- unit tests in `tests/test_execution_engine.py`
- specification `KYVERNEX_EXECUTION_ENGINE_SPEC_v0.1_DRAFT.md`

## Updated
- package exports in `src/kyvernex/__init__.py`

## Governance impact
The architecture is now separated into:
- KGO: orchestration and autonomous governance;
- KPM: milestone, dependency and Definition of Done management;
- KEX: policy-gated external execution and evidence capture.

KEX cannot independently declare tasks, milestones, tests or CI complete.

## Verification state
Implementation, tests and documentation were committed. The new test suite has not yet been freshly executed and CI has not yet been verified. Therefore KEX remains implemented but not fully DONE under the KPM Definition of Done.
