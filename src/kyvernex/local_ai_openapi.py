"""OpenAPI document for the loopback-only KYVERNEX AI server."""
from __future__ import annotations

from typing import Any


def build_local_ai_openapi(*, host: str, port: int) -> dict[str, Any]:
    """Build the OpenAPI description for the existing local server contract."""
    base_url = f"http://{host}:{port}"
    invoke_schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["input"],
        "properties": {
            "input": {"type": "object"},
            "context": {"type": "object"},
            "request_id": {"type": "string", "minLength": 1},
        },
    }
    tool_call_schema = {
        "type": "object",
        "additionalProperties": False,
        "required": ["name", "arguments"],
        "properties": {
            "id": {"type": "string", "minLength": 1},
            "name": {"type": "string", "const": "kyvernex_execute"},
            "arguments": invoke_schema,
        },
    }
    json_response = {
        "description": "JSON response",
        "content": {"application/json": {"schema": {"type": "object"}}},
    }
    return {
        "openapi": "3.1.0",
        "info": {
            "title": "KYVERNEX Local AI Tool Server",
            "version": "1.2.0.dev0",
            "description": "Loopback-only API for one governed KYVERNEX AI tool.",
        },
        "servers": [{"url": base_url, "description": "Local loopback server"}],
        "paths": {
            "/health": {
                "get": {
                    "operationId": "kyvernexHealth",
                    "summary": "Read local bridge health",
                    "responses": {"200": json_response},
                }
            },
            "/manifest": {
                "get": {
                    "operationId": "kyvernexManifest",
                    "summary": "Read the canonical or provider-shaped tool manifest",
                    "parameters": [{
                        "name": "format",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "enum": ["canonical", "openai", "anthropic", "gemini"],
                            "default": "canonical",
                        },
                    }],
                    "responses": {"200": json_response, "400": json_response},
                }
            },
            "/invoke": {
                "post": {
                    "operationId": "kyvernexInvoke",
                    "summary": "Execute one governed KYVERNEX request with direct arguments",
                    "requestBody": {
                        "required": True,
                        "content": {"application/json": {"schema": invoke_schema}},
                    },
                    "responses": {
                        "200": json_response,
                        "400": json_response,
                        "422": json_response,
                    },
                }
            },
            "/tool-call": {
                "post": {
                    "operationId": "kyvernexToolCall",
                    "summary": "Execute one governed KYVERNEX canonical tool-call envelope",
                    "requestBody": {
                        "required": True,
                        "content": {"application/json": {"schema": tool_call_schema}},
                    },
                    "responses": {
                        "200": json_response,
                        "400": json_response,
                        "422": json_response,
                    },
                }
            },
            "/openapi.json": {
                "get": {
                    "operationId": "kyvernexOpenAPI",
                    "summary": "Read this OpenAPI document",
                    "responses": {"200": json_response},
                }
            },
        },
    }
