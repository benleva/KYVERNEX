"""Product-first command line interface for KYVERNEX."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import sys
from pathlib import Path
from typing import Sequence

from . import plugin_cli
from .plugin_loader import PluginHandlerLoadError, load_plugin_handler

CONFIG_DIR = ".kyvernex"
CONFIG_FILE = "config.json"
EXAMPLE_FILE = "request.example.json"

DEFAULT_CONFIG = {
    "schema": "kyvernex.product.config.v1",
    "principal": "local-user",
    "capabilities": ["governed.execute"],
    "handler": None,
}

DEFAULT_REQUEST = {
    "input": {
        "message": "Hello from KYVERNEX"
    }
}


def _package_version() -> str:
    try:
        return importlib.metadata.version("kyvernex")
    except importlib.metadata.PackageNotFoundError:
        return "development"


def _write_json(path: Path, payload: object, *, force: bool = False) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return True


def _load_config(root: Path) -> dict[str, object]:
    path = root / CONFIG_DIR / CONFIG_FILE
    if not path.exists():
        raise ValueError(f"KYVERNEX is not initialized in {root}. Run 'kyvernex init'.")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid KYVERNEX configuration from {path}") from exc
    if not isinstance(payload, dict):
        raise ValueError("KYVERNEX configuration must be a JSON object")
    return payload


def _validated_settings(config: dict[str, object]) -> tuple[str, str | None, list[str]]:
    schema = config.get("schema")
    if schema != DEFAULT_CONFIG["schema"]:
        raise ValueError(
            f"unsupported configuration schema {schema!r}; expected {DEFAULT_CONFIG['schema']!r}"
        )

    principal = config.get("principal") or "local-user"
    if not isinstance(principal, str) or not principal.strip():
        raise ValueError("configured principal must be a non-empty string")

    handler = config.get("handler")
    if handler is not None and (not isinstance(handler, str) or not handler.strip()):
        raise ValueError("configured handler must be null or a non-empty MODULE:ATTRIBUTE string")

    capabilities = config.get("capabilities") or ["governed.execute"]
    if (
        not isinstance(capabilities, list)
        or not capabilities
        or not all(isinstance(item, str) and item.strip() for item in capabilities)
    ):
        raise ValueError("configured capabilities must be a non-empty list of strings")

    return principal.strip(), handler.strip() if isinstance(handler, str) else None, capabilities


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex",
        description="Initialize, diagnose and run the KYVERNEX governed plugin.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {_package_version()}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="initialize KYVERNEX in a directory")
    init_parser.add_argument("directory", nargs="?", type=Path, default=Path.cwd())
    init_parser.add_argument("--force", action="store_true", help="replace generated files")

    status_parser = subparsers.add_parser("status", help="show local product configuration")
    status_parser.add_argument("directory", nargs="?", type=Path, default=Path.cwd())

    doctor_parser = subparsers.add_parser("doctor", help="diagnose installation and configuration")
    doctor_parser.add_argument("directory", nargs="?", type=Path, default=Path.cwd())

    run_parser = subparsers.add_parser("run", help="execute one governed plugin request")
    source = run_parser.add_mutually_exclusive_group()
    source.add_argument("--text", help="plain text wrapped as a KYVERNEX message request")
    source.add_argument("--input", help="inline JSON request")
    source.add_argument("--input-file", type=Path, help="UTF-8 JSON request file")
    run_parser.add_argument("--directory", type=Path, default=Path.cwd())
    run_parser.add_argument("--output-file", type=Path)
    run_parser.add_argument("--principal")
    run_parser.add_argument("--handler", metavar="MODULE:ATTRIBUTE")
    run_parser.add_argument("--capability", action="append", dest="capabilities")
    run_parser.add_argument("--request-id")
    return parser


def _command_init(directory: Path, *, force: bool) -> int:
    root = directory.expanduser().resolve()
    config_path = root / CONFIG_DIR / CONFIG_FILE
    example_path = root / CONFIG_DIR / EXAMPLE_FILE
    created = [
        path
        for path, was_created in (
            (config_path, _write_json(config_path, DEFAULT_CONFIG, force=force)),
            (example_path, _write_json(example_path, DEFAULT_REQUEST, force=force)),
        )
        if was_created
    ]
    result = {
        "status": "INITIALIZED",
        "version": _package_version(),
        "root": str(root),
        "created": [str(path) for path in created],
        "config": str(config_path),
        "example": str(example_path),
        "next": f"kyvernex doctor {root}",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def _command_status(directory: Path) -> int:
    root = directory.expanduser().resolve()
    config = _load_config(root)
    _validated_settings(config)
    result = {
        "status": "READY",
        "version": _package_version(),
        "root": str(root),
        "config": config,
        "example_exists": (root / CONFIG_DIR / EXAMPLE_FILE).exists(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def _command_doctor(directory: Path) -> int:
    root = directory.expanduser().resolve()
    checks: list[dict[str, object]] = []

    config_path = root / CONFIG_DIR / CONFIG_FILE
    checks.append({"name": "configuration_file", "ok": config_path.is_file(), "path": str(config_path)})

    try:
        config = _load_config(root)
        principal, handler, capabilities = _validated_settings(config)
        checks.append({"name": "configuration_schema", "ok": True})
        checks.append({"name": "principal", "ok": True, "value": principal})
        checks.append({"name": "capabilities", "ok": True, "count": len(capabilities)})
        if handler:
            try:
                load_plugin_handler(handler)
                checks.append({"name": "handler", "ok": True, "value": handler})
            except PluginHandlerLoadError as exc:
                checks.append({"name": "handler", "ok": False, "value": handler, "error": str(exc)})
        else:
            checks.append({"name": "handler", "ok": True, "value": "built-in echo handler"})
    except (OSError, TypeError, ValueError) as exc:
        checks.append({"name": "configuration", "ok": False, "error": str(exc)})

    example_path = root / CONFIG_DIR / EXAMPLE_FILE
    checks.append({"name": "example_request", "ok": example_path.is_file(), "path": str(example_path)})

    healthy = all(bool(check.get("ok")) for check in checks)
    result = {
        "status": "READY" if healthy else "NOT_READY",
        "version": _package_version(),
        "root": str(root),
        "checks": checks,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if healthy else 2


def _command_run(args: argparse.Namespace) -> int:
    root = args.directory.expanduser().resolve()
    config = _load_config(root)
    configured_principal, configured_handler, configured_capabilities = _validated_settings(config)

    inline = args.input
    input_file = args.input_file
    if args.text is not None:
        inline = json.dumps({"input": {"message": args.text}}, ensure_ascii=False)
    elif inline is None and input_file is None:
        input_file = root / CONFIG_DIR / EXAMPLE_FILE

    principal = args.principal or configured_principal
    handler = args.handler if args.handler is not None else configured_handler
    capabilities = args.capabilities or configured_capabilities

    forwarded: list[str] = []
    if inline is not None:
        forwarded.extend(["--input", inline])
    else:
        forwarded.extend(["--input-file", str(input_file)])
    if args.output_file is not None:
        forwarded.extend(["--output-file", str(args.output_file)])
    if handler:
        forwarded.extend(["--handler", str(handler)])
    forwarded.extend(["--principal", principal])
    if args.request_id:
        forwarded.extend(["--request-id", args.request_id])
    for capability in capabilities:
        forwarded.extend(["--capability", capability])
    return plugin_cli.main(forwarded)


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "init":
            return _command_init(args.directory, force=args.force)
        if args.command == "status":
            return _command_status(args.directory)
        if args.command == "doctor":
            return _command_doctor(args.directory)
        if args.command == "run":
            return _command_run(args)
        raise ValueError(f"unsupported command: {args.command}")
    except (OSError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
