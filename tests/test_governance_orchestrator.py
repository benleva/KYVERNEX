from kyvernex.program_manager import (
    DefinitionOfDone,
    GovernanceMode,
    GovernanceState,
    KyvernexGovernanceOrchestrator,
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


def test_kgo_starts_next_dependency_valid_item(tmp_path):
    manager = KyvernexProgramManager(
        milestones=[Milestone("M1", "Core", "1.0")],
        items=[
            WorkItem("T1", "First", "M1", Priority.P1, 2),
            WorkItem("T2", "Second", "M1", Priority.P1, 3, dependencies=("T1",)),
        ],
    )
    kgo = KyvernexGovernanceOrchestrator(
        manager=manager,
        checkpoint_path=tmp_path / "checkpoint.json",
    )

    checkpoint = kgo.start_autonomous()

    assert checkpoint.mode == GovernanceMode.AUTONOMOUS
    assert checkpoint.state == GovernanceState.RUNNING
    assert checkpoint.current_item_id == "T1"
    assert manager.items["T1"].status == WorkStatus.IN_DEVELOPMENT


def test_kgo_completes_item_and_advances(tmp_path):
    manager = KyvernexProgramManager(
        milestones=[Milestone("M1", "Core", "1.0")],
        items=[
            WorkItem("T1", "First", "M1", Priority.P1, 2),
            WorkItem("T2", "Second", "M1", Priority.P1, 3, dependencies=("T1",)),
        ],
    )
    kgo = KyvernexGovernanceOrchestrator(
        manager=manager,
        checkpoint_path=tmp_path / "checkpoint.json",
    )
    kgo.start_autonomous()

    checkpoint = kgo.complete_current_item(complete_dod())

    assert manager.items["T1"].status == WorkStatus.DONE
    assert checkpoint.current_item_id == "T2"
    assert manager.items["T2"].status == WorkStatus.IN_DEVELOPMENT


def test_kgo_closes_completed_milestone(tmp_path):
    item = WorkItem("T1", "Only", "M1", Priority.P1, 2, status=WorkStatus.IN_DEVELOPMENT)
    manager = KyvernexProgramManager(
        milestones=[Milestone("M1", "Core", "1.0")],
        items=[item],
    )
    kgo = KyvernexGovernanceOrchestrator(
        manager=manager,
        checkpoint_path=tmp_path / "checkpoint.json",
    )
    kgo.mode = GovernanceMode.AUTONOMOUS
    kgo.state = GovernanceState.RUNNING
    kgo.current_milestone_id = "M1"
    kgo.current_item_id = "T1"

    checkpoint = kgo.complete_current_item(complete_dod())

    assert checkpoint.state == GovernanceState.MILESTONE_COMPLETE
    assert manager.milestones["M1"].closed is True


def test_checkpoint_can_be_resumed(tmp_path):
    path = tmp_path / "checkpoint.json"
    manager = KyvernexProgramManager(
        milestones=[Milestone("M1", "Core", "1.0")],
        items=[WorkItem("T1", "Only", "M1", Priority.P1, 2)],
    )
    first = KyvernexGovernanceOrchestrator(manager=manager, checkpoint_path=path)
    original = first.start_autonomous()

    second = KyvernexGovernanceOrchestrator(manager=manager, checkpoint_path=path)
    restored = second.resume()

    assert restored.mode == original.mode
    assert restored.state == original.state
    assert restored.current_item_id == original.current_item_id
    assert restored.cycle == original.cycle
