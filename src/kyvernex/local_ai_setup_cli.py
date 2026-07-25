"""Create one explicit local KYVERNEX launch profile."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .local_ai_profile import load_local_ai_profile


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex-ai-setup",
        description="Create a strict local JSON profile for kyvernex-ai-app.",
    )
    parser.add_argument("--output", default="kyvernex.local.json")
    parser.add_argument("--handler", required=True, help="Host callable as module:attribute")
    parser.add_argument("--principal", default="ai-host")
    parser.add_argument("--port", type=int, default=8765)
    browser = parser.add_mutually_exclusive_group()
    browser.add_argument("--browser", dest="open_browser", action="store_true")
    browser.add_argument("--no-browser", dest="open_browser", action="store_false")
    parser.set_defaults(open_browser=True)
    parser.add_argument("--force", action="store_true", help="Replace an existing output file")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    output = Path(args.output)
    try:
        if output.exists() and not args.force:
            raise ValueError(f"profile already exists: {output}; use --force to replace it")
        payload = {
            "handler": args.handler,
            "principal": args.principal,
            "port": args.port,
            "open_browser": args.open_browser,
        }
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        validated = load_local_ai_profile(output)
        print(json.dumps({"status": "CREATED", "profile": str(output), "configuration": validated}, ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
