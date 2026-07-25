from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


class AIManifestFormatError(ValueError):
    pass


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


def export_manifest(manifest: Mapping[str, Any], provider: str) -> dict[str, Any]:
    name, description, schema = _parts(manifest)
    provider = provider.strip().lower()
    if provider == "canonical":
        return {"name": name, "description": description, "input_schema": schema}
    if provider == "openai":
        return {"type": "function", "function": {"name": name, "description": description, "parameters": schema, "strict": True}}
    if provider == "anthropic":
        return {"name": name, "description": description, "input_schema": schema}
    if provider == "gemini":
        return {"functionDeclarations": [{"name": name, "description": description, "parameters": schema}]}
    raise AIManifestFormatError("provider must be canonical, openai, anthropic, or gemini")
