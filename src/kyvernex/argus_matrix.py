"""Deterministic JSON-defined ARGUS decision matrix evaluator."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence


class ArgusMatrixError(ValueError):
    """Raised when an ARGUS matrix or request violates the explicit contract."""


_ALLOWED_DECISIONS = {"ALLOW", "DENY", "REVIEW", "ABSTAIN"}
_ALLOWED_OPERATORS = {"eq", "ne", "in", "contains", "exists"}


def _require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ArgusMatrixError(f"{field} must be a non-empty string")
    return value.strip()


def _lookup(payload: Mapping[str, Any], path: str) -> tuple[bool, Any]:
    current: Any = payload
    for part in path.split("."):
        if not isinstance(current, Mapping) or part not in current:
            return False, None
        current = current[part]
    return True, current


def _matches(condition: Mapping[str, Any], request: Mapping[str, Any]) -> bool:
    unknown = sorted(set(condition) - {"path", "operator", "value"})
    if unknown:
        raise ArgusMatrixError(f"unknown condition fields: {', '.join(unknown)}")
    path = _require_text(condition.get("path"), "condition.path")
    operator = _require_text(condition.get("operator"), "condition.operator").lower()
    if operator not in _ALLOWED_OPERATORS:
        raise ArgusMatrixError(f"unsupported condition operator: {operator}")
    exists, actual = _lookup(request, path)
    if operator == "exists":
        expected = condition.get("value", True)
        if not isinstance(expected, bool):
            raise ArgusMatrixError("condition.value must be boolean for exists")
        return exists is expected
    if not exists:
        return False
    expected = condition.get("value")
    if operator == "eq":
        return actual == expected
    if operator == "ne":
        return actual != expected
    if operator == "in":
        if not isinstance(expected, Sequence) or isinstance(expected, (str, bytes, bytearray)):
            raise ArgusMatrixError("condition.value must be an array for in")
        return actual in expected
    if operator == "contains":
        if isinstance(actual, Mapping):
            return expected in actual
        if isinstance(actual, Sequence) and not isinstance(actual, (str, bytes, bytearray)):
            return expected in actual
        if isinstance(actual, str) and isinstance(expected, str):
            return expected in actual
        return False
    raise ArgusMatrixError(f"unsupported condition operator: {operator}")


def evaluate_argus_matrix(matrix: Mapping[str, Any], request: Mapping[str, Any]) -> dict[str, Any]:
    """Evaluate one request against a strict, ordered ARGUS rule matrix."""
    if not isinstance(matrix, Mapping):
        raise ArgusMatrixError("matrix must be an object")
    if not isinstance(request, Mapping):
        raise ArgusMatrixError("request must be an object")
    unknown = sorted(set(matrix) - {"matrix_id", "version", "default_decision", "rules"})
    if unknown:
        raise ArgusMatrixError(f"unknown matrix fields: {', '.join(unknown)}")
    matrix_id = _require_text(matrix.get("matrix_id"), "matrix.matrix_id")
    version = _require_text(matrix.get("version"), "matrix.version")
    default_decision = _require_text(matrix.get("default_decision", "ABSTAIN"), "matrix.default_decision").upper()
    if default_decision not in _ALLOWED_DECISIONS:
        raise ArgusMatrixError("matrix.default_decision must be ALLOW, DENY, REVIEW, or ABSTAIN")
    rules = matrix.get("rules")
    if not isinstance(rules, list):
        raise ArgusMatrixError("matrix.rules must be an array")

    trace: list[dict[str, Any]] = []
    selected: dict[str, Any] | None = None
    seen_ids: set[str] = set()
    for index, raw_rule in enumerate(rules):
        if not isinstance(raw_rule, Mapping):
            raise ArgusMatrixError(f"matrix.rules[{index}] must be an object")
        unknown_rule = sorted(set(raw_rule) - {"id", "priority", "when", "decision", "reason", "stop"})
        if unknown_rule:
            raise ArgusMatrixError(f"unknown rule fields in index {index}: {', '.join(unknown_rule)}")
        rule_id = _require_text(raw_rule.get("id"), f"matrix.rules[{index}].id")
        if rule_id in seen_ids:
            raise ArgusMatrixError(f"duplicate rule id: {rule_id}")
        seen_ids.add(rule_id)
        priority = raw_rule.get("priority", index)
        if not isinstance(priority, int):
            raise ArgusMatrixError(f"matrix.rules[{index}].priority must be an integer")
        conditions = raw_rule.get("when", [])
        if not isinstance(conditions, list):
            raise ArgusMatrixError(f"matrix.rules[{index}].when must be an array")
        matched = all(isinstance(item, Mapping) and _matches(item, request) for item in conditions)
        trace.append({"rule_id": rule_id, "priority": priority, "matched": matched})
        if not matched:
            continue
        decision = _require_text(raw_rule.get("decision"), f"matrix.rules[{index}].decision").upper()
        if decision not in _ALLOWED_DECISIONS:
            raise ArgusMatrixError(f"invalid decision for rule {rule_id}")
        candidate = {
            "rule_id": rule_id,
            "priority": priority,
            "decision": decision,
            "reason": _require_text(raw_rule.get("reason"), f"matrix.rules[{index}].reason"),
            "stop": bool(raw_rule.get("stop", True)),
        }
        if selected is None or candidate["priority"] < selected["priority"]:
            selected = candidate
        if candidate["stop"]:
            break

    decision = selected["decision"] if selected else default_decision
    reason = selected["reason"] if selected else "No rule matched; matrix default applied."
    return {
        "status": "DECIDED",
        "matrix": {"matrix_id": matrix_id, "version": version},
        "decision": decision,
        "reason": reason,
        "selected_rule": deepcopy(selected),
        "trace": trace,
        "request": deepcopy(dict(request)),
    }
