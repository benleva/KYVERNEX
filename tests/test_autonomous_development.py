import json

from kyvernex.autonomous_development import (
    AutonomousDevelopmentEngine,
    DevelopmentAction,
    DevelopmentPolicy,
    build_m3_backlog,
)
from kyvernex.program_manager import (
    KyvernexGovernanceOrchestrator,
    KyvernexProgramManager,
    Milestone,
    Priority,
)


def make_engine(tmp_path, *, policy=None):
    manager = KyvernexProgramManager(
        milestones=(Milestone("M3", "Autonomous Development", "0.2.0"),),
        items=build_m3_backlog(),
    )
    orchestrator = KyvernexGovernanceOrchestrator(
        manager=manager,
        target_version="0.2.0",
        checkpoint_path=tmp_path / "kgo-checkpoint.json",
    )
    return AutonomousDevelopmentEngine(
        orchestrator=orchestrator,
        policy=policy,
        artifact_directory=tmp_path / "artifacts",
    )


def test_selects_first_dependency_valid_m3_item(tmp_path):
    engine = make_engine(tmp_path)

    plan = engine.plan_next_cycle(milestone_id="M3")

    assert plan.item_id == "M3-W001"
    assert plan.priority == "P0"
    assert plan.state == "RUNNING"
    assert plan.steps[0].action == DevelopmentAction.SELECT_TASK
    assert any(step.action == DevelopmentAction.RUN_COMPLETE_TESTS for step in plan.steps)


def test_default_policy_requires_authorization_for_implementation_and_merge(tmp_path):
    engine = make_engine(tmp_path)

    plan = engine.plan_next_cycle(milestone_id="M3")

    implementation = next(step for step in plan.steps if step.action == DevelopmentAction.IMPLEMENT)
    merge_stop = plan.steps[-1]
    assert implementation.requires_authorization is True
    assert merge_stop.action == DevelopmentAction.STOP_FOR_AUTHORIZATION
    assert merge_stop.requires_authorization is True


def test_policy_blocks_item_above_cycle_story_point_limit(tmp_path):
    policy = DevelopmentPolicy(
        allowed_priorities=frozenset({Priority.P0, Priority.P1}),
        max_story_points_per_cycle=2,
    )
    engine = make_engine(tmp_path, policy=policy)

    plan = engine.plan_next_cycle(milestone_id="M3")

    assert plan.state == "BLOCKED"
    assert plan.stop_reason == "STORY_POINT_LIMIT_EXCEEDED"
    assert plan.steps[-1].action == DevelopmentAction.STOP_FOR_AUTHORIZATION


def test_writes_machine_readable_plan_and_checkpoint(tmp_path):
    engine = make_engine(tmp_path)

    plan = engine.plan_next_cycle(milestone_id="M3")

    plan_payload = json.loads((tmp_path / "artifacts" / "ADE_CYCLE_PLAN.json").read_text())
    checkpoint_payload = json.loads((tmp_path / "artifacts" / "ADE_CHECKPOINT.json").read_text())
    assert plan_payload["item_id"] == plan.item_id
    assert checkpoint_payload["current_item_id"] == "M3-W001"
