import json
from pathlib import Path

import pytest

from kyvernex.bootstrap import BootstrapError, boot


def _write(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _project(tmp_path: Path) -> Path:
    root = tmp_path / "project"
    load_order = [
        ".kyvernex/Constitution.argus",
        ".kyvernex/Rules/KPM.argus",
        ".kyvernex/Rules/KGO.argus",
        ".kyvernex/Rules/KTC.argus",
        ".kyvernex/Memory/KPM.json",
        ".kyvernex/Memory/KGO_BACKLOG.json",
    ]
    _write(
        root / ".kyvernex/BOOT.argus",
        {
            "schema": "kyvernex.argus.boot.v1",
            "mandatory": True,
            "load_order": load_order,
        },
    )
    _write(root / ".kyvernex/Constitution.argus", {"schema": "constitution", "phase": "alpha"})
    _write(root / ".kyvernex/Rules/KPM.argus", {"schema": "rules", "module": "KPM"})
    _write(root / ".kyvernex/Rules/KGO.argus", {"schema": "rules", "module": "KGO"})
    _write(root / ".kyvernex/Rules/KTC.argus", {"schema": "rules", "module": "KTC"})
    _write(root / ".kyvernex/Memory/KPM.json", {"schema": "kpm", "phase": "alpha"})
    _write(
        root / ".kyvernex/Memory/KGO_BACKLOG.json",
        {
            "schema": "kgo",
            "tasks": [
                {"id": "LATER", "priority": 5, "status": "READY"},
                {"id": "FIRST", "priority": 1, "status": "READY"},
                {"id": "BLOCKED", "priority": 0, "status": "BLOCKED"},
            ],
        },
    )
    return root


def test_boot_loads_documents_and_selects_highest_priority_ready_task(tmp_path):
    root = _project(tmp_path)

    state = boot(root)

    assert state.root == root.resolve()
    assert state.constitution["phase"] == "alpha"
    assert state.kpm["phase"] == "alpha"
    assert state.next_task is not None
    assert state.next_task["id"] == "FIRST"
    assert len(state.documents) == 6


def test_boot_rejects_missing_boot_document(tmp_path):
    with pytest.raises(BootstrapError, match="required bootstrap document is missing"):
        boot(tmp_path)


def test_boot_rejects_unsupported_schema(tmp_path):
    root = _project(tmp_path)
    _write(root / ".kyvernex/BOOT.argus", {"schema": "bad", "mandatory": True, "load_order": ["x"]})

    with pytest.raises(BootstrapError, match="unsupported BOOT.argus schema"):
        boot(root)


def test_boot_rejects_non_mandatory_bootstrap(tmp_path):
    root = _project(tmp_path)
    path = root / ".kyvernex/BOOT.argus"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["mandatory"] = False
    _write(path, payload)

    with pytest.raises(BootstrapError, match="must be mandatory"):
        boot(root)


def test_boot_rejects_document_outside_project_root(tmp_path):
    root = _project(tmp_path)
    path = root / ".kyvernex/BOOT.argus"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["load_order"] = ["../outside.json"]
    _write(path, payload)

    with pytest.raises(BootstrapError, match="escapes the project root"):
        boot(root)


def test_boot_returns_no_task_when_backlog_has_no_ready_items(tmp_path):
    root = _project(tmp_path)
    backlog = root / ".kyvernex/Memory/KGO_BACKLOG.json"
    _write(backlog, {"tasks": [{"id": "WAIT", "priority": 1, "status": "BLOCKED"}]})

    assert boot(root).next_task is None
