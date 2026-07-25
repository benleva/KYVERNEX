# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Active milestone: **M7 — Plugin Product Interface**
- Active sprint: **S010 — Usable plugin API**
- Governance mode: **KPM/KGO ACTIVE — PRODUCT CODE**
- KPM cycle: `KPM-CYCLE-020`
- KGO cycle: `KGO-CYCLE-031`
- Target version: `1.2.0`

## Direction change authorized by user
M6 test-only work is paused. No claim is made that M6-W006, M6-W007, M6-W008 or M6-W009 are complete.

KPM and KGO now prioritize executable product code over additional governance and test expansion.

## M7 objective
Expose KYVERNEX as a directly usable Python plugin with a compact host-facing API and an installed command.

The first product path is:

```text
host handler -> KyvernexPlugin -> governed runtime -> bounded adapter -> structured response
```

## Active implementation
- M7-W001 usable Python facade and installed command: `CODE_COMPLETE_UNVERIFIED`

Repository code added:
- `src/kyvernex/plugin.py` with public `KyvernexPlugin` facade;
- `src/kyvernex/plugin_cli.py` with `kyvernex-plugin` command;
- `pyproject.toml` entry point `kyvernex-plugin`;
- public package export from `src/kyvernex/__init__.py`.

The facade owns initialization, validation, governed execution, status and shutdown. It accepts one host-supplied callable and converts compact host arguments into the existing structured request contract.

## Current product use
Python:

```python
from kyvernex import KyvernexPlugin

plugin = KyvernexPlugin(handler)
response = plugin.execute({"message": "ciao"}, principal="andrea")
plugin.shutdown()
```

Installed command:

```text
kyvernex-plugin '{"message":"ciao"}' --principal andrea
```

## Continuation rule
Continue M7 with product code that makes the plugin easier to install and use. Do not return to test-only work unless explicitly requested. Do not claim verification or release evidence that has not been observed.