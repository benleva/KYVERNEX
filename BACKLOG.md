# KYVERNEX BACKLOG

## Baseline
- Stable release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Verified milestones: `M16`, `M17`, `M18`
- Active delivery cycle: `PLUGIN FIRST`
- Development package version: `1.2.0.dev0`

## Immediate objectives

| Priority | Objective | Status |
|---:|---|---|
| P0 | Primary `kyvernex` product command | IN_PROGRESS |
| P0 | One-command local initialization | IMPLEMENTED |
| P0 | Default governed example execution | IMPLEMENTED |
| P0 | Installation and publication metadata | NEXT |
| P0 | Minimal operator instructions | NEXT |
| P0 | Build distributable package | PENDING |
| P0 | Demonstrate install and operational run | PENDING |
| P1 | Marketplace or registry publication | PENDING_AUTHORIZATION |

## Implemented in current cycle
- `src/kyvernex/product_cli.py` provides `init`, `status`, and `run`;
- initialization creates `.kyvernex/config.json` and `.kyvernex/request.example.json`;
- run uses the existing governed `KyvernexPlugin` execution path through `plugin_cli`;
- `pyproject.toml` maps `kyvernex` to the product CLI;
- the previous prototype remains available as `kyvernex-core`.

## Delivery rule
Work is accepted when it directly shortens the path to an installable, understandable, and operational plugin. New test campaigns, broad refactors, and nonessential features are deferred unless they block installation, compatibility, security, or execution.

## Release boundary
No tag or release may be created without explicit authorization. Stable `v1.1.0` remains unchanged.
