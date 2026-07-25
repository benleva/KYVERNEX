from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import PurePosixPath
from typing import Iterable

from .program_manager import WorkItem


class ChangeManifestError(RuntimeError):
    """Raised when a specification-to-change manifest is incomplete or unsafe."""


class ChangeKind(StrEnum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


@dataclass(slots=True, frozen=True)
class PlannedChange:
    path: str
    kind: ChangeKind
    rationale: str

    def __post_init__(self) -> None:
        normalized = PurePosixPath(self.path)
        if not self.path.strip() or normalized.is_absolute() or ".." in normalized.parts:
            raise ValueError("PERCORSO_MODIFICA_NON_VALIDO")
        if not self.rationale.strip():
            raise ValueError("MOTIVAZIONE_MODIFICA_MANCANTE")


@dataclass(slots=True, frozen=True)
class ChangeManifest:
    schema: str
    manifest_id: str
    work_item_id: str
    specification_path: str
    changes: tuple[PlannedChange, ...]
    targeted_tests: tuple[str, ...]
    complete_test_command: tuple[str, ...]
    dependencies: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.manifest_id.strip() or not self.work_item_id.strip():
            raise ValueError("IDENTIFICATORI_MANIFEST_MANCANTI")
        specification = PurePosixPath(self.specification_path)
        if specification.is_absolute() or ".." in specification.parts or not self.specification_path.strip():
            raise ValueError("PERCORSO_SPECIFICA_NON_VALIDO")
        if not self.changes:
            raise ChangeManifestError("MODIFICHE_MANIFEST_MANCANTI")
        if not self.targeted_tests:
            raise ChangeManifestError("TEST_MIRATI_MANCANTI")
        if not self.complete_test_command:
            raise ChangeManifestError("COMANDO_TEST_COMPLETO_MANCANTE")

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True) + "\n"


class SpecificationChangePlanner:
    """Builds deterministic change manifests from approved work-item scope."""

    def build(
        self,
        *,
        item: WorkItem,
        specification_path: str,
        changes: Iterable[PlannedChange],
        targeted_tests: Iterable[str],
        dependencies: Iterable[str] | None = None,
    ) -> ChangeManifest:
        planned_changes = tuple(changes)
        tests = tuple(dict.fromkeys(test.strip() for test in targeted_tests if test.strip()))
        declared_dependencies = tuple(dependencies) if dependencies is not None else item.dependencies
        return ChangeManifest(
            schema="kyvernex.change-manifest.v1",
            manifest_id=f"CM-{item.item_id}",
            work_item_id=item.item_id,
            specification_path=specification_path,
            changes=planned_changes,
            targeted_tests=tests,
            complete_test_command=("python", "-m", "pytest", "-q"),
            dependencies=tuple(declared_dependencies),
        )
