# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Verified local report: `M16 — LOCAL_APP_SMOKE_VERIFIED`
- Verified matrix runner: `M17 — ARGUS_MATRIX_SMOKE_VERIFIED`
- Verified milestone: `M18 — ARGUS Executive Translator`
- Development package version: `1.2.0.dev0`

## M18 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M18-W001 | Deterministic Italian translator | P0 | VERIFIED |
| M18-W002 | Installed `kyvernex-argus-translate` command | P0 | VERIFIED |
| M18-W003 | Direct translator-to-matrix execution path | P0 | VERIFIED |
| M18-W004 | Accent-folded normalization, controlled synonyms and expanded canonical fields | P1 | VERIFIED |
| M18-W005 | Reversible canonical symbolic projection | P1 | VERIFIED |
| M18-W006 | Reusable staged audit envelope and CLI emission | P1 | VERIFIED |
| M18-W007 | End-of-milestone verification manifest and operator runbook | P0 | VERIFIED |
| M18-W008 | Execute automated and operator verification | P0 | VERIFIED |

## Current canonical vocabulary

- `consent`: boolean;
- `authorization`: boolean;
- `risk`: `low`, `medium`, `high`, `critical`;
- `subject.minor`: boolean;
- `domain`: `health`, `finance`, `legal`, `education`.

## Code evidence

- `src/kyvernex/argus_translator.py`: deterministic Italian lexical translation and normalization;
- `src/kyvernex/argus_symbols.py`: strict canonical JSON to ARGUS token conversion and reverse decoding;
- `src/kyvernex/argus_audit.py`: staged audit envelope with optional decision;
- `src/kyvernex/argus_translator_cli.py`: text, file, stdin, symbols, audit, output, and matrix options;
- `src/kyvernex/argus_matrix.py`: unchanged deterministic decision engine;
- contradictory values and lossy symbolic projections fail closed;
- no LLM or external network is used.

## Verification evidence

- `tests/test_argus_translator_m18.py`: automated V02–V13 coverage plus CLI integration;
- `.github/workflows/m18-verification.yml`: isolated installation, installed-command verification, M18 suite, complete regression suite, Python 3.11–3.13 matrix, and retained artifacts;
- `docs/M18_VERIFICATION_RUNBOOK.md`: operator sequence V01–V13 and completion criteria;
- `governance/verification/m18_verification_manifest.json`: completed machine-readable evidence record;
- successful workflow: `M18 Verification #3`;
- verified commit: `4ce2c5a04530e89496994cf26d38acfb6bad2065`;
- success marker: `M18_ARGUS_EXECUTIVE_TRANSLATOR_VERIFIED`.

## Verification policy

M18 is verified because the dedicated GitHub Actions workflow completed successfully across its configured Python matrix. A separate workflow failure does not alter this milestone-specific result unless it demonstrates a regression inside the M18 verification boundary.

## Boundary

M18 translates only explicitly supported Italian statements. General semantics, complete constitutional vocabulary, probabilistic inference, learning, external data, and release qualification remain outside the current code. Stable `v1.1.0` remains unchanged. No tag or release was created.