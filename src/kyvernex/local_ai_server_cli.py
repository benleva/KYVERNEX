"""Installed command for the localhost-only KYVERNEX AI tool server."""
from __future__ import annotations

import argparse
import json
import sys

from .ai_bridge import KyvernexAIBridge
from .local_ai_server import KyvernexLocalAIServer
from .plugin_loader import load_handler


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex-ai-server",
        description="Serve the canonical KYVERNEX AI tool on 127.0.0.1 only.",
    )
    parser.add_argument("--handler", required=True, help="Host callable as module:attribute")
    parser.add_argument("--principal", default="ai-host")
    parser.add_argument("--port", type=int, default=8765)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        handler = load_handler(args.handler)
        bridge = KyvernexAIBridge(handler, principal=args.principal)
        server = KyvernexLocalAIServer(bridge, port=args.port)
        host, port = server.address
        print(json.dumps({"status": "READY", "host": host, "port": port}, sort_keys=True))
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
