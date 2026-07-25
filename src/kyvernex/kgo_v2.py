from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from .kgo_ci import FailureRecord, KGOAnalysis, parse_pytest_output


@dataclass(slots=True, frozen=True)
class RootCause:
    cause_id: str
    signature: str
    category: str
    priority: str
    affected_tests: tuple[str, ...]
    probable_files: tuple[str, ...]
    confidence: float
    estimated_effort: str
    expected_failures_removed: int
    projected_success_percent: float
    rationale: str
    suggested_action: str


@dataclass(slots=True, frozen=True)
class PatchPlan:
    plan_id: str
    cause_id: str
    priority: str
    target_files: tuple[str, ...]
    validation_tests: tuple[str, ...]
    suggested_command: str
    autonomous_patch_allowed: bool
    approval_reason: str


@dataclass(slots=True, frozen=True)
class KGOV2Report:
    schema: str
    state: str
    baseline: KGOAnalysis
    root_causes: tuple[RootCause, ...]
    patch_plans: tuple[PatchPlan, ...]
    next_cause_id: str | None
    release_projection_percent: float


def _signature(item: FailureRecord) -> str:
    reason = item.reason.lower()
    if "unhashable type: 'dict'" in reason:
        return "UNHASHABLE_DICT"
    if "timeout_supera_politica" in reason:
        return "KEX_TIMEOUT_POLICY"
    if "regex pattern did not match" in reason:
        return "ERROR_CONTRACT_REGEX"
    if "assert " in reason or "assertionerror" in reason:
        return f"ASSERTION_CONTRACT:{item.nodeid.split('::', 1)[0]}"
    return f"{item.category}:{reason[:80]}"


def _probable_files(signature: str, tests: tuple[str, ...]) -> tuple[str, ...]:
    if signature == "UNHASHABLE_DICT":
        return (
            "src/kyvernex/deletion.py",
            "src/kyvernex/durable_deletion.py",
            "src/kyvernex/transaction_journal.py",
            "src/kyvernex/process_safe_journal.py",
        )
    if signature == "KEX_TIMEOUT_POLICY":
        return ("src/kyvernex/execution_engine.py", "tests/test_execution_engine.py")
    if signature == "ERROR_CONTRACT_REGEX":
        return ("src/kyvernex/execution_engine.py", "tests/test_execution_engine.py")
    files = []
    for nodeid in tests:
        test_path = nodeid.split("::", 1)[0]
        stem = Path(test_path).stem.removeprefix("test_")
        files.append(f"src/kyvernex/{stem}.py")
    return tuple(sorted(set(files)))


def _confidence(signature: str, count: int) -> float:
    if signature == "UNHASHABLE_DICT":
        return 0.94 if count >= 2 else 0.86
    if signature in {"KEX_TIMEOUT_POLICY", "ERROR_CONTRACT_REGEX"}:
        return 0.88
    if signature.startswith("ASSERTION_CONTRACT"):
        return 0.72
    return 0.55


def _effort(signature: str, count: int) -> str:
    if signature == "UNHASHABLE_DICT":
        return "MEDIUM"
    if signature in {"KEX_TIMEOUT_POLICY", "ERROR_CONTRACT_REGEX"}:
        return "SMALL"
    if signature.startswith("ASSERTION_CONTRACT"):
        return "MEDIUM"
    return "UNKNOWN"


def _rationale(signature: str) -> tuple[str, str]:
    if signature == "UNHASHABLE_DICT":
        return (
            "A mutable dict is being used where a hashable identifier or immutable key is required across deletion coordination paths.",
            "Trace the shared deletion identifier flow and replace mutable mapping keys with stable object or transaction identifiers; do not patch each failing test independently.",
        )
    if signature == "KEX_TIMEOUT_POLICY":
        return (
            "The test request exceeds the configured execution policy before sequence execution can exercise stop-on-failure behavior.",
            "Align the test timeout with policy limits or construct the sequence with an allowed timeout while preserving the intended failure path.",
        )
    if signature == "ERROR_CONTRACT_REGEX":
        return (
            "The raised governance error is semantically correct but does not match the declared external error contract.",
            "Reconcile the stable error code and the test contract; prefer changing implementation only when the specification requires that code.",
        )
    return (
        "Observed output differs from the declared test contract.",
        "Inspect specification, implementation and test together before changing either side.",
    )


def build_v2_report(analysis: KGOAnalysis) -> KGOV2Report:
    grouped: dict[str, list[FailureRecord]] = defaultdict(list)
    for item in analysis.failures:
        grouped[_signature(item)].append(item)

    causes: list[RootCause] = []
    denominator = analysis.summary.passed + analysis.summary.failed
    for index, (signature, failures) in enumerate(sorted(grouped.items()), start=1):
        tests = tuple(sorted(item.nodeid for item in failures))
        priorities = [item.priority for item in failures]
        priority = sorted(priorities, key=lambda value: int(value[1:]))[0]
        category = Counter(item.category for item in failures).most_common(1)[0][0]
        removed = len(failures)
        projected_passed = analysis.summary.passed + removed
        projected = round((projected_passed / denominator * 100.0) if denominator else 100.0, 2)
        rationale, action = _rationale(signature)
        causes.append(
            RootCause(
                cause_id=f"KGO-RC-{index:03d}",
                signature=signature,
                category=category,
                priority=priority,
                affected_tests=tests,
                probable_files=_probable_files(signature, tests),
                confidence=_confidence(signature, removed),
                estimated_effort=_effort(signature, removed),
                expected_failures_removed=removed,
                projected_success_percent=projected,
                rationale=rationale,
                suggested_action=action,
            )
        )

    rank = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4}
    causes.sort(key=lambda item: (rank[item.priority], -item.expected_failures_removed, -item.confidence, item.cause_id))

    plans: list[PatchPlan] = []
    for index, cause in enumerate(causes, start=1):
        command = "python -m pytest -q " + " ".join(cause.affected_tests)
        allowed = cause.confidence >= 0.9 and cause.estimated_effort in {"SMALL", "MEDIUM"}
        plans.append(
            PatchPlan(
                plan_id=f"KGO-PP-{index:03d}",
                cause_id=cause.cause_id,
                priority=cause.priority,
                target_files=cause.probable_files,
                validation_tests=cause.affected_tests,
                suggested_command=command,
                autonomous_patch_allowed=allowed,
                approval_reason=(
                    "Eligible for isolated branch proposal; merge remains prohibited without passing tests."
                    if allowed
                    else "Human or coding-agent review required before patch generation."
                ),
            )
        )

    release_projection = max((cause.projected_success_percent for cause in causes), default=analysis.summary.success_percent)
    return KGOV2Report(
        schema="kyvernex.kgo.v2.report.v1",
        state=analysis.state,
        baseline=analysis,
        root_causes=tuple(causes),
        patch_plans=tuple(plans),
        next_cause_id=causes[0].cause_id if causes else None,
        release_projection_percent=release_projection,
    )


def write_v2_artifacts(report: KGOV2Report, output_dir: str | Path) -> None:
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    payload = asdict(report)
    (root / "KGO_V2_REPORT.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (root / "KGO_ROOT_CAUSES.json").write_text(json.dumps(payload["root_causes"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (root / "KGO_PATCH_PLAN.json").write_text(json.dumps(payload["patch_plans"], indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# KGO v2 governed intelligence",
        "",
        f"- State: **{report.state}**",
        f"- Baseline success: **{report.baseline.summary.success_percent}%**",
        f"- Root causes: **{len(report.root_causes)}**",
        f"- Release projection after best single root-cause fix: **{report.release_projection_percent}%**",
    ]
    if report.root_causes:
        cause = report.root_causes[0]
        lines.extend([
            "",
            "## Next root cause",
            f"- ID: `{cause.cause_id}`",
            f"- Priority: **{cause.priority}**",
            f"- Signature: `{cause.signature}`",
            f"- Confidence: **{round(cause.confidence * 100, 1)}%**",
            f"- Estimated effort: **{cause.estimated_effort}**",
            f"- Tests affected: **{cause.expected_failures_removed}**",
            f"- Projected success: **{cause.projected_success_percent}%**",
            f"- Rationale: {cause.rationale}",
            f"- Suggested action: {cause.suggested_action}",
            "- Probable files: " + ", ".join(f"`{path}`" for path in cause.probable_files),
        ])
    if report.patch_plans:
        lines.extend(["", "## Patch plans"])
        for plan in report.patch_plans:
            lines.append(
                f"- `{plan.plan_id}` for `{plan.cause_id}` | {plan.priority} | autonomous proposal: "
                f"**{'YES' if plan.autonomous_patch_allowed else 'NO'}** | `{plan.suggested_command}`"
            )
    (root / "KGO_V2_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build deterministic KGO v2 root-cause and patch-planning artifacts.")
    parser.add_argument("pytest_output", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts"))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    analysis = parse_pytest_output(args.pytest_output.read_text(encoding="utf-8", errors="replace"))
    report = build_v2_report(analysis)
    write_v2_artifacts(report, args.output_dir)
    print(json.dumps(asdict(report), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
