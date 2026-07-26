# KYVERNEX

KYVERNEX is a deterministic governance and plugin execution engine for the ARGUS cognitive constitution.

The current development line is focused on one practical goal: make the plugin installable, understandable and operational with the smallest possible setup.

## Status

- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Development version: `1.2.0.dev0`
- M18 ARGUS Executive Translator: verified and closed
- Current work: plugin-first publication path

No new tag or release is created by development commits.

## Requirements

- Python 3.11 or newer
- `pip`

## Install from the repository

```bash
python -m pip install "git+https://github.com/benleva/KYVERNEX.git"
```

For local development:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[test,build]"
```

On Windows PowerShell activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Quick start

Create the local KYVERNEX configuration and an example request:

```bash
kyvernex init
```

Inspect the current local configuration:

```bash
kyvernex status
```

Run the generated example request:

```bash
kyvernex run
```

The initialization command creates:

```text
.kyvernex/config.json
.kyvernex/request.example.json
```

## Product commands

```text
kyvernex init     create the local configuration and example request
kyvernex status   show product and configuration status
kyvernex run      execute a governed plugin request
```

The previous reference-engine command remains available as:

```bash
kyvernex-core "content" --source local
```

Advanced installed commands remain available for governance, plugin execution, local AI integration and ARGUS translation.

## Direct plugin execution

A JSON object can be executed through the governed in-process plugin runtime:

```bash
kyvernex-plugin --input '{"message":"hello"}'
```

A custom Python handler can be loaded with an exact `MODULE:ATTRIBUTE` reference:

```bash
kyvernex-plugin \
  --input '{"message":"hello"}' \
  --handler my_package.handlers:handle
```

The handler is executed inside the existing KYVERNEX capability and authority boundary.

## ARGUS translation

Translate supported Italian statements into canonical ARGUS data:

```bash
kyvernex-argus-translate "L'utente ha dato il consenso e il rischio è basso"
```

The translator is deterministic, closed-world and does not infer facts that are not explicitly represented by its supported vocabulary.

## Build a distributable package

```bash
python -m pip install ".[build]"
python -m build
```

The source distribution and wheel are written to `dist/`.

## Governance boundary

KYVERNEX does not claim that code, verification, releases or repository mutations occurred without corresponding evidence. KPM selects dependency-valid work; KGO preserves the stable baseline and blocks unsupported claims.

The current plugin-first phase deliberately avoids expanding scope unless a change is required for installation, operation or publication.

## License

Proprietary software. All rights reserved.

See `PROJECT_STATUS.md` for the authoritative project state, `BACKLOG.md` for ordered work and `CHANGELOG.md` for release history.
