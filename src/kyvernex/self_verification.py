from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path

from .kgo_ci import KGOAnalysis, parse_pytest_output


class VerificationStatus(StrEnum):
    VERIFIED = "VERIFIED"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"
    EXECUTION_BLOCKED = "EXECUTION_BLOCKED"


@dataclass(slots=True, frozen=True)
class VerificationEvidence:
    name: str
    outcome: str
    analysis: KGOAnalysis

    @property
    def succeeded(self) -> bool:
        return self.outcome == "success" and not self.analysis.failures


@dataclass(slots=True, frozen=True)
class SelfVerificationResult:
    schema: str
    work_item_id: str
    status: str
    targeted: VerificationEvidence
    complete: VerificationEvidence
    reason: str
    next_action: str


class ContinuousSelfVerificationController:
    """Validates a work item against targeted and complete current evidence.

    A work item is verified only when both current executions succeed. Explicit
    current test failures require repair. Missing or inconclusive execution
    evidence blocks advancement without inventing a source-code defect.
    """

    def evaluate(
        self,
        *,
        work_item_id: str,
        targeted_output: str,
        targeted_outcome: str,
        complete_output: str,
        complete_outcome: str,
    ) -> SelfVerificationResult:
        if not work_item_id.strip():
            raise ValueError("WORK_ITEM_ID_REQUIRED")

        targeted = self._evidence("targeted", targeted_output, targeted_outcome)
        complete = self._evidence("complete", complete_output, complete_outcome)

        if targeted.analysis.failures or complete.analysis.failures:
            status = VerificationStatus.REPAIR_REQUIRED
            reason = "CURRENT_TEST_FAILURE_EVIDENCE"
            next_action = "Repair the evidenced current failure and rerun targeted and complete verification."
        elif targeted.succeeded and complete.succeeded:
            status = VerificationStatus.VERIFIED
            reason = "TARGETED_AND_COMPLETE_TESTS_SUCCEEDED"
            next_action = "Record the verification checkpoint and advance the governed work item."
        else:
            status = VerificationStatus.EXECUTION_BLOCKED
            reason = "VERIFICATION_EXECUTION_INCOMPLETE"
            next_action = "Restore the unavailable execution boundary and rerun verification without creating a code defect."

        return SelfVerificationResult(
            schema="kyvernex.self-verification.v1",
            work_item_id=work_item_id,
            status=status.value,
            targeted=targeted,
            complete=complete,
            reason=reason,
            next_action=next_action,
        )

    @staticmethod
    def _evidence(name: str, output: str, outcome: str) -> VerificationEvidence:
        return VerificationEvidence(
            name=name,
            outcome=outcome.strip().lower() or "unknown",
            analysis=parse_pytest_output(output),
        )


def write_verification_result(result: SelfVerificationResult, path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(asdict(result), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
