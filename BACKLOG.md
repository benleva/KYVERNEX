# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Verified local report: `M16 — LOCAL_APP_SMOKE_VERIFIED`
- Active milestone: `M17 — ARGUS Matrix Runner`
- Development package version: `1.2.0.dev0`

## M17 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M17-W001 | Strict deterministic ARGUS JSON matrix evaluator | P0 | CODE_COMPLETE_UNVERIFIED |
| M17-W002 | Installed `kyvernex-argus` command and example matrix | P0 | CODE_COMPLETE_UNVERIFIED |
| M17-W003 | Operator execution with saved request and decision report | P0 | READY_FOR_OPERATOR_RUN |

## Code evidence
- `src/kyvernex/argus_matrix.py` evaluates explicit ordered rules;
- `src/kyvernex/argus_matrix_cli.py` reads matrix and request JSON;
- `examples/argus_matrix.json` demonstrates consent and risk decisions;
- `pyproject.toml` installs `kyvernex-argus`;
- output replacement requires `--force`.

## Operator example

```text
printf '{"consent":true,"risk":"low"}' > argus-request.json
python -m pip install -e .
kyvernex-argus --matrix examples/argus_matrix.json --request argus-request.json --output argus-decision.json --force
python -m json.tool argus-decision.json
```

## Boundary
The matrix runner is not yet the complete ARGUS Constitution or translator. Natural language, symbolic conversion, weighted inference, conflict resolution across matrices, persistence, and full testing remain future work. Stable `v1.1.0` remains unchanged.
