# KYVERNEX PROGRAM MANAGER SPEC v1.0 DRAFT

## Purpose
The KYVERNEX Program Manager (KPM) governs the development lifecycle of KYVERNEX according to the KYVERNEX Development Protocol (KDP). It prevents uncontrolled scope growth, selects executable work, verifies the Definition of Done and determines when a task or milestone may be closed.

## Core rules
1. Every new idea starts in the backlog.
2. Every work item belongs to one milestone and one status.
3. Dependencies must be complete before work starts.
4. A work item is DONE only when every Definition of Done field is true.
5. A milestone is closed only when all its work items are DONE.
6. A closed milestone rejects every new work item. New scope belongs to a later version.
7. Progress is calculated from explicit work items and story points, never from narrative estimates.

## States
BACKLOG, READY, IN_DEVELOPMENT, TEST, REVIEW, DONE, BLOCKED.

## Priorities
P0 blocking, P1 fundamental, P2 important, P3 improvement, P4 research.

## Definition of Done
- specification
- implementation
- unit tests
- integration tests
- CI passed
- documentation
- README update
- CHANGELOG update
- audit review
- final review

## Commands represented by the API
- STATUS / REPORT: `report()`
- NEXT: `next_item()`
- START: `start()`
- REVIEW: `review()`
- CLOSE TASK: `close_item()`
- CLOSE MILESTONE: `close_milestone()`

## Anti-infinite invariant
Once `Milestone.closed` is true, `add_item()` must fail with `REGOLA_ANTIINFINITO_MILESTONE_CHIUSA`.

## Completion of KYVERNEX 1.0
KYVERNEX 1.0 is complete only when all 1.0 milestones are closed, all tasks satisfy the Definition of Done, the 1.0 backlog is empty, CI and required tests are verified, no P0/P1 defects remain and a release report has been produced.
