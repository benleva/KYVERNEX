"""Universal host bridge for AI systems invoking the KYVERNEX plugin."""
from __future__ import annotations

from typing import Any, Callable, Mapping

from .ai_formats import export_manifest
from .plugin import KyvernexPlugin


class KyvernexAIBridge:
    """Expose one provider-neutral AI tool over the governed KYVERNEX plugin."""

    tool_name = "kyvernex_execute"
    tool_description = "Execute one governed request through the KYVERNEX plugin."

    def __init__(
        self,
        handler: Callable[[Mapping[str, Any], Mapping[str, Any]], Any],
        *,
        principal: str = "ai-host",
        capabilities: set[str] | frozenset[str] | None = None,
        configuration: Mapping[str, Any] | None = None,
    ) -> None:
        if not isinstance(principal, str) or not principal:
            raise ValueError("principal must be a non-empty string")
        self._principal = principal
        self._plugin = KyvernexPlugin(
            handler,
            capabilities=capabilities,
            configuration=configuration,
        )

    def manifest(self) -> dict[str, Any]:
        """Return the canonical provider-neutral JSON Schema tool definition."""
        return {
            "name": self.tool_name,
            "description": self.tool_description,
            "input_schema": {
                "type": "object",
                "additionalProperties": False,
                "required": ["input"],
                "properties": {
                    "input": {"type": "object"},
                    "context": {"type": "object"},
                    "request_id": {"type": "string", "minLength": 1},
                },
            },
        }

    def manifest_for(self, provider: str) -> dict[str, Any]:
        """Translate the canonical manifest without changing execution behavior."""
        return export_manifest(self.manifest(), provider)

    def invoke(self, arguments: Mapping[str, Any]) -> dict[str, Any]:
        """Invoke the single AI tool with provider-neutral arguments."""
        if not isinstance(arguments, Mapping):
            raise TypeError("arguments must be a mapping")
        allowed = {"input", "context", "request_id"}
        unknown = sorted(set(arguments) - allowed)
        if unknown:
            raise ValueError(f"unknown AI bridge fields: {', '.join(unknown)}")
        input_data = arguments.get("input")
        if not isinstance(input_data, Mapping):
            raise ValueError("arguments.input must be an object")
        context = arguments.get("context", {})
        if not isinstance(context, Mapping):
            raise ValueError("arguments.context must be an object")
        request_id = arguments.get("request_id")
        if request_id is not None and (not isinstance(request_id, str) or not request_id):
            raise ValueError("arguments.request_id must be a non-empty string")
        return self._plugin.execute(
            input_data,
            principal=self._principal,
            context=context,
            request_id=request_id,
        )

    def status(self) -> Mapping[str, Any]:
        return self._plugin.status()

    def shutdown(self) -> Mapping[str, Any]:
        return self._plugin.shutdown()

    def __enter__(self) -> "KyvernexAIBridge":
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.shutdown()
