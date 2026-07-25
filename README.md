# KYVERNEX

KYVERNEX is the execution and governance engine for the ARGUS cognitive constitution.

> Stable baseline: **KYVERNEX 1.0.0** is published under immutable tag `v1.0.0`. Governed development toward `1.1.0` is active in milestone M4 and does not alter the published release.

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

KGO analyzes current verification evidence, groups probable root causes and produces ordered patch plans. KPM selects the next dependency-valid task. KYVERNEX does not claim that code was written, merged, rolled back or verified without corresponding evidence and authorization.

## Stable Release 1.0

Release `1.0.0` includes the completed M3 backlog:

1. autonomous task scheduler;
2. specification-to-change manifest;
3. continuous self-verification controller;
4. safe isolated commit manager;
5. evidence-based rollback controller;
6. execution performance clock and improvement metrics.

KGO and KPM remain frozen for the published Release 1.0 baseline except for verified blocking defects.

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

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## KPM/KGO governance control CLI

Milestone M4 adds a deterministic command-line path over the existing KPM/KGO orchestration API:

```bash
kyvernex-governance start --plan plan.json --checkpoint checkpoint.json
kyvernex-governance status --plan plan.json --checkpoint checkpoint.json
kyvernex-governance advance --plan plan.json --checkpoint checkpoint.json
kyvernex-governance resume --plan plan.json --checkpoint checkpoint.json
```

The plan is a UTF-8 JSON document containing `target_version`, `milestones` and `items`. The CLI:

- selects only dependency-valid work;
- fails closed on malformed plans and unknown dependencies;
- writes only the explicitly supplied checkpoint path;
- does not edit source files, Git refs, branches, issues or releases;
- does not invent test, CI, repository-write or completion evidence;
- returns exit code `2` for a governed `BLOCKED` state, `3` for invalid input or policy errors and `4` for operations not currently permitted.

`start` refuses to overwrite an existing checkpoint. `status` and `resume` are non-mutating. `advance` refuses to proceed while a current work item remains active.

## Verification

Run the complete suite locally:

```bash
python -m pytest -q
```

The workflow `.github/workflows/kgo.yml` runs targeted M4 governance CLI tests and the complete suite, evaluates continuous self-verification, builds source and wheel distributions, installs the wheel in a clean virtual environment and performs an installed `kyvernex-governance start` smoke test.

The Release 1.0 baseline passed GitHub Actions run `#58`. Current M4 implementation evidence must come from a fresh workflow run for the tested commit.

## Autonomous development cycle

Generate a policy-bounded development plan locally with:

```bash
python -m kyvernex.ade_cli --artifact-directory artifacts
```

The command creates `ADE_CYCLE_PLAN.json` and `ADE_CHECKPOINT.json`. Planning does not itself authorize repository mutation.

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

## Release and development status

- Stable version: `1.0.0`
- Immutable tag: `v1.0.0`
- GitHub Release: `KYVERNEX 1.0.0`, marked `Latest`
- Active milestone: `M4 — Governed post-release evolution`
- Target version: `1.1.0`
- Current implementation: KPM/KGO autonomous control CLI, fresh CI evidence pending
- License: proprietary, all rights reserved

See `PROJECT_STATUS.md` for authoritative state, `BACKLOG.md` for ordered work and `CHANGELOG.md` for release history.