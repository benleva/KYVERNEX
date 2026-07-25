from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import PurePosixPath
from typing import Iterable


class IsolatedCommitError(RuntimeError):
    """Raised when a proposed repository change violates the isolated boundary."""


class ChangeOperation(StrEnum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


@dataclass(slots=True, frozen=True)
class FileChange:
    path: str
    operation: ChangeOperation
    content_sha256: str | None = None

    def __post_init__(self) -> None:
        normalized = _normalize_path(self.path)
        object.__setattr__(self, "path", normalized)
        if self.operation in {ChangeOperation.CREATE, ChangeOperation.UPDATE} and not self.content_sha256:
            raise ValueError("CONTENT_HASH_REQUIRED")
        if self.operation is ChangeOperation.DELETE and self.content_sha256 is not None:
            raise ValueError("DELETE_CONTENT_HASH_FORBIDDEN")

    @classmethod
    def from_content(cls, path: str, operation: ChangeOperation, content: str) -> "FileChange":
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return cls(path=path, operation=operation, content_sha256=digest)


@dataclass(slots=True, frozen=True)
class IsolatedCommitPolicy:
    allowed_roots: tuple[str, ...] = ("src", "tests", "repository", ".github", "PROJECT_STATUS.md")
    forbidden_paths: tuple[str, ...] = (".git", ".env", "secrets")
    max_files: int = 25
    require_base_commit: bool = True
    require_explicit_authorization: bool = True

    def __post_init__(self) -> None:
        if self.max_files <= 0:
            raise ValueError("MAX_FILES_INVALID")
        if not self.allowed_roots:
            raise ValueError("ALLOWED_ROOTS_REQUIRED")


@dataclass(slots=True, frozen=True)
class IsolatedCommitPlan:
    schema: str
    work_item: str
    base_commit: str | None
    commit_message: str
    changes: tuple[FileChange, ...]
    authorized: bool
    fingerprint: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True) + "\n"


class SafeIsolatedCommitManager:
    """Validates and seals one coherent, policy-bounded repository mutation.

    This component does not call GitHub or execute git commands. It creates a
    deterministic plan that an authorized executor can apply without silently
    widening the selected work-item boundary.
    """

    def __init__(self, policy: IsolatedCommitPolicy | None = None) -> None:
        self.policy = policy or IsolatedCommitPolicy()

    def prepare(
        self,
        *,
        work_item: str,
        base_commit: str | None,
        commit_message: str,
        changes: Iterable[FileChange],
        authorized: bool = False,
    ) -> IsolatedCommitPlan:
        item = work_item.strip()
        message = commit_message.strip()
        if not item:
            raise IsolatedCommitError("WORK_ITEM_REQUIRED")
        if not message:
            raise IsolatedCommitError("COMMIT_MESSAGE_REQUIRED")
        if self.policy.require_base_commit and not base_commit:
            raise IsolatedCommitError("BASE_COMMIT_REQUIRED")
        if self.policy.require_explicit_authorization and not authorized:
            raise IsolatedCommitError("EXPLICIT_AUTHORIZATION_REQUIRED")

        ordered = tuple(sorted(changes, key=lambda change: (change.path, change.operation.value)))
        if not ordered:
            raise IsolatedCommitError("EMPTY_CHANGESET")
        if len(ordered) > self.policy.max_files:
            raise IsolatedCommitError("CHANGESET_FILE_LIMIT_EXCEEDED")

        seen: set[str] = set()
        for change in ordered:
            self._validate_path(change.path)
            if change.path in seen:
                raise IsolatedCommitError(f"DUPLICATE_PATH:{change.path}")
            seen.add(change.path)

        payload = {
            "work_item": item,
            "base_commit": base_commit,
            "commit_message": message,
            "changes": [asdict(change) for change in ordered],
            "authorized": authorized,
        }
        fingerprint = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return IsolatedCommitPlan(
            schema="kyvernex.isolated-commit-plan.v1",
            work_item=item,
            base_commit=base_commit,
            commit_message=message,
            changes=ordered,
            authorized=authorized,
            fingerprint=fingerprint,
        )

    def verify_unchanged(self, plan: IsolatedCommitPlan, changes: Iterable[FileChange]) -> bool:
        candidate = self.prepare(
            work_item=plan.work_item,
            base_commit=plan.base_commit,
            commit_message=plan.commit_message,
            changes=changes,
            authorized=plan.authorized,
        )
        return candidate.fingerprint == plan.fingerprint

    def _validate_path(self, path: str) -> None:
        parts = PurePosixPath(path).parts
        if any(forbidden in parts or path == forbidden for forbidden in self.policy.forbidden_paths):
            raise IsolatedCommitError(f"FORBIDDEN_PATH:{path}")
        if not any(path == root or path.startswith(f"{root}/") for root in self.policy.allowed_roots):
            raise IsolatedCommitError(f"PATH_OUTSIDE_ISOLATED_BOUNDARY:{path}")


def _normalize_path(path: str) -> str:
    raw = path.strip().replace("\\", "/")
    candidate = PurePosixPath(raw)
    if not raw or candidate.is_absolute() or ".." in candidate.parts or "." in candidate.parts:
        raise ValueError("INVALID_REPOSITORY_PATH")
    normalized = candidate.as_posix()
    if normalized.startswith("/"):
        raise ValueError("INVALID_REPOSITORY_PATH")
    return normalized
