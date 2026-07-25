"""Localhost-only HTTP server exposing the canonical KYVERNEX AI bridge."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse

from .ai_bridge import KyvernexAIBridge
from .local_ai_openapi import build_local_ai_openapi
from .local_ai_page import build_local_ai_page


class KyvernexLocalAIServer:
    """Serve one KYVERNEX AI bridge on the loopback interface only."""

    def __init__(self, bridge: KyvernexAIBridge, *, port: int = 8765) -> None:
        if not isinstance(port, int) or isinstance(port, bool) or not 0 <= port <= 65535:
            raise ValueError("port must be an integer between 0 and 65535")
        self._bridge = bridge
        handler_type = self._build_handler(bridge)
        self._server = ThreadingHTTPServer(("127.0.0.1", port), handler_type)
        host, bound_port = self._server.server_address
        handler_type.openapi_document = build_local_ai_openapi(
            host=str(host),
            port=int(bound_port),
        )
        handler_type.console_page = build_local_ai_page()

    @property
    def address(self) -> tuple[str, int]:
        host, port = self._server.server_address
        return str(host), int(port)

    def serve_forever(self) -> None:
        self._server.serve_forever()

    def shutdown(self) -> None:
        self._server.shutdown()
        self._server.server_close()
        self._bridge.shutdown()

    @staticmethod
    def _build_handler(bridge: KyvernexAIBridge) -> type[BaseHTTPRequestHandler]:
        class Handler(BaseHTTPRequestHandler):
            server_version = "KYVERNEXLocalAI/1.0"
            openapi_document: dict[str, Any] = {}
            console_page: bytes = b""

            def _write_json(self, status: int, payload: Any) -> None:
                body = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)

            def _write_html(self, body: bytes) -> None:
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'")
                self.end_headers()
                self.wfile.write(body)

            def _read_json_object(self) -> dict[str, Any]:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 1_048_576:
                    raise ValueError("request body must be between 1 and 1048576 bytes")
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                if not isinstance(payload, dict):
                    raise ValueError("request JSON must be an object")
                return payload

            def do_GET(self) -> None:
                parsed = urlparse(self.path)
                if parsed.path in {"/", "/console"}:
                    self._write_html(self.console_page)
                    return
                if parsed.path == "/health":
                    self._write_json(200, dict(bridge.status()))
                    return
                if parsed.path == "/manifest":
                    format_name = parse_qs(parsed.query).get("format", ["canonical"])[0]
                    try:
                        payload = bridge.manifest_for(format_name)
                    except ValueError as exc:
                        self._write_json(400, {"status": "FAILED", "error": str(exc)})
                        return
                    self._write_json(200, payload)
                    return
                if parsed.path == "/openapi.json":
                    self._write_json(200, self.openapi_document)
                    return
                self._write_json(404, {"status": "FAILED", "error": "route not found"})

            def do_POST(self) -> None:
                path = urlparse(self.path).path
                if path not in {"/invoke", "/tool-call"}:
                    self._write_json(404, {"status": "FAILED", "error": "route not found"})
                    return
                try:
                    payload = self._read_json_object()
                    response = (
                        bridge.invoke_tool_call(payload)
                        if path == "/tool-call"
                        else bridge.invoke(payload)
                    )
                except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError, RuntimeError) as exc:
                    self._write_json(400, {"status": "FAILED", "error": str(exc)})
                    return
                status = 200 if response.get("status") == "SUCCEEDED" else 422
                self._write_json(status, response)

            def log_message(self, format: str, *args: object) -> None:
                return

        return Handler
