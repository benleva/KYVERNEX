"""Command-line entry point for the KYVERNEX product plugin."""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Mapping

from .plugin import KyvernexPlugin


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
    parser.add_argument("input", help="JSON object passed to the plugin")
    parser.add_argument("--principal", default="local-user")
    parser.add_argument("--request-id")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        payload = json.loads(args.input)
        if not isinstance(payload, dict):
            raise ValueError("input JSON must be an object")
        with KyvernexPlugin(_echo_handler) as plugin:
            response = plugin.execute(
                payload,
                principal=args.principal,
                request_id=args.request_id,
            )
        print(json.dumps(response, ensure_ascii=False, sort_keys=True))
        return 0 if response.get("status") == "SUCCEEDED" else 2
    except (TypeError, ValueError, RuntimeError) as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
