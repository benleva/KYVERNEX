import pytest

from kyvernex.rollback import EvidenceBasedRollbackController, RollbackDecision, RollbackError
from kyvernex.self_verification import ContinuousSelfVerificationController


def verification(*, targeted_output: str, targeted_outcome: str, complete_output: str, complete_outcome: str):
    return ContinuousSelfVerificationController().evaluate(
        work_item_id="M3-W005",
        targeted_output=targeted_output,
        targeted_outcome=targeted_outcome,
        complete_output=complete_output,
        complete_outcome=complete_outcome,
    )


def evaluate(controller, result, *, approved="fingerprint", current="fingerprint", authorized=True):
    return controller.evaluate(
        verification=result,
        failed_commit="bad123",
        restore_commit="base123",
        approved_changeset_fingerprint=approved,
        current_changeset_fingerprint=current,
        authorized=authorized,
    )


def test_current_failure_evidence_approves_deterministic_rollback():
    controller = EvidenceBasedRollbackController()
    result = verification(
        targeted_output="1 failed in 0.10s",
        targeted_outcome="failure",
        complete_output="1 failed, 20 passed in 0.40s",
        complete_outcome="failure",
    )

    first = evaluate(controller, result)
    second = evaluate(controller, result)

    assert first.schema == "kyvernex.rollback-plan.v1"
    assert first.decision == RollbackDecision.ROLLBACK_APPROVED.value
    assert first.command_hint == "git revert --no-edit bad123"
    assert first.evidence_fingerprint == second.evidence_fingerprint
    assert len(first.evidence_fingerprint) == 64


def test_successful_verification_does_not_request_rollback():
    result = verification(
        targeted_output="3 passed in 0.10s",
        targeted_outcome="success",
        complete_output="24 passed in 0.40s",
        complete_outcome="success",
    )

    plan = evaluate(EvidenceBasedRollbackController(), result)

    assert plan.decision == RollbackDecision.NOT_REQUIRED.value
    assert plan.command_hint is None


def test_incomplete_execution_blocks_rollback_without_inventing_failure():
    result = verification(
        targeted_output="",
        targeted_outcome="cancelled",
        complete_output="",
        complete_outcome="unknown",
    )

    plan = evaluate(EvidenceBasedRollbackController(), result)

    assert plan.decision == RollbackDecision.EXECUTION_BLOCKED.value
    assert plan.command_hint is None


def test_explicit_authorization_is_required():
    result = verification(
        targeted_output="1 failed in 0.10s",
        targeted_outcome="failure",
        complete_output="1 failed in 0.20s",
        complete_outcome="failure",
    )

    with pytest.raises(RollbackError, match="EXPLICIT_AUTHORIZATION_REQUIRED"):
        evaluate(EvidenceBasedRollbackController(), result, authorized=False)


def test_changeset_mutation_blocks_rollback():
    result = verification(
        targeted_output="1 failed in 0.10s",
        targeted_outcome="failure",
        complete_output="1 failed in 0.20s",
        complete_outcome="failure",
    )

    with pytest.raises(RollbackError, match="CHANGESET_FINGERPRINT_MISMATCH"):
        evaluate(EvidenceBasedRollbackController(), result, approved="approved", current="mutated")


def test_restore_commit_must_differ_from_failed_commit():
    result = verification(
        targeted_output="1 failed in 0.10s",
        targeted_outcome="failure",
        complete_output="1 failed in 0.20s",
        complete_outcome="failure",
    )

    with pytest.raises(RollbackError, match="RESTORE_COMMIT_MUST_DIFFER"):
        EvidenceBasedRollbackController().evaluate(
            verification=result,
            failed_commit="same",
            restore_commit="same",
            approved_changeset_fingerprint="fingerprint",
            current_changeset_fingerprint="fingerprint",
            authorized=True,
        )
