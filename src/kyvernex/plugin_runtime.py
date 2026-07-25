"""Bounded KYVERNEX plugin runtime."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from threading import RLock
from types import MappingProxyType
from typing import Any, Mapping, Protocol, runtime_checkable
from uuid import uuid4

from .plugin_config import PluginConfiguration, PluginConfigurationError
from .plugin_contracts import (
    GovernedPluginError, PluginContractError, PluginDecision, PluginErrorCategory,
    PluginEvidence, PluginResponse, PluginResponseStatus, decide_request,
    new_execution_id, parse_plugin_request, utc_timestamp,
)

PLUGIN_ID = "kyvernex.plugin.runtime"
PLUGIN_API_VERSION = "1.0.0"


class PluginState(str, Enum):
    CREATED = "CREATED"
    INITIALIZED = "INITIALIZED"
    READY = "READY"
    EXECUTING = "EXECUTING"
    DEGRADED = "DEGRADED"
    SHUTDOWN = "SHUTDOWN"


class PluginRuntimeError(RuntimeError):
    def __init__(self, code: str, message: str, *, category: PluginErrorCategory, retryable: bool = False, details: Mapping[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.category = category
        self.retryable = retryable
        self.details = dict(details or {})

    def to_dict(self) -> dict[str, Any]:
        return GovernedPluginError(self.code, str(self), self.category, self.retryable, self.details).to_dict()


@runtime_checkable
class PluginHostAdapter(Protocol):
    adapter_id: str
    adapter_version: str
    def capabilities(self) -> set[str]: ...
    def invoke(self, request: Mapping[str, Any], authority: Mapping[str, Any]) -> Any: ...
    def health(self) -> Any: ...
    def shutdown(self) -> None: ...


@dataclass(frozen=True)
class PluginIdentity:
    plugin_id: str
    plugin_api_version: str
    kyvernex_version: str
    instance_id: str


_ALLOWED_TRANSITIONS = MappingProxyType({
    (PluginState.CREATED, "initialize"): PluginState.INITIALIZED,
    (PluginState.INITIALIZED, "validate"): PluginState.READY,
    (PluginState.READY, "execute"): PluginState.EXECUTING,
    (PluginState.EXECUTING, "complete"): PluginState.READY,
    (PluginState.EXECUTING, "integrity_failure"): PluginState.DEGRADED,
    (PluginState.CREATED, "shutdown"): PluginState.SHUTDOWN,
    (PluginState.INITIALIZED, "shutdown"): PluginState.SHUTDOWN,
    (PluginState.READY, "shutdown"): PluginState.SHUTDOWN,
    (PluginState.DEGRADED, "shutdown"): PluginState.SHUTDOWN,
})


class KyvernexPluginRuntime:
    """Deterministic, single-request governed plugin runtime."""
    def __init__(self, *, kyvernex_version: str, instance_id: str | None = None) -> None:
        if not kyvernex_version:
            raise ValueError("kyvernex_version must be non-empty")
        self._identity = PluginIdentity(PLUGIN_ID, PLUGIN_API_VERSION, kyvernex_version, instance_id or uuid4().hex)
        self._state = PluginState.CREATED
        self._config: PluginConfiguration | None = None
        self._adapter: PluginHostAdapter | None = None
        self._capabilities: frozenset[str] = frozenset()
        self._seen_request_ids: set[str] = set()
        self._current_request_id: str | None = None
        self._last_completed_status: str | None = None
        self._degraded_reason: str | None = None
        self._adapter_shutdown = False
        self._lock = RLock()

    @property
    def state(self) -> PluginState:
        return self._state

    @property
    def identity(self) -> PluginIdentity:
        return self._identity

    @property
    def configuration(self) -> PluginConfiguration | None:
        return self._config

    def _transition(self, operation: str) -> None:
        target = _ALLOWED_TRANSITIONS.get((self._state, operation))
        if target is None:
            raise PluginRuntimeError("INVALID_LIFECYCLE_TRANSITION", f"Operation {operation!r} is not allowed from state {self._state.value}", category=PluginErrorCategory.LIFECYCLE, details={"state": self._state.value, "operation": operation})
        self._state = target

    def _plugin_metadata(self) -> dict[str, str]:
        return {"plugin_id": self._identity.plugin_id, "plugin_api_version": self._identity.plugin_api_version, "kyvernex_version": self._identity.kyvernex_version}

    def initialize(self, config: Mapping[str, Any], adapter: PluginHostAdapter) -> dict[str, Any]:
        with self._lock:
            if self._state is not PluginState.CREATED:
                self._transition("initialize")
            if not isinstance(adapter, PluginHostAdapter):
                raise PluginRuntimeError("ADAPTER_CONTRACT_VIOLATION", "Host adapter does not implement the required protocol", category=PluginErrorCategory.ADAPTER)
            try:
                parsed = PluginConfiguration.load(config)
            except PluginConfigurationError as exc:
                category = PluginErrorCategory.COMPATIBILITY if exc.code == "INCOMPATIBLE_PLUGIN_API" else exc.category
                raise PluginRuntimeError(exc.code, str(exc), category=category, details=exc.details) from exc
            adapter_capabilities = adapter.capabilities()
            if not isinstance(adapter_capabilities, set) or not all(isinstance(item, str) and item for item in adapter_capabilities):
                raise PluginRuntimeError("ADAPTER_CONTRACT_VIOLATION", "Adapter capabilities must be returned as set[str]", category=PluginErrorCategory.ADAPTER)
            self._config = parsed
            self._adapter = adapter
            self._capabilities = frozenset(parsed.allowed_capabilities).intersection(adapter_capabilities)
            self._transition("initialize")
            return self.status()

    def validate(self) -> dict[str, Any]:
        with self._lock:
            if self._state is not PluginState.INITIALIZED:
                self._transition("validate")
            if self._adapter is None or self._config is None:
                self._state = PluginState.DEGRADED
                self._degraded_reason = "Runtime integrity data is missing"
                raise PluginRuntimeError("RUNTIME_DEGRADED", self._degraded_reason, category=PluginErrorCategory.INTEGRITY)
            try:
                self._adapter.health()
            except Exception as exc:
                raise PluginRuntimeError("ADAPTER_CONTRACT_VIOLATION", "Adapter health check failed", category=PluginErrorCategory.ADAPTER, details={"exception_type": type(exc).__name__}) from exc
            self._transition("validate")
            return self.status()

    def _response(self, *, request_id: str, status: PluginResponseStatus, result: Any, error: GovernedPluginError | None, decision: PluginDecision, started_at: str, execution_id: str | None) -> dict[str, Any]:
        return PluginResponse(request_id, status, result, error, decision, PluginEvidence(execution_id, (), started_at, utc_timestamp()), self._plugin_metadata()).to_dict()

    def execute(self, request: Mapping[str, Any]) -> dict[str, Any]:
        with self._lock:
            if self._state is not PluginState.READY:
                raise PluginRuntimeError("PLUGIN_NOT_READY", "Plugin runtime is not ready for execution", category=PluginErrorCategory.LIFECYCLE, details={"state": self._state.value})
            if self._adapter is None or self._config is None:
                self._state = PluginState.DEGRADED
                self._degraded_reason = "Adapter or configuration missing at execution boundary"
                raise PluginRuntimeError("RUNTIME_DEGRADED", self._degraded_reason, category=PluginErrorCategory.INTEGRITY)
            try:
                parsed = parse_plugin_request(request, max_timeout_seconds=self._config.timeout_seconds, max_output_bytes=self._config.max_output_bytes)
            except PluginContractError as exc:
                raise PluginRuntimeError(exc.error.code, exc.error.message, category=exc.error.category, retryable=exc.error.retryable, details=exc.error.details) from exc
            if parsed.request_id in self._seen_request_ids:
                raise PluginRuntimeError("DUPLICATE_REQUEST_ID", "request_id has already been used by this runtime instance", category=PluginErrorCategory.VALIDATION, details={"request_id": parsed.request_id})
            self._seen_request_ids.add(parsed.request_id)
            started_at = utc_timestamp()
            decision = decide_request(parsed, self._capabilities)
            if not decision.authorized:
                self._last_completed_status = PluginResponseStatus.BLOCKED.value
                return self._response(request_id=parsed.request_id, status=PluginResponseStatus.BLOCKED, result=None, error=GovernedPluginError(decision.reason, "Request was blocked by the governed authorization boundary", PluginErrorCategory.AUTHORIZATION), decision=decision, started_at=started_at, execution_id=None)
            self._current_request_id = parsed.request_id
            self._transition("execute")
            execution_id = new_execution_id()
            authority = {
                "principal": parsed.authorization.principal,
                "grants": list(parsed.authorization.grants),
                "capabilities": list(parsed.requested_capabilities),
                "limits": {"timeout_seconds": parsed.limits.timeout_seconds, "max_output_bytes": parsed.limits.max_output_bytes},
                "configured_authority": dict(self._config.authority_summary()),
            }
            try:
                result = self._adapter.invoke(parsed.to_adapter_request(), authority)
            except Exception as exc:
                self._last_completed_status = PluginResponseStatus.FAILED.value
                self._transition("complete")
                return self._response(request_id=parsed.request_id, status=PluginResponseStatus.FAILED, result=None, error=GovernedPluginError("EXECUTION_FAILED", "Adapter execution failed", PluginErrorCategory.EXECUTION, details={"exception_type": type(exc).__name__}), decision=decision, started_at=started_at, execution_id=execution_id)
            else:
                self._last_completed_status = PluginResponseStatus.SUCCEEDED.value
                self._transition("complete")
                return self._response(request_id=parsed.request_id, status=PluginResponseStatus.SUCCEEDED, result=result, error=None, decision=decision, started_at=started_at, execution_id=execution_id)
            finally:
                self._current_request_id = None

    def status(self) -> dict[str, Any]:
        with self._lock:
            adapter_health: Any = None
            if self._adapter is not None and self._state is not PluginState.SHUTDOWN:
                try:
                    adapter_health = self._adapter.health()
                except Exception:
                    adapter_health = {"status": "UNAVAILABLE"}
            authority = dict(self._config.authority_summary()) if self._config else {"filesystem": {"read_roots": (), "write_roots": ()}, "network": {"enabled": False, "allowed_hosts": ()}, "process": {"enabled": False, "allowed_commands": ()}, "repository": "FORBIDDEN"}
            return {
                "plugin": {**self._plugin_metadata(), "instance_id": self._identity.instance_id},
                "state": self._state.value,
                "capabilities": sorted(self._capabilities),
                "authority": authority,
                "current_request_id": self._current_request_id,
                "degraded_reason": self._degraded_reason,
                "adapter_health": adapter_health,
                "last_completed_request_status": self._last_completed_status,
            }

    def shutdown(self) -> dict[str, Any]:
        with self._lock:
            if self._state is PluginState.SHUTDOWN:
                return self.status()
            if self._state is PluginState.EXECUTING:
                raise PluginRuntimeError("INVALID_LIFECYCLE_TRANSITION", "Shutdown during active execution is not supported by contract 1.0.0", category=PluginErrorCategory.LIFECYCLE)
            if self._adapter is not None and not self._adapter_shutdown:
                self._adapter.shutdown()
                self._adapter_shutdown = True
            self._transition("shutdown")
            self._capabilities = frozenset()
            self._config = None
            return self.status()
