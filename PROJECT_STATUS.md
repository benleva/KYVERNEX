# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestones: **M7** through **M15**
- Verified milestone: **M16 — Local Verification Report**
- Active milestone: **M17 — ARGUS Matrix Runner**
- Active sprint: **S020 — First executable ARGUS use case**
- KPM cycle: `KPM-CYCLE-043`
- KGO cycle: `KGO-CYCLE-054`
- Development package version: `1.2.0.dev0`

## Verified local product path
The operator executed `kyvernex-ai-smoke --diagnose` and `kyvernex-ai-smoke --output local-verification.json --force` in GitHub Codespaces. The persistent report returned `status: SUCCEEDED`, `verification: LOCAL_APP_SMOKE_VERIFIED`, package version `1.2.0.dev0`, the repository module path, healthy adapter state, four provider manifests, OpenAPI routes, direct invocation and tool-call correlation.

## M17 objective
Execute one explicit JSON-defined ARGUS matrix against one JSON request and return a deterministic decision with rule trace.

```text
kyvernex-argus --matrix examples/argus_matrix.json --request request.json
-> strict matrix validation
-> ordered rule evaluation
-> ALLOW | DENY | REVIEW | ABSTAIN
-> selected rule and trace
```

## M17 delivered code
### M17-W001 — Deterministic matrix evaluator
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/argus_matrix.py` validates matrices and requests;
- supported operators are `eq`, `ne`, `in`, `contains`, and `exists`;
- decisions are limited to `ALLOW`, `DENY`, `REVIEW`, and `ABSTAIN`;
- rule ids must be unique;
- unknown fields and unsupported operators fail closed;
- the response contains the selected rule, reason, request copy, and rule trace.

### M17-W002 — Installed ARGUS command and example
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/argus_matrix_cli.py` provides `kyvernex-argus`;
- `pyproject.toml` installs the command;
- requests may come from a JSON file or stdin;
- optional output replacement requires `--force`;
- `examples/argus_matrix.json` supplies a minimal explicit matrix.

## Boundary
M17 does not claim to encode the complete ARGUS Constitution, natural-language translation, symbolic mathematics, probabilistic reasoning, learning, external data access, or release readiness. It is the first narrow executable matrix contract. No tests, tag, or release were created in this change.
