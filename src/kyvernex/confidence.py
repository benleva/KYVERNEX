from __future__ import annotations

from dataclasses import dataclass
from math import prod

from .graph import CognitiveGraph, RelationType
from .memory import SessionMemory


class ConfidenceError(RuntimeError):
    """Base error for KYVERNEX confidence evaluation."""


class ConfidenceCycleError(ConfidenceError):
    """Raised when confidence dependencies contain a cycle."""


@dataclass(slots=True, frozen=True)
class ConfidenceAssessment:
    session_id: str
    object_id: str
    direct_confidence: float
    propagated_confidence: float
    supporting_object_ids: tuple[str, ...]
    contradicting_object_ids: tuple[str, ...]
    reservations: tuple[str, ...]


class CognitiveConfidenceEngine:
    """Computes conservative confidence from metadata and cognitive relations.

    Direct confidence is read from ``object.metadata['confidence']`` and must be
    between 0 and 1. Missing values use ``default_confidence``. SUPPORTS and
    DEPENDS_ON relations contribute evidence; CONTRADICTS relations reduce the
    result. The algorithm is deterministic and intentionally conservative.
    """

    def __init__(
        self,
        *,
        memory: SessionMemory,
        graph: CognitiveGraph,
        default_confidence: float = 0.5,
        contradiction_weight: float = 1.0,
    ) -> None:
        self.memory = memory
        self.graph = graph
        self.default_confidence = self._validate_score(default_confidence)
        if contradiction_weight < 0:
            raise ValueError("PESO_CONTRADDIZIONE_NON_VALIDO")
        self.contradiction_weight = contradiction_weight

    def assess(self, *, session_id: str, object_id: str) -> ConfidenceAssessment:
        if not session_id.strip():
            raise ValueError("SESSION_ID_MANCANTE")
        return self._assess(session_id=session_id, object_id=object_id, path=())

    def _assess(
        self,
        *,
        session_id: str,
        object_id: str,
        path: tuple[str, ...],
    ) -> ConfidenceAssessment:
        if object_id in path:
            raise ConfidenceCycleError("CICLO_NELLA_PROPAGAZIONE_CONFIDENZA")

        obj = self.memory.get(session_id, object_id)
        if obj is None:
            raise ConfidenceError("OGGETTO_COGNITIVO_NON_TROVATO")

        direct = self._score_from_metadata(obj.metadata)
        incoming = self.graph.incoming(session_id, object_id)
        supporters = tuple(
            relation.source_object_id
            for relation in incoming
            if relation.relation_type in {RelationType.SUPPORTS, RelationType.DEPENDS_ON}
        )
        contradictions = tuple(
            relation.source_object_id
            for relation in incoming
            if relation.relation_type is RelationType.CONTRADICTS
        )

        next_path = (*path, object_id)
        support_scores = tuple(
            self._assess(session_id=session_id, object_id=supporter, path=next_path).propagated_confidence
            for supporter in supporters
        )
        contradiction_scores = tuple(
            self._assess(session_id=session_id, object_id=contradiction, path=next_path).propagated_confidence
            for contradiction in contradictions
        )

        combined_support = 1.0 - prod(1.0 - score for score in (direct, *support_scores))
        contradiction_penalty = prod(
            max(0.0, 1.0 - self.contradiction_weight * score)
            for score in contradiction_scores
        )
        propagated = max(0.0, min(1.0, combined_support * contradiction_penalty))

        reservations: list[str] = []
        if "confidence" not in obj.metadata:
            reservations.append("CONFIDENZA_DIRETTA_ASSENTE")
        if contradictions:
            reservations.append("CONTRADDIZIONI_PRESENTI")
        if not supporters and not contradictions:
            reservations.append("NESSUNA_EVIDENZA_RELAZIONALE")

        return ConfidenceAssessment(
            session_id=session_id,
            object_id=object_id,
            direct_confidence=direct,
            propagated_confidence=propagated,
            supporting_object_ids=supporters,
            contradicting_object_ids=contradictions,
            reservations=tuple(reservations),
        )

    def _score_from_metadata(self, metadata: dict[str, object]) -> float:
        value = metadata.get("confidence", self.default_confidence)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ConfidenceError("CONFIDENZA_NON_NUMERICA")
        return self._validate_score(float(value))

    @staticmethod
    def _validate_score(value: float) -> float:
        if not 0.0 <= value <= 1.0:
            raise ValueError("CONFIDENZA_FUORI_INTERVALLO")
        return value
