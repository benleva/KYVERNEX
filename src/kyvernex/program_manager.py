from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, fields
from enum import StrEnum
from pathlib import Path
from typing import Iterable


class KPMError(RuntimeError):
    """Raised when the development governance state is invalid."""


class KGOError(RuntimeError):
    """Raised when autonomous governance orchestration cannot continue."""


class WorkStatus(StrEnum):
    BACKLOG = "BACKLOG"
    READY = "READY"
    IN_DEVELOPMENT = "IN_DEVELOPMENT"
    TEST = "TEST"
    REVIEW = "REVIEW"
    DONE = "DONE"
    BLOCKED = "BLOCKED"


class Priority(StrEnum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class GovernanceMode(StrEnum):
    MANUAL = "MANUAL"
    AUTONOMOUS = "AUTONOMOUS"


class GovernanceState(StrEnum):
    READY = "READY"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    BLOCKED = "BLOCKED"
    MILESTONE_COMPLETE = "MILESTONE_COMPLETE"
    RELEASE_COMPLETE = "RELEASE_COMPLETE"


@dataclass(slots=True, frozen=True)
class DefinitionOfDone:
    specification: bool = False
    implementation: bool = False
    unit_tests: bool = False
    integration_tests: bool = False
    ci_passed: bool = False
    documentation: bool = False
    readme: bool = False
    changelog: bool = False
    audit_review: bool = False
    review: bool = False

    def missing(self) -> tuple[str, ...]:
        return tuple(item.name for item in fields(self) if not getattr(self, item.name))

    @property
    def complete(self) -> bool:
        return not self.missing()


@dataclass(slots=True)
class WorkItem:
    item_id: str
    title: str
    milestone_id: str
    priority: Priority
    story_points: int
    status: WorkStatus = WorkStatus.BACKLOG
    dependencies: tuple[str, ...] = ()
    done: DefinitionOfDone = field(default_factory=DefinitionOfDone)

    def __post_init__(self) -> None:
        if not self.item_id.strip() or not self.title.strip() or not self.milestone_id.strip():
            raise ValueError("DATI_TASK_MANCANTI")
        if self.story_points <= 0:
            raise ValueError("STORY_POINT_NON_VALIDI")


@dataclass(slots=True)
class Milestone:
    milestone_id: str
    title: str
    target_version: str
    closed: bool = False


@dataclass(slots=True, frozen=True)
class KPMReport:
    total_items: int
    completed_items: int
    completion_percent: float
    completed_story_points: int
    remaining_story_points: int
    blocked_items: tuple[str, ...]
    next_item_id: str | None


@dataclass(slots=True, frozen=True)
class GovernanceCheckpoint:
    mode: GovernanceMode
    state: GovernanceState
    target_version: str
    current_milestone_id: str | None
    current_item_id: str | None
    completed_milestones: tuple[str, ...]
    completed_items: tuple[str, ...]
    blocked_items: tuple[str, ...]
    completion_percent: float
    cycle: int
    last_verified_commit: str | None = None
    last_verified_test: str | None = None
    last_verified_ci: str | None = None


class KyvernexProgramManager:
    """Deterministic development governor implementing the KDP anti-infinite rule."""

    def __init__(self, *, milestones: Iterable[Milestone], items: Iterable[WorkItem]) -> None:
        milestone_list = tuple(milestones)
        item_list = tuple(items)
        self.milestones = {m.milestone_id: m for m in milestone_list}
        self.items = {item.item_id: item for item in item_list}
        if len(self.milestones) != len(milestone_list):
            raise KPMError("MILESTONE_DUPLICATE")
        if len(self.items) != len(item_list):
            raise KPMError("TASK_DUPLICATI")
        self._validate_references()

    def _validate_references(self) -> None:
        for item in self.items.values():
            if item.milestone_id not in self.milestones:
                raise KPMError("MILESTONE_TASK_NON_TROVATA")
            unknown = [dep for dep in item.dependencies if dep not in self.items]
            if unknown:
                raise KPMError("DIPENDENZA_NON_TROVATA")

    def add_item(self, item: WorkItem) -> None:
        milestone = self.milestones.get(item.milestone_id)
        if milestone is None:
            raise KPMError("MILESTONE_NON_TROVATA")
        if milestone.closed:
            raise KPMError("REGOLA_ANTIINFINITO_MILESTONE_CHIUSA")
        if item.item_id in self.items:
            raise KPMError("TASK_GIA_ESISTENTE")
        self.items[item.item_id] = item
        try:
            self._validate_references()
        except Exception:
            del self.items[item.item_id]
            raise

    def dependencies_complete(self, item: WorkItem) -> bool:
        return all(self.items[dep].status == WorkStatus.DONE for dep in item.dependencies)

    def next_item(self, *, milestone_id: str | None = None) -> WorkItem | None:
        candidates = [
            item for item in self.items.values()
            if item.status in {WorkStatus.BACKLOG, WorkStatus.READY}
            and (milestone_id is None or item.milestone_id == milestone_id)
            and self.dependencies_complete(item)
            and not self.milestones[item.milestone_id].closed
        ]
        if not candidates:
            return None
        rank = {Priority.P0: 0, Priority.P1: 1, Priority.P2: 2, Priority.P3: 3, Priority.P4: 4}
        return sorted(candidates, key=lambda x: (rank[x.priority], x.story_points, x.item_id))[0]

    def start(self, item_id: str) -> WorkItem:
        item = self._get(item_id)
        if not self.dependencies_complete(item):
            raise KPMError("DIPENDENZE_NON_COMPLETE")
        if self.milestones[item.milestone_id].closed:
            raise KPMError("MILESTONE_CHIUSA")
        if item.status not in {WorkStatus.BACKLOG, WorkStatus.READY}:
            raise KPMError("TASK_NON_AVVIABILE")
        item.status = WorkStatus.IN_DEVELOPMENT
        return item

    def review(self, item_id: str) -> tuple[str, ...]:
        return self._get(item_id).done.missing()

    def close_item(self, item_id: str) -> WorkItem:
        item = self._get(item_id)
        missing = item.done.missing()
        if missing:
            raise KPMError("DEFINITION_OF_DONE_INCOMPLETA:" + ",".join(missing))
        item.status = WorkStatus.DONE
        return item

    def close_milestone(self, milestone_id: str) -> Milestone:
        milestone = self.milestones.get(milestone_id)
        if milestone is None:
            raise KPMError("MILESTONE_NON_TROVATA")
        related = [item for item in self.items.values() if item.milestone_id == milestone_id]
        if not related or any(item.status != WorkStatus.DONE for item in related):
            raise KPMError("MILESTONE_NON_COMPLETA")
        milestone.closed = True
        return milestone

    def report(self, *, milestone_id: str | None = None) -> KPMReport:
        selected = [
            item for item in self.items.values()
            if milestone_id is None or item.milestone_id == milestone_id
        ]
        total = len(selected)
        completed = sum(item.status == WorkStatus.DONE for item in selected)
        completed_points = sum(item.story_points for item in selected if item.status == WorkStatus.DONE)
        remaining_points = sum(item.story_points for item in selected if item.status != WorkStatus.DONE)
        blocked = tuple(item.item_id for item in selected if item.status == WorkStatus.BLOCKED)
        next_item = self.next_item(milestone_id=milestone_id)
        return KPMReport(
            total_items=total,
            completed_items=completed,
            completion_percent=round((completed / total * 100.0) if total else 0.0, 2),
            completed_story_points=completed_points,
            remaining_story_points=remaining_points,
            blocked_items=blocked,
            next_item_id=next_item.item_id if next_item else None,
        )

    def _get(self, item_id: str) -> WorkItem:
        try:
            return self.items[item_id]
        except KeyError as exc:
            raise KPMError("TASK_NON_TROVATO") from exc


class KyvernexGovernanceOrchestrator:
    """Autonomous coordinator layered over KPM and contained in the same module."""

    def __init__(
        self,
        *,
        manager: KyvernexProgramManager,
        target_version: str = "1.0",
        checkpoint_path: str | Path | None = None,
    ) -> None:
        self.manager = manager
        self.target_version = target_version
        self.checkpoint_path = Path(checkpoint_path) if checkpoint_path is not None else None
        self.mode = GovernanceMode.MANUAL
        self.state = GovernanceState.READY
        self.current_milestone_id: str | None = None
        self.current_item_id: str | None = None
        self.cycle = 0
        self.last_verified_commit: str | None = None
        self.last_verified_test: str | None = None
        self.last_verified_ci: str | None = None

    def start_autonomous(self, *, milestone_id: str | None = None) -> GovernanceCheckpoint:
        self.mode = GovernanceMode.AUTONOMOUS
        self.state = GovernanceState.RUNNING
        self.current_milestone_id = milestone_id or self._next_open_milestone_id()
        if self.current_milestone_id is None:
            self.state = GovernanceState.RELEASE_COMPLETE
            return self.save_checkpoint()
        return self.advance()

    def advance(self) -> GovernanceCheckpoint:
        if self.mode != GovernanceMode.AUTONOMOUS:
            raise KGOError("MODALITA_AUTONOMA_NON_ATTIVA")
        if self.state in {GovernanceState.RELEASE_COMPLETE, GovernanceState.MILESTONE_COMPLETE}:
            return self.save_checkpoint()
        self.cycle += 1
        milestone_id = self.current_milestone_id or self._next_open_milestone_id()
        self.current_milestone_id = milestone_id
        if milestone_id is None:
            self.current_item_id = None
            self.state = GovernanceState.RELEASE_COMPLETE
            return self.save_checkpoint()
        next_item = self.manager.next_item(milestone_id=milestone_id)
        if next_item is not None:
            self.manager.start(next_item.item_id)
            self.current_item_id = next_item.item_id
            self.state = GovernanceState.RUNNING
            return self.save_checkpoint()
        unfinished = [
            item for item in self.manager.items.values()
            if item.milestone_id == milestone_id and item.status != WorkStatus.DONE
        ]
        if unfinished:
            self.current_item_id = unfinished[0].item_id
            self.state = GovernanceState.BLOCKED
            return self.save_checkpoint()
        self.manager.close_milestone(milestone_id)
        self.current_item_id = None
        self.state = GovernanceState.MILESTONE_COMPLETE
        return self.save_checkpoint()

    def complete_current_item(self, done: DefinitionOfDone) -> GovernanceCheckpoint:
        if self.current_item_id is None:
            raise KGOError("NESSUN_TASK_CORRENTE")
        item = self.manager._get(self.current_item_id)
        item.done = done
        self.manager.close_item(item.item_id)
        self.current_item_id = None
        self.state = GovernanceState.RUNNING
        return self.advance()

    def resume(self) -> GovernanceCheckpoint:
        if self.checkpoint_path is None or not self.checkpoint_path.exists():
            raise KGOError("CHECKPOINT_NON_TROVATO")
        data = json.loads(self.checkpoint_path.read_text(encoding="utf-8"))
        self.mode = GovernanceMode(data["mode"])
        self.state = GovernanceState(data["state"])
        self.target_version = data["target_version"]
        self.current_milestone_id = data.get("current_milestone_id")
        self.current_item_id = data.get("current_item_id")
        self.cycle = int(data["cycle"])
        self.last_verified_commit = data.get("last_verified_commit")
        self.last_verified_test = data.get("last_verified_test")
        self.last_verified_ci = data.get("last_verified_ci")
        return self.checkpoint()

    def checkpoint(self) -> GovernanceCheckpoint:
        report = self.manager.report()
        return GovernanceCheckpoint(
            mode=self.mode,
            state=self.state,
            target_version=self.target_version,
            current_milestone_id=self.current_milestone_id,
            current_item_id=self.current_item_id,
            completed_milestones=tuple(sorted(m.milestone_id for m in self.manager.milestones.values() if m.closed)),
            completed_items=tuple(sorted(i.item_id for i in self.manager.items.values() if i.status == WorkStatus.DONE)),
            blocked_items=report.blocked_items,
            completion_percent=report.completion_percent,
            cycle=self.cycle,
            last_verified_commit=self.last_verified_commit,
            last_verified_test=self.last_verified_test,
            last_verified_ci=self.last_verified_ci,
        )

    def save_checkpoint(self) -> GovernanceCheckpoint:
        checkpoint = self.checkpoint()
        if self.checkpoint_path is not None:
            self.checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            payload = asdict(checkpoint)
            payload["mode"] = checkpoint.mode.value
            payload["state"] = checkpoint.state.value
            self.checkpoint_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
                encoding="utf-8",
            )
        return checkpoint

    def _next_open_milestone_id(self) -> str | None:
        candidates = [
            milestone for milestone in self.manager.milestones.values()
            if not milestone.closed and milestone.target_version <= self.target_version
        ]
        if not candidates:
            return None
        return sorted(candidates, key=lambda item: item.milestone_id)[0].milestone_id
