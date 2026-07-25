import json

import pytest

from kyvernex.change_manifest import (
    ChangeKind,
    ChangeManifestError,
    PlannedChange,
    SpecificationChangePlanner,
)
from kyvernex.program_manager import Priority, WorkItem, WorkStatus


def make_item():
    return WorkItem(
        "M3-W002",
        "Specification-to-change manifest",
        "M3",
        Priority.P0,
        5,
        WorkStatus.IN_DEVELOPMENT,
        dependencies=("M3-W001",),
    )


def test_builds_deterministic_manifest_from_work_item():
    manifest = SpecificationChangePlanner().build(
        item=make_item(),
        specification_path="repository/specifications/CHANGE_MANIFEST_SPEC_v0.1_DRAFT.md",
        changes=(
            PlannedChange("src/kyvernex/change_manifest.py", ChangeKind.CREATE, "Implement the manifest model."),
            PlannedChange("tests/test_change_manifest.py", ChangeKind.CREATE, "Verify manifest invariants."),
        ),
        targeted_tests=("tests/test_change_manifest.py", "tests/test_change_manifest.py"),
    )

    assert manifest.manifest_id == "CM-M3-W002"
    assert manifest.dependencies == ("M3-W001",)
    assert manifest.targeted_tests == ("tests/test_change_manifest.py",)
    assert manifest.complete_test_command == ("python", "-m", "pytest", "-q")


def test_manifest_is_machine_serializable():
    manifest = SpecificationChangePlanner().build(
        item=make_item(),
        specification_path="repository/specifications/CHANGE_MANIFEST_SPEC_v0.1_DRAFT.md",
        changes=(PlannedChange("README.md", ChangeKind.UPDATE, "Document the capability."),),
        targeted_tests=("tests/test_change_manifest.py",),
    )

    payload = json.loads(manifest.to_json())
    assert payload["schema"] == "kyvernex.change-manifest.v1"
    assert payload["changes"][0]["kind"] == "UPDATE"


def test_rejects_unsafe_repository_path():
    with pytest.raises(ValueError, match="PERCORSO_MODIFICA_NON_VALIDO"):
        PlannedChange("../outside.py", ChangeKind.UPDATE, "Unsafe escape.")


def test_rejects_manifest_without_targeted_tests():
    with pytest.raises(ChangeManifestError, match="TEST_MIRATI_MANCANTI"):
        SpecificationChangePlanner().build(
            item=make_item(),
            specification_path="repository/specifications/CHANGE_MANIFEST_SPEC_v0.1_DRAFT.md",
            changes=(PlannedChange("README.md", ChangeKind.UPDATE, "Document the capability."),),
            targeted_tests=(),
        )
