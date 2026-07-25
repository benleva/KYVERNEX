from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence


_SUMMARY_RE = re.compile(
    r"(?P<failed>\d+) failed(?:, (?P<passed>\d+) passed)?(?:, (?P<skipped>\d+) skipped)? in (?P<seconds>[0-9.]+)s"
)
_FAILED_RE = re.compile(r"^FAILED\s+(?P<nodeid>\S+)(?:\s+-\s+(?P<reason>.*))?$")
_ERROR_RE = re.compile(r"^ERROR\s+(?P<nodeid>\S+)(?:\s+-\s+(?P<reason>.*))?$")


@dataclass(slots=True, frozen=True)
class FailureRecord:
    nodeid: str
    reason: str
    category: str
    priority: str


@dataclass(slots=True, frozen=True)
class TestSummary:
    passed: int
    failed: int
    skipped: int
    duration_seconds: float | None

    @property
    def total(self) -> int:
        return self.passed + self.failed + self.skipped

    @property
    def success_percent(self) -> float:
        denominator = self.passed + self.failed
        return round((self.passed / denominator * 100.0) if denominator else 0.0, 2)


@dataclass(slots=True, frozen=True)
class KGOAnalysis:
    schema: str
    state: str
    summary: TestSummary
    failures: tuple[FailureRecord, ...]
    next_task: FailureRecord | None


def _classify(reason: str, nodeid: str) -> tuple[str, str]:
    text = f"{nodeid} {reason}".lower()
    if "collection" in text or "importerror" in text or "modulenotfounderror" in text:
        return "COLLECTION_OR_IMPORT", "P0"
    if "typeerror" in text or "kexerror" in text or "runtimeerror" in text:
        return "RUNTIME_DEFECT", "P0"
    if "assertionerror" in text or "assert " in text:
        return "CONTRACT_MISMATCH", "P1"
    if "timeout" in text:
        return "TIMEOUT", "P0"
    return "UNCLASSIFIED_TEST_FAILURE", "P1"


def parse_pytest_output(text: str) -> KGOAnalysis:
    failures: list[FailureRecord] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        match = _FAILED_RE.match(line) or _ERROR_RE.match(line)
        if match is None:
            continue
        nodeid = match.group("nodeid")
        reason = (match.group("reason") or "No concise reason reported").strip()
        category, priority = _classify(reason, nodeid)
        failures.append(FailureRecord(nodeid=nodeid, reason=reason, category=category, priority=priority))

    summary_match = None
    for match in _SUMMARY_RE.finditer(text):
        summary_match = match
    if summary_match is None:
        failed = len(failures)
        passed = 0
        skipped = 0
        duration = None
    else:
        failed = int(summary_match.group("failed"))
        passed = int(summary_match.group("passed") or 0)
        skipped = int(summary_match.group("skipped") or 0)
        duration = float(summary_match.group("seconds"))

    rank = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4}
    ordered = tuple(sorted(failures, key=lambda item: (rank[item.priority], item.category, item.nodeid)))
    state = "VERIFIED" if failed == 0 else "BLOCKED"
    return KGOAnalysis(
        schema="kyvernex.kgo.analysis.v1",
        state=state,
        summary=TestSummary(passed=passed, failed=failed, skipped=skipped, duration_seconds=duration),
        failures=ordered,
        next_task=ordered[0] if ordered else None,
    )


def write_artifacts(analysis: KGOAnalysis, output_dir: str | Path) -> None:
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    payload = asdict(analysis)
    (root / "KGO_BACKLOG.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    checkpoint = {
        "schema": "kyvernex.kgo.checkpoint.v1",
        "state": analysis.state,
        "completion_percent": analysis.summary.success_percent,
        "passed": analysis.summary.passed,
        "failed": analysis.summary.failed,
        "skipped": analysis.summary.skipped,
        "current_item_id": analysis.next_task.nodeid if analysis.next_task else None,
        "current_priority": analysis.next_task.priority if analysis.next_task else None,
        "stop_reason": None if analysis.state == "VERIFIED" else "TEST_FAILURES_PRESENT",
    }
    (root / "KGO_CHECKPOINT.json").write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# KGO governed verification",
        "",
        f"- State: **{analysis.state}**",
        f"- Passed: **{analysis.summary.passed}**",
        f"- Failed: **{analysis.summary.failed}**",
        f"- Skipped: **{analysis.summary.skipped}**",
        f"- Success: **{analysis.summary.success_percent}%**",
    ]
    if analysis.next_task:
        lines.extend([
            "",
            "## Next governed task",
            f"- Priority: **{analysis.next_task.priority}**",
            f"- Test: `{analysis.next_task.nodeid}`",
            f"- Category: `{analysis.next_task.category}`",
            f"- Evidence: `{analysis.next_task.reason}`",
        ])
    if analysis.failures:
        lines.extend(["", "## Ordered backlog"])
        for item in analysis.failures:
            lines.append(f"- `{item.priority}` `{item.category}` `{item.nodeid}`: {item.reason}")
    (root / "KGO_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze pytest evidence and create deterministic KGO governance artifacts.")
    parser.add_argument("pytest_output", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts"))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    analysis = parse_pytest_output(args.pytest_output.read_text(encoding="utf-8", errors="replace"))
    write_artifacts(analysis, args.output_dir)
    print(json.dumps(asdict(analysis), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
