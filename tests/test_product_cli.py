import json
from pathlib import Path

import pytest

from kyvernex.product_cli import _build_parser, main


def test_version_exits_zero_and_prints_program_name(capsys):
    parser = _build_parser()

    with pytest.raises(SystemExit) as exc:
        parser.parse_args(["--version"])

    assert exc.value.code == 0
    output = capsys.readouterr().out.strip()
    assert output.startswith("kyvernex ")
    assert len(output.split()) == 2


def test_init_creates_configuration_and_example(tmp_path, capsys):
    rc = main(["init", str(tmp_path)])
    init_output = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert init_output["status"] == "INITIALIZED"
    assert (tmp_path / ".kyvernex" / "config.json").is_file()
    assert (tmp_path / ".kyvernex" / "request.example.json").is_file()
    assert init_output["root"] == str(tmp_path.resolve())


def test_init_force_rewrites_existing_files(tmp_path, capsys):
    config_dir = tmp_path / ".kyvernex"
    config_dir.mkdir()
    config_path = config_dir / "config.json"
    example_path = config_dir / "request.example.json"
    config_path.write_text('{"schema": "bad"}', encoding="utf-8")
    example_path.write_text('{"input": {"message": "broken"}}', encoding="utf-8")

    rc = main(["init", "--force", str(tmp_path)])
    output = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert output["status"] == "INITIALIZED"
    assert len(output["created"]) == 2

    config = json.loads(config_path.read_text(encoding="utf-8"))
    assert config["schema"] == "kyvernex.product.config.v1"


def test_status_reports_ready_with_valid_configuration(tmp_path, capsys):
    main(["init", str(tmp_path)])
    capsys.readouterr()

    rc = main(["status", str(tmp_path)])
    output = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert output["status"] == "READY"
    assert output["config"]["schema"] == "kyvernex.product.config.v1"
    assert output["example_exists"] is True


def test_status_returns_failure_with_invalid_schema(tmp_path, capsys):
    main(["init", str(tmp_path)])
    capsys.readouterr()
    config_path = tmp_path / ".kyvernex" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["schema"] = "invalid.schema"
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")

    rc = main(["status", str(tmp_path)])
    err = capsys.readouterr().err
    output = json.loads(err)

    assert rc == 1
    assert output["status"] == "FAILED"
    assert "unsupported configuration schema" in output["error"]


def test_doctor_reports_ready_for_initialized_configuration(tmp_path, capsys):
    main(["init", str(tmp_path)])
    capsys.readouterr()

    rc = main(["doctor", str(tmp_path)])
    output = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert output["status"] == "READY"
    assert any(check["name"] == "handler" and check["ok"] for check in output["checks"])


def test_doctor_reports_not_ready_and_returns_code_2_for_bad_configuration(tmp_path, capsys):
    main(["init", str(tmp_path)])
    capsys.readouterr()
    config_path = tmp_path / ".kyvernex" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["schema"] = "invalid.schema"
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")

    rc = main(["doctor", str(tmp_path)])
    output = json.loads(capsys.readouterr().out)

    assert rc == 2
    assert output["status"] == "NOT_READY"
    assert any(check["name"] == "configuration" and check["ok"] is False for check in output["checks"])


def test_doctor_reports_handler_error_for_nonexistent_handler(tmp_path, capsys):
    main(["init", str(tmp_path)])
    capsys.readouterr()
    config_path = tmp_path / ".kyvernex" / "config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["handler"] = "nonexistent.module:handler"
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")

    rc = main(["doctor", str(tmp_path)])
    output = json.loads(capsys.readouterr().out)

    assert rc == 2
    assert output["status"] == "NOT_READY"
    assert any(
        check["name"] == "handler" and check["ok"] is False and "cannot import handler module" in check["error"]
        for check in output["checks"]
    )


def test_run_text_wraps_text_in_input_message(tmp_path, capsys):
    main(["init", str(tmp_path)])
    capsys.readouterr()
    rc = main(["run", "--text", "hello world", "--directory", str(tmp_path)])
    output = json.loads(capsys.readouterr().out)

    assert rc == 0
    assert output["status"] == "SUCCEEDED"
    assert output["result"]["input"] == {"input": {"message": "hello world"}}
    assert output["result"]["principal"] == "local-user"


@pytest.mark.parametrize(
    "args",
    [
        ["run", "--text", "hello", "--input", "{}"],
        ["run", "--text", "hello", "--input-file", str(Path("input.json"))],
        ["run", "--input", "{}", "--input-file", str(Path("input.json"))],
    ],
)
def test_run_input_flags_are_mutually_exclusive(args):
    parser = _build_parser()

    with pytest.raises(SystemExit) as exc:
        parser.parse_args(args)

    assert exc.value.code == 2
