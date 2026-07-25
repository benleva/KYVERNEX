import pytest

from kyvernex.execution_clock import (
    ExecutionClockError,
    ExecutionPerformanceClock,
    ExecutionSample,
)


def test_injected_monotonic_clock_records_elapsed_time():
    values = iter((10.0, 12.5))
    clock = ExecutionPerformanceClock(clock=lambda: next(values))

    clock.start("targeted-tests")
    sample = clock.stop("targeted-tests")

    assert sample == ExecutionSample("targeted-tests", 2.5)
    assert clock.samples == (sample,)


def test_metrics_include_baseline_improvement():
    clock = ExecutionPerformanceClock()
    clock.record("targeted", 2.0)
    clock.record("complete", 4.0)

    metrics = clock.summarize(work_item_id="M3-W006", baseline_seconds=5.0)

    assert metrics.schema == "kyvernex.execution-metrics.v1"
    assert metrics.sample_count == 2
    assert metrics.total_seconds == 6.0
    assert metrics.average_seconds == 3.0
    assert metrics.minimum_seconds == 2.0
    assert metrics.maximum_seconds == 4.0
    assert metrics.improvement_seconds == 2.0
    assert metrics.improvement_percent == 40.0


def test_slower_average_is_reported_as_negative_improvement():
    clock = ExecutionPerformanceClock()
    clock.record("complete", 6.0)

    metrics = clock.summarize(work_item_id="M3-W006", baseline_seconds=5.0)

    assert metrics.improvement_seconds == -1.0
    assert metrics.improvement_percent == -20.0


def test_running_sample_blocks_summary():
    clock = ExecutionPerformanceClock(clock=lambda: 10.0)
    clock.start("complete")

    with pytest.raises(ExecutionClockError, match="SAMPLES_STILL_RUNNING:complete"):
        clock.summarize(work_item_id="M3-W006")


def test_duplicate_start_and_missing_stop_are_rejected():
    clock = ExecutionPerformanceClock(clock=lambda: 10.0)
    clock.start("targeted")

    with pytest.raises(ExecutionClockError, match="SAMPLE_ALREADY_RUNNING:targeted"):
        clock.start("targeted")
    with pytest.raises(ExecutionClockError, match="SAMPLE_NOT_RUNNING:complete"):
        clock.stop("complete")


def test_backward_clock_is_rejected():
    values = iter((10.0, 9.0))
    clock = ExecutionPerformanceClock(clock=lambda: next(values))
    clock.start("complete")

    with pytest.raises(ExecutionClockError, match="CLOCK_MOVED_BACKWARD"):
        clock.stop("complete")


def test_invalid_samples_and_baselines_are_rejected():
    with pytest.raises(ValueError, match="SAMPLE_DURATION_INVALID"):
        ExecutionSample("complete", -1.0)

    clock = ExecutionPerformanceClock()
    clock.record("complete", 1.0)

    with pytest.raises(ExecutionClockError, match="BASELINE_DURATION_INVALID"):
        clock.summarize(work_item_id="M3-W006", baseline_seconds=0.0)
