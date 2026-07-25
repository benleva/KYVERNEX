from kyvernex.kgo_v3 import KGOState, KGOV3Loop, LoopDecision


def test_successful_current_run_continues_even_with_zero_parsed_counts():
    result = KGOV3Loop().evaluate(
        previous=KGOState(),
        pytest_output="100 passed in 0.50s\n",
        test_outcome="success",
        commit="abc123",
        current_work_item="M3-W003",
    )

    assert result.state.decision == LoopDecision.CONTINUE.value
    assert result.state.reason == "CURRENT_CI_SUCCESS"
    assert result.state.last_verified_commit == "abc123"
    assert result.state.last_failed_commit is None
    assert result.historical_failures_ignored is True


def test_current_failure_evidence_selects_repair():
    output = "FAILED tests/test_x.py::test_x - AssertionError: assert 1 == 2\n1 failed, 9 passed in 0.10s\n"
    result = KGOV3Loop().evaluate(
        previous=KGOState(last_verified_commit="good"),
        pytest_output=output,
        test_outcome="failure",
        commit="bad",
    )

    assert result.state.decision == LoopDecision.REPAIR.value
    assert result.state.reason == "CURRENT_FAILURE_EVIDENCE"
    assert result.state.last_verified_commit == "good"
    assert result.state.last_failed_commit == "bad"
    assert result.state.failed_tests == 1


def test_unsuccessful_run_without_code_failure_does_not_invent_blocker():
    result = KGOV3Loop().evaluate(
        previous=KGOState(last_verified_commit="good"),
        pytest_output="platform runner unavailable\n",
        test_outcome="cancelled",
        commit="candidate",
    )

    assert result.state.decision == LoopDecision.CONTINUE.value
    assert result.state.reason == "NO_SUPPORTED_CODE_FAILURE"
    assert result.state.last_verified_commit == "good"
    assert result.state.last_failed_commit is None


def test_completed_milestone_stops_the_loop_cleanly():
    result = KGOV3Loop().evaluate(
        previous=KGOState(cycle=4),
        pytest_output="",
        test_outcome="success",
        milestone_complete=True,
    )

    assert result.state.decision == LoopDecision.COMPLETE.value
    assert result.state.reason == "MILESTONE_COMPLETE"
    assert result.state.cycle == 5
