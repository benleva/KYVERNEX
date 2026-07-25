from kyvernex import (
    CognitiveDeletionCoordinator,
    CognitiveGraph,
    CognitiveObject,
    DeletionPolicy,
    EchoAdapter,
    JsonAuditTrace,
    KyvernexEngine,
    KyvernexOrchestrator,
    SessionMemory,
)


def test_engine_persists_complete_audit_batch(tmp_path):
    trace = JsonAuditTrace(tmp_path / "audit.json")
    engine = KyvernexEngine(audit_sink=trace)

    result = engine.execute("ciao", source="test", session_id="s")

    assert trace.count(session_id="s") == len(result.audit)
    assert trace.verify() is True


def test_orchestrator_persists_engine_and_adapter_audit(tmp_path):
    trace = JsonAuditTrace(tmp_path / "audit.json")
    engine = KyvernexEngine(audit_sink=trace)
    orchestrator = KyvernexOrchestrator(EchoAdapter(), engine=engine)

    result = orchestrator.execute("ciao", source="test", session_id="s")

    expected = len(result.governance.audit) + len(result.adapter_audit)
    assert trace.count(session_id="s") == expected
    assert trace.verify() is True


def test_deletion_coordinator_persists_deletion_audit(tmp_path):
    trace = JsonAuditTrace(tmp_path / "audit.json")
    memory = SessionMemory()
    graph = CognitiveGraph()
    obj = CognitiveObject(original_content="x", source="test")
    memory.store("s", obj)
    coordinator = CognitiveDeletionCoordinator(memory=memory, graph=graph, audit_sink=trace)

    result = coordinator.delete(session_id="s", object_id=obj.object_id, policy=DeletionPolicy.CASCADE)

    assert trace.count(session_id="s") == len(result.audit)
    assert trace.verify() is True
