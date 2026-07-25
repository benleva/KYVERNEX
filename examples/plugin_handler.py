"""Minimal host handler for the installed ``kyvernex-plugin`` command."""
from __future__ import annotations

from typing import Any, Mapping


def handle(request: Mapping[str, Any], authority: Mapping[str, Any]) -> dict[str, Any]:
    """Return a small application result from a governed plugin request."""
    input_data = dict(request.get("input", {}))
    return {
        "message": input_data.get("message", ""),
        "principal": authority.get("principal"),
        "governed": True,
    }
