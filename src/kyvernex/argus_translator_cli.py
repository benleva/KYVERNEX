"""Command-line executive translator for human text and ARGUS matrices."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .argus_matrix import ArgusMatrixError, evaluate_argus_matrix
from .argus_translator import ArgusTranslationError, extract_argus_request, translate_argus_text


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex-argus-translate",
        description="Translate supported Italian statements into canonical ARGUS JSON.",
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", help="Human-language request supplied directly")
    source.add_argument("--input", help="UTF-8 text file; use '-' to read stdin")
    parser.add_argument("--matrix", help="Optional ARGUS matrix JSON to evaluate immediately")
    parser.add_argument("--output", help="Optional UTF-8 JSON output path")
    parser.add_argument("--force", action="store_true", help="Replace an existing output file")
    return parser


def _read_text(args: argparse.Namespace) -> str:
    if args.text is not None:
        return args.text
    if args.input == "-":
        return sys.stdin.read()
    return Path(args.input).expanduser().resolve().read_text(encoding="utf-8")


def _load_matrix(path: str) -> dict[str, Any]:
    payload: Any = json.loads(Path(path).expanduser().resolve().read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ArgusMatrixError("matrix JSON must be an object")
    return payload


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    output_path = Path(args.output).expanduser().resolve() if args.output else None
    try:
        if output_path and output_path.exists() and not args.force:
            raise ArgusTranslationError(f"output already exists: {output_path}; use --force to replace it")
        translation = translate_argus_text(_read_text(args))
        result: dict[str, Any] = {"translation": translation}
        if args.matrix:
            request = extract_argus_request(translation)
            result["decision"] = evaluate_argus_matrix(_load_matrix(args.matrix), request)
            result["status"] = "DECIDED"
        else:
            result["status"] = "TRANSLATED"
        rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")
        sys.stdout.write(rendered)
        return 0
    except (OSError, json.JSONDecodeError, ArgusTranslationError, ArgusMatrixError) as exc:
        print(json.dumps({"status": "FAILED", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
