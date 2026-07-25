"""Single bounded reference adapter for the M6 minimum shippable plugin."""
from __future__ import annotations

import json
from threading import RLock
from types import MappingProxyType
from typing import Any, Callable, Mapping


class InProcessAdapterError(RuntimeError):
    """Raised when the bounded callable adapter contract is violated."""


class InProcessCallableAdapter:
    """Wrap exactly one host-supplied callable behind the frozen adapter protocol.

    The adapter does not authorize requests, inspect the environment, access external
    systems or expand authority. The runtime must authorize the request before invoke.
    """

    adapter_id = "kyvernex.adapter.in_process_callable"
    adapter_version = "1.0.0"

    def __init__(
        self,
        handler: Callable[[Mapping[str, Any], Mapping[str, Any]], Any],
        *,
        capabilities: set[str] | frozenset[str],
    ) -> None:
        if not callable(handler):
            raise TypeError("handler must be callable")
        if not isinstance(capabilities, (set, frozenset)) or not all(
            isinstance(item, str) and item for item in capabilities
        ):
            raise TypeError("capabilities must be set[str] or frozenset[str]")
        self._handler = handler
        self._capabilities = frozenset(capabilities)
        self._closed = False
        self._invocation_count = 0
        self._lock = RLock()

    def capabilities(self) -> set[str]:
        """Return a defensive copy of the immutable declared capabilities."""
        with self._lock:
            return set(self._capabilities)

    def invoke(self, request: Mapping[str, Any], authority: Mapping[str, Any]) -> Any:
        """Invoke the supplied callable with bounded immutable snapshots."""
        with self._lock:
            if self._closed:
                raise InProcessAdapterError("adapter is shut down")
            if not isinstance(request, Mapping) or not isinstance(authority, Mapping):
                raise InProcessAdapterError("request and authority must be mappings")

            request_snapshot = MappingProxyType(dict(request))
            authority_snapshot = MappingProxyType(dict(authority))
            result = self._handler(request_snapshot, authority_snapshot)
            try:
                json.dumps(result, allow_nan=False)
            except (TypeError, ValueError) as exc:
                raise InProcessAdapterError("handler result must be JSON-serializable") from exc
            self._invocation_count += 1
            return result

    def health(self) -> Mapping[str, Any]:
        """Return bounded, secret-free local health metadata."""
        with self._lock:
            return {
                "status": "SHUTDOWN" if self._closed else "HEALTHY",
                "adapter_id": self.adapter_id,
                "adapter_version": self.adapter_version,
                "invocation_count": self._invocation_count,
            }

    def shutdown(self) -> None:
        """Close the adapter idempotently without invoking host side effects."""
        with self._lock:
            self._closed = True
