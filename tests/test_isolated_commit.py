import pytest

from kyvernex.isolated_commit import (
    ChangeOperation,
    FileChange,
    IsolatedCommitError,
    SafeIsolatedCommitManager,
)


def test_authorized_changes_are_sorted_and_sealed_deterministically():
    manager = SafeIsolatedCommitManager()
    changes = [
        FileChange.from_content("tests/test_x.py", ChangeOperation.CREATE, "def test_x(): pass\n"),
        FileChange.from_content("src/kyvernex/x.py", ChangeOperation.CREATE, "VALUE = 1\n"),
    ]

    plan = manager.prepare(
        work_item="M3-W004",
        base_commit="abc123",
        commit_message="feat(m3): add isolated boundary",
        changes=changes,
        authorized=True,
    )

    assert plan.schema == "kyvernex.isolated-commit-plan.v1"
    assert [change.path for change in plan.changes] == ["src/kyvernex/x.py", "tests/test_x.py"]
    assert len(plan.fingerprint) == 64
    assert manager.verify_unchanged(plan, reversed(changes)) is True


def test_explicit_authorization_is_required():
    manager = SafeIsolatedCommitManager()
    change = FileChange.from_content("src/kyvernex/x.py", ChangeOperation.CREATE, "VALUE = 1\n")

    with pytest.raises(IsolatedCommitError, match="EXPLICIT_AUTHORIZATION_REQUIRED"):
        manager.prepare(
            work_item="M3-W004",
            base_commit="abc123",
            commit_message="feat: x",
            changes=(change,),
        )


def test_paths_outside_boundary_are_rejected():
    manager = SafeIsolatedCommitManager()
    change = FileChange.from_content("private/key.txt", ChangeOperation.CREATE, "secret")

    with pytest.raises(IsolatedCommitError, match="PATH_OUTSIDE_ISOLATED_BOUNDARY"):
        manager.prepare(
            work_item="M3-W004",
            base_commit="abc123",
            commit_message="feat: x",
            changes=(change,),
            authorized=True,
        )


def test_duplicate_path_is_rejected():
    manager = SafeIsolatedCommitManager()
    first = FileChange.from_content("src/kyvernex/x.py", ChangeOperation.CREATE, "VALUE = 1\n")
    second = FileChange.from_content("src/kyvernex/x.py", ChangeOperation.UPDATE, "VALUE = 2\n")

    with pytest.raises(IsolatedCommitError, match="DUPLICATE_PATH"):
        manager.prepare(
            work_item="M3-W004",
            base_commit="abc123",
            commit_message="feat: x",
            changes=(first, second),
            authorized=True,
        )


def test_mutated_changeset_fails_fingerprint_verification():
    manager = SafeIsolatedCommitManager()
    original = FileChange.from_content("src/kyvernex/x.py", ChangeOperation.CREATE, "VALUE = 1\n")
    plan = manager.prepare(
        work_item="M3-W004",
        base_commit="abc123",
        commit_message="feat: x",
        changes=(original,),
        authorized=True,
    )
    mutated = FileChange.from_content("src/kyvernex/x.py", ChangeOperation.CREATE, "VALUE = 2\n")

    assert manager.verify_unchanged(plan, (mutated,)) is False


def test_delete_cannot_carry_content_hash():
    with pytest.raises(ValueError, match="DELETE_CONTENT_HASH_FORBIDDEN"):
        FileChange("src/kyvernex/x.py", ChangeOperation.DELETE, "deadbeef")
