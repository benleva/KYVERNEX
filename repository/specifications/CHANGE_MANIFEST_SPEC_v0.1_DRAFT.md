# Specification-to-Change Manifest v0.1 DRAFT

## Purpose
Translate one approved KPM work item and its technical specification into a deterministic, machine-readable set of repository changes and verification commands.

## Required fields
- schema and manifest identifier;
- originating work-item identifier;
- specification path;
- ordered repository changes;
- targeted tests;
- complete-suite command;
- declared work-item dependencies.

## Governance rules
1. Every path must be repository-relative and must not contain parent traversal.
2. Every change must declare CREATE, UPDATE or DELETE and a non-empty rationale.
3. At least one targeted test is mandatory.
4. Complete-suite verification remains mandatory after targeted tests.
5. A manifest authorizes planning only. It does not authorize writing, committing or merging.
6. Duplicate targeted tests are normalized while preserving first occurrence order.

## Output schema
`kyvernex.change-manifest.v1`

## Definition of Done
- executable model implemented;
- unsafe path rejection covered by tests;
- deterministic JSON serialization covered by tests;
- dependency propagation covered by tests;
- integration with ADE planned as the next controlled step.
