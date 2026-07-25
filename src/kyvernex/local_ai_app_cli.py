"""One-command launcher for the local KYVERNEX AI console."""
from __future__ import annotations

import argparse
import json
import sys
import webbrowser
from threading import Timer
from typing import Any

from .ai_bridge import KyvernexAIBridge
from .local_ai_profile import load_local_ai_profile
from .local_ai_server import KyvernexLocalAIServer
from .plugin_loader import load_handler


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex-ai-app",
        description="Start the localhost KYVERNEX AI server and open its console.",
    )
    parser.add_argument("--profile", help="Explicit local JSON profile path")
    parser.add_argument("--handler", help="Host callable as module:attribute")
    parser.add_argument("--principal")
    parser.add_argument("--port", type=int)
    browser = parser.add_mutually_exclusive_group()
    browser.add_argument("--browser", dest="open_browser", action="store_true")
    browser.add_argument("--no-browser", dest="open_browser", action="store_false")
    parser.set_defaults(open_browser=None)
    return parser


def _settings(args: argparse.Namespace) -> dict[str, Any]:
    profile = load_local_ai_profile(args.profile) if args.profile else {}
    settings = {
        "handler": args.handler if args.handler is not None else profile.get("handler"),
        "principal": args.principal if args.principal is not None else profile.get("principal", "ai-host"),
        "port": args.port if args.port is not None else profile.get("port", 8765),
        "open_browser": (
            args.open_browser if args.open_browser is not None else profile.get("open_browser", True)
        ),
    }
    if not isinstance(settings["handler"], str) or not settings["handler"].strip():
        raise ValueError("handler is required via --handler or profile.handler")
    if not isinstance(settings["principal"], str) or not settings["principal"].strip():
        raise ValueError("principal must be a non-empty string")
    if not isinstance(settings["port"], int) or isinstance(settings["port"], bool) or not 1 <= settings["port"] <= 65535:
        raise ValueError("port must be an integer between 1 and 65535")
    return settings


def _open_console(url: str) -> None:
    try:
        webbrowser.open(url, new=1, autoraise=True)
    except webbrowser.Error:
        return


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        settings = _settings(args)
        handler = load_handler(settings["handler"])
        bridge = KyvernexAIBridge(handler, principal=settings["principal"])
        server = KyvernexLocalAIServer(bridge, port=settings["port"])
        host, port = server.address
        console_url = f"http://{host}:{port}/"
        print(
            json.dumps(
                {
                    "status": "READY",
                    "host": host,
                    "port": port,
                    "console": console_url,
                    "profile": args.profile,
                },
                sort_keys=True,
            )
        )
        if settings["open_browser"]:
            Timer(0.35, _open_console, args=(console_url,)).start()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.shutdown()
        return 0
    except (ImportError, AttributeError, TypeError, ValueError, RuntimeError, OSError) as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
