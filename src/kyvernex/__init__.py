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
from .confidence import (
    CognitiveConfidenceEngine,
    ConfidenceAssessment,
    ConfidenceCycleError,
    ConfidenceError,
)
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
from .explainability import (
    AuditTraceReader,
    CognitiveDecisionDossier,
    CognitiveDecisionExplainer,
    ExplainabilityError,
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
from .unit_of_work import (
    KyvernexUnitOfWork,
    UnitOfWorkCommitError,
    UnitOfWorkError,
    UnitOfWorkResult,
    UnitOfWorkState,
    UnitOfWorkStateError,
)
from .versioning import (
    CognitiveVersionManager,
    VersionChangeType,
    VersionConflictError,
    VersionTransition,
    VersioningError,
)

__all__ = [
    "AET", "AIAdapter", "AdapterExecutionError", "AdapterRequest", "AdapterResponse",
    "AuditEvent", "AuditSink", "AuditTraceError", "AuditTraceReader", "AuditTraceRecord",
    "CognitiveCategory", "CognitiveConfidenceEngine", "CognitiveDecisionDossier",
    "CognitiveDecisionExplainer", "CognitiveDeletionCoordinator", "CognitiveGraph",
    "CognitiveObject", "CognitiveRelation", "CognitiveState", "CognitiveVersionManager",
    "ConfidenceAssessment", "ConfidenceCycleError", "ConfidenceError", "ContinuousValidator",
    "DeletionJournalError", "DeletionJournalState", "DeletionPolicy", "DeletionRestrictedError",
    "DeletionResult", "DeletionTransactionError", "DurableDeletionCoordinator", "EchoAdapter",
    "ExecutionResult", "ExplainabilityError", "FailingAdapter", "GovernedExecutionResult",
    "GovernedResponse", "GraphPersistenceFormatError", "InterProcessFileLock", "JsonAuditTrace",
    "JsonCognitiveGraph", "JsonSessionMemory", "KyvernexEngine", "KyvernexOrchestrator",
    "KyvernexUnitOfWork", "MemoryConflictError", "MultiTransactionDeletionCoordinator",
    "PersistenceFormatError", "ProcessLockError", "ProcessSafeMultiTransactionDeletionCoordinator",
    "RecoveryBatch", "RecoveryResult", "ReferentialIntegrityError", "RelationConflictError",
    "RelationType", "ResponseGovernor", "Rule", "RuleEngine", "RuleResult", "RuleSeverity",
    "SessionMemory", "UnitOfWorkCommitError", "UnitOfWorkError", "UnitOfWorkResult",
    "UnitOfWorkState", "UnitOfWorkStateError", "ValidationOutcome", "ValidationRecord",
    "VersionChangeType", "VersionConflictError", "VersionTransition", "VersioningError",
    "default_rules", "persist_audit", "to_primitive",
]

__version__ = "0.1.0.dev0"
