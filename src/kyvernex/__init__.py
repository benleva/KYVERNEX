"""KYVERNEX Reference Prototype 0.1."""

from .adapters import (
    AIAdapter,
    AdapterExecutionError,
    AdapterRequest,
    AdapterResponse,
    EchoAdapter,
    FailingAdapter,
)
from .core import AET, ContinuousValidator, KyvernexEngine
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
from .response_governance import GovernedResponse, ResponseGovernor
from .rules import Rule, RuleEngine, RuleResult, RuleSeverity, default_rules
from .serialization import to_primitive

__all__ = [
    "AET",
    "AIAdapter",
    "AdapterExecutionError",
    "AdapterRequest",
    "AdapterResponse",
    "AuditEvent",
    "CognitiveCategory",
    "CognitiveObject",
    "CognitiveState",
    "ContinuousValidator",
    "EchoAdapter",
    "ExecutionResult",
    "FailingAdapter",
    "GovernedExecutionResult",
    "GovernedResponse",
    "JsonSessionMemory",
    "KyvernexEngine",
    "KyvernexOrchestrator",
    "MemoryConflictError",
    "PersistenceFormatError",
    "ResponseGovernor",
    "Rule",
    "RuleEngine",
    "RuleResult",
    "RuleSeverity",
    "SessionMemory",
    "ValidationOutcome",
    "ValidationRecord",
    "default_rules",
    "to_primitive",
]

__version__ = "0.1.0.dev0"
