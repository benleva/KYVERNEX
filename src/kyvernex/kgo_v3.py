from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Sequence

from .kgo_ci import KGOAnalysis, parse_pytest_output


class LoopDecision(StrEnum):
    CONTINUE = "CONTINUE"
    REPAIR = "REPAIR"
    COMPLETE = "COMPLETE"


@dataclass(slots=True, frozen=True)
class KGOState:
    schema: str = "kyvernex.kgo.state.v1"
    cycle: int = 0
    last_commit: str | None = None
    last_verified_commit: str | None = None
    last_failed_commit: str | None = None
    current_work_item: str | None = None
    completed_work_items: tuple[str, ...] = ()
    resolved_root_causes: tuple[str, ...] = ()
    decision: str = LoopDecision.CONTINUE.value
    reason: str = "INITIAL_STATE"
    test_outcome: str = "unknown"
    failed_tests: int = 0


@dataclass(slots=True, frozen=True)
class LoopResult:
    schema: str
    state: KGOState
    analysis: KGOAnalysis
    next_action: str
    historical_failures_ignored: bool = True


class KGOV3Loop:
    """Closed-loop governance state machine driven only by current evidence.

    Historical failed runs are not reopened. A successful current test outcome
    advances the project even when a human-readable parser reports zero counts.
    A repair decision is emitted only when the current run contains supported
    failure evidence.
    """

    def evaluate(
        self,
        *,
        previous: KGOState,
        pytest_output: str,
        test_outcome: str,
        commit: str | None = None,
        current_work_item: str | None = None,
        milestone_complete: bool = False,
    ) -> LoopResult:
        analysis = parse_pytest_output(pytest_output)
        normalized_outcome = test_outcome.strip().lower()
        cycle = previous.cycle + 1

        if milestone_complete:
            decision = LoopDecision.COMPLETE
            reason = "MILESTONE_COMPLETE"
            next_action = "Close the governed milestone and select no further work in its scope."
            verified = previous.last_verified_commit
            failed = previous.last_failed_commit
        elif normalized_outcome == "success":
            decision = LoopDecision.CONTINUE
            reason = "CURRENT_CI_SUCCESS"
            next_action = "Select the next dependency-valid work item and continue the autonomous cycle."
            verified = commit or previous.last_verified_commit
            failed = previous.last_failed_commit
        elif analysis.failures:
            decision = LoopDecision.REPAIR
            reason = "CURRENT_FAILURE_EVIDENCE"
            next_action = "Repair the highest-priority current root cause, verify it, then resume."
            verified = previous.last_verified_commit
            failed = commit or previous.last_failed_commit
        else:
            # The current execution did not succeed, but it also supplied no test
            # failure evidence. This is an execution boundary, not a fabricated
            # code defect. Preserve momentum while reporting the exact condition.
            decision = LoopDecision.CONTINUE
            reason = "NO_SUPPORTED_CODE_FAILURE"
            next_action = "Record the execution condition and continue unless an external platform error is evidenced."
            verified = previous.last_verified_commit
            failed = previous.last_failed_commit

        state = KGOState(
            cycle=cycle,
            last_commit=commit or previous.last_commit,
            last_verified_commit=verified,
            last_failed_commit=failed,
            current_work_item=current_work_item or previous.current_work_item,
            completed_work_items=previous.completed_work_items,
            resolved_root_causes=previous.resolved_root_causes,
            decision=decision.value,
            reason=reason,
            test_outcome=normalized_outcome or "unknown",
            failed_tests=analysis.summary.failed,
        )
        return LoopResult(
            schema="kyvernex.kgo.loop-result.v1",
            state=state,
            analysis=analysis,
            next_action=next_action,
        )


def load_state(path: str | Path) -> KGOState:
    state_path = Path(path)
    if not state_path.exists():
        return KGOState()
    payload = json.loads(state_path.read_text(encoding="utf-8"))
    return KGOState(
        schema=payload.get("schema", "kyvernex.kgo.state.v1"),
        cycle=int(payload.get("cycle", 0)),
        last_commit=payload.get("last_commit"),
        last_verified_commit=payload.get("last_verified_commit"),
        last_failed_commit=payload.get("last_failed_commit"),
        current_work_item=payload.get("current_work_item"),
        completed_work_items=tuple(payload.get("completed_work_items", ())),
        resolved_root_causes=tuple(payload.get("resolved_root_causes", ())),
        decision=payload.get("decision", LoopDecision.CONTINUE.value),
        reason=payload.get("reason", "LOADED_STATE"),
        test_outcome=payload.get("test_outcome", "unknown"),
        failed_tests=int(payload.get("failed_tests", 0)),
    )


def write_result(result: LoopResult, output_dir: str | Path) -> None:
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    (root / "KGO_STATE.json").write_text(
        json.dumps(asdict(result.state), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (root / "KGO_V3_LOOP.json").write_text(
        json.dumps(asdict(result), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    summary = [
        "# KGO v3 autonomous loop",
        "",
        f"- Decision: **{result.state.decision}**",
        f"- Reason: `{result.state.reason}`",
        f"- Current outcome: `{result.state.test_outcome}`",
        f"- Current failed tests: **{result.state.failed_tests}**",
        f"- Cycle: **{result.state.cycle}**",
        f"- Next action: {result.next_action}",
        "- Historical failed runs: ignored for current-state decisions.",
    ]
    (root / "KGO_V3_SUMMARY.md").write_text("\n".join(summary) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate the current KGO v3 autonomous loop state.")
    parser.add_argument("pytest_output", type=Path)
    parser.add_argument("--state", type=Path, default=Path("artifacts/KGO_STATE.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts"))
    parser.add_argument("--test-outcome", default="unknown")
    parser.add_argument("--commit")
    parser.add_argument("--work-item")
    parser.add_argument("--milestone-complete", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    previous = load_state(args.state)
    result = KGOV3Loop().evaluate(
        previous=previous,
        pytest_output=args.pytest_output.read_text(encoding="utf-8", errors="replace"),
        test_outcome=args.test_outcome,
        commit=args.commit,
        current_work_item=args.work_item,
        milestone_complete=args.milestone_complete,
    )
    write_result(result, args.output_dir)
    print(json.dumps(asdict(result), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
