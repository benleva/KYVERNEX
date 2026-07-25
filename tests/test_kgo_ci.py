from __future__ import annotations

import json

from kyvernex.kgo_ci import parse_pytest_output, write_artifacts


def test_parse_pytest_output_prioritizes_runtime_defects() -> None:
    output = """
FAILED tests/test_rule_engine.py::test_contract - AssertionError: assert 6 == 5
FAILED tests/test_delete.py::test_delete - TypeError: unhashable type: 'dict'
10 failed, 84 passed in 0.45s
"""
    analysis = parse_pytest_output(output)

    assert analysis.state == "BLOCKED"
    assert analysis.summary.passed == 84
    assert analysis.summary.failed == 10
    assert analysis.summary.success_percent == 89.36
    assert analysis.next_task is not None
    assert analysis.next_task.priority == "P0"
    assert analysis.next_task.category == "RUNTIME_DEFECT"


def test_parse_verified_suite() -> None:
    analysis = parse_pytest_output("94 passed in 0.45s")

    assert analysis.state == "VERIFIED"
    assert analysis.summary.failed == 0
    assert analysis.next_task is None


def test_write_artifacts_creates_checkpoint_backlog_and_summary(tmp_path) -> None:
    analysis = parse_pytest_output(
        "FAILED tests/test_delete.py::test_delete - TypeError: unhashable type: 'dict'\n"
        "1 failed, 3 passed in 0.10s\n"
    )

    write_artifacts(analysis, tmp_path)

    checkpoint = json.loads((tmp_path / "KGO_CHECKPOINT.json").read_text(encoding="utf-8"))
    backlog = json.loads((tmp_path / "KGO_BACKLOG.json").read_text(encoding="utf-8"))
    summary = (tmp_path / "KGO_SUMMARY.md").read_text(encoding="utf-8")

    assert checkpoint["state"] == "BLOCKED"
    assert checkpoint["current_priority"] == "P0"
    assert backlog["failures"][0]["category"] == "RUNTIME_DEFECT"
    assert "Next governed task" in summary
