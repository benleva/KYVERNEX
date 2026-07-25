# UPDATE 0036 — KGO GitHub Actions

## Change
Added `.github/workflows/kgo.yml` as the first hosted execution workflow for KGO verification.

## Capabilities
- manual and push-triggered execution;
- Python 3.11 environment;
- editable installation with test dependencies;
- complete pytest invocation;
- captured test output;
- structured KGO evidence artifact;
- explicit workflow failure when tests do not pass.

## Governance impact
KGO now has a GitHub-hosted verification channel. It does not yet mutate project state or automatically repair failing code. CI remains unverified until an actual workflow run completes successfully.

## Dependencies
- `pyproject.toml`
- `tests/`
- `src/`
- GitHub Actions availability for the repository
