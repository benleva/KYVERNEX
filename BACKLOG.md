# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Paused milestone: `M6 — KYVERNEX Plugin Runtime`
- Code-complete milestones: `M7`, `M8`, `M9`, `M10`, `M11`, `M12`, `M13`, `M14`
- Development package version: `1.2.0.dev0`

## Preserved state
- M6-W001 through M6-W005: `DONE`;
- M6-W006 through M6-W009: `PAUSED_BY_USER`;
- M7 through M13 work items: `CODE_COMPLETE_UNVERIFIED`.

## M14 product-code backlog

| Work item | Deliverable | Priority | Status |
|---|---|---:|---|
| M14-W001 | Unified strict handler loader API with compatibility alias | P0 | CODE_COMPLETE_UNVERIFIED |
| M14-W002 | Package-root exports for plugin sessions and AI manifest exporters | P0 | CODE_COMPLETE_UNVERIFIED |

## M14 code evidence
- `src/kyvernex/plugin_loader.py`: canonical `load_plugin_handler` plus `load_handler` compatibility alias;
- `src/kyvernex/plugin_session.py`: persistent session aligned to development version `1.2.0.dev0`;
- `src/kyvernex/ai_formats.py`: dedicated canonical, OpenAI, Anthropic and Gemini exporters;
- `src/kyvernex/__init__.py`: public exports for loaders, session and format APIs.

## Public imports

```python
from kyvernex import (
    AIManifestFormatError,
    KyvernexPluginSession,
    PluginHandlerLoadError,
    export_anthropic_tool,
    export_canonical_tool,
    export_gemini_tools,
    export_manifest,
    export_openai_tool,
    load_handler,
    load_plugin_handler,
)
```

## Boundary
M14 has no active coding item. It is code-complete but unverified. No tests, clean-install checks, CI assertions, tags or releases were produced.
