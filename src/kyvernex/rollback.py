from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path

from .self_verification import SelfVerificationResult, VerificationStatus


class RollbackError(RuntimeError):
    """Raised when rollback evidence or authorization is invalid."""


class RollbackDecision(StrEnum):
    NOT_REQUIRED = "NOT_REQUIRED"
    ROLLBACK_APPROVED = "ROLLBACK_APPROVED"
    EXECUTION_BLOCKED = "EXECUTION_BLOCKED"


@dataclass(slots=True, frozen=True)
class RollbackPolicy:
    require_explicit_authorization: bool = True
    require_matching_changeset: bool = True
    require_current_failure_evidence: bool = True


@dataclass(slots=True, frozen=True)
class RollbackPlan:
    schema: str
    work_item_id: str
    decision: str
    failed_commit: str
    restore_commit: str
    verification_status: str
    verification_reason: str
    changeset_fingerprint: str
    authorized: bool
    reason: str
    command_hint: str | None
    evidence_fingerprint: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True) + "\n"


class EvidenceBasedRollbackController:
    """Authorizes a commit-level rollback only from current failure evidence.

    The controller does not execute git or GitHub operations. It seals a
    deterministic rollback plan for an authorized executor and rejects stale,
    incomplete, or mismatched evidence.
    """

    def __init__(self, policy: RollbackPolicy | None = None) -> None:
        self.policy = policy or RollbackPolicy()

    def evaluate(
        self,
        *,
        verification: SelfVerificationResult,
        failed_commit: str,
        restore_commit: str,
        approved_changeset_fingerprint: str,
        current_changeset_fingerprint: str,
        authorized: bool = False,
    ) -> RollbackPlan:
        failed = failed_commit.strip()
        restore = restore_commit.strip()
        approved = approved_changeset_fingerprint.strip()
        current = current_changeset_fingerprint.strip()

        if not failed:
            raise RollbackError("FAILED_COMMIT_REQUIRED")
        if not restore:
            raise RollbackError("RESTORE_COMMIT_REQUIRED")
        if failed == restore:
            raise RollbackError("RESTORE_COMMIT_MUST_DIFFER")
        if not approved or not current:
            raise RollbackError("CHANGESET_FINGERPRINT_REQUIRED")
        if self.policy.require_explicit_authorization and not authorized:
            raise RollbackError("EXPLICIT_AUTHORIZATION_REQUIRED")
        if self.policy.require_matching_changeset and approved != current:
            raise RollbackError("CHANGESET_FINGERPRINT_MISMATCH")

        status = verification.status
        if status == VerificationStatus.VERIFIED.value:
            decision = RollbackDecision.NOT_REQUIRED
            reason = "CURRENT_VERIFICATION_SUCCEEDED"
            command_hint = None
        elif status == VerificationStatus.REPAIR_REQUIRED.value:
            if self.policy.require_current_failure_evidence and verification.reason != "CURRENT_TEST_FAILURE_EVIDENCE":
                raise RollbackError("SUPPORTED_FAILURE_EVIDENCE_REQUIRED")
            decision = RollbackDecision.ROLLBACK_APPROVED
            reason = "CURRENT_FAILURE_EVIDENCE_SUPPORTS_ROLLBACK"
            command_hint = f"git revert --no-edit {failed}"
        elif status == VerificationStatus.EXECUTION_BLOCKED.value:
            decision = RollbackDecision.EXECUTION_BLOCKED
            reason = "INCOMPLETE_VERIFICATION_CANNOT_AUTHORIZE_ROLLBACK"
            command_hint = None
        else:
            raise RollbackError(f"UNKNOWN_VERIFICATION_STATUS:{status}")

        payload = {
            "work_item_id": verification.work_item_id,
            "decision": decision.value,
            "failed_commit": failed,
            "restore_commit": restore,
            "verification_status": status,
            "verification_reason": verification.reason,
            "changeset_fingerprint": current,
            "authorized": authorized,
            "reason": reason,
            "command_hint": command_hint,
        }
        evidence_fingerprint = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

        return RollbackPlan(
            schema="kyvernex.rollback-plan.v1",
            work_item_id=verification.work_item_id,
            decision=decision.value,
            failed_commit=failed,
            restore_commit=restore,
            verification_status=status,
            verification_reason=verification.reason,
            changeset_fingerprint=current,
            authorized=authorized,
            reason=reason,
            command_hint=command_hint,
            evidence_fingerprint=evidence_fingerprint,
        )


def write_rollback_plan(plan: RollbackPlan, path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(plan.to_json(), encoding="utf-8")
