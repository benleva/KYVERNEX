# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Verified milestone: **M16 — Local Verification Report**
- Verified milestone: **M17 — ARGUS Matrix Runner**
- Verified milestone: **M18 — ARGUS Executive Translator**
- Active delivery cycle: **PLUGIN FIRST — operational publication**
- Development package version: `1.2.0.dev0`

## Closed milestone
M18 is closed and verified. GitHub Actions completed `M18 Verification #3` successfully for commit `4ce2c5a04530e89496994cf26d38acfb6bad2065`.

Success marker:

```text
M18_ARGUS_EXECUTIVE_TRANSLATOR_VERIFIED
```

## Current objective
Publish an installable and operational KYVERNEX plugin as soon as practical, without adding nonessential scope.

## KPM priorities
1. Make the primary `kyvernex` command initialize and run the plugin with minimal setup.
2. Provide one default local configuration and one working example request.
3. Prepare the package metadata and user-facing files required for publication.
4. Publish only after a direct installation and operational run can be demonstrated.

## KGO boundary
- keep stable release `1.1.0` and tag `v1.1.0` untouched;
- do not create a release or tag without explicit authorization;
- preserve the verified runtime and expose it through a simpler product interface;
- defer new test campaigns and nonessential documentation during this delivery cycle;
- block only critical packaging, compatibility, security, or execution defects.

## Work started
- `src/kyvernex/product_cli.py` adds `kyvernex init`, `kyvernex status`, and `kyvernex run`;
- `kyvernex run` delegates execution to the existing governed plugin runtime;
- `pyproject.toml` exposes the product CLI as `kyvernex` and preserves the previous prototype command as `kyvernex-core`;
- no tag or release has been created.
