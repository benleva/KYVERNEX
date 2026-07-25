from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Mapping, Sequence

from .program_manager import (
    DefinitionOfDone,
    GovernanceCheckpoint,
    GovernanceState,
    KGOError,
    KPMError,
    KyvernexGovernanceOrchestrator,
    KyvernexProgramManager,
    Milestone,
    Priority,
    WorkItem,
    WorkStatus,
)


class GovernanceCLIError(RuntimeError):
    """Raised when a governance CLI input or operation fails closed."""


EXIT_OK = 0
EXIT_BLOCKED = 2
EXIT_INVALID = 3
EXIT_NOT_PERMITTED = 4


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kyvernex-governance",
        description="Control the deterministic KYVERNEX KPM/KGO governance cycle.",
    )
    parser.add_argument("command", choices=("start", "status", "advance", "resume"))
    parser.add_argument("--plan", required=True, type=Path, help="UTF-8 JSON governance plan")
    parser.add_argument("--checkpoint", required=True, type=Path, help="Governed checkpoint path")
    parser.add_argument("--indent", type=int, default=2, help="JSON indentation level")
    return parser


def _read_json(path: Path, *, label: str) -> Mapping[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise GovernanceCLIError(f"{label}_NON_LEGGIBILE") from exc
    try:
        value = json.loads(raw)
    except JSONDecodeError as exc:
        raise GovernanceCLIError(f"{label}_JSON_NON_VALIDO") from exc
    if not isinstance(value, dict):
        raise GovernanceCLIError(f"{label}_OGGETTO_RICHIESTO")
    return value


def _required_text(data: Mapping[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise GovernanceCLIError(f"CAMPO_NON_VALIDO:{key}")
    return value


def _optional_bool(data: Mapping[str, Any], key: str, *, default: bool = False) -> bool:
    value = data.get(key, default)
    if not isinstance(value, bool):
        raise GovernanceCLIError(f"CAMPO_NON_VALIDO:{key}")
    return value


def _parse_done(value: Any) -> DefinitionOfDone:
    if value is None:
        return DefinitionOfDone()
    if not isinstance(value, dict):
        raise GovernanceCLIError("DEFINITION_OF_DONE_NON_VALIDA")
    allowed = set(DefinitionOfDone.__dataclass_fields__)
    unknown = set(value) - allowed
    if unknown or any(not isinstance(flag, bool) for flag in value.values()):
        raise GovernanceCLIError("DEFINITION_OF_DONE_NON_VALIDA")
    return DefinitionOfDone(**value)


def load_plan(path: Path) -> tuple[str, KyvernexProgramManager]:
    payload = _read_json(path, label="PLAN")
    target_version = _required_text(payload, "target_version")
    milestone_values = payload.get("milestones")
    item_values = payload.get("items")
    if not isinstance(milestone_values, list) or not milestone_values:
        raise GovernanceCLIError("MILESTONE_MANCANTI")
    if not isinstance(item_values, list):
        raise GovernanceCLIError("TASK_MANCANTI")

    milestones: list[Milestone] = []
    for raw in milestone_values:
        if not isinstance(raw, dict):
            raise GovernanceCLIError("MILESTONE_NON_VALIDO")
        milestones.append(
            Milestone(
                milestone_id=_required_text(raw, "milestone_id"),
                title=_required_text(raw, "title"),
                target_version=_required_text(raw, "target_version"),
                closed=_optional_bool(raw, "closed"),
            )
        )

    items: list[WorkItem] = []
    for raw in item_values:
        if not isinstance(raw, dict):
            raise GovernanceCLIError("TASK_NON_VALIDO")
        dependencies = raw.get("dependencies", [])
        if not isinstance(dependencies, list) or any(not isinstance(dep, str) or not dep for dep in dependencies):
            raise GovernanceCLIError("DIPENDENZE_NON_VALIDE")
        story_points = raw.get("story_points")
        if not isinstance(story_points, int) or isinstance(story_points, bool):
            raise GovernanceCLIError("STORY_POINT_NON_VALIDI")
        try:
            priority = Priority(raw.get("priority", Priority.P2.value))
            status = WorkStatus(raw.get("status", WorkStatus.BACKLOG.value))
        except ValueError as exc:
            raise GovernanceCLIError("ENUM_NON_VALIDO") from exc
        items.append(
            WorkItem(
                item_id=_required_text(raw, "item_id"),
                title=_required_text(raw, "title"),
                milestone_id=_required_text(raw, "milestone_id"),
                priority=priority,
                story_points=story_points,
                status=status,
                dependencies=tuple(dependencies),
                done=_parse_done(raw.get("done")),
            )
        )

    try:
        manager = KyvernexProgramManager(milestones=milestones, items=items)
    except (KPMError, ValueError) as exc:
        raise GovernanceCLIError(str(exc)) from exc

    for milestone in manager.milestones.values():
        if milestone.closed:
            related = [item for item in manager.items.values() if item.milestone_id == milestone.milestone_id]
            if not related or any(item.status != WorkStatus.DONE for item in related):
                raise GovernanceCLIError("MILESTONE_CHIUSA_CON_LAVORO_INCOMPLETO")
    return target_version, manager


def _checkpoint_payload(checkpoint: GovernanceCheckpoint) -> dict[str, Any]:
    payload = asdict(checkpoint)
    payload["mode"] = checkpoint.mode.value
    payload["state"] = checkpoint.state.value
    return payload


def _emit(checkpoint: GovernanceCheckpoint, *, indent: int) -> None:
    json.dump(_checkpoint_payload(checkpoint), sys.stdout, ensure_ascii=False, indent=indent, sort_keys=True)
    sys.stdout.write("\n")


def _exit_for(checkpoint: GovernanceCheckpoint) -> int:
    return EXIT_BLOCKED if checkpoint.state == GovernanceState.BLOCKED else EXIT_OK


def _orchestrator(plan: Path, checkpoint: Path) -> KyvernexGovernanceOrchestrator:
    target_version, manager = load_plan(plan)
    return KyvernexGovernanceOrchestrator(
        manager=manager,
        target_version=target_version,
        checkpoint_path=checkpoint,
    )


def run(command: str, *, plan: Path, checkpoint: Path) -> GovernanceCheckpoint:
    orchestrator = _orchestrator(plan, checkpoint)
    if command == "start":
        if checkpoint.exists():
            raise PermissionError("CHECKPOINT_GIA_ESISTENTE")
        return orchestrator.start_autonomous()
    if not checkpoint.exists():
        raise GovernanceCLIError("CHECKPOINT_NON_TROVATO")
    restored = orchestrator.resume()
    if command in {"status", "resume"}:
        return restored
    if command == "advance":
        if restored.current_item_id is not None:
            raise PermissionError("TASK_CORRENTE_ANCORA_ATTIVO")
        return orchestrator.advance()
    raise GovernanceCLIError("COMANDO_NON_SUPPORTATO")


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        checkpoint = run(args.command, plan=args.plan, checkpoint=args.checkpoint)
    except PermissionError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_NOT_PERMITTED
    except (GovernanceCLIError, KPMError, KGOError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_INVALID
    _emit(checkpoint, indent=args.indent)
    return _exit_for(checkpoint)


if __name__ == "__main__":
    raise SystemExit(main())
