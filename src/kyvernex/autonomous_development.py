from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from typing import Iterable

from .kpm_prioritization import execution_clock_assessment
from .program_manager import (
    GovernanceCheckpoint,
    GovernanceState,
    KyvernexGovernanceOrchestrator,
    Priority,
    WorkItem,
    WorkStatus,
)


class AutonomousDevelopmentError(RuntimeError):
    """Raised when a governed development cycle cannot continue safely."""


class DevelopmentAction(StrEnum):
    SELECT_TASK = "SELECT_TASK"
    PREPARE_SPECIFICATION = "PREPARE_SPECIFICATION"
    IMPLEMENT = "IMPLEMENT"
    RUN_TARGETED_TESTS = "RUN_TARGETED_TESTS"
    RUN_COMPLETE_TESTS = "RUN_COMPLETE_TESTS"
    RECORD_CHECKPOINT = "RECORD_CHECKPOINT"
    STOP_FOR_AUTHORIZATION = "STOP_FOR_AUTHORIZATION"
    COMPLETE = "COMPLETE"


@dataclass(slots=True, frozen=True)
class DevelopmentPolicy:
    allowed_priorities: frozenset[Priority] = frozenset(Priority)
    require_specification: bool = True
    require_targeted_tests: bool = True
    require_complete_tests: bool = True
    allow_direct_main_write: bool = False
    allow_automatic_merge: bool = False
    max_story_points_per_cycle: int = 8

    def __post_init__(self) -> None:
        if not self.allowed_priorities:
            raise ValueError("PRIORITA_AUTONOME_MANCANTI")
        if self.max_story_points_per_cycle <= 0:
            raise ValueError("LIMITE_STORY_POINT_NON_VALIDO")


@dataclass(slots=True, frozen=True)
class DevelopmentStep:
    order: int
    action: DevelopmentAction
    description: str
    command: tuple[str, ...] = ()
    requires_authorization: bool = False


@dataclass(slots=True, frozen=True)
class AutonomousCyclePlan:
    schema: str
    cycle_id: str
    milestone_id: str | None
    item_id: str | None
    item_title: str | None
    priority: str | None
    story_points: int | None
    state: str
    steps: tuple[DevelopmentStep, ...]
    stop_reason: str | None


class AutonomousDevelopmentEngine:
    """Builds deterministic, policy-bounded development cycles over KGO/KPM.

    The engine selects and starts dependency-valid work, creates the executable
    development plan and records checkpoints. Source-code generation and GitHub
    merge operations remain external authorized capabilities.
    """

    def __init__(
        self,
        *,
        orchestrator: KyvernexGovernanceOrchestrator,
        policy: DevelopmentPolicy | None = None,
        artifact_directory: str | Path = "artifacts",
    ) -> None:
        self.orchestrator = orchestrator
        self.policy = policy or DevelopmentPolicy()
        self.artifact_directory = Path(artifact_directory)

    def plan_next_cycle(self, *, milestone_id: str | None = None) -> AutonomousCyclePlan:
        checkpoint = self._start_or_advance(milestone_id=milestone_id)
        if checkpoint.state in {GovernanceState.RELEASE_COMPLETE, GovernanceState.MILESTONE_COMPLETE}:
            plan = AutonomousCyclePlan(
                schema="kyvernex.autonomous-development.v1",
                cycle_id=f"ADE-CYCLE-{checkpoint.cycle:04d}",
                milestone_id=checkpoint.current_milestone_id,
                item_id=None,
                item_title=None,
                priority=None,
                story_points=None,
                state=checkpoint.state.value,
                steps=(DevelopmentStep(1, DevelopmentAction.COMPLETE, "No eligible work remains in the governed scope."),),
                stop_reason=None,
            )
            self.write_artifacts(plan, checkpoint)
            return plan

        if checkpoint.current_item_id is None:
            raise AutonomousDevelopmentError("TASK_AUTONOMO_NON_SELEZIONATO")

        item = self.orchestrator.manager.items[checkpoint.current_item_id]
        stop_reason = self._policy_stop_reason(item)
        steps = self._build_steps(item, stop_reason=stop_reason)
        plan = AutonomousCyclePlan(
            schema="kyvernex.autonomous-development.v1",
            cycle_id=f"ADE-CYCLE-{checkpoint.cycle:04d}",
            milestone_id=item.milestone_id,
            item_id=item.item_id,
            item_title=item.title,
            priority=item.priority.value,
            story_points=item.story_points,
            state=(GovernanceState.BLOCKED.value if stop_reason else checkpoint.state.value),
            steps=steps,
            stop_reason=stop_reason,
        )
        self.write_artifacts(plan, checkpoint)
        return plan

    def _start_or_advance(self, *, milestone_id: str | None) -> GovernanceCheckpoint:
        if self.orchestrator.state == GovernanceState.READY:
            return self.orchestrator.start_autonomous(milestone_id=milestone_id)
        if self.orchestrator.current_item_id is not None:
            return self.orchestrator.checkpoint()
        return self.orchestrator.advance()

    def _policy_stop_reason(self, item: WorkItem) -> str | None:
        if item.priority not in self.policy.allowed_priorities:
            return "PRIORITY_OUTSIDE_AUTONOMOUS_POLICY"
        if item.story_points > self.policy.max_story_points_per_cycle:
            return "STORY_POINT_LIMIT_EXCEEDED"
        return None

    def _build_steps(self, item: WorkItem, *, stop_reason: str | None) -> tuple[DevelopmentStep, ...]:
        steps: list[DevelopmentStep] = [
            DevelopmentStep(1, DevelopmentAction.SELECT_TASK, f"Selected {item.item_id}: {item.title}."),
        ]
        if stop_reason:
            steps.append(DevelopmentStep(2, DevelopmentAction.STOP_FOR_AUTHORIZATION, stop_reason, requires_authorization=True))
            return tuple(steps)

        order = 2
        if self.policy.require_specification:
            steps.append(DevelopmentStep(order, DevelopmentAction.PREPARE_SPECIFICATION, "Create or update the technical specification and dependency records."))
            order += 1
        steps.append(
            DevelopmentStep(
                order,
                DevelopmentAction.IMPLEMENT,
                "Implement the smallest coherent change on an isolated development boundary.",
                requires_authorization=not self.policy.allow_direct_main_write,
            )
        )
        order += 1
        if self.policy.require_targeted_tests:
            steps.append(DevelopmentStep(order, DevelopmentAction.RUN_TARGETED_TESTS, "Run tests covering the selected work item.", ("python", "-m", "pytest", "-q", "-k", item.item_id)))
            order += 1
        if self.policy.require_complete_tests:
            steps.append(DevelopmentStep(order, DevelopmentAction.RUN_COMPLETE_TESTS, "Run the complete verification suite.", ("python", "-m", "pytest", "-q")))
            order += 1
        steps.append(DevelopmentStep(order, DevelopmentAction.RECORD_CHECKPOINT, "Persist evidence and advance only after the Definition of Done is complete."))
        if not self.policy.allow_automatic_merge:
            steps.append(DevelopmentStep(order + 1, DevelopmentAction.STOP_FOR_AUTHORIZATION, "Merge requires explicit authorization.", requires_authorization=True))
        return tuple(steps)

    def write_artifacts(self, plan: AutonomousCyclePlan, checkpoint: GovernanceCheckpoint) -> None:
        self.artifact_directory.mkdir(parents=True, exist_ok=True)
        (self.artifact_directory / "ADE_CYCLE_PLAN.json").write_text(
            json.dumps(asdict(plan), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (self.artifact_directory / "ADE_CHECKPOINT.json").write_text(
            json.dumps(asdict(checkpoint), indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf-8",
        )


def build_m3_backlog() -> tuple[WorkItem, ...]:
    """Canonical initial backlog for M3 autonomous development."""

    clock_priority = execution_clock_assessment().priority()
    return (
        WorkItem("M3-W001", "Autonomous task scheduler", "M3", Priority.P0, 3, WorkStatus.READY),
        WorkItem("M3-W002", "Specification-to-change manifest", "M3", Priority.P0, 5, dependencies=("M3-W001",)),
        WorkItem("M3-W003", "Continuous self-verification controller", "M3", Priority.P0, 5, dependencies=("M3-W002",)),
        WorkItem("M3-W004", "Safe isolated commit manager", "M3", Priority.P1, 8, dependencies=("M3-W003",)),
        WorkItem("M3-W005", "Evidence-based rollback controller", "M3", Priority.P1, 8, dependencies=("M3-W004",)),
        WorkItem(
            "M3-W006",
            "Execution performance clock and improvement metrics",
            "M3",
            clock_priority,
            5,
            dependencies=("M3-W003",),
        ),
    )
