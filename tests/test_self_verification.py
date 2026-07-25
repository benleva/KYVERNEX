from kyvernex.self_verification import (
    ContinuousSelfVerificationController,
    VerificationStatus,
    write_verification_result,
)


def test_verifies_only_when_targeted_and_complete_succeed(tmp_path):
    result = ContinuousSelfVerificationController().evaluate(
        work_item_id="M3-W003",
        targeted_output="3 passed in 0.02s\n",
        targeted_outcome="success",
        complete_output="100 passed in 0.50s\n",
        complete_outcome="success",
    )

    assert result.status == VerificationStatus.VERIFIED.value
    assert result.reason == "TARGETED_AND_COMPLETE_TESTS_SUCCEEDED"
    assert result.targeted.succeeded is True
    assert result.complete.succeeded is True

    output = tmp_path / "SELF_VERIFICATION.json"
    write_verification_result(result, output)
    assert output.exists()
    assert '"status": "VERIFIED"' in output.read_text(encoding="utf-8")


def test_explicit_current_failure_requires_repair():
    result = ContinuousSelfVerificationController().evaluate(
        work_item_id="M3-W003",
        targeted_output="FAILED tests/test_x.py::test_x - AssertionError\n1 failed in 0.01s\n",
        targeted_outcome="failure",
        complete_output="",
        complete_outcome="not_run",
    )

    assert result.status == VerificationStatus.REPAIR_REQUIRED.value
    assert result.reason == "CURRENT_TEST_FAILURE_EVIDENCE"
    assert result.targeted.analysis.summary.failed == 1


def test_infrastructure_gap_blocks_advancement_without_inventing_defect():
    result = ContinuousSelfVerificationController().evaluate(
        work_item_id="M3-W003",
        targeted_output="3 passed in 0.02s\n",
        targeted_outcome="success",
        complete_output="runner unavailable\n",
        complete_outcome="cancelled",
    )

    assert result.status == VerificationStatus.EXECUTION_BLOCKED.value
    assert result.reason == "VERIFICATION_EXECUTION_INCOMPLETE"
    assert not result.complete.analysis.failures


def test_work_item_id_is_required():
    controller = ContinuousSelfVerificationController()

    try:
        controller.evaluate(
            work_item_id=" ",
            targeted_output="",
            targeted_outcome="unknown",
            complete_output="",
            complete_outcome="unknown",
        )
    except ValueError as exc:
        assert str(exc) == "WORK_ITEM_ID_REQUIRED"
    else:
        raise AssertionError("expected ValueError")
