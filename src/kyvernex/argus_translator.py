"""Deterministic Italian-to-ARGUS canonical request translator."""
from __future__ import annotations

import re
import unicodedata
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Mapping, Sequence


class ArgusTranslationError(ValueError):
    """Raised when human text cannot be translated without ambiguity."""


@dataclass(frozen=True)
class _LexicalRule:
    rule_id: str
    path: str
    value: Any
    patterns: tuple[str, ...]


def _fold_text(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text.casefold())
    without_marks = "".join(char for char in decomposed if not unicodedata.combining(char))
    return " ".join(without_marks.replace("’", "'").strip().split())


_RULES: tuple[_LexicalRule, ...] = (
    _LexicalRule(
        "consent.absent",
        "consent",
        False,
        (
            r"\bmanca(?:\s+il)?\s+consenso\b",
            r"\bsenza\s+consenso\b",
            r"\bconsenso\s+(?:assente|negato|revocato|rifiutato|non valido)\b",
            r"\bnon\s+(?:ha|hanno|ho|abbiamo)\s+(?:dato|fornito|concesso|espresso)\s+(?:il\s+)?consenso\b",
            r"\bconsenso\s*:\s*(?:no|falso|false)\b",
        ),
    ),
    _LexicalRule(
        "consent.present",
        "consent",
        True,
        (
            r"\b(?:ha|hanno|ho|abbiamo)\s+(?:dato|fornito|concesso|espresso)\s+(?:il\s+)?consenso\b",
            r"\bconsenso\s+(?:presente|fornito|dato|concesso|espresso|valido|confermato|acquisito)\b",
            r"\bcon\s+(?:il\s+)?consenso\b",
            r"\bconsenso\s*:\s*(?:si|vero|true)\b",
        ),
    ),
    _LexicalRule(
        "authorization.absent",
        "authorization",
        False,
        (
            r"\bmanca(?:\s+l[' ]?)?autorizzazione\b",
            r"\bsenza\s+autorizzazione\b",
            r"\bautorizzazione\s+(?:assente|negata|revocata|rifiutata|non valida)\b",
            r"\bnon\s+(?:e|è|risulta)\s+autorizzato\b",
            r"\bnon\s+(?:ha|hanno|ho|abbiamo)\s+(?:autorizzato|approvato)\b",
        ),
    ),
    _LexicalRule(
        "authorization.present",
        "authorization",
        True,
        (
            r"\bautorizzazione\s+(?:presente|fornita|data|concessa|valida|confermata|approvata)\b",
            r"\b(?:ho|abbiamo|ha|hanno)\s+(?:l[' ]?)?autorizzazione\b",
            r"\b(?:e|è|risulta)\s+autorizzato\b",
            r"\b(?:ha|hanno|ho|abbiamo)\s+(?:autorizzato|approvato)\b",
        ),
    ),
    _LexicalRule("risk.critical", "risk", "critical", (r"\brischio\s+(?:e\s+|risulta\s+|considerato\s+)?critico\b", r"\brischio\s+massimo\b", r"\bcriticita\s+massima\b")),
    _LexicalRule("risk.high", "risk", "high", (r"\brischio\s+(?:e\s+|risulta\s+|considerato\s+)?(?:alto|elevato|grave)\b", r"\balto\s+rischio\b")),
    _LexicalRule("risk.medium", "risk", "medium", (r"\brischio\s+(?:e\s+|risulta\s+|considerato\s+)?(?:medio|moderato)\b", r"\brischio\s+intermedio\b")),
    _LexicalRule("risk.low", "risk", "low", (r"\brischio\s+(?:e\s+|risulta\s+|considerato\s+)?basso\b", r"\bbasso\s+rischio\b", r"\brischio\s+minimo\b", r"\brischio\s+contenuto\b")),
    _LexicalRule("subject.minor.true", "subject.minor", True, (r"\b(?:soggetto|utente|cliente|paziente|persona)\s+minorenne\b", r"\be\s+minorenne\b", r"\bminore\s+di\s+eta\b")),
    _LexicalRule("subject.minor.false", "subject.minor", False, (r"\b(?:soggetto|utente|cliente|paziente|persona)\s+maggiorenne\b", r"\be\s+maggiorenne\b", r"\bmaggiore\s+di\s+eta\b")),
    _LexicalRule("domain.health", "domain", "health", (r"\bambito\s+(?:sanitario|medico|clinico)\b", r"\bdati?\s+(?:sanitari|medici|clinici)\b", r"\btrattamento\s+sanitario\b")),
    _LexicalRule("domain.finance", "domain", "finance", (r"\bambito\s+(?:finanziario|bancario|economico)\b", r"\bdati?\s+(?:finanziari|bancari)\b", r"\boperazione\s+(?:finanziaria|bancaria)\b")),
    _LexicalRule("domain.legal", "domain", "legal", (r"\bambito\s+(?:legale|giuridico)\b", r"\bprocedimento\s+(?:legale|giudiziario)\b")),
    _LexicalRule("domain.education", "domain", "education", (r"\bambito\s+(?:scolastico|educativo|formativo)\b", r"\bdati?\s+scolastici\b")),
)


def _set_path(target: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    current = target
    for part in parts[:-1]:
        child = current.get(part)
        if child is None:
            child = {}
            current[part] = child
        if not isinstance(child, dict):
            raise ArgusTranslationError(f"canonical path conflict at {path}")
        current = child
    current[parts[-1]] = value


def _matched_fragments(text: str, patterns: Sequence[str]) -> list[dict[str, str]]:
    matches: list[dict[str, str]] = []
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            matches.append({"pattern": pattern, "matched_text": match.group(0)})
    return matches


def translate_argus_text(text: str) -> dict[str, Any]:
    """Translate supported Italian statements into a canonical ARGUS request.

    The translator is closed-world and deterministic. It extracts only facts backed
    by explicit lexical rules and rejects conflicting values instead of guessing.
    """
    if not isinstance(text, str) or not text.strip():
        raise ArgusTranslationError("text must be a non-empty string")

    source_text = " ".join(text.strip().split())
    normalized_text = _fold_text(source_text)
    hits_by_path: dict[str, list[tuple[_LexicalRule, list[dict[str, str]]]]] = {}

    for rule in _RULES:
        matches = _matched_fragments(normalized_text, rule.patterns)
        if matches:
            hits_by_path.setdefault(rule.path, []).append((rule, matches))

    if not hits_by_path:
        raise ArgusTranslationError("no supported ARGUS facts were found in the text")

    request: dict[str, Any] = {}
    trace: list[dict[str, Any]] = []
    for path in sorted(hits_by_path):
        hits = hits_by_path[path]
        distinct_values = {repr(rule.value) for rule, _ in hits}
        if len(distinct_values) > 1:
            rule_ids = ", ".join(rule.rule_id for rule, _ in hits)
            raise ArgusTranslationError(f"conflicting statements detected for {path}: {rule_ids}")
        rule, matches = hits[0]
        _set_path(request, path, deepcopy(rule.value))
        trace.append(
            {
                "field": path,
                "value": deepcopy(rule.value),
                "rule_ids": [item.rule_id for item, _ in hits],
                "matches": [match for _, group in hits for match in group],
            }
        )

    return {
        "status": "TRANSLATED",
        "language": "it",
        "translator": {"id": "argus.executive.deterministic.it", "version": "0.2"},
        "source_text": source_text,
        "normalized_text": normalized_text,
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
