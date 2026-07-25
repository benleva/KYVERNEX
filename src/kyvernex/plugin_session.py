"""Persistent local session for repeated KYVERNEX plugin calls."""
from __future__ import annotations

from types import MappingProxyType
from typing import Any, Callable, Mapping

from .plugin import KyvernexPlugin


class KyvernexPluginSession:
    """Keep one product plugin alive across multiple governed executions."""

    def __init__(
        self,
        handler: Callable[[Mapping[str, Any], Mapping[str, Any]], Any],
        *,
        principal: str,
        capabilities: set[str] | frozenset[str] | None = None,
        configuration: Mapping[str, Any] | None = None,
        context: Mapping[str, Any] | None = None,
        kyvernex_version: str = "1.2.0.dev0",
        instance_id: str | None = None,
    ) -> None:
        if not isinstance(principal, str) or not principal:
            raise ValueError("principal must be a non-empty string")
        self._principal = principal
        self._capabilities = frozenset(capabilities or {"governed.execute"})
        self._context = MappingProxyType(dict(context or {}))
        self._plugin = KyvernexPlugin(
            handler,
            capabilities=self._capabilities,
            configuration=configuration,
            kyvernex_version=kyvernex_version,
            instance_id=instance_id,
        )
        self._sequence = 0
        self._closed = False

    @property
    def sequence(self) -> int:
        return self._sequence

    @property
    def closed(self) -> bool:
        return self._closed

    def execute(
        self,
        input_data: Mapping[str, Any],
        *,
        context: Mapping[str, Any] | None = None,
        request_id: str | None = None,
        timeout_seconds: int = 30,
        max_output_bytes: int = 1_048_576,
    ) -> dict[str, Any]:
        """Execute one request while reusing the same initialized plugin instance."""
        if self._closed:
            raise RuntimeError("plugin session is closed")
        merged_context = dict(self._context)
        merged_context.update(dict(context or {}))
        self._sequence += 1
        merged_context.setdefault("session_sequence", self._sequence)
        return self._plugin.execute(
            input_data,
            principal=self._principal,
            grants=self._capabilities,
            requested_capabilities=self._capabilities,
            context=merged_context,
            request_id=request_id,
            timeout_seconds=timeout_seconds,
            max_output_bytes=max_output_bytes,
        )

    def status(self) -> Mapping[str, Any]:
        status = dict(self._plugin.status())
        status["session"] = {
            "principal": self._principal,
            "sequence": self._sequence,
            "closed": self._closed,
        }
        return MappingProxyType(status)

    def shutdown(self) -> Mapping[str, Any]:
        if not self._closed:
            self._closed = True
        return self._plugin.shutdown()

    def __enter__(self) -> "KyvernexPluginSession":
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.shutdown()
