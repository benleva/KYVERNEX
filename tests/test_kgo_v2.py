from kyvernex.kgo_ci import parse_pytest_output
from kyvernex.kgo_v2 import build_v2_report


def test_groups_shared_unhashable_dict_failures_into_one_root_cause() -> None:
    output = """
FAILED tests/test_a.py::test_one - TypeError: unhashable type: 'dict'
FAILED tests/test_b.py::test_two - TypeError: unhashable type: 'dict'
2 failed, 8 passed in 0.10s
"""
    report = build_v2_report(parse_pytest_output(output))
    assert len(report.root_causes) == 1
    cause = report.root_causes[0]
    assert cause.signature == "UNHASHABLE_DICT"
    assert cause.expected_failures_removed == 2
    assert cause.projected_success_percent == 100.0
    assert cause.confidence >= 0.9


def test_prioritizes_runtime_root_cause_over_contract_mismatch() -> None:
    output = """
FAILED tests/test_contract.py::test_schema - AssertionError: assert 6 == 5
FAILED tests/test_runtime.py::test_delete - TypeError: unhashable type: 'dict'
2 failed, 8 passed in 0.10s
"""
    report = build_v2_report(parse_pytest_output(output))
    assert report.root_causes[0].priority == "P0"
    assert report.root_causes[0].signature == "UNHASHABLE_DICT"
    assert report.next_cause_id == report.root_causes[0].cause_id


def test_patch_plan_never_authorizes_low_confidence_contract_change() -> None:
    output = """
FAILED tests/test_contract.py::test_schema - AssertionError: assert 6 == 5
1 failed, 9 passed in 0.10s
"""
    report = build_v2_report(parse_pytest_output(output))
    assert report.patch_plans[0].autonomous_patch_allowed is False
    assert "review" in report.patch_plans[0].approval_reason.lower()
