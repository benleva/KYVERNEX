from __future__ import annotations

import json
from pathlib import Path

from kyvernex.governance_cli import EXIT_BLOCKED, EXIT_INVALID, EXIT_NOT_PERMITTED, main


def write_plan(path: Path, *, closed: bool = False, unknown_dependency: bool = False) -> None:
    done = {
        "specification": True,
        "implementation": True,
        "unit_tests": True,
        "integration_tests": True,
        "ci_passed": True,
        "documentation": True,
        "readme": True,
        "changelog": True,
        "audit_review": True,
        "review": True,
    }
    path.write_text(
        json.dumps(
            {
                "target_version": "1.1.0",
                "milestones": [
                    {
                        "milestone_id": "M4",
                        "title": "Governed evolution",
                        "target_version": "1.1.0",
                        "closed": closed,
                    }
                ],
                "items": [
                    {
                        "item_id": "M4-W001",
                        "title": "Foundation",
                        "milestone_id": "M4",
                        "priority": "P1",
                        "story_points": 3,
                        "status": "DONE",
                        "dependencies": [],
                        "done": done,
                    },
                    {
                        "item_id": "M4-W002",
                        "title": "Highest priority ready task",
                        "milestone_id": "M4",
                        "priority": "P0",
                        "story_points": 5,
                        "status": "READY",
                        "dependencies": ["UNKNOWN" if unknown_dependency else "M4-W001"],
                        "done": {},
                    },
                    {
                        "item_id": "M4-W003",
                        "title": "Lower priority task",
                        "milestone_id": "M4",
                        "priority": "P2",
                        "story_points": 1,
                        "status": "BACKLOG",
                        "dependencies": [],
                        "done": {},
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def test_start_selects_highest_priority_dependency_valid_item(tmp_path: Path, capsys) -> None:
    plan = tmp_path / "plan.json"
    checkpoint = tmp_path / "checkpoint.json"
    write_plan(plan)

    assert main(["start", "--plan", str(plan), "--checkpoint", str(checkpoint)]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["current_item_id"] == "M4-W002"
    assert output["state"] == "RUNNING"
    assert checkpoint.exists()


def test_status_does_not_mutate_checkpoint(tmp_path: Path, capsys) -> None:
    plan = tmp_path / "plan.json"
    checkpoint = tmp_path / "checkpoint.json"
    write_plan(plan)
    assert main(["start", "--plan", str(plan), "--checkpoint", str(checkpoint)]) == 0
    capsys.readouterr()
    before = checkpoint.read_bytes()

    assert main(["status", "--plan", str(plan), "--checkpoint", str(checkpoint)]) == 0
    capsys.readouterr()
    assert checkpoint.read_bytes() == before


def test_malformed_plan_fails_closed(tmp_path: Path, capsys) -> None:
    plan = tmp_path / "plan.json"
    checkpoint = tmp_path / "checkpoint.json"
    plan.write_text("{not-json", encoding="utf-8")

    assert main(["start", "--plan", str(plan), "--checkpoint", str(checkpoint)]) == EXIT_INVALID
    assert "PLAN_JSON_NON_VALIDO" in capsys.readouterr().err
    assert not checkpoint.exists()


def test_unknown_dependency_fails_closed(tmp_path: Path, capsys) -> None:
    plan = tmp_path / "plan.json"
    checkpoint = tmp_path / "checkpoint.json"
    write_plan(plan, unknown_dependency=True)

    assert main(["start", "--plan", str(plan), "--checkpoint", str(checkpoint)]) == EXIT_INVALID
    assert "DIPENDENZA_NON_TROVATA" in capsys.readouterr().err


def test_closed_milestone_rejects_incomplete_work(tmp_path: Path, capsys) -> None:
    plan = tmp_path / "plan.json"
    checkpoint = tmp_path / "checkpoint.json"
    write_plan(plan, closed=True)

    assert main(["start", "--plan", str(plan), "--checkpoint", str(checkpoint)]) == EXIT_INVALID
    assert "MILESTONE_CHIUSA_CON_LAVORO_INCOMPLETO" in capsys.readouterr().err


def test_blocked_state_returns_exit_code_two(tmp_path: Path, capsys) -> None:
    plan = tmp_path / "plan.json"
    checkpoint = tmp_path / "checkpoint.json"
    write_plan(plan)
    checkpoint.write_text(
        json.dumps(
            {
                "mode": "AUTONOMOUS",
                "state": "BLOCKED",
                "target_version": "1.1.0",
                "current_milestone_id": "M4",
                "current_item_id": "M4-W002",
                "completed_milestones": [],
                "completed_items": ["M4-W001"],
                "blocked_items": ["M4-W002"],
                "completion_percent": 33.33,
                "cycle": 2,
                "last_verified_commit": None,
                "last_verified_test": None,
                "last_verified_ci": None,
            }
        ),
        encoding="utf-8",
    )

    assert main(["resume", "--plan", str(plan), "--checkpoint", str(checkpoint)]) == EXIT_BLOCKED
    assert json.loads(capsys.readouterr().out)["state"] == "BLOCKED"


def test_output_contains_no_unsupported_execution_claim(tmp_path: Path, capsys) -> None:
    plan = tmp_path / "plan.json"
    checkpoint = tmp_path / "checkpoint.json"
    write_plan(plan)

    assert main(["start", "--plan", str(plan), "--checkpoint", str(checkpoint)]) == 0
    output = json.loads(capsys.readouterr().out)
    forbidden = {"repository_written", "tests_passed", "ci_passed", "release_published"}
    assert forbidden.isdisjoint(output)


def test_advance_rejects_active_item(tmp_path: Path, capsys) -> None:
    plan = tmp_path / "plan.json"
    checkpoint = tmp_path / "checkpoint.json"
    write_plan(plan)
    assert main(["start", "--plan", str(plan), "--checkpoint", str(checkpoint)]) == 0
    capsys.readouterr()

    assert main(["advance", "--plan", str(plan), "--checkpoint", str(checkpoint)]) == EXIT_NOT_PERMITTED
    assert "TASK_CORRENTE_ANCORA_ATTIVO" in capsys.readouterr().err


def test_start_rejects_existing_checkpoint(tmp_path: Path, capsys) -> None:
    plan = tmp_path / "plan.json"
    checkpoint = tmp_path / "checkpoint.json"
    write_plan(plan)
    checkpoint.write_text("{}", encoding="utf-8")

    assert main(["start", "--plan", str(plan), "--checkpoint", str(checkpoint)]) == EXIT_NOT_PERMITTED
    assert "CHECKPOINT_GIA_ESISTENTE" in capsys.readouterr().err
