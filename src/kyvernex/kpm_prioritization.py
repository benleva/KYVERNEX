from __future__ import annotations

from dataclasses import dataclass

from .program_manager import Priority


@dataclass(slots=True, frozen=True)
class KPMFeatureAssessment:
    """Deterministic KPM assessment for backlog features.

    Scores are integers from 0 to 5. Higher values increase urgency, except
    implementation_cost where a higher value lowers priority when benefit is
    otherwise equal.
    """

    operational_impact: int
    governance_value: int
    urgency: int
    dependency_pressure: int
    implementation_cost: int

    def __post_init__(self) -> None:
        for value in (
            self.operational_impact,
            self.governance_value,
            self.urgency,
            self.dependency_pressure,
            self.implementation_cost,
        ):
            if value < 0 or value > 5:
                raise ValueError("KPM_PRIORITY_FACTOR_OUT_OF_RANGE")

    @property
    def score(self) -> int:
        return (
            self.operational_impact * 3
            + self.governance_value * 3
            + self.urgency * 2
            + self.dependency_pressure * 2
            - self.implementation_cost
        )

    def priority(self) -> Priority:
        score = self.score
        if score >= 38:
            return Priority.P0
        if score >= 30:
            return Priority.P1
        if score >= 21:
            return Priority.P2
        if score >= 12:
            return Priority.P3
        return Priority.P4


def execution_clock_assessment() -> KPMFeatureAssessment:
    """Canonical KPM assessment for the execution-performance clock.

    The clock improves observability and comparison of cycle speed, but it does
    not block correctness, repair or autonomous continuation. KPM therefore
    assigns its priority from measurable factors instead of a manually forced
    rank.
    """

    return KPMFeatureAssessment(
        operational_impact=3,
        governance_value=4,
        urgency=2,
        dependency_pressure=1,
        implementation_cost=2,
    )
