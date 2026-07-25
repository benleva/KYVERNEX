"""Governed host contracts for the KYVERNEX plugin runtime.

The module implements the frozen M6 request, response and error envelopes.
Validation is deliberately fail closed: unknown fields, ambiguous authority and
unsupported operations are rejected before the host adapter can be invoked.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping
from uuid import uuid4


SUPPORTED_OPERATION = "governed.execute"
_REQUEST_FIELDS = {
    "request_id",
    "operation",
    "input",
    "context",
    "requested_capabilities",
    "authorization",
    "limits",
}
_AUTHORIZATION_FIELDS = {"principal", "grants"}
_LIMIT_FIELDS = {"timeout_seconds", "max_output_bytes"}


class PluginResponseStatus(str, Enum):
    SUCCEEDED = "SUCCEEDED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"


class PluginErrorCategory(str, Enum):
    VALIDATION = "VALIDATION"
    LIFECYCLE = "LIFECYCLE"
    AUTHORIZATION = "AUTHORIZATION"
    POLICY = "POLICY"
    ADAPTER = "ADAPTER"
    EXECUTION = "EXECUTION"
    INTEGRITY = "INTEGRITY"
    COMPATIBILITY = "COMPATIBILITY"


@dataclass(frozen=True)
class GovernedPluginError:
    code: str
    message: str
    category: PluginErrorCategory
    retryable: bool = False
    details: Mapping[str, Any] = field(default_factory=dict)
    cause_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "category": self.category.value,
            "retryable": self.retryable,
            "details": dict(self.details),
            "cause_id": self.cause_id,
        }


class PluginContractError(ValueError):
    """Raised when a host envelope violates the frozen plugin contract."""

    def __init__(self, error: GovernedPluginError) -> None:
        super().__init__(error.message)
        self.error = error


@dataclass(frozen=True)
class PluginAuthorization:
    principal: str
    grants: tuple[str, ...]


@dataclass(frozen=True)
class PluginLimits:
    timeout_seconds: int
    max_output_bytes: int


@dataclass(frozen=True)
class PluginRequest:
    request_id: str
    operation: str
    input: Mapping[str, Any]
    context: Mapping[str, Any]
    requested_capabilities: tuple[str, ...]
    authorization: PluginAuthorization
    limits: PluginLimits

    def to_adapter_request(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "operation": self.operation,
            "input": dict(self.input),
            "context": dict(self.context),
            "requested_capabilities": list(self.requested_capabilities),
            "authorization": {
                "principal": self.authorization.principal,
                "grants": list(self.authorization.grants),
            },
            "limits": {
                "timeout_seconds": self.limits.timeout_seconds,
                "max_output_bytes": self.limits.max_output_bytes,
            },
        }


@dataclass(frozen=True)
class PluginDecision:
    authorized: bool
    reason: str
    policy_ids: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "authorized": self.authorized,
            "reason": self.reason,
            "policy_ids": list(self.policy_ids),
        }


@dataclass(frozen=True)
class PluginEvidence:
    execution_id: str | None
    audit_record_ids: tuple[str, ...]
    started_at: str
    completed_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "audit_record_ids": list(self.audit_record_ids),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }


@dataclass(frozen=True)
class PluginResponse:
    request_id: str
    status: PluginResponseStatus
    result: Any
    error: GovernedPluginError | None
    decision: PluginDecision
    evidence: PluginEvidence
    plugin: Mapping[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "status": self.status.value,
            "result": self.result,
            "error": None if self.error is None else self.error.to_dict(),
            "decision": self.decision.to_dict(),
            "evidence": self.evidence.to_dict(),
            "plugin": dict(self.plugin),
        }


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def new_execution_id() -> str:
    return uuid4().hex


def _error(code: str, message: str, category: PluginErrorCategory, **details: Any) -> PluginContractError:
    return PluginContractError(
        GovernedPluginError(
            code=code,
            message=message,
            category=category,
            details=details,
        )
    )


def _string_list(value: Any, field_name: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise _error(
            "REQUEST_SCHEMA_INVALID",
            f"{field_name} must be a list of non-empty strings",
            PluginErrorCategory.VALIDATION,
            field=field_name,
        )
    if len(set(value)) != len(value):
        raise _error(
            "REQUEST_SCHEMA_INVALID",
            f"{field_name} must not contain duplicates",
            PluginErrorCategory.VALIDATION,
            field=field_name,
        )
    return tuple(value)


def parse_plugin_request(
    raw: Mapping[str, Any],
    *,
    max_timeout_seconds: int,
    max_output_bytes: int,
) -> PluginRequest:
    if not isinstance(raw, Mapping):
        raise _error(
            "REQUEST_SCHEMA_INVALID",
            "Plugin request must be a mapping",
            PluginErrorCategory.VALIDATION,
        )
    unknown = set(raw) - _REQUEST_FIELDS
    if unknown:
        raise _error(
            "REQUEST_SCHEMA_INVALID",
            "Plugin request contains unknown fields",
            PluginErrorCategory.VALIDATION,
            fields=sorted(unknown),
        )
    missing = _REQUEST_FIELDS - set(raw)
    if missing:
        raise _error(
            "REQUEST_SCHEMA_INVALID",
            "Plugin request is missing required fields",
            PluginErrorCategory.VALIDATION,
            fields=sorted(missing),
        )

    request_id = raw["request_id"]
    if not isinstance(request_id, str) or not request_id.strip():
        raise _error(
            "REQUEST_SCHEMA_INVALID",
            "request_id must be a non-empty string",
            PluginErrorCategory.VALIDATION,
            field="request_id",
        )
    operation = raw["operation"]
    if operation != SUPPORTED_OPERATION:
        raise _error(
            "REQUEST_SCHEMA_INVALID",
            "Unsupported plugin operation",
            PluginErrorCategory.VALIDATION,
            field="operation",
            supported=SUPPORTED_OPERATION,
        )
    input_value = raw["input"]
    context = raw["context"]
    if not isinstance(input_value, Mapping) or not isinstance(context, Mapping):
        raise _error(
            "REQUEST_SCHEMA_INVALID",
            "input and context must be mappings",
            PluginErrorCategory.VALIDATION,
        )

    requested = _string_list(raw["requested_capabilities"], "requested_capabilities")

    authorization = raw["authorization"]
    if not isinstance(authorization, Mapping):
        raise _error(
            "REQUEST_SCHEMA_INVALID",
            "authorization must be a mapping",
            PluginErrorCategory.VALIDATION,
        )
    unknown_auth = set(authorization) - _AUTHORIZATION_FIELDS
    if unknown_auth or set(authorization) != _AUTHORIZATION_FIELDS:
        raise _error(
            "REQUEST_SCHEMA_INVALID",
            "authorization fields do not match the contract",
            PluginErrorCategory.VALIDATION,
            fields=sorted(unknown_auth or (_AUTHORIZATION_FIELDS - set(authorization))),
        )
    principal = authorization["principal"]
    if not isinstance(principal, str) or not principal.strip():
        raise _error(
            "AUTHORIZATION_REQUIRED",
            "authorization principal is required",
            PluginErrorCategory.AUTHORIZATION,
        )
    grants = _string_list(authorization["grants"], "authorization.grants")

    limits = raw["limits"]
    if not isinstance(limits, Mapping) or set(limits) != _LIMIT_FIELDS:
        raise _error(
            "REQUEST_SCHEMA_INVALID",
            "limits fields do not match the contract",
            PluginErrorCategory.VALIDATION,
        )
    timeout = limits["timeout_seconds"]
    output_limit = limits["max_output_bytes"]
    if not isinstance(timeout, int) or isinstance(timeout, bool) or timeout <= 0 or timeout > max_timeout_seconds:
        raise _error(
            "REQUEST_SCHEMA_INVALID",
            "timeout_seconds is outside configured limits",
            PluginErrorCategory.VALIDATION,
            maximum=max_timeout_seconds,
        )
    if (
        not isinstance(output_limit, int)
        or isinstance(output_limit, bool)
        or output_limit <= 0
        or output_limit > max_output_bytes
    ):
        raise _error(
            "REQUEST_SCHEMA_INVALID",
            "max_output_bytes is outside configured limits",
            PluginErrorCategory.VALIDATION,
            maximum=max_output_bytes,
        )

    return PluginRequest(
        request_id=request_id,
        operation=operation,
        input=dict(input_value),
        context=dict(context),
        requested_capabilities=requested,
        authorization=PluginAuthorization(principal=principal, grants=grants),
        limits=PluginLimits(timeout_seconds=timeout, max_output_bytes=output_limit),
    )


def decide_request(request: PluginRequest, negotiated_capabilities: frozenset[str]) -> PluginDecision:
    requested = set(request.requested_capabilities)
    grants = set(request.authorization.grants)
    if SUPPORTED_OPERATION not in negotiated_capabilities:
        return PluginDecision(False, "CAPABILITY_NOT_NEGOTIATED", ("M6-CAPABILITY-INTERSECTION",))
    if not requested.issubset(negotiated_capabilities):
        return PluginDecision(False, "CAPABILITY_NOT_NEGOTIATED", ("M6-CAPABILITY-INTERSECTION",))
    if not requested.issubset(grants) or SUPPORTED_OPERATION not in grants:
        return PluginDecision(False, "AUTHORIZATION_REQUIRED", ("M6-EXPLICIT-GRANTS",))
    return PluginDecision(True, "AUTHORIZED", ("M6-EXPLICIT-GRANTS", "M6-CAPABILITY-INTERSECTION"))
