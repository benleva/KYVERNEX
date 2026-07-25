"""Create one explicit local KYVERNEX profile, portable launchers, and optionally run it."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .local_ai_app_cli import main as launch_local_ai_app
from .local_ai_profile import load_local_ai_profile
from .local_ai_shortcut_cli import main as create_local_ai_shortcuts


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex-ai-setup",
        description="Create a strict local profile and optional portable launchers for KYVERNEX.",
    )
    parser.add_argument("--output", default="kyvernex.local.json")
    parser.add_argument("--handler", required=True, help="Host callable as module:attribute")
    parser.add_argument("--principal", default="ai-host")
    parser.add_argument("--port", type=int, default=8765)
    browser = parser.add_mutually_exclusive_group()
    browser.add_argument("--browser", dest="open_browser", action="store_true")
    browser.add_argument("--no-browser", dest="open_browser", action="store_false")
    parser.set_defaults(open_browser=True)
    parser.add_argument("--force", action="store_true", help="Replace existing generated files")
    parser.add_argument(
        "--launchers",
        action="store_true",
        help="Generate portable Windows, macOS and Linux launch files",
    )
    parser.add_argument(
        "--launcher-platform",
        choices=("all", "windows", "macos", "linux"),
        default="all",
    )
    parser.add_argument("--launcher-dir", default="kyvernex-launchers")
    parser.add_argument(
        "--launch",
        action="store_true",
        help="Start kyvernex-ai-app immediately with the profile just created",
    )
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

        launcher_status: int | None = None
        if args.launchers:
            shortcut_args = [
                "--profile",
                str(output),
                "--platform",
                args.launcher_platform,
                "--output-dir",
                args.launcher_dir,
            ]
            if args.force:
                shortcut_args.append("--force")
            launcher_status = create_local_ai_shortcuts(shortcut_args)
            if launcher_status != 0:
                return launcher_status

        print(
            json.dumps(
                {
                    "status": "CREATED",
                    "profile": str(output),
                    "configuration": validated,
                    "launchers_requested": args.launchers,
                    "launcher_platform": args.launcher_platform if args.launchers else None,
                    "launcher_directory": args.launcher_dir if args.launchers else None,
                    "launch_requested": args.launch,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        if args.launch:
            return launch_local_ai_app(["--profile", str(output)])
        return 0
    except (OSError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
