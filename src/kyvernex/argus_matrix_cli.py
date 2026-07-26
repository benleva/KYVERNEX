"""Command-line runner for one explicit ARGUS JSON matrix."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .argus_matrix import ArgusMatrixError, evaluate_argus_matrix


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex-argus",
        description="Evaluate one JSON request against one deterministic ARGUS matrix.",
    )
    parser.add_argument("--matrix", required=True, help="Path to the ARGUS matrix JSON file")
    parser.add_argument("--request", help="Path to a request JSON file; stdin is used when omitted")
    parser.add_argument("--output", help="Optional path for the resulting JSON decision")
    parser.add_argument("--force", action="store_true", help="Replace an existing output file")
    return parser


def _load_object(path: Path | None, *, label: str) -> dict[str, Any]:
    raw = path.read_text(encoding="utf-8") if path else sys.stdin.read()
    payload: Any = json.loads(raw)
    if not isinstance(payload, dict):
        raise ArgusMatrixError(f"{label} JSON must be an object")
    return payload


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    matrix_path = Path(args.matrix).expanduser().resolve()
    request_path = Path(args.request).expanduser().resolve() if args.request else None
    output_path = Path(args.output).expanduser().resolve() if args.output else None
    try:
        if output_path and output_path.exists() and not args.force:
            raise ArgusMatrixError(f"output already exists: {output_path}; use --force to replace it")
        matrix = _load_object(matrix_path, label="matrix")
        request = _load_object(request_path, label="request")
        result = evaluate_argus_matrix(matrix, request)
        rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")
        sys.stdout.write(rendered)
        return 0
    except (OSError, json.JSONDecodeError, ArgusMatrixError) as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
