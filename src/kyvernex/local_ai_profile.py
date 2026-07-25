"""Strict JSON profile loading for the local KYVERNEX desktop launcher."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

_ALLOWED_FIELDS = frozenset({"handler", "principal", "port", "open_browser"})


def load_local_ai_profile(path: str | Path) -> dict[str, Any]:
    """Load one explicit local JSON profile without discovery or environment reads."""
    profile_path = Path(path)
    try:
        payload = json.loads(profile_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"cannot read profile: {profile_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"profile is not valid JSON: {profile_path}") from exc
    if not isinstance(payload, Mapping):
        raise ValueError("profile JSON must be an object")
    unknown = sorted(set(payload) - _ALLOWED_FIELDS)
    if unknown:
        raise ValueError(f"unknown profile fields: {', '.join(unknown)}")

    result = dict(payload)
    handler = result.get("handler")
    if handler is not None and (not isinstance(handler, str) or not handler.strip()):
        raise ValueError("profile.handler must be a non-empty string")
    principal = result.get("principal")
    if principal is not None and (not isinstance(principal, str) or not principal.strip()):
        raise ValueError("profile.principal must be a non-empty string")
    port = result.get("port")
    if port is not None and (not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535):
        raise ValueError("profile.port must be an integer between 1 and 65535")
    open_browser = result.get("open_browser")
    if open_browser is not None and not isinstance(open_browser, bool):
        raise ValueError("profile.open_browser must be a boolean")
    return result
