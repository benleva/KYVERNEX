import pytest

from kyvernex.program_manager import (
    DefinitionOfDone,
    KPMError,
    KyvernexProgramManager,
    Milestone,
    Priority,
    WorkItem,
    WorkStatus,
)


def complete_dod() -> DefinitionOfDone:
    return DefinitionOfDone(
        specification=True,
        implementation=True,
        unit_tests=True,
        integration_tests=True,
        ci_passed=True,
        documentation=True,
        readme=True,
        changelog=True,
        audit_review=True,
        review=True,
    )


def test_next_item_respects_priority_and_dependencies() -> None:
    first = WorkItem("T1", "Base", "M1", Priority.P1, 3, done=complete_dod())
    second = WorkItem("T2", "Dependent", "M1", Priority.P0, 2, dependencies=("T1",))
    manager = KyvernexProgramManager(
        milestones=[Milestone("M1", "Core", "1.0")],
        items=[first, second],
    )
    assert manager.next_item().item_id == "T1"
    manager.close_item("T1")
    assert manager.next_item().item_id == "T2"


def test_item_cannot_close_without_definition_of_done() -> None:
    manager = KyvernexProgramManager(
        milestones=[Milestone("M1", "Core", "1.0")],
        items=[WorkItem("T1", "Base", "M1", Priority.P1, 3)],
    )
    with pytest.raises(KPMError, match="DEFINITION_OF_DONE_INCOMPLETA"):
        manager.close_item("T1")


def test_closed_milestone_rejects_scope_growth() -> None:
    milestone = Milestone("M1", "Core", "1.0")
    item = WorkItem("T1", "Base", "M1", Priority.P1, 3, done=complete_dod())
    manager = KyvernexProgramManager(milestones=[milestone], items=[item])
    manager.close_item("T1")
    manager.close_milestone("M1")
    with pytest.raises(KPMError, match="REGOLA_ANTIINFINITO"):
        manager.add_item(WorkItem("T2", "Late scope", "M1", Priority.P1, 2))


def test_report_exposes_progress_and_remaining_work() -> None:
    done = WorkItem("T1", "Done", "M1", Priority.P1, 3, status=WorkStatus.DONE, done=complete_dod())
    pending = WorkItem("T2", "Pending", "M1", Priority.P2, 5)
    manager = KyvernexProgramManager(
        milestones=[Milestone("M1", "Core", "1.0")],
        items=[done, pending],
    )
    report = manager.report(milestone_id="M1")
    assert report.completion_percent == 50.0
    assert report.completed_story_points == 3
    assert report.remaining_story_points == 5
    assert report.next_item_id == "T2"
