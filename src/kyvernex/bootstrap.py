"""Executable ARGUS bootstrap loader for KYVERNEX projects."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

BOOT_PATH = Path(".kyvernex/BOOT.argus")
EXPECTED_BOOT_SCHEMA = "kyvernex.argus.boot.v1"


class BootstrapError(ValueError):
    """Raised when a KYVERNEX project cannot be bootstrapped safely."""


@dataclass(frozen=True, slots=True)
class ProjectState:
    """Immutable state produced by one deterministic ARGUS bootstrap."""

    root: Path
    boot: Mapping[str, Any]
    documents: Mapping[str, Mapping[str, Any]]
    constitution: Mapping[str, Any]
    kpm: Mapping[str, Any]
    kgo_backlog: Mapping[str, Any]
    next_task: Mapping[str, Any] | None


def _load_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise BootstrapError(f"required bootstrap document is missing: {path}") from exc
    except OSError as exc:
        raise BootstrapError(f"cannot read bootstrap document: {path}") from exc
    except json.JSONDecodeError as exc:
        raise BootstrapError(f"bootstrap document is not valid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise BootstrapError(f"bootstrap document must contain a JSON object: {path}")
    return payload


def _resolve_document(root: Path, relative_name: object) -> Path:
    if not isinstance(relative_name, str) or not relative_name.strip():
        raise BootstrapError("BOOT.argus load_order entries must be non-empty strings")
    candidate = (root / relative_name).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise BootstrapError(f"bootstrap document escapes the project root: {relative_name}") from exc
    return candidate


def _select_next_task(backlog: Mapping[str, Any]) -> Mapping[str, Any] | None:
    tasks = backlog.get("tasks", [])
    if not isinstance(tasks, list):
        raise BootstrapError("KGO backlog tasks must be a list")
    ready = [task for task in tasks if isinstance(task, dict) and task.get("status") == "READY"]
    if not ready:
        return None
    return min(ready, key=lambda task: (task.get("priority", 2**31), str(task.get("id", ""))))


def boot(project_path: str | Path) -> ProjectState:
    """Load BOOT.argus and return the governed state for *project_path*.

    The loader intentionally executes no arbitrary actions. During Alpha it
    interprets the bootstrap as a deterministic document graph, validates that
    every referenced file stays inside the project root, and selects the
    highest-priority READY KGO task.
    """

    root = Path(project_path).expanduser().resolve()
    boot_document = _load_object(root / BOOT_PATH)
    if boot_document.get("schema") != EXPECTED_BOOT_SCHEMA:
        raise BootstrapError(
            f"unsupported BOOT.argus schema {boot_document.get('schema')!r}; "
            f"expected {EXPECTED_BOOT_SCHEMA!r}"
        )
    if boot_document.get("mandatory") is not True:
        raise BootstrapError("BOOT.argus must be mandatory")

    load_order = boot_document.get("load_order")
    if not isinstance(load_order, list) or not load_order:
        raise BootstrapError("BOOT.argus load_order must be a non-empty list")

    documents: dict[str, Mapping[str, Any]] = {}
    for relative_name in load_order:
        document_path = _resolve_document(root, relative_name)
        documents[str(relative_name)] = _load_object(document_path)

    constitution = documents.get(".kyvernex/Constitution.argus")
    kpm = documents.get(".kyvernex/Memory/KPM.json")
    kgo_backlog = documents.get(".kyvernex/Memory/KGO_BACKLOG.json")
    if constitution is None:
        raise BootstrapError("BOOT.argus must load .kyvernex/Constitution.argus")
    if kpm is None:
        raise BootstrapError("BOOT.argus must load .kyvernex/Memory/KPM.json")
    if kgo_backlog is None:
        raise BootstrapError("BOOT.argus must load .kyvernex/Memory/KGO_BACKLOG.json")

    return ProjectState(
        root=root,
        boot=boot_document,
        documents=documents,
        constitution=constitution,
        kpm=kpm,
        kgo_backlog=kgo_backlog,
        next_task=_select_next_task(kgo_backlog),
    )
