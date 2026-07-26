# M18 End-of-Milestone Verification Runbook

## Purpose

This runbook defines the single verification campaign for M18 — ARGUS Executive Translator. It is intentionally executable only after all M18 implementation items are complete.

## Policy

- Do not run this campaign during implementation.
- Run every automated and operator check in one controlled session.
- Record exact commands, outputs, environment, package version, commit SHA, and timestamps.
- Any unexpected acceptance, silent coercion, lossy conversion, or missing trace is a failure.
- Do not create a tag or release as part of verification.

## Preconditions

1. Worktree is clean and points to the intended M18 verification commit.
2. Python environment is isolated.
3. Development package version is `1.2.0.dev0`.
4. Stable tag `v1.1.0` remains unchanged.
5. The M18 implementation boundary is declared closed in `PROJECT_STATUS.md`.

## Verification sequence

### V01 — Package installation

Install the project in editable mode and confirm that these commands resolve:

```text
kyvernex-argus
kyvernex-argus-translate
```

Expected result: both commands are installed and callable.

### V02 — Translator positive cases

Verify explicit supported Italian statements for every canonical field:

- consent: true and false;
- authorization: true and false;
- risk: low, medium, high, critical;
- subject.minor: true and false;
- domain: health, finance, legal, education.

Expected result: canonical values, normalized text, lexical rule ids, and matched fragments are present and stable.

### V03 — Normalization equivalence

Repeat representative cases with:

- uppercase and lowercase;
- repeated whitespace;
- accented and unaccented forms where supported;
- apostrophe variants.

Expected result: equivalent statements produce identical canonical requests.

### V04 — Closed-world rejection

Submit unsupported, empty, and whitespace-only text.

Expected result: translation fails without inventing facts.

### V05 — Contradiction rejection

Submit text that explicitly states conflicting values for the same canonical path.

Expected result: translation fails closed and identifies the conflicting field and rules.

### V06 — Symbolic projection

Encode every supported canonical fact and representative multi-field requests.

Expected result: stable canonical token order and no information loss.

### V07 — Symbolic round trip

For every valid symbolic case, perform:

```text
canonical JSON -> ARGUS symbols -> canonical JSON
```

Expected result: decoded JSON is structurally equal to the original canonical request.

### V08 — Symbol rejection

Submit malformed, unknown, duplicate, and conflicting symbols.

Expected result: decoding fails closed.

### V09 — Audit envelope

Generate an audit envelope without matrix evaluation.

Expected result: the envelope contains source input, normalization, lexical trace, canonical request, symbolic projection, status, and versioned component metadata.

### V10 — Matrix integration

Translate a supported request and evaluate it against a valid ARGUS matrix.

Expected result: translator trace and matrix decision trace remain distinct and are both preserved in the audit envelope.

### V11 — CLI input modes

Verify:

- `--text`;
- `--input <file>`;
- `--input -` for stdin;
- `--output`;
- replacement rejection without `--force`;
- replacement with `--force`;
- `--audit-envelope`;
- optional `--matrix`.

Expected result: all modes return deterministic JSON and consistent exit codes.

### V12 — Determinism repetition

Repeat representative translation, symbolic, audit, and matrix commands multiple times.

Expected result: identical inputs and configuration produce byte-stable JSON apart from fields explicitly documented as variable. M18 should contain no variable timestamp field in deterministic payloads.

### V13 — Regression boundary

Re-run the established M17 Matrix Runner verification.

Expected result: M18 additions do not alter the existing deterministic Matrix Runner contract.

## Evidence to retain

Create one verification evidence directory outside the source package containing:

- environment metadata;
- commit SHA;
- command transcript;
- automated test output;
- operator output files;
- failure log, even when empty;
- final verification report.

## Completion criteria

M18 may be marked verified only when all V01–V13 checks pass, the evidence is retained, and the final report explicitly records:

```text
M18_ARGUS_EXECUTIVE_TRANSLATOR_VERIFIED
```

A failed check leaves M18 unverified. No release qualification is implied.