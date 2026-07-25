"""Create a self-contained editable local KYVERNEX project scaffold."""
from __future__ import annotations

import argparse
import json
import os
import shlex
import stat
import subprocess
import sys
from pathlib import Path

from .local_ai_app_cli import main as launch_local_ai_app
from .local_ai_profile import load_local_ai_profile

_HANDLER_SOURCE = '''"""Editable KYVERNEX host handler."""
from __future__ import annotations

from typing import Any, Mapping


def handle(request: Mapping[str, Any], authority: Mapping[str, Any]) -> dict[str, Any]:
    """Return a simple governed response. Replace this body with product logic."""
    return {
        "received": dict(request),
        "principal": authority.get("principal"),
        "capabilities": list(authority.get("capabilities", ())),
        "handled_by": "local-project",
    }
'''

_README = """# KYVERNEX local project

This folder is an editable local KYVERNEX project.

- `handler.py` contains the host callable.
- `kyvernex.local.json` contains the explicit launch profile.
- `start-kyvernex.cmd` launches on Windows.
- `start-kyvernex.command` launches on macOS.
- `start-kyvernex.sh` launches on Linux.

The launch files change into this folder before starting `kyvernex-ai-app`, so the local `handler.py` module can be imported explicitly as `handler:handle`.

The project can also be created and started immediately with `kyvernex-ai-project DIRECTORY --launch`.
"""


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex-ai-project",
        description="Create an editable local KYVERNEX project with handler, profile and portable launchers.",
    )
    parser.add_argument("directory", nargs="?", default="kyvernex-local-project")
    parser.add_argument("--principal", default="ai-host")
    parser.add_argument("--port", type=int, default=8765)
    browser = parser.add_mutually_exclusive_group()
    browser.add_argument("--browser", dest="open_browser", action="store_true")
    browser.add_argument("--no-browser", dest="open_browser", action="store_false")
    parser.set_defaults(open_browser=True)
    parser.add_argument("--force", action="store_true", help="Replace scaffold files that already exist")
    parser.add_argument(
        "--launch",
        action="store_true",
        help="Start the generated local project immediately after successful creation",
    )
    return parser


def _windows_script(project: Path) -> str:
    app = subprocess.list2cmdline(["kyvernex-ai-app", "--profile", "kyvernex.local.json"])
    return f"@echo off\r\ncd /d \"{project}\"\r\n{app}\r\n"


def _posix_script(project: Path) -> str:
    return "#!/bin/sh\nset -eu\ncd " + shlex.quote(str(project)) + "\nexec kyvernex-ai-app --profile kyvernex.local.json\n"


def _launch_project(project: Path) -> int:
    previous = Path.cwd()
    try:
        os.chdir(project)
        return launch_local_ai_app(["--profile", "kyvernex.local.json"])
    finally:
        os.chdir(previous)


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    project = Path(args.directory).expanduser().resolve()
    files = {
        project / "handler.py": _HANDLER_SOURCE,
        project / "kyvernex.local.json": json.dumps(
            {
                "handler": "handler:handle",
                "principal": args.principal,
                "port": args.port,
                "open_browser": args.open_browser,
            },
            ensure_ascii=False,
            indent=2,
        ) + "\n",
        project / "start-kyvernex.cmd": _windows_script(project),
        project / "start-kyvernex.command": _posix_script(project),
        project / "start-kyvernex.sh": _posix_script(project),
        project / "README.md": _README,
    }
    try:
        existing = [path for path in files if path.exists()]
        if existing and not args.force:
            names = ", ".join(str(path) for path in existing)
            raise ValueError(f"project files already exist: {names}; use --force to replace them")
        project.mkdir(parents=True, exist_ok=True)
        for path, content in files.items():
            path.write_text(content, encoding="utf-8", newline="")
        for path in (project / "start-kyvernex.command", project / "start-kyvernex.sh"):
            path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        profile = load_local_ai_profile(project / "kyvernex.local.json")
        print(json.dumps({
            "status": "CREATED",
            "project": str(project),
            "profile": profile,
            "files": [str(path) for path in files],
            "launch_requested": args.launch,
        }, ensure_ascii=False, sort_keys=True))
        if args.launch:
            return _launch_project(project)
        return 0
    except (OSError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
