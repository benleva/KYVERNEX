"""Run a real local verification of the KYVERNEX app stack."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
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


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex-ai-smoke",
        description="Run a local KYVERNEX app verification and emit one JSON report.",
    )
    parser.add_argument(
        "--output",
        help="Optional UTF-8 JSON report path",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing report file",
    )
    return parser


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


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _write_report(path: Path | None, report: Mapping[str, Any], *, force: bool) -> None:
    if path is None:
        return
    if path.exists() and not force:
        raise ValueError(f"report already exists: {path}; use --force to replace it")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(dict(report), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    output = Path(args.output).expanduser() if args.output else None

    bridge = KyvernexAIBridge(_demo_handler, principal="smoke-user")
    server = KyvernexLocalAIServer(bridge, port=0)
    host, port = server.address
    base_url = f"http://{host}:{port}"
    thread = Thread(target=server.serve_forever, name="kyvernex-smoke-server", daemon=True)
    thread.start()

    checks: dict[str, Any] = {}
    report: dict[str, Any]
    exit_code = 0
    try:
        health = _read_json(f"{base_url}/health")
        _require(health.get("adapter_health", {}).get("status") == "HEALTHY", "adapter health is not HEALTHY")
        checks["health"] = health

        canonical = _read_json(f"{base_url}/manifest?format=canonical")
        _require(canonical.get("name") == "kyvernex_execute", "canonical manifest tool name is invalid")
        checks["manifest_canonical"] = canonical

        openai = _read_json(f"{base_url}/manifest?format=openai")
        _require(openai.get("function", {}).get("name") == "kyvernex_execute", "OpenAI manifest tool name is invalid")
        checks["manifest_openai"] = openai

        anthropic = _read_json(f"{base_url}/manifest?format=anthropic")
        _require(anthropic.get("name") == "kyvernex_execute", "Anthropic manifest tool name is invalid")
        checks["manifest_anthropic"] = anthropic

        gemini = _read_json(f"{base_url}/manifest?format=gemini")
        declarations = gemini.get("functionDeclarations")
        _require(
            isinstance(declarations, list)
            and len(declarations) == 1
            and declarations[0].get("name") == "kyvernex_execute",
            "Gemini manifest tool declaration is invalid",
        )
        checks["manifest_gemini"] = gemini

        openapi = _read_json(f"{base_url}/openapi.json")
        paths = openapi.get("paths", {})
        _require("/invoke" in paths and "/tool-call" in paths, "OpenAPI document is missing invocation routes")
        checks["openapi"] = {
            "openapi": openapi.get("openapi"),
            "version": openapi.get("info", {}).get("version"),
            "paths": sorted(paths),
        }

        direct = _post_json(
            f"{base_url}/invoke",
            {"input": {"message": "hello-direct"}},
        )
        _require(direct.get("status") == "SUCCEEDED", "direct invocation did not succeed")
        checks["invoke"] = direct

        tool_call = _post_json(
            f"{base_url}/tool-call",
            {
                "id": "smoke-call-1",
                "name": "kyvernex_execute",
                "arguments": {"input": {"message": "hello-tool-call"}},
            },
        )
        _require(tool_call.get("status") == "SUCCEEDED", "tool-call invocation did not succeed")
        _require(tool_call.get("tool_call_id") == "smoke-call-1", "tool-call correlation id was not preserved")
        checks["tool_call"] = tool_call

        report = {
            "status": "SUCCEEDED",
            "verification": "LOCAL_APP_SMOKE_VERIFIED",
            "server": base_url,
            "checks": checks,
            "not_verified": [
                "clean installation outside the current environment",
                "Windows, macOS and Linux launcher execution",
                "persistent JSONL mode",
                "timeouts, size limits and concurrent load",
                "full automated test suite",
                "release qualification",
            ],
        }
    except (OSError, TypeError, ValueError, RuntimeError) as exc:
        exit_code = 1
        report = {
            "status": "FAILED",
            "verification": "NOT_VERIFIED",
            "server": base_url,
            "error": str(exc),
            "checks": checks,
        }
    finally:
        server.shutdown()
        thread.join(timeout=5)

    try:
        _write_report(output, report, force=args.force)
    except (OSError, ValueError) as exc:
        print(
            json.dumps(
                {"status": "FAILED", "error": str(exc), "report": report},
                ensure_ascii=False,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 1

    stream = sys.stdout if exit_code == 0 else sys.stderr
    print(json.dumps(report, ensure_ascii=False, sort_keys=True), file=stream)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
