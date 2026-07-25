"""Explicit handler loading for the KYVERNEX product plugin."""
from __future__ import annotations

from importlib import import_module
from typing import Any, Callable, Mapping


PluginHandler = Callable[[Mapping[str, Any], Mapping[str, Any]], Any]


class PluginHandlerLoadError(RuntimeError):
    """Raised when a requested plugin handler cannot be loaded safely."""


def load_plugin_handler(reference: str) -> PluginHandler:
    """Load one explicit ``module:attribute`` Python callable.

    The loader performs no discovery, scanning, fallback lookup or environment
    expansion. The caller must provide the exact importable module and attribute.
    """
    if not isinstance(reference, str) or not reference.strip():
        raise PluginHandlerLoadError("handler reference must be a non-empty module:attribute string")
    if reference.count(":") != 1:
        raise PluginHandlerLoadError("handler reference must use exactly one ':' separator")

    module_name, attribute_name = (part.strip() for part in reference.split(":", 1))
    if not module_name or not attribute_name:
        raise PluginHandlerLoadError("handler reference requires both module and attribute")
    if attribute_name.startswith("_"):
        raise PluginHandlerLoadError("private handler attributes are not loadable")

    try:
        module = import_module(module_name)
    except Exception as exc:
        raise PluginHandlerLoadError(f"cannot import handler module {module_name!r}") from exc

    try:
        handler = getattr(module, attribute_name)
    except AttributeError as exc:
        raise PluginHandlerLoadError(
            f"handler attribute {attribute_name!r} does not exist in module {module_name!r}"
        ) from exc

    if not callable(handler):
        raise PluginHandlerLoadError("loaded handler attribute is not callable")
    return handler


def load_handler(reference: str) -> PluginHandler:
    """Compatibility name for :func:`load_plugin_handler`.

    All command-line products use the same strict loader implementation. This
    alias preserves the shorter name without creating a second loading path.
    """
    return load_plugin_handler(reference)
