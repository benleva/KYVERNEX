# UPDATE 0038 — KGO v2

## Status
IMPLEMENTED_NOT_VERIFIED

## Added
- `src/kyvernex/kgo_v2.py`
- `tests/test_kgo_v2.py`
- `repository/specifications/KGO_V2_SPEC_v0.1_DRAFT.md`

## Updated
- `.github/workflows/kgo.yml`

## Behavior
KGO v2 groups repeated pytest failures into probable root causes, ranks them, estimates confidence and effort, projects test-impact improvement, and creates controlled patch plans with targeted validation commands.

## Governance boundary
KGO v2 does not modify source code, create repair branches, approve pull requests or merge changes. Patch eligibility only marks a cause as suitable for a future isolated coding-agent proposal. The full suite remains the release gate.

## Verification
The files and workflow integration are committed. No fresh complete run has yet verified this update. The most recent user-observed run before KGO v2 reported 87 passed and 10 failed.
