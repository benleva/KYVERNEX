"""Command-line entry point for the KYVERNEX product plugin."""
from __future__ import annotations

import argparse
import json
import sys
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
    parser.add_argument("input", help="JSON object passed to the plugin")
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


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        payload = json.loads(args.input)
        if not isinstance(payload, dict):
            raise ValueError("input JSON must be an object")

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
        print(json.dumps(response, ensure_ascii=False, sort_keys=True))
        return 0 if response.get("status") == "SUCCEEDED" else 2
    except (PluginHandlerLoadError, TypeError, ValueError, RuntimeError) as exc:
        print(
            json.dumps(
                {"status": "FAILED", "error": str(exc)},
                ensure_ascii=False,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
