"""Deterministic audit envelope for ARGUS translation and evaluation."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from .argus_symbols import ArgusSymbolError, encode_argus_symbols
from .argus_translator import ArgusTranslationError, extract_argus_request


class ArgusAuditError(ValueError):
    """Raised when an audit envelope cannot be assembled safely."""


def build_argus_audit_envelope(
    translation: Mapping[str, Any],
    decision: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a self-contained, deterministic record of the ARGUS execution path."""
    try:
        request = extract_argus_request(translation)
        symbols = encode_argus_symbols(request)
    except (ArgusTranslationError, ArgusSymbolError) as exc:
        raise ArgusAuditError(str(exc)) from exc

    source_text = translation.get("source_text")
    normalized_text = translation.get("normalized_text")
    trace = translation.get("trace")
    translator = translation.get("translator")
    if not isinstance(source_text, str) or not isinstance(normalized_text, str):
        raise ArgusAuditError("translation must contain source_text and normalized_text")
    if not isinstance(trace, list):
        raise ArgusAuditError("translation.trace must be an array")
    if not isinstance(translator, Mapping):
        raise ArgusAuditError("translation.translator must be an object")
    if decision is not None and not isinstance(decision, Mapping):
        raise ArgusAuditError("decision must be an object when supplied")

    stages: list[dict[str, Any]] = [
        {"id": "input", "status": "CAPTURED", "data": {"source_text": source_text}},
        {"id": "normalization", "status": "COMPLETED", "data": {"normalized_text": normalized_text}},
        {"id": "translation", "status": "COMPLETED", "data": {"trace": deepcopy(trace)}},
        {"id": "canonical_request", "status": "COMPLETED", "data": deepcopy(request)},
        {"id": "symbol_projection", "status": "COMPLETED", "data": deepcopy(symbols)},
    ]
    status = "TRANSLATED"
    if decision is not None:
        stages.append({"id": "matrix_evaluation", "status": "COMPLETED", "data": deepcopy(dict(decision))})
        status = "DECIDED"

    return {
        "schema": "argus.audit.envelope.v1",
        "status": status,
        "language": translation.get("language"),
        "translator": deepcopy(dict(translator)),
        "canonical_request": deepcopy(request),
        "symbols": deepcopy(symbols),
        "decision": deepcopy(dict(decision)) if decision is not None else None,
        "stages": stages,
    }
