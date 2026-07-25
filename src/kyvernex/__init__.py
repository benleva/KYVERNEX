"""KYVERNEX Reference Prototype 0.1."""

from .adapters import (
    AIAdapter, AdapterExecutionError, AdapterRequest, AdapterResponse, EchoAdapter, FailingAdapter,
)
from .audit_sink import AuditSink, persist_audit
from .audit_trace import AuditTraceError, AuditTraceRecord, JsonAuditTrace
from .autonomous_development import (
    AutonomousCyclePlan,
    AutonomousDevelopmentEngine,
    AutonomousDevelopmentError,
    DevelopmentAction,
    DevelopmentPolicy,
    DevelopmentStep,
    build_m3_backlog,
)
from .change_manifest import (
    ChangeKind,
    ChangeManifest,
    ChangeManifestError,
    PlannedChange,
    SpecificationChangePlanner,
)
from .confidence import CognitiveConfidenceEngine, ConfidenceAssessment, ConfidenceCycleError, ConfidenceError
from .core import AET, ContinuousValidator, KyvernexEngine
from .decision_gate import CognitiveDecisionGate, DecisionDisposition, DecisionGateError, DecisionPolicy, GovernedDecision
from .deletion import CognitiveDeletionCoordinator, DeletionPolicy, DeletionRestrictedError, DeletionResult, DeletionTransactionError
from .durable_deletion import DeletionJournalError, DeletionJournalState, DurableDeletionCoordinator, RecoveryResult
from .execution_engine import (
    CommandRunner, ExecutionPolicy, ExecutionRequest, ExecutionResult as KEXExecutionResult,
    ExecutionStatus, KEXError, KyvernexExecutionEngine, SubprocessCommandRunner,
)
from .explainability import AuditTraceReader, CognitiveDecisionDossier, CognitiveDecisionExplainer, ExplainabilityError
from .graph import CognitiveGraph, CognitiveRelation, RelationConflictError, RelationType
from .graph_persistence import GraphPersistenceFormatError, JsonCognitiveGraph, ReferentialIntegrityError
from .kgo_v3 import KGOState, KGOV3Loop, LoopDecision, LoopResult, load_state, write_result
from .kpm_prioritization import KPMFeatureAssessment, execution_clock_assessment
from .memory import MemoryConflictError, SessionMemory
from .models import AuditEvent, CognitiveCategory, CognitiveObject, CognitiveState, ExecutionResult, ValidationOutcome, ValidationRecord
from .orchestrator import GovernedExecutionResult, KyvernexOrchestrator
from .persistence import JsonSessionMemory, PersistenceFormatError
from .process_lock import InterProcessFileLock, ProcessLockError
from .process_safe_journal import ProcessSafeMultiTransactionDeletionCoordinator
from .program_manager import (
    DefinitionOfDone, GovernanceCheckpoint, GovernanceMode, GovernanceState, KGOError, KPMError,
    KPMReport, KyvernexGovernanceOrchestrator, KyvernexProgramManager, Milestone, Priority,
    WorkItem, WorkStatus,
)
from .response_governance import GovernedResponse, ResponseGovernor
from .rules import Rule, RuleEngine, RuleResult, RuleSeverity, default_rules
from .self_verification import (
    ContinuousSelfVerificationController,
    SelfVerificationResult,
    VerificationEvidence,
    VerificationStatus,
    write_verification_result,
)
from .serialization import to_primitive
from .transaction_journal import MultiTransactionDeletionCoordinator, RecoveryBatch
from .unit_of_work import KyvernexUnitOfWork, UnitOfWorkCommitError, UnitOfWorkError, UnitOfWorkResult, UnitOfWorkState, UnitOfWorkStateError
from .versioning import CognitiveVersionManager, VersionChangeType, VersionConflictError, VersionTransition, VersioningError

__all__ = [
    "AET", "AIAdapter", "AdapterExecutionError", "AdapterRequest", "AdapterResponse",
    "AuditEvent", "AuditSink", "AuditTraceError", "AuditTraceReader", "AuditTraceRecord",
    "AutonomousCyclePlan", "AutonomousDevelopmentEngine", "AutonomousDevelopmentError",
    "ChangeKind", "ChangeManifest", "ChangeManifestError",
    "CognitiveCategory", "CognitiveConfidenceEngine", "CognitiveDecisionDossier",
    "CognitiveDecisionExplainer", "CognitiveDecisionGate", "CognitiveDeletionCoordinator",
    "CognitiveGraph", "CognitiveObject", "CognitiveRelation", "CognitiveState",
    "CognitiveVersionManager", "CommandRunner", "ConfidenceAssessment", "ConfidenceCycleError",
    "ConfidenceError", "ContinuousSelfVerificationController", "ContinuousValidator",
    "DecisionDisposition", "DecisionGateError", "DecisionPolicy", "DefinitionOfDone",
    "DeletionJournalError", "DeletionJournalState", "DeletionPolicy", "DeletionRestrictedError",
    "DeletionResult", "DeletionTransactionError", "DevelopmentAction", "DevelopmentPolicy",
    "DevelopmentStep", "DurableDeletionCoordinator", "EchoAdapter", "ExecutionPolicy",
    "ExecutionRequest", "ExecutionResult", "ExecutionStatus", "ExplainabilityError",
    "FailingAdapter", "GovernanceCheckpoint", "GovernanceMode", "GovernanceState",
    "GovernedDecision", "GovernedExecutionResult", "GovernedResponse", "GraphPersistenceFormatError",
    "InterProcessFileLock", "JsonAuditTrace", "JsonCognitiveGraph", "JsonSessionMemory",
    "KEXError", "KEXExecutionResult", "KGOError", "KGOState", "KGOV3Loop", "KPMError",
    "KPMFeatureAssessment", "KPMReport", "KyvernexEngine", "KyvernexExecutionEngine",
    "KyvernexGovernanceOrchestrator", "KyvernexOrchestrator", "KyvernexProgramManager",
    "KyvernexUnitOfWork", "LoopDecision", "LoopResult", "MemoryConflictError", "Milestone",
    "MultiTransactionDeletionCoordinator", "PersistenceFormatError", "PlannedChange", "Priority",
    "ProcessLockError", "ProcessSafeMultiTransactionDeletionCoordinator", "RecoveryBatch",
    "RecoveryResult", "ReferentialIntegrityError", "RelationConflictError", "RelationType",
    "ResponseGovernor", "Rule", "RuleEngine", "RuleResult", "RuleSeverity", "SelfVerificationResult",
    "SessionMemory", "SpecificationChangePlanner", "SubprocessCommandRunner", "UnitOfWorkCommitError",
    "UnitOfWorkError", "UnitOfWorkResult", "UnitOfWorkState", "UnitOfWorkStateError",
    "ValidationOutcome", "ValidationRecord", "VerificationEvidence", "VerificationStatus",
    "VersionChangeType", "VersionConflictError", "VersionTransition", "VersioningError",
    "WorkItem", "WorkStatus", "build_m3_backlog", "default_rules", "execution_clock_assessment",
    "load_state", "persist_audit", "to_primitive", "write_result", "write_verification_result",
]

__version__ = "0.1.0.dev0"
