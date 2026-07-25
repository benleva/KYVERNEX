"""Provider-shaped exports for the canonical KYVERNEX AI tool manifest."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


class AIManifestFormatError(ValueError):
    """Raised when a canonical manifest or provider name is invalid."""


def _parts(manifest: Mapping[str, Any]) -> tuple[str, str, dict[str, Any]]:
    if not isinstance(manifest, Mapping):
        raise AIManifestFormatError("manifest must be a mapping")
    unknown = sorted(set(manifest) - {"name", "description", "input_schema"})
    if unknown:
        raise AIManifestFormatError(f"unknown manifest fields: {', '.join(unknown)}")
    name = manifest.get("name")
    description = manifest.get("description")
    schema = manifest.get("input_schema")
    if not isinstance(name, str) or not name:
        raise AIManifestFormatError("manifest.name must be a non-empty string")
    if not isinstance(description, str) or not description:
        raise AIManifestFormatError("manifest.description must be a non-empty string")
    if not isinstance(schema, Mapping):
        raise AIManifestFormatError("manifest.input_schema must be an object")
    return name, description, deepcopy(dict(schema))


def export_canonical_tool(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Return an isolated copy of the canonical KYVERNEX tool manifest."""
    name, description, schema = _parts(manifest)
    return {"name": name, "description": description, "input_schema": schema}


def export_openai_tool(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Return the canonical tool in OpenAI function-tool shape."""
    name, description, schema = _parts(manifest)
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": schema,
            "strict": True,
        },
    }


def export_anthropic_tool(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Return the canonical tool in Anthropic tool shape."""
    name, description, schema = _parts(manifest)
    return {"name": name, "description": description, "input_schema": schema}


def export_gemini_tools(manifest: Mapping[str, Any]) -> dict[str, Any]:
    """Return the canonical tool in Gemini function-declarations shape."""
    name, description, schema = _parts(manifest)
    return {
        "functionDeclarations": [
            {"name": name, "description": description, "parameters": schema}
        ]
    }


def export_manifest(manifest: Mapping[str, Any], provider: str) -> dict[str, Any]:
    """Export one canonical manifest through the selected provider shape."""
    if not isinstance(provider, str):
        raise AIManifestFormatError("provider must be a string")
    normalized = provider.strip().lower()
    exporters = {
        "canonical": export_canonical_tool,
        "openai": export_openai_tool,
        "anthropic": export_anthropic_tool,
        "gemini": export_gemini_tools,
    }
    try:
        exporter = exporters[normalized]
    except KeyError as exc:
        raise AIManifestFormatError(
            "provider must be canonical, openai, anthropic, or gemini"
        ) from exc
    return exporter(manifest)
