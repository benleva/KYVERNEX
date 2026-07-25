"""One-command launcher for the local KYVERNEX AI console."""
from __future__ import annotations

import argparse
import json
import sys
import webbrowser
from threading import Timer

from .ai_bridge import KyvernexAIBridge
from .local_ai_server import KyvernexLocalAIServer
from .plugin_loader import load_handler


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex-ai-app",
        description="Start the localhost KYVERNEX AI server and open its console.",
    )
    parser.add_argument("--handler", required=True, help="Host callable as module:attribute")
    parser.add_argument("--principal", default="ai-host")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Start the local app without opening the system browser",
    )
    return parser


def _open_console(url: str) -> None:
    try:
        webbrowser.open(url, new=1, autoraise=True)
    except webbrowser.Error:
        return


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        handler = load_handler(args.handler)
        bridge = KyvernexAIBridge(handler, principal=args.principal)
        server = KyvernexLocalAIServer(bridge, port=args.port)
        host, port = server.address
        console_url = f"http://{host}:{port}/"
        print(
            json.dumps(
                {
                    "status": "READY",
                    "host": host,
                    "port": port,
                    "console": console_url,
                },
                sort_keys=True,
            )
        )
        if not args.no_browser:
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
