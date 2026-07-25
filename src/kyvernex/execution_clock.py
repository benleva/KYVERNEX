from __future__ import annotations

import json
import math
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable


class ExecutionClockError(RuntimeError):
    """Raised when execution timing evidence is invalid or incomplete."""


@dataclass(slots=True, frozen=True)
class ExecutionSample:
    name: str
    duration_seconds: float

    def __post_init__(self) -> None:
        normalized = self.name.strip()
        if not normalized:
            raise ValueError("SAMPLE_NAME_REQUIRED")
        if not math.isfinite(self.duration_seconds) or self.duration_seconds < 0:
            raise ValueError("SAMPLE_DURATION_INVALID")
        object.__setattr__(self, "name", normalized)


@dataclass(slots=True, frozen=True)
class ExecutionMetrics:
    schema: str
    work_item_id: str
    sample_count: int
    total_seconds: float
    average_seconds: float
    minimum_seconds: float
    maximum_seconds: float
    baseline_seconds: float | None
    improvement_seconds: float | None
    improvement_percent: float | None
    samples: tuple[ExecutionSample, ...]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True) + "\n"


class ExecutionPerformanceClock:
    """Records policy-neutral execution durations and deterministic metrics.

    The clock observes elapsed time only. It does not alter governance decisions,
    execute repository mutations, or treat performance as correctness evidence.
    A monotonic clock can be injected to keep tests deterministic.
    """

    def __init__(self, clock: Callable[[], float] | None = None) -> None:
        self._clock = clock or time.monotonic
        self._started_at: dict[str, float] = {}
        self._samples: list[ExecutionSample] = []

    def start(self, name: str) -> None:
        normalized = name.strip()
        if not normalized:
            raise ExecutionClockError("SAMPLE_NAME_REQUIRED")
        if normalized in self._started_at:
            raise ExecutionClockError(f"SAMPLE_ALREADY_RUNNING:{normalized}")
        started = self._clock()
        if not math.isfinite(started):
            raise ExecutionClockError("CLOCK_VALUE_INVALID")
        self._started_at[normalized] = started

    def stop(self, name: str) -> ExecutionSample:
        normalized = name.strip()
        if normalized not in self._started_at:
            raise ExecutionClockError(f"SAMPLE_NOT_RUNNING:{normalized}")
        finished = self._clock()
        started = self._started_at.pop(normalized)
        duration = finished - started
        if not math.isfinite(duration) or duration < 0:
            raise ExecutionClockError("CLOCK_MOVED_BACKWARD")
        sample = ExecutionSample(normalized, duration)
        self._samples.append(sample)
        return sample

    def record(self, name: str, duration_seconds: float) -> ExecutionSample:
        sample = ExecutionSample(name, duration_seconds)
        self._samples.append(sample)
        return sample

    @property
    def samples(self) -> tuple[ExecutionSample, ...]:
        return tuple(self._samples)

    def summarize(
        self,
        *,
        work_item_id: str,
        baseline_seconds: float | None = None,
        samples: Iterable[ExecutionSample] | None = None,
    ) -> ExecutionMetrics:
        item = work_item_id.strip()
        if not item:
            raise ExecutionClockError("WORK_ITEM_ID_REQUIRED")
        if self._started_at:
            running = ",".join(sorted(self._started_at))
            raise ExecutionClockError(f"SAMPLES_STILL_RUNNING:{running}")
        selected = tuple(samples) if samples is not None else self.samples
        if not selected:
            raise ExecutionClockError("EXECUTION_SAMPLES_REQUIRED")
        if baseline_seconds is not None and (
            not math.isfinite(baseline_seconds) or baseline_seconds <= 0
        ):
            raise ExecutionClockError("BASELINE_DURATION_INVALID")

        total = sum(sample.duration_seconds for sample in selected)
        average = total / len(selected)
        minimum = min(sample.duration_seconds for sample in selected)
        maximum = max(sample.duration_seconds for sample in selected)
        improvement_seconds = None
        improvement_percent = None
        if baseline_seconds is not None:
            improvement_seconds = baseline_seconds - average
            improvement_percent = (improvement_seconds / baseline_seconds) * 100

        return ExecutionMetrics(
            schema="kyvernex.execution-metrics.v1",
            work_item_id=item,
            sample_count=len(selected),
            total_seconds=total,
            average_seconds=average,
            minimum_seconds=minimum,
            maximum_seconds=maximum,
            baseline_seconds=baseline_seconds,
            improvement_seconds=improvement_seconds,
            improvement_percent=improvement_percent,
            samples=selected,
        )


def write_execution_metrics(metrics: ExecutionMetrics, path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(metrics.to_json(), encoding="utf-8")
