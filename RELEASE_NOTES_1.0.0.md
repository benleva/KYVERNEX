# KYVERNEX 1.0.0

KYVERNEX 1.0.0 is the first stable release of the execution and governance engine for the ARGUS cognitive constitution.

## Release status

- Version: `1.0.0`
- Milestone: M3 Autonomous Development completed
- License: proprietary, all rights reserved
- Verification: GitHub Actions release-candidate run `#58` green
- Supported Python: 3.11 or later

## Included capabilities

### Governed program control
- KPM milestone and dependency-valid work-item prioritization.
- KGO v1 test-evidence analysis and governed backlog generation.
- KGO v2 root-cause grouping and ordered patch planning.
- KGO v3 current-evidence autonomous governance loop.
- KEX governed execution boundary.

### M3 autonomous development engine
- autonomous task scheduler;
- specification-to-change manifest;
- continuous self-verification controller;
- safe isolated commit manager;
- evidence-based rollback controller;
- execution performance clock and improvement metrics.

### Reliability and evidence
- deterministic verification behavior;
- explicit current-failure evidence requirements;
- policy-bounded rollback planning;
- governed execution records;
- persistent JSON and Markdown evidence artifacts;
- targeted and complete test execution in CI.

### Release engineering
- synchronized package and public API version `1.0.0`;
- source distribution build;
- wheel distribution build;
- clean virtual-environment wheel installation;
- installed metadata and public API version verification;
- CI distribution artifacts.

## Verification evidence

The verified release candidate passed:

1. M3 targeted tests;
2. the complete repository test suite;
3. source-package build;
4. wheel build;
5. clean-environment wheel installation;
6. installed metadata version verification;
7. public API version verification.

The successful evidence was observed in GitHub Actions run `#58` for commit `1c5c0aef855b876c3c79fd20808689066e35b5e1`.

## Installation

```bash
python -m pip install ./dist/kyvernex-1.0.0-py3-none-any.whl
```

For development and testing:

```bash
python -m pip install -e ".[test]"
python -m pytest -q
```

## Governance boundary

KYVERNEX produces governed decisions, plans and evidence. Repository writes, branch creation, commits, rollback execution, tagging, release publication and other external operations remain subject to an authorized executor and available permissions.

Performance measurements are observational. They cannot replace correctness evidence or authorize execution.

## License

Copyright © 2026 Andrea Pernarcic. All rights reserved.

KYVERNEX, ARGUS, their source code, specifications, documentation, governance models and related materials are proprietary. No permission is granted to use, copy, modify, distribute, sublicense, sell or commercially exploit them without prior written authorization from the rights holder. See the root `LICENSE` file for the controlling terms.
