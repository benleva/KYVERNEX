from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from .core import KyvernexEngine
from .serialization import to_primitive


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex",
        description="Run the KYVERNEX Reference Prototype on one input.",
    )
    parser.add_argument("content", help="Content to acquire, translate and validate")
    parser.add_argument(
        "--source",
        required=True,
        help="Declared origin of the content",
    )
    parser.add_argument(
        "--session-id",
        default=None,
        help="Optional stable session identifier",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation level",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = KyvernexEngine().execute(
        args.content,
        source=args.source,
        session_id=args.session_id,
    )
    json.dump(
        to_primitive(result),
        sys.stdout,
        ensure_ascii=False,
        indent=args.indent,
        sort_keys=True,
    )
    sys.stdout.write("\n")
    return 0 if not result.validation.errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
