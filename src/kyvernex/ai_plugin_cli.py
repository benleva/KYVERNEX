"""Command-line bridge for AI hosts using JSON or persistent JSON Lines."""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, TextIO

from .ai_bridge import KyvernexAIBridge
from .ai_formats import export_manifest
from .plugin_loader import load_handler


MappingLike = dict[str, Any]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex-ai-plugin",
        description="Expose one provider-neutral KYVERNEX AI tool over JSON input/output.",
    )
    parser.add_argument("--handler", required=True, help="Host callable as module:attribute")
    parser.add_argument("--principal", default="ai-host")
    parser.add_argument("--manifest", action="store_true", help="Print the tool manifest and exit")
    parser.add_argument(
        "--manifest-format",
        choices=("canonical", "openai", "anthropic", "gemini"),
        default="canonical",
        help="Shape used when printing the canonical tool manifest",
    )
    parser.add_argument(
        "--stream",
        action="store_true",
        help="Keep one bridge alive and process one JSON object per input line",
    )
    return parser


def _write_json(stream: TextIO, payload: MappingLike) -> None:
    stream.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")
    stream.flush()


def _load_object(raw: str, *, source: str) -> dict[str, Any]:
    payload: Any = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError(f"{source} JSON must be an object")
    return payload


def _invoke_payload(bridge: KyvernexAIBridge, payload: dict[str, Any]) -> dict[str, Any]:
    envelope_keys = {"name", "arguments", "id"}
    if "name" in payload or "arguments" in payload:
        unknown = set(payload) - envelope_keys
        if unknown:
            raise ValueError(f"mixed or unknown tool-call fields: {', '.join(sorted(unknown))}")
        return bridge.invoke_tool_call(payload)
    return bridge.invoke(payload)


def _stream_requests(bridge: KyvernexAIBridge, input_stream: TextIO, output_stream: TextIO) -> int:
    had_failure = False
    for line_number, raw_line in enumerate(input_stream, start=1):
        raw = raw_line.strip()
        if not raw:
            continue
        try:
            response = _invoke_payload(bridge, _load_object(raw, source=f"line {line_number}"))
        except (TypeError, ValueError, RuntimeError) as exc:
            had_failure = True
            response = {"status": "FAILED", "error": str(exc), "line": line_number}
        else:
            if response.get("status") != "SUCCEEDED":
                had_failure = True
        _write_json(output_stream, response)
    return 2 if had_failure else 0


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        handler = load_handler(args.handler)
        with KyvernexAIBridge(handler, principal=args.principal) as bridge:
            if args.manifest:
                _write_json(sys.stdout, export_manifest(bridge.manifest(), args.manifest_format))
                return 0
            if args.stream:
                return _stream_requests(bridge, sys.stdin, sys.stdout)
            payload = _load_object(sys.stdin.read(), source="stdin")
            response = _invoke_payload(bridge, payload)
            _write_json(sys.stdout, response)
            return 0 if response.get("status") == "SUCCEEDED" else 2
    except (ImportError, AttributeError, TypeError, ValueError, RuntimeError) as exc:
        _write_json(sys.stderr, {"status": "FAILED", "error": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
