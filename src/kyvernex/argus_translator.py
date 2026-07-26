"""Deterministic Italian-to-ARGUS canonical request translator."""
from __future__ import annotations

import re
from copy import deepcopy
from typing import Any, Mapping


class ArgusTranslationError(ValueError):
    """Raised when human text cannot be translated without ambiguity."""


_CONSENT_FALSE = (
    r"\bmanca(?:\s+il)?\s+consenso\b",
    r"\bsenza\s+consenso\b",
    r"\bconsenso\s+(?:non\s+)?(?:presente|fornito|dato|concesso)\s*:\s*no\b",
    r"\bnon\s+(?:ha|hanno|ho|abbiamo)\s+(?:dato|fornito|concesso)\s+(?:il\s+)?consenso\b",
    r"\bconsenso\s+(?:negato|assente|revocato)\b",
)
_CONSENT_TRUE = (
    r"\b(?:ha|hanno|ho|abbiamo)\s+(?:dato|fornito|concesso)\s+(?:il\s+)?consenso\b",
    r"\bconsenso\s+(?:presente|fornito|dato|concesso|valido|confermato)\b",
    r"\bcon\s+(?:il\s+)?consenso\b",
    r"\bautorizzazione\s+(?:presente|fornita|data|concessa|valida|confermata)\b",
    r"\b(?:ho|abbiamo)\s+(?:l['’])?autorizzazione\b",
)
_RISK_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("critical", (r"\brischio\s+(?:e|è|risulta|considerato)?\s*critico\b", r"\brischio\s+massimo\b")),
    ("high", (r"\brischio\s+(?:e|è|risulta|considerato)?\s*(?:alto|elevato)\b", r"\balto\s+rischio\b")),
    ("medium", (r"\brischio\s+(?:e|è|risulta|considerato)?\s*(?:medio|moderato)\b", r"\brischio\s+intermedio\b")),
    ("low", (r"\brischio\s+(?:e|è|risulta|considerato)?\s*basso\b", r"\bbasso\s+rischio\b", r"\brischio\s+minimo\b")),
)


def _matches(text: str, patterns: tuple[str, ...]) -> list[str]:
    return [pattern for pattern in patterns if re.search(pattern, text, flags=re.IGNORECASE)]


def translate_argus_text(text: str) -> dict[str, Any]:
    """Translate supported Italian statements into a canonical ARGUS request.

    The translator is deliberately closed-world: it extracts only fields backed by
    explicit patterns and rejects contradictory values instead of guessing.
    """
    if not isinstance(text, str) or not text.strip():
        raise ArgusTranslationError("text must be a non-empty string")
    normalized = " ".join(text.strip().split())
    request: dict[str, Any] = {}
    trace: list[dict[str, Any]] = []

    false_hits = _matches(normalized, _CONSENT_FALSE)
    true_hits = _matches(normalized, _CONSENT_TRUE)
    if false_hits and true_hits:
        raise ArgusTranslationError("conflicting consent statements detected")
    if false_hits:
        request["consent"] = False
        trace.append({"field": "consent", "value": False, "patterns": false_hits})
    elif true_hits:
        request["consent"] = True
        trace.append({"field": "consent", "value": True, "patterns": true_hits})

    risk_hits: list[tuple[str, list[str]]] = []
    for value, patterns in _RISK_PATTERNS:
        hits = _matches(normalized, patterns)
        if hits:
            risk_hits.append((value, hits))
    if len(risk_hits) > 1:
        values = ", ".join(value for value, _ in risk_hits)
        raise ArgusTranslationError(f"conflicting risk statements detected: {values}")
    if risk_hits:
        value, hits = risk_hits[0]
        request["risk"] = value
        trace.append({"field": "risk", "value": value, "patterns": hits})

    if not request:
        raise ArgusTranslationError("no supported ARGUS facts were found in the text")

    return {
        "status": "TRANSLATED",
        "language": "it",
        "source_text": normalized,
        "request": deepcopy(request),
        "trace": trace,
        "unresolved": [],
    }


def extract_argus_request(translation: Mapping[str, Any]) -> dict[str, Any]:
    """Extract the canonical request from one validated translation result."""
    if not isinstance(translation, Mapping):
        raise ArgusTranslationError("translation must be an object")
    request = translation.get("request")
    if not isinstance(request, Mapping):
        raise ArgusTranslationError("translation.request must be an object")
    return deepcopy(dict(request))
