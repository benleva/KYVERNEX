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
| M18-W001 | Deterministic Italian consent and risk translator | P0 | CODE_COMPLETE_UNVERIFIED |
| M18-W002 | Installed `kyvernex-argus-translate` command | P0 | CODE_COMPLETE_UNVERIFIED |
| M18-W003 | Direct translator-to-matrix execution path | P0 | CODE_COMPLETE_UNVERIFIED |
| M18-W004 | Expand bounded vocabulary and produce milestone test plan | P1 | IN_PROGRESS |
| M18-W005 | End-of-milestone operator and automated verification | P0 | DEFERRED_UNTIL_MILESTONE_END |

## Code evidence
- `src/kyvernex/argus_translator.py`: closed-world Italian phrase extraction;
- `src/kyvernex/argus_translator_cli.py`: text, file, stdin, output and matrix options;
- `src/kyvernex/argus_matrix.py`: unchanged deterministic decision engine;
- `pyproject.toml`: installs `kyvernex-argus-translate`;
- contradictory consent or risk statements fail closed;
- no LLM or external network is used.

## Product example

```text
kyvernex-argus-translate \
  --text "Il cliente ha dato il consenso e il rischio è basso." \
  --matrix examples/argus_matrix.json \
  --output argus-human-decision.json \
  --force
```

## Boundary
M18 translates only explicitly supported Italian statements. General semantics, complete constitutional vocabulary, symbolic language, multilingual interpretation, probabilistic inference, learning, external data, and release qualification remain outside the current code. Tests are intentionally deferred until the milestone is complete.
