# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestone: `M7 — Plugin Product Interface`
- Active milestone: `M8 — Universal AI Plugin Bridge`
- Development package version: `1.2.0.dev0`

## M6 paused state
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`.

## M7 preserved state
M7-W001 through M7-W005 remain `CODE_COMPLETE_UNVERIFIED`. No test, installation or release claim is inferred.

## M8 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M8-W001 | Public provider-neutral `KyvernexAIBridge` | P0 | CODE_COMPLETE_UNVERIFIED |
| M8-W002 | Installed `kyvernex-ai-plugin` JSON bridge command | P0 | CODE_COMPLETE_UNVERIFIED |
| M8-W003 | Streaming multi-request process mode | P0 | BACKLOG |
| M8-W004 | Provider format exporters using the same canonical manifest | P1 | BACKLOG |

## M8 code evidence
- `src/kyvernex/ai_bridge.py`: canonical AI tool bridge;
- `src/kyvernex/ai_plugin_cli.py`: standard-input JSON command;
- `pyproject.toml`: installed `kyvernex-ai-plugin` entry point;
- `src/kyvernex/__init__.py`: public `KyvernexAIBridge` export.

## Current product behavior

```text
kyvernex-ai-plugin --handler examples.plugin_handler:handle --manifest
```

```text
echo '{"input":{"message":"ciao"}}' | kyvernex-ai-plugin --handler examples.plugin_handler:handle --principal andrea
```

## Product rule
M8 must preserve one canonical KYVERNEX plugin. Provider-specific representations may translate the same manifest but must not fork governance logic or create separate runtime implementations. Testing is not the active user-directed workstream and no green claim is made.
