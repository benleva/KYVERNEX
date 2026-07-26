"""Product-first command line interface for KYVERNEX."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from . import plugin_cli

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


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex",
        description="Initialize and run the KYVERNEX governed plugin.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="initialize KYVERNEX in a directory")
    init_parser.add_argument("directory", nargs="?", type=Path, default=Path.cwd())
    init_parser.add_argument("--force", action="store_true", help="replace generated files")

    status_parser = subparsers.add_parser("status", help="show local product configuration")
    status_parser.add_argument("directory", nargs="?", type=Path, default=Path.cwd())

    run_parser = subparsers.add_parser("run", help="execute one governed plugin request")
    source = run_parser.add_mutually_exclusive_group()
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
        "root": str(root),
        "created": [str(path) for path in created],
        "config": str(config_path),
        "example": str(example_path),
        "next": f"kyvernex run --directory {root}",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def _command_status(directory: Path) -> int:
    root = directory.expanduser().resolve()
    config = _load_config(root)
    result = {
        "status": "READY",
        "root": str(root),
        "config": config,
        "example_exists": (root / CONFIG_DIR / EXAMPLE_FILE).exists(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def _command_run(args: argparse.Namespace) -> int:
    root = args.directory.expanduser().resolve()
    config = _load_config(root)

    inline = args.input
    input_file = args.input_file
    if inline is None and input_file is None:
        input_file = root / CONFIG_DIR / EXAMPLE_FILE

    principal = args.principal or str(config.get("principal") or "local-user")
    handler = args.handler if args.handler is not None else config.get("handler")
    capabilities = args.capabilities or config.get("capabilities") or ["governed.execute"]
    if not isinstance(capabilities, list) or not all(isinstance(item, str) for item in capabilities):
        raise ValueError("configured capabilities must be a list of strings")

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
        if args.command == "run":
            return _command_run(args)
        raise ValueError(f"unsupported command: {args.command}")
    except (OSError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
