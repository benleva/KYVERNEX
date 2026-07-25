"""Usable product facade for the KYVERNEX governed in-process plugin."""
from __future__ import annotations

from types import MappingProxyType
from typing import Any, Callable, Mapping
from uuid import uuid4

from .plugin_adapter import InProcessCallableAdapter
from .plugin_runtime import KyvernexPluginRuntime


class KyvernexPlugin:
    """Small host-facing API that owns the runtime and its single adapter.

    The host supplies one Python callable. The facade initializes the bounded
    adapter and deterministic runtime, then exposes a compact execute/status/
    shutdown product interface.
    """

    def __init__(
        self,
        handler: Callable[[Mapping[str, Any], Mapping[str, Any]], Any],
        *,
        capabilities: set[str] | frozenset[str] | None = None,
        configuration: Mapping[str, Any] | None = None,
        kyvernex_version: str = "1.2.0.dev0",
        instance_id: str | None = None,
    ) -> None:
        declared = frozenset(capabilities or {"governed.execute"})
        config = dict(configuration or {})
        config.setdefault("plugin_api_version", "1.0.0")
        config.setdefault("allowed_capabilities", sorted(declared))

        self._adapter = InProcessCallableAdapter(handler, capabilities=declared)
        self._runtime = KyvernexPluginRuntime(
            kyvernex_version=kyvernex_version,
            instance_id=instance_id,
        )
        self._runtime.initialize(config, self._adapter)
        self._runtime.validate()

    @property
    def runtime(self) -> KyvernexPluginRuntime:
        return self._runtime

    def execute(
        self,
        input_data: Mapping[str, Any],
        *,
        principal: str,
        grants: set[str] | frozenset[str] | None = None,
        requested_capabilities: set[str] | frozenset[str] | None = None,
        context: Mapping[str, Any] | None = None,
        request_id: str | None = None,
        timeout_seconds: int = 30,
        max_output_bytes: int = 1_048_576,
    ) -> dict[str, Any]:
        """Execute one governed request through the complete plugin path."""
        if not isinstance(input_data, Mapping):
            raise TypeError("input_data must be a mapping")
        if not isinstance(principal, str) or not principal:
            raise ValueError("principal must be a non-empty string")

        requested = frozenset(requested_capabilities or {"governed.execute"})
        effective_grants = frozenset(grants if grants is not None else requested)
        request = {
            "request_id": request_id or uuid4().hex,
            "operation": "governed.execute",
            "input": dict(input_data),
            "context": dict(context or {}),
            "requested_capabilities": sorted(requested),
            "authorization": {
                "principal": principal,
                "grants": sorted(effective_grants),
            },
            "limits": {
                "timeout_seconds": timeout_seconds,
                "max_output_bytes": max_output_bytes,
            },
        }
        return self._runtime.execute(request)

    def status(self) -> Mapping[str, Any]:
        """Return a read-only snapshot of the current plugin status."""
        return MappingProxyType(self._runtime.status())

    def shutdown(self) -> Mapping[str, Any]:
        """Shut down the product facade and its adapter idempotently."""
        return MappingProxyType(self._runtime.shutdown())

    def __enter__(self) -> "KyvernexPlugin":
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.shutdown()