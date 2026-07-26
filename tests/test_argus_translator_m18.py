from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from kyvernex.argus_audit import build_argus_audit_envelope
from kyvernex.argus_matrix import evaluate_argus_matrix
from kyvernex.argus_symbols import ArgusSymbolError, decode_argus_symbols, encode_argus_symbols
from kyvernex.argus_translator import ArgusTranslationError, extract_argus_request, translate_argus_text


MATRIX = {
    "matrix_id": "m18-verification",
    "version": "1.0",
    "default_decision": "REVIEW",
    "rules": [
        {
            "id": "deny-critical",
            "priority": 10,
            "when": [{"path": "risk", "operator": "eq", "value": "critical"}],
            "decision": "DENY",
            "reason": "Critical risk.",
            "stop": True,
        },
        {
            "id": "allow-consented-low-risk",
            "priority": 20,
            "when": [
                {"path": "consent", "operator": "eq", "value": True},
                {"path": "risk", "operator": "eq", "value": "low"},
            ],
            "decision": "ALLOW",
            "reason": "Consent present and risk low.",
            "stop": True,
        },
    ],
}


@pytest.mark.parametrize(
    ("text", "path", "expected"),
    [
        ("Ha dato il consenso", "consent", True),
        ("Senza consenso", "consent", False),
        ("Ho l'autorizzazione", "authorization", True),
        ("Senza autorizzazione", "authorization", False),
        ("Il rischio è basso", "risk", "low"),
        ("Il rischio è medio", "risk", "medium"),
        ("Il rischio è alto", "risk", "high"),
        ("Il rischio è critico", "risk", "critical"),
        ("Il soggetto è minorenne", "subject.minor", True),
        ("Il soggetto è maggiorenne", "subject.minor", False),
        ("Ambito sanitario", "domain", "health"),
        ("Ambito finanziario", "domain", "finance"),
        ("Ambito legale", "domain", "legal"),
        ("Ambito educativo", "domain", "education"),
    ],
)
def test_v02_supported_vocabulary(text: str, path: str, expected: object) -> None:
    translation = translate_argus_text(text)
    request = extract_argus_request(translation)
    current: object = request
    for part in path.split("."):
        assert isinstance(current, dict)
        current = current[part]
    assert current == expected
    assert translation["trace"]
    assert translation["trace"][0]["rule_ids"]
    assert translation["trace"][0]["matches"]


def test_v03_normalization_equivalence() -> None:
    variants = [
        "Il rischio è alto",
        "  IL   RISCHIO   È   ALTO  ",
        "Il rischio e alto",
    ]
    requests = [extract_argus_request(translate_argus_text(item)) for item in variants]
    assert requests == [{"risk": "high"}] * len(variants)


@pytest.mark.parametrize("text", ["", "   ", "testo senza fatti argus"])
def test_v04_closed_world_rejection(text: str) -> None:
    with pytest.raises(ArgusTranslationError):
        translate_argus_text(text)


def test_v05_contradiction_rejection() -> None:
    with pytest.raises(ArgusTranslationError, match="conflicting statements detected for consent"):
        translate_argus_text("Ha dato il consenso ma è senza consenso")


def test_v06_symbolic_projection_is_stable() -> None:
    request = {
        "risk": "high",
        "consent": True,
        "authorization": False,
        "subject": {"minor": True},
        "domain": "health",
    }
    projection = encode_argus_symbols(request)
    assert projection["tokens"] == ["⟦A-⟧", "⟦C+⟧", "⟦DH⟧", "⟦R3⟧", "⟦M+⟧"]
    assert projection["sequence"] == "⟦A-⟧⟦C+⟧⟦DH⟧⟦R3⟧⟦M+⟧"


@pytest.mark.parametrize(
    "request",
    [
        {"consent": True},
        {"authorization": False, "risk": "critical"},
        {"domain": "legal", "subject": {"minor": False}},
        {
            "consent": True,
            "authorization": True,
            "risk": "medium",
            "subject": {"minor": True},
            "domain": "education",
        },
    ],
)
def test_v07_symbolic_round_trip(request: dict[str, object]) -> None:
    projection = encode_argus_symbols(request)
    assert decode_argus_symbols(projection["sequence"]) == request


@pytest.mark.parametrize(
    "sequence",
    [
        "garbage",
        "⟦UNKNOWN⟧",
        "⟦C+⟧⟦C+⟧",
        "⟦C+⟧⟦C-⟧",
        "⟦C+⟧ trailing",
    ],
)
def test_v08_symbol_rejection(sequence: str) -> None:
    with pytest.raises(ArgusSymbolError):
        decode_argus_symbols(sequence)


def test_v09_audit_envelope() -> None:
    translation = translate_argus_text("Ha dato il consenso e il rischio è basso")
    envelope = build_argus_audit_envelope(translation)
    assert envelope["schema"] == "argus.audit.envelope.v1"
    assert envelope["status"] == "TRANSLATED"
    assert envelope["canonical_request"] == {"consent": True, "risk": "low"}
    assert envelope["symbols"]["sequence"] == "⟦C+⟧⟦R1⟧"
    assert [stage["id"] for stage in envelope["stages"]] == [
        "input",
        "normalization",
        "translation",
        "canonical_request",
        "symbol_projection",
    ]


def test_v10_matrix_integration_preserves_both_traces() -> None:
    translation = translate_argus_text("Ha dato il consenso e il rischio è basso")
    request = extract_argus_request(translation)
    decision = evaluate_argus_matrix(MATRIX, request)
    envelope = build_argus_audit_envelope(translation, decision)
    assert decision["decision"] == "ALLOW"
    assert translation["trace"]
    assert envelope["decision"]["trace"]
    assert envelope["stages"][-1]["id"] == "matrix_evaluation"


def _run_cli(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "kyvernex.argus_translator_cli", *args],
        input=stdin,
        text=True,
        capture_output=True,
        check=False,
    )


def test_v11_cli_modes(tmp_path: Path) -> None:
    direct = _run_cli("--text", "Il rischio è basso")
    assert direct.returncode == 0
    assert json.loads(direct.stdout)["translation"]["request"] == {"risk": "low"}

    input_path = tmp_path / "input.txt"
    input_path.write_text("Ambito sanitario", encoding="utf-8")
    from_file = _run_cli("--input", str(input_path))
    assert from_file.returncode == 0

    from_stdin = _run_cli("--input", "-", stdin="Senza consenso")
    assert from_stdin.returncode == 0

    output_path = tmp_path / "result.json"
    first_write = _run_cli("--text", "Il rischio è alto", "--output", str(output_path))
    assert first_write.returncode == 0
    blocked_write = _run_cli("--text", "Il rischio è alto", "--output", str(output_path))
    assert blocked_write.returncode == 1
    forced_write = _run_cli("--text", "Il rischio è alto", "--output", str(output_path), "--force")
    assert forced_write.returncode == 0

    audit = _run_cli("--text", "Il rischio è basso", "--audit-envelope")
    assert audit.returncode == 0
    assert json.loads(audit.stdout)["schema"] == "argus.audit.envelope.v1"

    matrix_path = tmp_path / "matrix.json"
    matrix_path.write_text(json.dumps(MATRIX), encoding="utf-8")
    decided = _run_cli(
        "--text",
        "Ha dato il consenso e il rischio è basso",
        "--matrix",
        str(matrix_path),
        "--audit-envelope",
    )
    assert decided.returncode == 0
    assert json.loads(decided.stdout)["decision"]["decision"] == "ALLOW"


def test_v12_deterministic_payloads() -> None:
    outputs = [
        json.dumps(
            build_argus_audit_envelope(translate_argus_text("Ambito legale e rischio medio")),
            ensure_ascii=False,
            sort_keys=True,
        )
        for _ in range(5)
    ]
    assert len(set(outputs)) == 1


def test_v13_matrix_regression_boundary() -> None:
    critical = evaluate_argus_matrix(MATRIX, {"risk": "critical"})
    defaulted = evaluate_argus_matrix(MATRIX, {"risk": "medium"})
    assert critical["decision"] == "DENY"
    assert critical["selected_rule"]["rule_id"] == "deny-critical"
    assert defaulted["decision"] == "REVIEW"
    assert defaulted["selected_rule"] is None
