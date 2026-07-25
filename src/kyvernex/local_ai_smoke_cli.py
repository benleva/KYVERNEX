"""Run a real local smoke verification of the KYVERNEX app stack."""
from __future__ import annotations

import json
import sys
from threading import Thread
from typing import Any, Mapping
from urllib.request import Request, urlopen

from .ai_bridge import KyvernexAIBridge
from .local_ai_server import KyvernexLocalAIServer


def _demo_handler(
    request: Mapping[str, Any],
    authority: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "received": dict(request),
        "principal": authority.get("principal"),
        "handled_by": "kyvernex-local-smoke",
    }


def _read_json(url: str) -> dict[str, Any]:
    with urlopen(url, timeout=5) as response:
        payload = json.load(response)
    if not isinstance(payload, dict):
        raise ValueError(f"response from {url} must be a JSON object")
    return payload


def _post_json(url: str, payload: Mapping[str, Any]) -> dict[str, Any]:
    request = Request(
        url,
        data=json.dumps(dict(payload), ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=5) as response:
        result = json.load(response)
    if not isinstance(result, dict):
        raise ValueError(f"response from {url} must be a JSON object")
    return result


def main(argv: list[str] | None = None) -> int:
    if argv:
        print(
            json.dumps(
                {"status": "FAILED", "error": "kyvernex-ai-smoke accepts no arguments"},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 2

    bridge = KyvernexAIBridge(_demo_handler, principal="smoke-user")
    server = KyvernexLocalAIServer(bridge, port=0)
    host, port = server.address
    base_url = f"http://{host}:{port}"
    thread = Thread(target=server.serve_forever, name="kyvernex-smoke-server", daemon=True)
    thread.start()

    checks: dict[str, Any] = {}
    try:
        health = _read_json(f"{base_url}/health")
        checks["health"] = health

        direct = _post_json(
            f"{base_url}/invoke",
            {"input": {"message": "hello-direct"}},
        )
        if direct.get("status") != "SUCCEEDED":
            raise RuntimeError("direct invocation did not succeed")
        checks["invoke"] = direct

        tool_call = _post_json(
            f"{base_url}/tool-call",
            {
                "id": "smoke-call-1",
                "name": "kyvernex_execute",
                "arguments": {"input": {"message": "hello-tool-call"}},
            },
        )
        if tool_call.get("status") != "SUCCEEDED":
            raise RuntimeError("tool-call invocation did not succeed")
        if tool_call.get("tool_call_id") != "smoke-call-1":
            raise RuntimeError("tool-call correlation id was not preserved")
        checks["tool_call"] = tool_call

        print(
            json.dumps(
                {
                    "status": "SUCCEEDED",
                    "server": base_url,
                    "checks": checks,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 0
    except (OSError, TypeError, ValueError, RuntimeError) as exc:
        print(
            json.dumps(
                {
                    "status": "FAILED",
                    "server": base_url,
                    "error": str(exc),
                    "checks": checks,
                },
                ensure_ascii=False,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 1
    finally:
        server.shutdown()
        thread.join(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
