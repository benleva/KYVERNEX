"""Reversible symbolic projection for the bounded ARGUS canonical request."""
from __future__ import annotations

import re
from copy import deepcopy
from typing import Any, Mapping


class ArgusSymbolError(ValueError):
    """Raised when canonical data cannot be represented without information loss."""


_PATH_TO_TOKEN: dict[tuple[str, Any], str] = {
    ("authorization", False): "⟦A-⟧",
    ("authorization", True): "⟦A+⟧",
    ("consent", False): "⟦C-⟧",
    ("consent", True): "⟦C+⟧",
    ("domain", "education"): "⟦DE⟧",
    ("domain", "finance"): "⟦DF⟧",
    ("domain", "health"): "⟦DH⟧",
    ("domain", "legal"): "⟦DL⟧",
    ("risk", "critical"): "⟦R4⟧",
    ("risk", "high"): "⟦R3⟧",
    ("risk", "low"): "⟦R1⟧",
    ("risk", "medium"): "⟦R2⟧",
    ("subject.minor", False): "⟦M-⟧",
    ("subject.minor", True): "⟦M+⟧",
}
_TOKEN_TO_PATH: dict[str, tuple[str, Any]] = {token: pair for pair, token in _PATH_TO_TOKEN.items()}
_TOKEN_PATTERN = re.compile(r"⟦[^⟧]+⟧")


def _flatten(value: Mapping[str, Any], prefix: str = "") -> dict[str, Any]:
    flattened: dict[str, Any] = {}
    for key in sorted(value):
        if not isinstance(key, str) or not key:
            raise ArgusSymbolError("canonical request keys must be non-empty strings")
        path = f"{prefix}.{key}" if prefix else key
        item = value[key]
        if isinstance(item, Mapping):
            nested = _flatten(item, path)
            if not nested:
                raise ArgusSymbolError(f"empty canonical object cannot be projected: {path}")
            flattened.update(nested)
        else:
            flattened[path] = item
    return flattened


def _set_path(target: dict[str, Any], path: str, value: Any) -> None:
    current = target
    parts = path.split(".")
    for part in parts[:-1]:
        child = current.setdefault(part, {})
        if not isinstance(child, dict):
            raise ArgusSymbolError(f"symbol path conflict at {path}")
        current = child
    current[parts[-1]] = deepcopy(value)


def encode_argus_symbols(request: Mapping[str, Any]) -> dict[str, Any]:
    """Encode every supported canonical fact as an ordered symbolic sequence."""
    if not isinstance(request, Mapping) or not request:
        raise ArgusSymbolError("canonical request must be a non-empty object")
    flattened = _flatten(request)
    tokens: list[str] = []
    facts: list[dict[str, Any]] = []
    for path, value in sorted(flattened.items()):
        token = _PATH_TO_TOKEN.get((path, value))
        if token is None:
            raise ArgusSymbolError(f"unsupported canonical fact: {path}={value!r}")
        tokens.append(token)
        facts.append({"path": path, "value": deepcopy(value), "token": token})
    return {
        "schema": "argus.symbols.bounded.v1",
        "sequence": "".join(tokens),
        "tokens": tokens,
        "facts": facts,
    }


def decode_argus_symbols(sequence: str) -> dict[str, Any]:
    """Decode one complete symbolic sequence into canonical JSON."""
    if not isinstance(sequence, str) or not sequence.strip():
        raise ArgusSymbolError("symbol sequence must be a non-empty string")
    compact = "".join(sequence.split())
    tokens = _TOKEN_PATTERN.findall(compact)
    if not tokens or "".join(tokens) != compact:
        raise ArgusSymbolError("symbol sequence contains malformed or unsupported text")
    request: dict[str, Any] = {}
    seen_paths: dict[str, Any] = {}
    for token in tokens:
        pair = _TOKEN_TO_PATH.get(token)
        if pair is None:
            raise ArgusSymbolError(f"unsupported ARGUS symbol: {token}")
        path, value = pair
        if path in seen_paths:
            if seen_paths[path] != value:
                raise ArgusSymbolError(f"conflicting symbols for canonical path: {path}")
            raise ArgusSymbolError(f"duplicate symbol for canonical path: {path}")
        seen_paths[path] = value
        _set_path(request, path, value)
    return request
