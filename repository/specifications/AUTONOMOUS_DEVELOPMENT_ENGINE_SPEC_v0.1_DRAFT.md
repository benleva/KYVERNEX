# AUTONOMOUS DEVELOPMENT ENGINE SPEC v0.1 DRAFT

## Purpose
Define the M3 governed development layer that converts KPM/KGO backlog state into deterministic, policy-bounded development cycles.

## Scope
The engine shall:
- select the next dependency-valid work item;
- enforce priority and story-point limits;
- require specification, targeted tests, complete tests and checkpoints according to policy;
- emit machine-readable cycle plans and checkpoints;
- stop at authorization boundaries for source modification or merge when policy requires it;
- preserve the KDP anti-infinite rule.

## Architecture
User goal -> KGO -> KPM -> AutonomousDevelopmentEngine -> KEX/authorized coding boundary -> tests -> CI evidence -> checkpoint.

## Canonical M3 backlog
1. M3-W001 Autonomous task scheduler.
2. M3-W002 Specification-to-change manifest.
3. M3-W003 Continuous self-verification controller.
4. M3-W004 Safe isolated commit manager.
5. M3-W005 Evidence-based rollback controller.

## Artifacts
- `ADE_CYCLE_PLAN.json`
- `ADE_CHECKPOINT.json`
- optional governance checkpoint supplied to KGO

## Safety and authority boundary
The engine may select, plan and persist a cycle. It shall not claim that code was generated, committed, merged or verified without evidence from the corresponding authorized executor and CI run.

## Definition of Done
- implementation present;
- deterministic tests present;
- specification and update record present;
- architecture documentation updated;
- complete CI suite executed successfully on the resulting commit.
