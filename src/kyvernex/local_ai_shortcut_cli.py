"""Generate portable launch scripts for an explicit local KYVERNEX profile."""
from __future__ import annotations

import argparse
import json
import os
import shlex
import stat
import subprocess
import sys
from pathlib import Path

from .local_ai_profile import load_local_ai_profile


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex-ai-shortcut",
        description="Generate portable Windows, macOS or Linux launch files for kyvernex-ai-app.",
    )
    parser.add_argument("--profile", required=True, help="Explicit local JSON profile")
    parser.add_argument("--output-dir", default="kyvernex-launchers")
    parser.add_argument(
        "--platform",
        choices=("all", "windows", "macos", "linux"),
        default="all",
    )
    parser.add_argument("--force", action="store_true", help="Replace existing launcher files")
    return parser


def _windows_script(profile: Path) -> str:
    command = subprocess.list2cmdline(["kyvernex-ai-app", "--profile", str(profile)])
    return "@echo off\r\n" + command + "\r\n"


def _posix_script(profile: Path) -> str:
    command = "kyvernex-ai-app --profile " + shlex.quote(str(profile))
    return "#!/bin/sh\nset -eu\nexec " + command + "\n"


def _targets(platform: str, output_dir: Path, profile: Path) -> list[tuple[Path, str, bool]]:
    result: list[tuple[Path, str, bool]] = []
    if platform in {"all", "windows"}:
        result.append((output_dir / "start-kyvernex.cmd", _windows_script(profile), False))
    if platform in {"all", "macos"}:
        result.append((output_dir / "start-kyvernex.command", _posix_script(profile), True))
    if platform in {"all", "linux"}:
        result.append((output_dir / "start-kyvernex.sh", _posix_script(profile), True))
    return result


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        profile = Path(args.profile).expanduser().resolve(strict=True)
        load_local_ai_profile(profile)
        output_dir = Path(args.output_dir).expanduser()
        targets = _targets(args.platform, output_dir, profile)
        existing = [path for path, _, _ in targets if path.exists()]
        if existing and not args.force:
            names = ", ".join(str(path) for path in existing)
            raise ValueError(f"launcher files already exist: {names}; use --force to replace them")

        output_dir.mkdir(parents=True, exist_ok=True)
        created: list[str] = []
        for path, content, executable in targets:
            path.write_text(content, encoding="utf-8", newline="")
            if executable:
                mode = path.stat().st_mode
                path.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            created.append(str(path))

        print(
            json.dumps(
                {
                    "status": "CREATED",
                    "profile": str(profile),
                    "launchers": created,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except (OSError, TypeError, ValueError) as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
