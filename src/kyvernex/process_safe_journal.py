from __future__ import annotations

from pathlib import Path

from .deletion import DeletionPolicy, DeletionResult
from .graph import CognitiveGraph
from .memory import SessionMemory
from .process_lock import InterProcessFileLock
from .transaction_journal import MultiTransactionDeletionCoordinator, RecoveryBatch


class ProcessSafeMultiTransactionDeletionCoordinator(MultiTransactionDeletionCoordinator):
    """Serializes journal mutation across cooperating operating-system processes."""

    LOCK_FILENAME = ".kyvernex-deletion.lock"

    def __init__(
        self,
        *,
        memory: SessionMemory,
        graph: CognitiveGraph,
        journal_directory: str | Path,
        recover_on_startup: bool = True,
        lock_timeout: float = 10.0,
        lock_poll_interval: float = 0.05,
    ) -> None:
        directory = Path(journal_directory)
        self._process_lock = InterProcessFileLock(
            directory / self.LOCK_FILENAME,
            timeout=lock_timeout,
            poll_interval=lock_poll_interval,
        )
        super().__init__(
            memory=memory,
            graph=graph,
            journal_directory=directory,
            recover_on_startup=False,
        )
        if recover_on_startup:
            self.recover_all()

    @property
    def process_lock_path(self) -> Path:
        return self._process_lock.path

    def delete(
        self,
        *,
        session_id: str,
        object_id: str,
        policy: DeletionPolicy = DeletionPolicy.RESTRICT,
    ) -> DeletionResult:
        with self._process_lock:
            return super().delete(
                session_id=session_id,
                object_id=object_id,
                policy=policy,
            )

    def recover_all(self, *, continue_on_error: bool = False) -> RecoveryBatch:
        with self._process_lock:
            return super().recover_all(continue_on_error=continue_on_error)

    def pending_transactions(self) -> tuple[str, ...]:
        with self._process_lock:
            return super().pending_transactions()
