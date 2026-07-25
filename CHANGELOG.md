# Changelog

All notable changes to KYVERNEX are documented in this file.

The project follows semantic versioning after the first stable release. Until Release 1.0 is certified, changes remain under the `Unreleased` section.

## [Unreleased]

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
- Persistent governance, verification, rollback and performance artifacts.

### Changed
- README synchronized with the completed six-item M3 backlog and Release 1.0 audit state.
- Project governance state advanced from M3 implementation to Release 1.0 audit.

### Fixed
- Rollback-controller test fixture now includes explicit current failed-test evidence matching the verification parser contract.

### Security and governance
- Rollback execution remains outside the controller and requires an authorized executor.
- Performance evidence cannot replace correctness evidence or authorize execution.
- Historical failed runs do not override current commit evidence.

## Release policy

Release `1.0.0` must not be published until:

- package and public API versions are synchronized;
- licensing terms are explicitly selected and recorded in a root `LICENSE` file;
- a clean package build succeeds;
- installation and tests succeed in a clean environment;
- the final GitHub Actions verification is green;
- the `Unreleased` entries are moved into a dated `1.0.0` section.