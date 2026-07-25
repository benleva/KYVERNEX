from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Mapping, Protocol, Sequence


class KEXError(RuntimeError):
    """Raised when a governed execution cannot be accepted or completed."""


class ExecutionStatus(StrEnum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


@dataclass(slots=True, frozen=True)
class ExecutionRequest:
    request_id: str
    command: tuple[str, ...]
    working_directory: str | Path
    purpose: str
    timeout_seconds: float = 60.0
    environment: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.request_id.strip() or not self.purpose.strip():
            raise ValueError("DATI_ESECUZIONE_MANCANTI")
        if not self.command or any(not part.strip() for part in self.command):
            raise ValueError("COMANDO_NON_VALIDO")
        if self.timeout_seconds <= 0:
            raise ValueError("TIMEOUT_NON_VALIDO")


@dataclass(slots=True, frozen=True)
class ExecutionResult:
    request_id: str
    status: ExecutionStatus
    return_code: int | None
    stdout: str
    stderr: str
    command: tuple[str, ...]
    working_directory: str

    @property
    def succeeded(self) -> bool:
        return self.status == ExecutionStatus.SUCCEEDED


@dataclass(slots=True, frozen=True)
class ExecutionPolicy:
    allowed_programs: frozenset[str]
    allowed_working_roots: tuple[str | Path, ...]
    allow_environment_override: bool = False
    max_timeout_seconds: float = 900.0

    def __post_init__(self) -> None:
        if not self.allowed_programs:
            raise ValueError("PROGRAMMI_CONSENTITI_MANCANTI")
        if not self.allowed_working_roots:
            raise ValueError("RADICI_DI_LAVORO_MANCANTI")
        if self.max_timeout_seconds <= 0:
            raise ValueError("TIMEOUT_MASSIMO_NON_VALIDO")


class CommandRunner(Protocol):
    def run(self, request: ExecutionRequest) -> ExecutionResult:
        """Execute a previously governed request."""


class SubprocessCommandRunner:
    """Concrete local runner. It never uses a shell and captures all evidence."""

    def run(self, request: ExecutionRequest) -> ExecutionResult:
        cwd = str(Path(request.working_directory).resolve())
        try:
            completed = subprocess.run(
                list(request.command),
                cwd=cwd,
                env=dict(request.environment) or None,
                capture_output=True,
                text=True,
                timeout=request.timeout_seconds,
                check=False,
                shell=False,
            )
        except subprocess.TimeoutExpired as exc:
            return ExecutionResult(
                request_id=request.request_id,
                status=ExecutionStatus.FAILED,
                return_code=None,
                stdout=exc.stdout or "",
                stderr=exc.stderr or "TIMEOUT_ESECUZIONE",
                command=request.command,
                working_directory=cwd,
            )
        except OSError as exc:
            return ExecutionResult(
                request_id=request.request_id,
                status=ExecutionStatus.FAILED,
                return_code=None,
                stdout="",
                stderr=str(exc),
                command=request.command,
                working_directory=cwd,
            )
        return ExecutionResult(
            request_id=request.request_id,
            status=(ExecutionStatus.SUCCEEDED if completed.returncode == 0 else ExecutionStatus.FAILED),
            return_code=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            command=request.command,
            working_directory=cwd,
        )


class KyvernexExecutionEngine:
    """Policy-gated execution boundary used by KGO to act on external systems."""

    def __init__(self, *, policy: ExecutionPolicy, runner: CommandRunner) -> None:
        self.policy = policy
        self.runner = runner
        self.history: list[ExecutionResult] = []

    def validate(self, request: ExecutionRequest) -> None:
        program = Path(request.command[0]).name
        if program not in self.policy.allowed_programs:
            raise KEXError("PROGRAMMA_NON_AUTORIZZATO")
        if request.timeout_seconds > self.policy.max_timeout_seconds:
            raise KEXError("TIMEOUT_SUPERA_POLITICA")
        if request.environment and not self.policy.allow_environment_override:
            raise KEXError("OVERRIDE_AMBIENTE_NON_AUTORIZZATO")
        cwd = Path(request.working_directory).resolve()
        roots = tuple(Path(root).resolve() for root in self.policy.allowed_working_roots)
        if not any(cwd == root or root in cwd.parents for root in roots):
            raise KEXError("DIRECTORY_DI_LAVORO_NON_AUTORIZZATA")

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        self.validate(request)
        result = self.runner.run(request)
        if result.request_id != request.request_id:
            raise KEXError("RISULTATO_NON_CORRELATO")
        self.history.append(result)
        return result

    def execute_sequence(self, requests: Sequence[ExecutionRequest], *, stop_on_failure: bool = True) -> tuple[ExecutionResult, ...]:
        results: list[ExecutionResult] = []
        seen: set[str] = set()
        for request in requests:
            if request.request_id in seen:
                raise KEXError("REQUEST_ID_DUPLICATO")
            seen.add(request.request_id)
            result = self.execute(request)
            results.append(result)
            if stop_on_failure and not result.succeeded:
                break
        return tuple(results)
