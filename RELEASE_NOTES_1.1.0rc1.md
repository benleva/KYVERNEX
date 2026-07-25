# KYVERNEX 1.1.0rc1

KYVERNEX 1.1.0rc1 is the release candidate for the governed post-release evolution milestone M4.

## Added

- Installed `kyvernex-governance` console command.
- Deterministic `start`, `status`, `advance` and `resume` operations.
- Fail-closed JSON plan loading and enum validation.
- Dependency, closed-milestone and active-item safeguards.
- Explicit checkpoint write boundary.
- Installed-wheel CLI smoke verification in GitHub Actions.

## Governance boundaries

The CLI may read an explicitly supplied plan and checkpoint and may write only the supplied checkpoint path. It does not edit source files, Git references, branches, issues, releases or documentation. It does not claim tests, CI success, repository writes or publication without evidence.

## Verification

The M4 implementation was verified green for commit `0312f97857dd954b71ad44b07834c545f40a9db1` by the KGO v3, Reference Prototype Tests and Test Suite workflows. The synchronized `1.1.0rc1` package and clean installation require a fresh release-candidate workflow run before tagging or publication.

## Stable baseline

Release `1.0.0` and tag `v1.0.0` remain immutable and published as the stable baseline.

## License

Copyright © 2026 Andrea Pernarcic. All rights reserved. See `LICENSE`.
