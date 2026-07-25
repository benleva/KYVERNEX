# KYVERNEX

KYVERNEX is the execution and governance engine for the ARGUS cognitive constitution.

## Governed architecture

```text
User goal
  -> KGO governance
  -> KPM milestone and work-item selection
  -> Autonomous Development Engine
  -> authorized implementation boundary
  -> targeted tests
  -> complete CI verification
  -> checkpoint and next cycle
```

KGO v2 analyzes verification evidence, groups probable root causes and produces ordered patch plans. The M3 Autonomous Development Engine selects the next dependency-valid task and emits a policy-bounded cycle plan. It does not claim that code was written, merged or verified without corresponding execution evidence.

## M3 autonomous development

The initial governed backlog is:

1. autonomous task scheduler;
2. specification-to-change manifest;
3. continuous self-verification controller;
4. safe isolated commit manager;
5. evidence-based rollback controller.

Generate the next cycle locally with:

```bash
python -m kyvernex.ade_cli --artifact-directory artifacts
```

The command creates `ADE_CYCLE_PLAN.json` and `ADE_CHECKPOINT.json`.

## Verification

The workflow `.github/workflows/kgo.yml` runs the complete test suite, creates KGO v1/v2 governance artifacts and, in autonomous mode after successful verification, creates the next M3 development-cycle plan.

## Public site

Run the static public site locally with:

```bash
python -m http.server 8080 --directory site
```

The Validator shown on the homepage is a deterministic browser demonstration. It does not replace the Reference Engine, the Compliance Suite or the governed CI evidence.
