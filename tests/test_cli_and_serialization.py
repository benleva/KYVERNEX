from __future__ import annotations

import json

from kyvernex import KyvernexEngine, ValidationOutcome, to_primitive
from kyvernex.cli import main


def test_execution_result_is_json_serializable() -> None:
    result = KyvernexEngine().execute(
        "contenuto verificabile",
        source="test-suite",
        session_id="session-json",
    )

    payload = to_primitive(result)
    encoded = json.dumps(payload, ensure_ascii=False)

    assert payload["session_id"] == "session-json"
    assert payload["validation"]["outcome"] == ValidationOutcome.VALIDATED.value
    assert "contenuto verificabile" in encoded
    assert len(payload["audit"]) == 4


def test_cli_returns_json_and_success(capsys) -> None:
    exit_code = main([
        "Il cielo è blu.",
        "--source",
        "cli-test",
        "--session-id",
        "session-cli",
        "--indent",
        "0",
    ])

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert output["session_id"] == "session-cli"
    assert output["cognitive_object"]["source"] == "cli-test"
    assert output["validation"]["outcome"] == "VALIDATO"


def test_cli_returns_nonzero_for_invalid_input(capsys) -> None:
    exit_code = main(["", "--source", "cli-test"])

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 2
    assert output["validation"]["outcome"] == "INCOMPLETO"
    assert "CONTENUTO_ORIGINALE_MANCANTE" in output["validation"]["errors"]
