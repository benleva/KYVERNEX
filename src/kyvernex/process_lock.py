from __future__ import annotations

import os
import time
from pathlib import Path
from typing import IO


class ProcessLockError(RuntimeError):
    """Raised when an inter-process lock cannot be acquired or released safely."""


class InterProcessFileLock:
    """Advisory exclusive lock backed by a stable file.

    The implementation uses ``fcntl.flock`` on POSIX and ``msvcrt.locking`` on
    Windows. It protects cooperating KYVERNEX processes that use the same lock
    path. It is not a distributed lock and does not coordinate different hosts.
    """

    def __init__(
        self,
        path: str | Path,
        *,
        timeout: float = 10.0,
        poll_interval: float = 0.05,
    ) -> None:
        if timeout < 0:
            raise ValueError("LOCK_TIMEOUT_NEGATIVO")
        if poll_interval <= 0:
            raise ValueError("LOCK_POLL_INTERVAL_NON_VALIDO")
        self._path = Path(path)
        self._timeout = timeout
        self._poll_interval = poll_interval
        self._handle: IO[bytes] | None = None

    @property
    def path(self) -> Path:
        return self._path

    def acquire(self) -> None:
        if self._handle is not None:
            raise ProcessLockError("PROCESS_LOCK_GIA_ACQUISITO")
        self._path.parent.mkdir(parents=True, exist_ok=True)
        handle = self._path.open("a+b")
        deadline = time.monotonic() + self._timeout
        try:
            while True:
                try:
                    self._try_lock(handle)
                    self._handle = handle
                    return
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise ProcessLockError("PROCESS_LOCK_TIMEOUT")
                    time.sleep(self._poll_interval)
        except Exception:
            handle.close()
            raise

    def release(self) -> None:
        handle = self._handle
        if handle is None:
            raise ProcessLockError("PROCESS_LOCK_NON_ACQUISITO")
        try:
            self._unlock(handle)
        except OSError as exc:
            raise ProcessLockError("PROCESS_LOCK_RELEASE_FAILED") from exc
        finally:
            handle.close()
            self._handle = None

    def __enter__(self) -> InterProcessFileLock:
        self.acquire()
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.release()

    @staticmethod
    def _try_lock(handle: IO[bytes]) -> None:
        if os.name == "nt":
            import msvcrt

            handle.seek(0)
            if handle.read(1) == b"":
                handle.write(b"0")
                handle.flush()
            handle.seek(0)
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                raise BlockingIOError from exc
            return

        import fcntl

        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            raise BlockingIOError from exc

    @staticmethod
    def _unlock(handle: IO[bytes]) -> None:
        if os.name == "nt":
            import msvcrt

            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            return

        import fcntl

        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
