# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestones: **M7**, **M8**, **M9**, **M10**
- Sprint: **S013 — One-command local app**
- Governance mode: **KPM/KGO PRODUCT CODE BOUNDARY**
- KPM cycle: `KPM-CYCLE-030`
- KGO cycle: `KGO-CYCLE-041`
- Development package version: `1.2.0.dev0`

## Product objective delivered
Start the existing loopback server and open its console with one installed command, optionally configured by one explicit local JSON profile.

```text
kyvernex-ai-app
-> command arguments or explicit profile
-> host callable
-> KyvernexLocalAIServer on 127.0.0.1
-> system browser
-> local KYVERNEX console
```

## Preserved product code
M7, M8 and M9 remain `CODE_COMPLETE_UNVERIFIED`. M10 reuses the same plugin, AI bridge, local server and browser console. No second backend or runtime is introduced.

## M10 code delivered
### M10-W001 — One-command desktop launcher
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_app_cli.py` provides the launcher;
- `pyproject.toml` installs `kyvernex-ai-app`;
- the launcher starts the fixed loopback server and opens the local console;
- `--no-browser` keeps the same application headless;
- `Ctrl+C` shuts down server and bridge.

### M10-W002 — Explicit local JSON profile
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_profile.py` loads one explicitly named UTF-8 JSON file;
- supported fields are only `handler`, `principal`, `port` and `open_browser`;
- unknown fields fail closed;
- no automatic discovery, environment read or fallback profile is used;
- command-line values override profile values;
- `examples/local_ai_profile.json` provides a minimal usable profile.

## Current use

```text
kyvernex-ai-app --profile examples/local_ai_profile.json
```

Command-line override:

```text
kyvernex-ai-app --profile examples/local_ai_profile.json --port 9000 --no-browser
```

## Boundary
M10 is code-complete but unverified. It launches only the already delivered loopback product. It does not add public binding, remote hosting, authentication, databases, accounts, installers, operating-system services or release publication. No CI, clean-install or runtime verification claim is made.
