# KYVERNEX PROJECT STATUS

## Control
- Stable published release: `1.1.0`
- Immutable stable tag: `v1.1.0`
- Paused milestone: **M6 — KYVERNEX Plugin Runtime**
- Code-complete milestones: **M7**, **M8**, **M9**, **M10**, **M11**, **M12**
- Sprint: **S015 — Cross-platform local start files**
- Governance mode: **KPM/KGO PRODUCT CODE BOUNDARY**
- KPM cycle: `KPM-CYCLE-034`
- KGO cycle: `KGO-CYCLE-045`
- Development package version: `1.2.0.dev0`

## Product objective delivered
Generate readable Windows, macOS and Linux launch files from one validated local profile, either directly or during initial setup.

```text
kyvernex-ai-setup --launchers
-> strict JSON profile
-> portable launch files
-> optional immediate app launch
-> loopback KYVERNEX console
```

## Preserved product code
M7 through M11 remain `CODE_COMPLETE_UNVERIFIED`. M12 reuses the same profile validator, setup command and desktop launcher. No installer, system registration or background service is introduced.

## M12 code delivered
### M12-W001 — Portable launcher generator
Status: `CODE_COMPLETE_UNVERIFIED`

- `src/kyvernex/local_ai_shortcut_cli.py` provides `kyvernex-ai-shortcut`;
- `pyproject.toml` installs the command;
- one explicit profile is resolved and validated before generation;
- Windows output is `start-kyvernex.cmd`;
- macOS output is `start-kyvernex.command`;
- Linux output is `start-kyvernex.sh`;
- POSIX files receive executable permission bits;
- existing files require `--force` before replacement;
- every file invokes only `kyvernex-ai-app --profile <absolute path>`.

### M12-W002 — Launcher generation during setup
Status: `CODE_COMPLETE_UNVERIFIED`

- `kyvernex-ai-setup --launchers` invokes the existing portable launcher generator after profile validation;
- `--launcher-platform all|windows|macos|linux` selects generated formats;
- `--launcher-dir` selects the output directory;
- `--force` applies consistently to the profile and generated launcher files;
- launcher generation failure stops the setup flow before optional app launch;
- `--launch` may still start the existing loopback app after successful generation.

## Current use

Create profile and all portable launchers:

```text
kyvernex-ai-setup --handler examples.plugin_handler:handle --principal andrea --launchers
```

Create Windows launcher and start the app:

```text
kyvernex-ai-setup --handler examples.plugin_handler:handle --principal andrea --launchers --launcher-platform windows --launch
```

## Boundary
M12 is code-complete but unverified. It creates portable text files only. It does not create installers, Start-menu entries, desktop registrations, login items, system services, automatic startup, public binding, network access or release publication. No CI, clean-install or runtime compatibility claim is made.
