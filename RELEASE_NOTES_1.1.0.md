# KYVERNEX 1.1.0

KYVERNEX 1.1.0 promotes the verified 1.1.0 release candidate to the stable release line without adding new functional scope.

## Added

- Installed `kyvernex-governance` console command.
- Deterministic `start`, `status`, `advance` and `resume` operations.
- Fail-closed JSON plan loading and enum validation.
- Dependency, closed-milestone and active-item safeguards.
- Explicit checkpoint write boundary.
- Installed-wheel governance CLI smoke verification in GitHub Actions.

## Governance boundaries

The CLI may read an explicitly supplied plan and checkpoint and may write only the supplied checkpoint path. It does not edit source files, Git references, branches, issues, releases or documentation. It does not claim tests, CI success, repository writes or publication without evidence.

## Promotion policy

This stable release contains the behavior verified in `v1.1.0-rc.1`. Promotion to `1.1.0` changes package and public API version metadata, release documentation and verification evidence only. No additional feature is introduced during promotion.

## Verification

Before tagging or publication, the stable `1.1.0` state must pass targeted governance tests, the complete repository suite, source and wheel builds, clean installation, package and public API version checks and the installed `kyvernex-governance` smoke test.

## Previous releases

- `v1.0.0` remains an immutable historical stable release.
- `v1.1.0-rc.1` remains an immutable prerelease record.

## License

Copyright © 2026 Andrea Pernarcic. All rights reserved. See `LICENSE`.
