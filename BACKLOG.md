# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Verified local report: `M16 — LOCAL_APP_SMOKE_VERIFIED`
- Verified matrix runner: `M17 — ARGUS_MATRIX_SMOKE_VERIFIED`
- Active milestone: `M18 — ARGUS Executive Translator`
- Development package version: `1.2.0.dev0`

## M18 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M18-W001 | Deterministic Italian translator | P0 | CODE_COMPLETE_UNVERIFIED |
| M18-W002 | Installed `kyvernex-argus-translate` command | P0 | CODE_COMPLETE_UNVERIFIED |
| M18-W003 | Direct translator-to-matrix execution path | P0 | CODE_COMPLETE_UNVERIFIED |
| M18-W004 | Accent-folded normalization, controlled synonyms and expanded canonical fields | P1 | CODE_COMPLETE_UNVERIFIED |
| M18-W005 | Canonical symbolic projection and reusable audit envelope | P1 | IN_PROGRESS |
| M18-W006 | End-of-milestone automated and operator verification | P0 | DEFERRED_UNTIL_MILESTONE_END |

## Current canonical vocabulary

- `consent`: boolean;
- `authorization`: boolean;
- `risk`: `low`, `medium`, `high`, `critical`;
- `subject.minor`: boolean;
- `domain`: `health`, `finance`, `legal`, `education`.

## Code evidence

- `src/kyvernex/argus_translator.py`: deterministic Italian lexical translation and normalization;
- `src/kyvernex/argus_translator_cli.py`: direct text, file, stdin, output and matrix options;
- `src/kyvernex/argus_matrix.py`: unchanged deterministic decision engine;
- `pyproject.toml`: installs `kyvernex-argus-translate`;
- contradictory values fail closed;
- trace records lexical rule ids and exact normalized fragments;
- no LLM or external network is used.

## Verification policy

No tests are run during M18 implementation. The complete translator, symbolic projection, audit envelope and integrated matrix path will be checked together at milestone closure.

## Boundary

M18 translates only explicitly supported Italian statements. General semantics, complete constitutional vocabulary, probabilistic inference, learning, external data and release qualification remain outside the current code. Stable `v1.1.0` remains unchanged.
