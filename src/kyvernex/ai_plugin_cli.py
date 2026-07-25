"""Command-line bridge for AI hosts using newline-delimited JSON."""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from .ai_bridge import KyvernexAIBridge
from .plugin_loader import load_handler


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex-ai-plugin",
        description="Expose one provider-neutral KYVERNEX AI tool over JSON input/output.",
    )
    parser.add_argument("--handler", required=True, help="Host callable as module:attribute")
    parser.add_argument("--principal", default="ai-host")
    parser.add_argument("--manifest", action="store_true", help="Print the tool manifest and exit")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        handler = load_handler(args.handler)
        with KyvernexAIBridge(handler, principal=args.principal) as bridge:
            if args.manifest:
                print(json.dumps(bridge.manifest(), ensure_ascii=False, sort_keys=True))
                return 0
            raw = sys.stdin.read()
            payload: Any = json.loads(raw)
            if not isinstance(payload, dict):
                raise ValueError("stdin JSON must be an object")
            response = bridge.invoke(payload)
            print(json.dumps(response, ensure_ascii=False, sort_keys=True))
            return 0 if response.get("status") == "SUCCEEDED" else 2
    except (ImportError, AttributeError, TypeError, ValueError, RuntimeError) as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
