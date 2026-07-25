# KYVERNEX

KYVERNEX is the execution and governance engine for the ARGUS cognitive constitution.

> Current status: M3 autonomous development is complete and verified. Release 1.0 remains under audit and has not yet been tagged.

## Governed architecture

```text
User goal
  -> KGO governance
  -> KPM milestone and work-item selection
  -> Autonomous Development Engine
  -> authorized implementation boundary
  -> targeted tests
  -> complete CI verification
  -> evidence checkpoint
  -> isolated commit or evidence-based rollback plan
  -> execution-performance metrics
```

KGO analyzes current verification evidence, groups probable root causes and produces ordered patch plans. The Autonomous Development Engine selects the next dependency-valid task and emits a policy-bounded cycle plan. KYVERNEX does not claim that code was written, merged, rolled back or verified without corresponding execution evidence and authorization.

## Completed M3 backlog

1. autonomous task scheduler;
2. specification-to-change manifest;
3. continuous self-verification controller;
4. safe isolated commit manager;
5. evidence-based rollback controller;
6. execution performance clock and improvement metrics.

KGO and KPM are frozen for Release 1.0 except for verified blocking defects.

## Requirements

- Python 3.11 or newer
- `pip`

## Installation for development

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Verification

Run the complete suite locally:

```bash
python -m pytest -q
```

The workflow `.github/workflows/kgo.yml` runs targeted M3 tests and the complete suite, evaluates continuous self-verification, creates KGO governance evidence and uploads the resulting artifacts.

A historical failed workflow remains part of the repository record. Only current evidence for the tested commit determines advancement.

## Autonomous development cycle

Generate the next policy-bounded cycle plan locally with:

```bash
python -m kyvernex.ade_cli --artifact-directory artifacts
```

The command creates:

- `ADE_CYCLE_PLAN.json`
- `ADE_CHECKPOINT.json`

## Evidence artifacts

Depending on the authorized execution path, KYVERNEX can produce:

- `KGO_STATE.json`
- `KGO_V3_LOOP.json`
- `KGO_V3_SUMMARY.md`
- `SELF_VERIFICATION.json`
- `SELF_VERIFICATION_SUMMARY.md`
- `ROLLBACK_PLAN.json`
- `EXECUTION_METRICS.json`

Performance metrics are observational. They cannot replace correctness evidence or authorize repository mutation.

## Public site

Run the static public site locally with:

```bash
python -m http.server 8080 --directory site
```

The Validator shown on the homepage is a deterministic browser demonstration. It does not replace the Reference Engine, the Compliance Suite or governed CI evidence.

## Release status

The package is still versioned `0.1.0.dev0` while Release 1.0 audit gates are completed. A `v1.0.0` tag must not be created until version synchronization, licensing, changelog, clean build and clean-environment installation are verified.

See `PROJECT_STATUS.md` for the current authoritative project state and `CHANGELOG.md` for release history.