"""Fail-closed configuration for the KYVERNEX plugin runtime."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from .plugin_contracts import PluginErrorCategory

PLUGIN_API_VERSION = "1.0.0"
_ALLOWED_TOP = frozenset({"plugin_api_version", "instance_id", "allowed_capabilities", "filesystem", "network", "process", "limits", "audit"})


class PluginConfigurationError(ValueError):
    def __init__(self, code: str, message: str, *, details: Mapping[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.category = PluginErrorCategory.VALIDATION
        self.details = dict(details or {})


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise PluginConfigurationError("INVALID_CONFIGURATION", f"{name} must be a mapping")
    return value


def _known_fields(value: Mapping[str, Any], allowed: set[str] | frozenset[str], name: str) -> None:
    unknown = sorted(set(value) - set(allowed))
    if unknown:
        raise PluginConfigurationError("UNKNOWN_CONFIGURATION_FIELD", f"Unknown {name} field", details={"fields": unknown})


def _string_list(value: Any, name: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise PluginConfigurationError("INVALID_CONFIGURATION", f"{name} must be a list of non-empty strings")
    if len(value) != len(set(value)):
        raise PluginConfigurationError("INVALID_CONFIGURATION", f"{name} must not contain duplicates")
    return tuple(value)


def _absolute_roots(value: Any, name: str) -> tuple[str, ...]:
    roots = _string_list(value, name)
    normalized: list[str] = []
    for raw in roots:
        path = Path(raw).expanduser()
        if not path.is_absolute():
            raise PluginConfigurationError("INVALID_CONFIGURATION", f"{name} paths must be absolute", details={"path": raw})
        resolved = str(path.resolve(strict=False))
        if resolved != raw.rstrip("/") and raw != "/":
            raise PluginConfigurationError("INVALID_CONFIGURATION", f"{name} paths must already be normalized", details={"path": raw, "normalized": resolved})
        normalized.append(resolved)
    return tuple(normalized)


def _positive_int(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise PluginConfigurationError("INVALID_CONFIGURATION", f"{name} must be a positive integer")
    return value


@dataclass(frozen=True)
class PluginConfiguration:
    plugin_api_version: str
    instance_id: str | None
    allowed_capabilities: tuple[str, ...]
    filesystem_read_roots: tuple[str, ...]
    filesystem_write_roots: tuple[str, ...]
    network_enabled: bool
    allowed_hosts: tuple[str, ...]
    process_enabled: bool
    allowed_commands: tuple[str, ...]
    timeout_seconds: int
    max_output_bytes: int
    audit_required: bool
    audit_include_request_input: bool

    @classmethod
    def load(cls, raw: Mapping[str, Any]) -> "PluginConfiguration":
        data = _mapping(raw, "configuration")
        _known_fields(data, _ALLOWED_TOP, "configuration")
        version = data.get("plugin_api_version", PLUGIN_API_VERSION)
        if version != PLUGIN_API_VERSION:
            raise PluginConfigurationError("INCOMPATIBLE_PLUGIN_API", "Unsupported plugin API version", details={"requested": version, "supported": PLUGIN_API_VERSION})
        instance_id = data.get("instance_id")
        if instance_id is not None and (not isinstance(instance_id, str) or not instance_id):
            raise PluginConfigurationError("INVALID_CONFIGURATION", "instance_id must be a non-empty string")
        capabilities = _string_list(data.get("allowed_capabilities", []), "allowed_capabilities")

        filesystem = _mapping(data.get("filesystem", {}), "filesystem")
        _known_fields(filesystem, {"read_roots", "write_roots"}, "filesystem")
        read_roots = _absolute_roots(filesystem.get("read_roots", []), "filesystem.read_roots")
        write_roots = _absolute_roots(filesystem.get("write_roots", []), "filesystem.write_roots")

        network = _mapping(data.get("network", {}), "network")
        _known_fields(network, {"enabled", "allowed_hosts"}, "network")
        network_enabled = network.get("enabled", False)
        if not isinstance(network_enabled, bool):
            raise PluginConfigurationError("INVALID_CONFIGURATION", "network.enabled must be boolean")
        hosts = _string_list(network.get("allowed_hosts", []), "network.allowed_hosts")
        if any("*" in host for host in hosts):
            raise PluginConfigurationError("INVALID_CONFIGURATION", "Wildcard hosts are forbidden")
        if not network_enabled and hosts:
            raise PluginConfigurationError("AUTHORITY_EXCEEDED", "allowed_hosts require network.enabled=true")

        process = _mapping(data.get("process", {}), "process")
        _known_fields(process, {"enabled", "allowed_commands"}, "process")
        process_enabled = process.get("enabled", False)
        if not isinstance(process_enabled, bool):
            raise PluginConfigurationError("INVALID_CONFIGURATION", "process.enabled must be boolean")
        commands = _string_list(process.get("allowed_commands", []), "process.allowed_commands")
        if not process_enabled and commands:
            raise PluginConfigurationError("AUTHORITY_EXCEEDED", "allowed_commands require process.enabled=true")

        limits = _mapping(data.get("limits", {}), "limits")
        _known_fields(limits, {"timeout_seconds", "max_output_bytes"}, "limits")
        timeout = _positive_int(limits.get("timeout_seconds", 30), "limits.timeout_seconds")
        output = _positive_int(limits.get("max_output_bytes", 1048576), "limits.max_output_bytes")

        audit = _mapping(data.get("audit", {}), "audit")
        _known_fields(audit, {"required", "include_request_input"}, "audit")
        audit_required = audit.get("required", True)
        include_input = audit.get("include_request_input", False)
        if not isinstance(audit_required, bool) or not isinstance(include_input, bool):
            raise PluginConfigurationError("INVALID_CONFIGURATION", "audit flags must be boolean")
        if not audit_required:
            raise PluginConfigurationError("AUTHORITY_EXCEEDED", "audit.required cannot be disabled in contract 1.0.0")

        return cls(version, instance_id, capabilities, read_roots, write_roots, network_enabled, hosts, process_enabled, commands, timeout, output, audit_required, include_input)

    def authority_summary(self) -> Mapping[str, Any]:
        return MappingProxyType({
            "filesystem": {"read_roots": self.filesystem_read_roots, "write_roots": self.filesystem_write_roots},
            "network": {"enabled": self.network_enabled, "allowed_hosts": self.allowed_hosts},
            "process": {"enabled": self.process_enabled, "allowed_commands": self.allowed_commands},
            "repository": "FORBIDDEN",
        })
