# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestone: `M7 — Plugin Product Interface`
- Code-complete milestone: `M8 — Universal AI Plugin Bridge`
- Development package version: `1.2.0.dev0`

## M6 paused state
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`.

## M7 preserved state
M7-W001 through M7-W005 remain `CODE_COMPLETE_UNVERIFIED`.

## M8 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M8-W001 | Public provider-neutral `KyvernexAIBridge` | P0 | CODE_COMPLETE_UNVERIFIED |
| M8-W002 | Installed `kyvernex-ai-plugin` JSON bridge command | P0 | CODE_COMPLETE_UNVERIFIED |
| M8-W003 | Persistent JSONL multi-request process mode | P0 | CODE_COMPLETE_UNVERIFIED |
| M8-W004 | Canonical, OpenAI, Anthropic and Gemini manifest shapes | P1 | CODE_COMPLETE_UNVERIFIED |

## M8 code evidence
- `src/kyvernex/ai_bridge.py`: canonical bridge plus `manifest_for(provider)`;
- `src/kyvernex/ai_formats.py`: provider-shape translation;
- `src/kyvernex/ai_plugin_cli.py`: single request, JSONL stream and selectable manifest format;
- `pyproject.toml`: installed `kyvernex-ai-plugin` entry point;
- `src/kyvernex/__init__.py`: public `KyvernexAIBridge` export.

## Product behavior

```text
kyvernex-ai-plugin --handler examples.plugin_handler:handle --manifest --manifest-format openai
kyvernex-ai-plugin --handler examples.plugin_handler:handle --manifest --manifest-format anthropic
kyvernex-ai-plugin --handler examples.plugin_handler:handle --manifest --manifest-format gemini
```

## Boundary
M8 has no active coding item. It is code-complete but unverified. The provider exporters reshape one canonical manifest and do not fork execution or governance. No green, clean-install, publication or release claim is made.
