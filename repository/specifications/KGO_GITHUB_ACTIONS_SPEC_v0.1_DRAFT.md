# KGO GitHub Actions Specification v0.1 DRAFT

## Purpose
Provide a reproducible GitHub-hosted execution boundary for KYVERNEX governance verification.

## Workflow
Path: `.github/workflows/kgo.yml`

Triggers:
- manual `workflow_dispatch`;
- pushes to `main` affecting source, tests, packaging or the workflow itself.

## Governed sequence
1. Checkout the exact repository commit.
2. Provision Python 3.11.
3. Install KYVERNEX with test dependencies.
4. Execute the complete pytest suite.
5. Capture test output.
6. Produce `KGO_EVIDENCE.json` with commit, run and outcome metadata.
7. Upload the evidence as a retained workflow artifact.
8. Fail the workflow when the test step is not successful.

## Security boundary
- Repository permission is read-only.
- No shell-generated repository commit is permitted.
- No secret is required.
- The workflow cannot declare CI verified until GitHub reports a completed successful run.

## Evidence rule
The existence of the workflow is implementation evidence only. A successful CI claim requires a completed GitHub Actions run associated with a specific commit.
