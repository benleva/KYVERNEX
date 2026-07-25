"""KYVERNEX Reference Prototype 0.1."""

from .adapters import (
    AIAdapter,
    AdapterExecutionError,
    AdapterRequest,
    AdapterResponse,
    EchoAdapter,
    FailingAdapter,
)
from .audit_sink import AuditSink, persist_audit
from .audit_trace import AuditTraceError, AuditTraceRecord, JsonAuditTrace
from .core import AET, ContinuousValidator, KyvernexEngine
from .deletion import (
    CognitiveDeletionCoordinator,
    DeletionPolicy,
    DeletionRestrictedError,
    DeletionResult,
    DeletionTransactionError,
)
from .durable_deletion import (
    DeletionJournalError,
    DeletionJournalState,
    DurableDeletionCoordinator,
    RecoveryResult,
)
from .graph import CognitiveGraph, CognitiveRelation, RelationConflictError, RelationType
from .graph_persistence import GraphPersistenceFormatError, JsonCognitiveGraph, ReferentialIntegrityError
from .memory import MemoryConflictError, SessionMemory
from .models import (
    AuditEvent,
    CognitiveCategory,
    CognitiveObject,
    CognitiveState,
    ExecutionResult,
    ValidationOutcome,
    ValidationRecord,
)
from .orchestrator import GovernedExecutionResult, KyvernexOrchestrator
from .persistence import JsonSessionMemory, PersistenceFormatError
from .process_lock import InterProcessFileLock, ProcessLockError
from .process_safe_journal import ProcessSafeMultiTransactionDeletionCoordinator
from .response_governance import GovernedResponse, ResponseGovernor
from .rules import Rule, RuleEngine, RuleResult, RuleSeverity, default_rules
from .serialization import to_primitive
from .transaction_journal import MultiTransactionDeletionCoordinator, RecoveryBatch

__all__ = [
    "AET", "AIAdapter", "AdapterExecutionError", "AdapterRequest", "AdapterResponse",
    "AuditEvent", "AuditSink", "AuditTraceError", "AuditTraceRecord",
    "CognitiveCategory", "CognitiveDeletionCoordinator", "CognitiveGraph", "CognitiveObject",
    "CognitiveRelation", "CognitiveState", "ContinuousValidator", "DeletionJournalError",
    "DeletionJournalState", "DeletionPolicy", "DeletionRestrictedError", "DeletionResult",
    "DeletionTransactionError", "DurableDeletionCoordinator", "EchoAdapter", "ExecutionResult",
    "FailingAdapter", "GovernedExecutionResult", "GovernedResponse", "GraphPersistenceFormatError",
    "InterProcessFileLock", "JsonAuditTrace", "JsonCognitiveGraph", "JsonSessionMemory",
    "KyvernexEngine", "KyvernexOrchestrator", "MemoryConflictError",
    "MultiTransactionDeletionCoordinator", "PersistenceFormatError", "ProcessLockError",
    "ProcessSafeMultiTransactionDeletionCoordinator", "RecoveryBatch", "RecoveryResult",
    "ReferentialIntegrityError", "RelationConflictError", "RelationType", "ResponseGovernor",
    "Rule", "RuleEngine", "RuleResult", "RuleSeverity", "SessionMemory", "ValidationOutcome",
    "ValidationRecord", "default_rules", "persist_audit", "to_primitive",
]

__version__ = "0.1.0.dev0"
