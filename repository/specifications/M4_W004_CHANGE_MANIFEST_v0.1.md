# M4-W004 Change Manifest v0.1

## Selected specification

`repository/specifications/KPM_KGO_AUTONOMOUS_CONTROL_CLI_SPEC_v0.1.md`

## Authorized changes

### Add
- `src/kyvernex/governance_cli.py`
- `tests/test_governance_cli.py`

### Modify
- `pyproject.toml` to add the `kyvernex-governance` console script;
- `src/kyvernex/__init__.py` only if a public export is required;
- `.github/workflows/kgo.yml` to add targeted CLI tests and preserve complete-suite, build and clean-install gates;
- `README.md`, `CHANGELOG.md`, `PROJECT_STATUS.md`, `BACKLOG.md`, `SPRINT.md`, `QUALITY.md` and `KGO_CHECKPOINT.json` for synchronized evidence.

## Forbidden changes

- no mutation of tag `v1.0.0` or the published Release;
- no weakening of KPM dependency checks or Definition of Done;
- no weakening of KGO stop conditions;
- no unrestricted filesystem or GitHub writes;
- no new semantic code-generation system;
- no unrelated refactor.

## Verification sequence

1. targeted governance CLI tests;
2. existing program-manager and KGO tests;
3. complete repository suite;
4. source and wheel build;
5. clean wheel installation;
6. installed console-script smoke test;
7. governed evidence upload.

## Rollback boundary

If current verification fails, stop and record the failure. Any rollback must target only the isolated M4 implementation changes and must use the existing evidence-based rollback policy.