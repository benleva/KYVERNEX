from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


class AdapterExecutionError(RuntimeError):
    """Raised when an external AI adapter cannot complete an invocation."""


@dataclass(slots=True, frozen=True)
class AdapterRequest:
    session_id: str
    object_id: str
    content: Any
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class AdapterResponse:
    adapter_name: str
    model: str
    content: Any
    metadata: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class AIAdapter(Protocol):
    """Controlled boundary between KYVERNEX and an external reasoning model."""

    @property
    def name(self) -> str: ...

    def invoke(self, request: AdapterRequest) -> AdapterResponse: ...


class EchoAdapter:
    """Deterministic adapter for development and tests; performs no network call."""

    def __init__(self, *, prefix: str = "ECHO") -> None:
        self._prefix = prefix

    @property
    def name(self) -> str:
        return "echo-adapter"

    def invoke(self, request: AdapterRequest) -> AdapterResponse:
        return AdapterResponse(
            adapter_name=self.name,
            model="deterministic-echo-0.1",
            content=f"{self._prefix}: {request.content}",
            metadata={
                "session_id": request.session_id,
                "object_id": request.object_id,
                "network_used": False,
            },
        )


class FailingAdapter:
    """Deterministic failure adapter used to verify controlled error handling."""

    @property
    def name(self) -> str:
        return "failing-adapter"

    def invoke(self, request: AdapterRequest) -> AdapterResponse:
        raise AdapterExecutionError("ADAPTER_EXECUTION_FAILED")
