# SAFE ISOLATED COMMIT MANAGER SPEC v0.1

## Work item
`M3-W004 — Safe isolated commit manager`

## Purpose
Create a deterministic, policy-bounded commit plan for one authorized work item without executing git or GitHub operations internally.

## Required controls
- explicit work-item identifier;
- immutable base commit reference;
- explicit authorization;
- normalized repository-relative paths;
- allowed-root enforcement;
- forbidden-path enforcement;
- duplicate-path rejection;
- maximum files per changeset;
- SHA-256 content hashes for create and update operations;
- deterministic changeset fingerprint.

## Boundary
The manager seals a plan for an external authorized executor. It does not create branches, write repository content, merge pull requests or bypass GitHub permissions.

## Result
An `IsolatedCommitPlan` contains the work item, base commit, message, ordered changes, authorization state and deterministic fingerprint.

## Definition of Done
- implementation present;
- public API exported;
- tests cover authorization, path boundaries, duplicate paths and mutation detection;
- project status synchronized;
- complete CI succeeds.
