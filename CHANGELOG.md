# Changelog

All notable changes to KYVERNEX are documented in this file.

The project follows semantic versioning from Release 1.0 onward.

## [Unreleased]

No unreleased changes.

## [1.1.0] - 2026-07-25

### Added
- Deterministic `kyvernex-governance` console script for KPM/KGO `start`, `status`, `advance` and `resume` operations.
- Fail-closed JSON governance-plan loading with enum, dependency, milestone and Definition of Done validation.
- Targeted governance CLI tests and installed-wheel console-script smoke verification in CI.
- Stable release notes in `RELEASE_NOTES_1.1.0.md`.

### Changed
- Package metadata and public API version promoted from `1.1.0rc1` to `1.1.0`.
- GitHub Actions verifies the stable package version, full suite, distributions, clean installation and installed console-script behavior.
- M5 records the governed promotion from the verified release candidate to the stable 1.1 line.

### Security and governance
- The governance CLI may write only the explicitly supplied checkpoint path.
- The CLI cannot edit source files, Git refs, branches, issues or releases.
- Active work, incomplete dependencies and closed milestones cannot be bypassed.
- Published tags `v1.0.0` and `v1.1.0-rc.1` remain immutable.

### Verification
- Fresh stable-promotion CI is required before tag `v1.1.0` and GitHub Release publication.

## [1.1.0rc1] - 2026-07-25

### Added
- Deterministic `kyvernex-governance` console script for KPM/KGO `start`, `status`, `advance` and `resume` operations.
- Fail-closed JSON governance-plan loading with enum, dependency, milestone and Definition of Done validation.
- Targeted governance CLI tests and installed-wheel console-script smoke verification in CI.
- Release Candidate notes in `RELEASE_NOTES_1.1.0rc1.md`.

### Changed
- Package metadata and public API version advanced to `1.1.0rc1`.
- GitHub Actions now verifies the governance CLI, full suite, distributions, clean installation and installed console-script behavior.
- KPM/KGO checkpoint and governance records advanced through M4 and Sprint S002.

### Security and governance
- The governance CLI may write only the explicitly supplied checkpoint path.
- The CLI cannot edit source files, Git refs, branches, issues or releases.
- Active work, incomplete dependencies and closed milestones cannot be bypassed.
- The published `v1.0.0` tag remains immutable.

### Verification
- M4 targeted tests passed.
- Complete repository suite passed.
- Source and wheel distributions built successfully.
- Generated wheel installed successfully in a clean virtual environment.
- Installed package metadata and public API both reported `1.1.0rc1`.
- Installed `kyvernex-governance start` smoke test passed.
- KGO v3 final Release Candidate workflow was observed green on commit `807def6`.

## [1.0.0] - 2026-07-25

### Added
- KGO v1 governed test-output analysis and backlog generation.
- KGO v2 root-cause grouping and ordered patch planning.
- KGO v3 current-evidence autonomous governance loop.
- KPM milestone and dependency-valid work-item prioritization.
- KEX governed execution boundary.
- M3 autonomous task scheduler.
- Specification-to-change manifest generation.
- Continuous self-verification controller.
- Safe isolated commit planning.
- Evidence-based rollback planning with explicit authorization and matching changeset controls.
- Execution performance clock with deterministic timing, baseline comparison and improvement metrics.
- GitHub Actions workflow for targeted and complete verification evidence.
- Source and wheel package builds in CI.
- Clean-environment wheel installation and version verification.
- Persistent governance, verification, rollback and performance artifacts.
- Proprietary repository license.

### Changed
- Package and public API versions synchronized to `1.0.0`.
- README synchronized with the completed six-item M3 backlog and Release 1.0 workflow.
- Project governance state advanced from M3 implementation to Release 1.0 finalization.

### Fixed
- Rollback-controller test fixture now includes explicit current failed-test evidence matching the verification parser contract.

### Security and governance
- Rollback execution remains outside the controller and requires an authorized executor.
- Performance evidence cannot replace correctness evidence or authorize execution.
- Historical failed runs do not override current commit evidence.
- The source code, specifications and documentation remain proprietary and all rights are reserved.

### Verification
- Targeted tests passed.
- Complete test suite passed.
- Source distribution built successfully.
- Wheel distribution built successfully.
- Generated wheel installed successfully in a clean virtual environment.
- Installed package metadata and public API both reported version `1.0.0`.
- GitHub Actions release-candidate run `#58` completed successfully.
