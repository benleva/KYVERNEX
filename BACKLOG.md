# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestones: `M7` through `M15`
- Local runtime path: `LOCAL_APP_SMOKE_VERIFIED`
- Development package version: `1.2.0.dev0`

## Preserved state
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`;
- M7 through M14 remain code-complete, with only the portions exercised by the local app smoke path promoted beyond `UNVERIFIED`.

## M15 status

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M15-W001 | Strict `name` plus `arguments` tool-call envelope on `KyvernexAIBridge` | P0 | CODE_COMPLETE_SMOKE_COVERED |
| M15-W002 | Automatic direct/envelope routing in single JSON and JSONL CLI modes | P0 | CODE_COMPLETE_PARTIALLY_VERIFIED |
| M15-W003 | Loopback `POST /tool-call` route reusing the same bridge method | P1 | LOCAL_HTTP_SMOKE_VERIFIED |

## Runtime evidence

`RUNTIME_SMOKE_EVIDENCE.md` records the operator-run Codespaces evidence:

- editable installation of `1.2.0.dev0`;
- execution of `kyvernex-ai-smoke`;
- generation of `prova-kyvernex`;
- loopback app readiness on port `8765`;
- private Codespaces forwarding;
- browser console loading;
- healthy adapter and restricted authority state;
- governed browser invocation returning `SUCCEEDED` with principal `andrea` and handler marker `local-project`.

## Remaining verification backlog

| Verification item | Priority | Status |
|---|---:|---|
| Full automated test suite | P0 | NOT_RUN |
| Clean install outside Codespaces | P0 | NOT_RUN |
| Windows portable launcher | P1 | NOT_RUN |
| macOS portable launcher | P1 | NOT_RUN |
| Linux portable launcher outside Codespaces | P1 | NOT_RUN |
| JSONL persistent CLI path | P1 | NOT_RUN |
| All provider manifest shapes | P1 | NOT_RUN |
| Failure, timeout and size-limit paths | P1 | NOT_RUN |
| Concurrency, load and recovery behavior | P2 | NOT_RUN |
| Release qualification | P0 | NOT_STARTED |

## Boundary

The successful smoke run verifies one concrete local Codespaces path. It does not justify a green test-suite claim, cross-platform compatibility claim or release publication. Stable `v1.1.0` remains unchanged.