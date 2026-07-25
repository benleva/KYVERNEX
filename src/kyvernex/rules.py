from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Callable

from .models import CognitiveObject


class RuleSeverity(StrEnum):
    INFO = "INFO"
    RESERVATION = "RISERVA"
    ERROR = "ERRORE"


@dataclass(slots=True, frozen=True)
class RuleResult:
    rule_id: str
    passed: bool
    severity: RuleSeverity
    message: str


RulePredicate = Callable[[CognitiveObject], bool]


@dataclass(slots=True, frozen=True)
class Rule:
    rule_id: str
    description: str
    severity: RuleSeverity
    predicate: RulePredicate
    failure_message: str

    def evaluate(self, obj: CognitiveObject) -> RuleResult:
        try:
            passed = bool(self.predicate(obj))
        except Exception as exc:  # defensive boundary for plugin rules
            return RuleResult(
                rule_id=self.rule_id,
                passed=False,
                severity=RuleSeverity.ERROR,
                message=f"REGOLA_NON_ESEGUIBILE:{type(exc).__name__}",
            )
        return RuleResult(
            rule_id=self.rule_id,
            passed=passed,
            severity=self.severity,
            message="OK" if passed else self.failure_message,
        )


class RuleEngine:
    """Deterministic rule evaluator for the executable subset of ARGUS."""

    def __init__(self, rules: tuple[Rule, ...] | None = None) -> None:
        self._rules = rules or default_rules()

    @property
    def rules(self) -> tuple[Rule, ...]:
        return self._rules

    def evaluate(self, obj: CognitiveObject) -> tuple[RuleResult, ...]:
        return tuple(rule.evaluate(obj) for rule in self._rules)


def default_rules() -> tuple[Rule, ...]:
    return (
        Rule(
            rule_id="ARGUS-R001",
            description="Ogni oggetto deve dichiarare una fonte non vuota.",
            severity=RuleSeverity.ERROR,
            predicate=lambda obj: bool(obj.source.strip()),
            failure_message="ORIGINE_MANCANTE",
        ),
        Rule(
            rule_id="ARGUS-R002",
            description="Il contenuto originale deve essere preservato.",
            severity=RuleSeverity.ERROR,
            predicate=lambda obj: obj.original_content is not None and obj.original_content != "",
            failure_message="CONTENUTO_ORIGINALE_MANCANTE",
        ),
        Rule(
            rule_id="ARGUS-R003",
            description="Ogni trasformazione osservabile deve essere registrata.",
            severity=RuleSeverity.RESERVATION,
            predicate=lambda obj: bool(obj.transformations),
            failure_message="TRASFORMAZIONE_NON_TRACCIATA",
        ),
    )
