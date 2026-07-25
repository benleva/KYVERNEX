# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestones: **M7**, **M8**, **M9**, **M10**, **M11**, **M12**, **M13**, **M14**
- Sprint: **S017 — Public integration surface**
- Governance mode: **KPM/KGO PRODUCT CODE BOUNDARY**
- KPM cycle: `KPM-CYCLE-037`
- KGO cycle: `KGO-CYCLE-048`
- Development package version: `1.2.0.dev0`

## M14 objective delivered
Expose one coherent Python integration surface for handler loading, persistent plugin sessions and AI manifest translation.

```text
from kyvernex import (
    KyvernexPluginSession,
    load_plugin_handler,
    export_openai_tool,
)
```

## M14 code delivered
### M14-W001 — Unified handler loader API
Status: `CODE_COMPLETE_UNVERIFIED`

- `load_plugin_handler` remains the canonical strict loader;
- `load_handler` is now an explicit compatibility alias using the same implementation;
- command-line products and Python callers no longer depend on two separate loading paths;
- `PluginHandler` and `PluginHandlerLoadError` are exported from the package root.

### M14-W002 — Public session and AI format APIs
Status: `CODE_COMPLETE_UNVERIFIED`

- `KyvernexPluginSession` is exported from `kyvernex`;
- its default development version is aligned to `1.2.0.dev0`;
- dedicated exporters are available for canonical, OpenAI, Anthropic and Gemini shapes;
- `export_manifest` dispatches through those dedicated exporters;
- all exporter functions and `AIManifestFormatError` are exported from the package root.

## Public integration example

```python
from kyvernex import KyvernexPluginSession, load_plugin_handler

handler = load_plugin_handler("handler:handle")
with KyvernexPluginSession(handler, principal="andrea") as session:
    response = session.execute({"message": "ciao"})
```

## Boundary
M14 changes only the public Python integration surface and version alignment. It adds no runtime, transport, network access, installer, operating-system registration, verification or release publication. No tests were executed and no compatibility claim is made.
