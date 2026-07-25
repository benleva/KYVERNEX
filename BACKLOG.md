# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestones: `M7` through `M15`
- Local runtime path: `LOCAL_APP_SMOKE_VERIFIED`
- Active milestone: `M16 — Local Verification Report`
- Development package version: `1.2.0.dev0`

## Preserved state
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`;
- M7 through M15 retain their recorded code and smoke-verification qualifiers;
- `RUNTIME_SMOKE_EVIDENCE.md` remains the evidence for the operator-run Codespaces path.

## M16 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M16-W001 | Expanded `kyvernex-ai-smoke` checks and optional persistent JSON report | P0 | CODE_COMPLETE_UNVERIFIED |
| M16-W002 | Operator execution of the expanded command with saved report | P0 | READY_FOR_OPERATOR_RUN |

## M16 code evidence

- `src/kyvernex/local_ai_smoke_cli.py` accepts `--output` and `--force`;
- adapter health, four provider manifest shapes and OpenAPI invocation routes are checked;
- `/invoke` and `/tool-call` must both succeed;
- tool-call correlation id preservation is checked;
- report output lists remaining unverified areas instead of implying full qualification;
- existing report files require `--force` before replacement.

## Operator command

```text
python -m pip install -e .
kyvernex-ai-smoke --output local-verification.json
```

Readable output:

```text
python -m json.tool local-verification.json
```

## Remaining verification backlog

| Verification item | Priority | Status |
|---|---:|---|
| Expanded M16 verification run | P0 | READY_FOR_OPERATOR_RUN |
| Full automated test suite | P0 | NOT_RUN |
| Clean install outside Codespaces | P0 | NOT_RUN |
| Windows portable launcher | P1 | NOT_RUN |
| macOS portable launcher | P1 | NOT_RUN |
| Linux portable launcher outside Codespaces | P1 | NOT_RUN |
| JSONL persistent CLI path | P1 | NOT_RUN |
| Failure, timeout and size-limit paths | P1 | NOT_RUN |
| Concurrency, load and recovery behavior | P2 | NOT_RUN |
| Release qualification | P0 | NOT_STARTED |

## Boundary

The existing successful smoke run verifies one concrete local Codespaces path. M16 adds repeatable reporting but remains unverified until the operator runs the updated command. Stable `v1.1.0` remains unchanged.
