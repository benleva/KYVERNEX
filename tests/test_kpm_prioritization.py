import pytest

from kyvernex import KPMFeatureAssessment, Priority, execution_clock_assessment


def test_execution_clock_priority_is_assigned_by_kpm_factors() -> None:
    assessment = execution_clock_assessment()

    assert assessment.priority() == Priority.P2
    assert assessment.score == 25


def test_higher_governance_value_increases_priority() -> None:
    lower = KPMFeatureAssessment(2, 2, 1, 1, 3)
    higher = KPMFeatureAssessment(4, 5, 4, 3, 1)

    assert higher.score > lower.score
    assert higher.priority().value < lower.priority().value


def test_priority_factors_must_remain_in_range() -> None:
    with pytest.raises(ValueError, match="KPM_PRIORITY_FACTOR_OUT_OF_RANGE"):
        KPMFeatureAssessment(6, 1, 1, 1, 1)
