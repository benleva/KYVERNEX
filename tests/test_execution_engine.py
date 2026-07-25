from pathlib import Path

import pytest

from kyvernex.execution_engine import (
    ExecutionPolicy,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
    KEXError,
    KyvernexExecutionEngine,
)


class FakeRunner:
    def __init__(self, *, return_code: int = 0) -> None:
        self.return_code = return_code
        self.calls: list[ExecutionRequest] = []

    def run(self, request: ExecutionRequest) -> ExecutionResult:
        self.calls.append(request)
        return ExecutionResult(
            request_id=request.request_id,
            status=ExecutionStatus.SUCCEEDED if self.return_code == 0 else ExecutionStatus.FAILED,
            return_code=self.return_code,
            stdout="ok" if self.return_code == 0 else "",
            stderr="" if self.return_code == 0 else "failed",
            command=request.command,
            working_directory=str(Path(request.working_directory).resolve()),
        )


def make_engine(tmp_path: Path, runner: FakeRunner | None = None) -> KyvernexExecutionEngine:
    return KyvernexExecutionEngine(
        policy=ExecutionPolicy(
            allowed_programs=frozenset({"python", "git"}),
            allowed_working_roots=(tmp_path,),
            max_timeout_seconds=60,
        ),
        runner=runner or FakeRunner(),
    )


def test_executes_authorized_request_and_records_evidence(tmp_path: Path) -> None:
    runner = FakeRunner()
    engine = make_engine(tmp_path, runner)
    request = ExecutionRequest(
        request_id="KEX-001",
        command=("python", "-m", "pytest", "-q"),
        working_directory=tmp_path,
        purpose="Run the verified test suite",
        timeout_seconds=30,
    )

    result = engine.execute(request)

    assert result.succeeded
    assert runner.calls == [request]
    assert engine.history == [result]


def test_blocks_program_outside_allowlist(tmp_path: Path) -> None:
    engine = make_engine(tmp_path)
    request = ExecutionRequest(
        request_id="KEX-002",
        command=("sh", "-c", "echo unsafe"),
        working_directory=tmp_path,
        purpose="Attempt unauthorized shell execution",
    )

    with pytest.raises(KEXError, match="PROGRAMMA_NON_AUTORIZZATO"):
        engine.execute(request)


def test_blocks_working_directory_outside_governed_root(tmp_path: Path) -> None:
    engine = make_engine(tmp_path)
    request = ExecutionRequest(
        request_id="KEX-003",
        command=("git", "status"),
        working_directory=tmp_path.parent,
        purpose="Read repository status",
    )

    with pytest.raises(KEXError, match="DIRECTORY_DI_LAVORO_NON_AUTORIZZATA"):
        engine.execute(request)


def test_sequence_stops_after_failure(tmp_path: Path) -> None:
    runner = FakeRunner(return_code=1)
    engine = make_engine(tmp_path, runner)
    requests = (
        ExecutionRequest("KEX-004", ("python", "-m", "pytest"), tmp_path, "Run tests"),
        ExecutionRequest("KEX-005", ("git", "status"), tmp_path, "Inspect status"),
    )

    results = engine.execute_sequence(requests)

    assert len(results) == 1
    assert results[0].status == ExecutionStatus.FAILED
    assert len(runner.calls) == 1
