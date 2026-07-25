"""Bounded KYVERNEX plugin lifecycle runtime.

This module implements the M6-W002 lifecycle state machine only. Governed host
request, response and authorization contracts are added by subsequent M6 work
items. The runtime therefore grants no execution authority by itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from threading import RLock
from types import MappingProxyType
from typing import Any, Mapping, Protocol, runtime_checkable
from uuid import uuid4


PLUGIN_ID = "kyvernex.plugin.runtime"
PLUGIN_API_VERSION = "1.0.0"


class PluginState(str, Enum):
    CREATED = "CREATED"
    INITIALIZED = "INITIALIZED"
    READY = "READY"
    EXECUTING = "EXECUTING"
    DEGRADED = "DEGRADED"
    SHUTDOWN = "SHUTDOWN"


class PluginErrorCategory(str, Enum):
    VALIDATION = "VALIDATION"
    LIFECYCLE = "LIFECYCLE"
    ADAPTER = "ADAPTER"
    EXECUTION = "EXECUTION"
    INTEGRITY = "INTEGRITY"
    COMPATIBILITY = "COMPATIBILITY"


class PluginRuntimeError(RuntimeError):
    """Structured fail-closed plugin runtime error."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        category: PluginErrorCategory,
        retryable: bool = False,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.category = category
        self.retryable = retryable
        self.details = dict(details or {})

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": str(self),
            "category": self.category.value,
            "retryable": self.retryable,
            "details": dict(self.details),
            "cause_id": None,
        }


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


_ALLOWED_TRANSITIONS: Mapping[tuple[PluginState, str], PluginState] = MappingProxyType(
    {
        (PluginState.CREATED, "initialize"): PluginState.INITIALIZED,
        (PluginState.INITIALIZED, "validate"): PluginState.READY,
        (PluginState.READY, "execute"): PluginState.EXECUTING,
        (PluginState.EXECUTING, "complete"): PluginState.READY,
        (PluginState.EXECUTING, "integrity_failure"): PluginState.DEGRADED,
        (PluginState.CREATED, "shutdown"): PluginState.SHUTDOWN,
        (PluginState.INITIALIZED, "shutdown"): PluginState.SHUTDOWN,
        (PluginState.READY, "shutdown"): PluginState.SHUTDOWN,
        (PluginState.DEGRADED, "shutdown"): PluginState.SHUTDOWN,
    }
)


class KyvernexPluginRuntime:
    """Deterministic, single-request plugin lifecycle state machine.

    M6-W002 intentionally does not implement governance authorization. Calling
    ``execute`` exercises the lifecycle boundary and delegates to the adapter
    only when the caller explicitly supplies an already-bounded authority map.
    Later M6 work items replace this narrow bridge with the full governed host
    request and response contract.
    """

    def __init__(self, *, kyvernex_version: str, instance_id: str | None = None) -> None:
        if not kyvernex_version:
            raise ValueError("kyvernex_version must be non-empty")
        self._identity = PluginIdentity(
            plugin_id=PLUGIN_ID,
            plugin_api_version=PLUGIN_API_VERSION,
            kyvernex_version=kyvernex_version,
            instance_id=instance_id or uuid4().hex,
        )
        self._state = PluginState.CREATED
        self._config: dict[str, Any] | None = None
        self._adapter: PluginHostAdapter | None = None
        self._capabilities: frozenset[str] = frozenset()
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

    def _transition(self, operation: str) -> None:
        target = _ALLOWED_TRANSITIONS.get((self._state, operation))
        if target is None:
            raise PluginRuntimeError(
                "INVALID_LIFECYCLE_TRANSITION",
                f"Operation {operation!r} is not allowed from state {self._state.value}",
                category=PluginErrorCategory.LIFECYCLE,
                details={"state": self._state.value, "operation": operation},
            )
        self._state = target

    def initialize(self, config: Mapping[str, Any], adapter: PluginHostAdapter) -> dict[str, Any]:
        with self._lock:
            if self._state is not PluginState.CREATED:
                self._transition("initialize")
            if not isinstance(config, Mapping):
                raise PluginRuntimeError(
                    "INVALID_CONFIGURATION",
                    "Plugin configuration must be a mapping",
                    category=PluginErrorCategory.VALIDATION,
                )
            if not isinstance(adapter, PluginHostAdapter):
                raise PluginRuntimeError(
                    "ADAPTER_CONTRACT_VIOLATION",
                    "Host adapter does not implement the required protocol",
                    category=PluginErrorCategory.ADAPTER,
                )
            api_version = config.get("plugin_api_version", PLUGIN_API_VERSION)
            if api_version != PLUGIN_API_VERSION:
                raise PluginRuntimeError(
                    "INCOMPATIBLE_PLUGIN_API",
                    "Unsupported plugin API version",
                    category=PluginErrorCategory.COMPATIBILITY,
                    details={"requested": api_version, "supported": PLUGIN_API_VERSION},
                )
            allowed = config.get("allowed_capabilities", [])
            if not isinstance(allowed, list) or not all(isinstance(item, str) for item in allowed):
                raise PluginRuntimeError(
                    "INVALID_CONFIGURATION",
                    "allowed_capabilities must be a list of strings",
                    category=PluginErrorCategory.VALIDATION,
                )
            adapter_capabilities = adapter.capabilities()
            if not isinstance(adapter_capabilities, set) or not all(
                isinstance(item, str) for item in adapter_capabilities
            ):
                raise PluginRuntimeError(
                    "ADAPTER_CONTRACT_VIOLATION",
                    "Adapter capabilities must be returned as set[str]",
                    category=PluginErrorCategory.ADAPTER,
                )
            self._config = dict(config)
            self._adapter = adapter
            self._capabilities = frozenset(allowed).intersection(adapter_capabilities)
            self._transition("initialize")
            return self.status()

    def validate(self) -> dict[str, Any]:
        with self._lock:
            if self._state is not PluginState.INITIALIZED:
                self._transition("validate")
            if self._adapter is None or self._config is None:
                self._state = PluginState.DEGRADED
                self._degraded_reason = "Runtime integrity data is missing"
                raise PluginRuntimeError(
                    "RUNTIME_DEGRADED",
                    self._degraded_reason,
                    category=PluginErrorCategory.INTEGRITY,
                )
            try:
                self._adapter.health()
            except Exception as exc:
                raise PluginRuntimeError(
                    "ADAPTER_CONTRACT_VIOLATION",
                    "Adapter health check failed",
                    category=PluginErrorCategory.ADAPTER,
                    details={"exception_type": type(exc).__name__},
                ) from exc
            self._transition("validate")
            return self.status()

    def execute(
        self,
        request: Mapping[str, Any],
        *,
        authority: Mapping[str, Any] | None = None,
    ) -> Any:
        with self._lock:
            if self._state is not PluginState.READY:
                raise PluginRuntimeError(
                    "PLUGIN_NOT_READY",
                    "Plugin runtime is not ready for execution",
                    category=PluginErrorCategory.LIFECYCLE,
                    details={"state": self._state.value},
                )
            if self._adapter is None:
                self._state = PluginState.DEGRADED
                self._degraded_reason = "Adapter missing at execution boundary"
                raise PluginRuntimeError(
                    "RUNTIME_DEGRADED",
                    self._degraded_reason,
                    category=PluginErrorCategory.INTEGRITY,
                )
            request_id = request.get("request_id") if isinstance(request, Mapping) else None
            self._current_request_id = request_id if isinstance(request_id, str) else None
            self._transition("execute")
            try:
                result = self._adapter.invoke(request, dict(authority or {}))
            except Exception as exc:
                self._last_completed_status = "FAILED"
                self._transition("complete")
                raise PluginRuntimeError(
                    "EXECUTION_FAILED",
                    "Adapter execution failed",
                    category=PluginErrorCategory.EXECUTION,
                    details={"exception_type": type(exc).__name__},
                ) from exc
            else:
                self._last_completed_status = "SUCCEEDED"
                self._transition("complete")
                return result
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
            return {
                "plugin": {
                    "plugin_id": self._identity.plugin_id,
                    "plugin_api_version": self._identity.plugin_api_version,
                    "kyvernex_version": self._identity.kyvernex_version,
                    "instance_id": self._identity.instance_id,
                },
                "state": self._state.value,
                "capabilities": sorted(self._capabilities),
                "authority": {
                    "filesystem": "NONE",
                    "network": "DISABLED",
                    "process": "DISABLED",
                    "repository": "FORBIDDEN",
                },
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
                raise PluginRuntimeError(
                    "INVALID_LIFECYCLE_TRANSITION",
                    "Shutdown during active execution is not supported by contract 1.0.0",
                    category=PluginErrorCategory.LIFECYCLE,
                )
            adapter = self._adapter
            if adapter is not None and not self._adapter_shutdown:
                adapter.shutdown()
                self._adapter_shutdown = True
            self._transition("shutdown")
            self._capabilities = frozenset()
            self._config = None
            return self.status()
