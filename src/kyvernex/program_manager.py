from __future__ import annotations

from dataclasses import dataclass, field, fields
from enum import StrEnum
from typing import Iterable


class KPMError(RuntimeError):
    """Raised when the development governance state is invalid."""


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
