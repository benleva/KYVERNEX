"""Command-line entry point for the KYVERNEX product plugin."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping

from .plugin import KyvernexPlugin
from .plugin_loader import PluginHandlerLoadError, load_plugin_handler


def _echo_handler(request: Mapping[str, Any], authority: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "input": dict(request.get("input", {})),
        "principal": authority.get("principal"),
        "capabilities": list(authority.get("capabilities", [])),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex-plugin",
        description="Execute one governed in-process KYVERNEX plugin request.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", help="JSON object passed directly to the plugin")
    source.add_argument("--input-file", type=Path, help="UTF-8 JSON object read from a file")
    parser.add_argument(
        "--output-file",
        type=Path,
        help="write the structured UTF-8 JSON response to this file",
    )
    parser.add_argument(
        "--handler",
        metavar="MODULE:ATTRIBUTE",
        help="exact importable Python callable; defaults to the built-in local echo handler",
    )
    parser.add_argument("--principal", default="local-user")
    parser.add_argument("--request-id")
    parser.add_argument(
        "--capability",
        action="append",
        dest="capabilities",
        help="declared and requested capability; may be repeated",
    )
    return parser


def _load_payload(*, inline: str | None, input_file: Path | None) -> dict[str, Any]:
    if input_file is not None:
        try:
            raw = input_file.read_text(encoding="utf-8")
        except OSError as exc:
            raise ValueError(f"cannot read input file {input_file}") from exc
    else:
        raw = inline or ""

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError("input must contain valid JSON") from exc
    if not isinstance(payload, dict):
        raise ValueError("input JSON must be an object")
    return payload


def _emit_response(response: Mapping[str, Any], output_file: Path | None) -> None:
    rendered = json.dumps(response, ensure_ascii=False, sort_keys=True, indent=2)
    if output_file is None:
        print(rendered)
        return
    try:
        output_file.write_text(rendered + "\n", encoding="utf-8")
    except OSError as exc:
        raise ValueError(f"cannot write output file {output_file}") from exc


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        payload = _load_payload(inline=args.input, input_file=args.input_file)
        handler = load_plugin_handler(args.handler) if args.handler else _echo_handler
        capabilities = set(args.capabilities or ["governed.execute"])
        with KyvernexPlugin(handler, capabilities=capabilities) as plugin:
            response = plugin.execute(
                payload,
                principal=args.principal,
                requested_capabilities=capabilities,
                grants=capabilities,
                request_id=args.request_id,
            )
        _emit_response(response, args.output_file)
        return 0 if response.get("status") == "SUCCEEDED" else 2
    except (PluginHandlerLoadError, TypeError, ValueError, RuntimeError) as exc:
        failure = {"status": "FAILED", "error": str(exc)}
        print(json.dumps(failure, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
