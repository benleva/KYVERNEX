from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .audit_sink import AuditSink, persist_audit
from .explainability import CognitiveDecisionDossier, CognitiveDecisionExplainer
from .models import AuditEvent


class DecisionGateError(RuntimeError):
    """Raised when a governed decision cannot be evaluated."""


class DecisionDisposition(StrEnum):
    APPROVED = "APPROVATA"
    APPROVED_WITH_RESERVATION = "APPROVATA_CON_RISERVA"
    MANUAL_REVIEW = "REVISIONE_UMANA_RICHIESTA"
    BLOCKED = "BLOCCATA"


@dataclass(slots=True, frozen=True)
class DecisionPolicy:
    approval_threshold: float = 0.80
    reservation_threshold: float = 0.60
    require_verified_audit: bool = False
    block_on_contradictions: bool = False
    max_reservations_for_approval: int = 0

    def __post_init__(self) -> None:
        if not 0.0 <= self.reservation_threshold <= self.approval_threshold <= 1.0:
            raise ValueError("SOGLIE_DECISIONE_NON_VALIDE")
        if self.max_reservations_for_approval < 0:
            raise ValueError("LIMITE_RISERVE_NON_VALIDO")


@dataclass(slots=True, frozen=True)
class GovernedDecision:
    session_id: str
    object_id: str
    disposition: DecisionDisposition
    confidence: float
    reasons: tuple[str, ...]
    reservations: tuple[str, ...]
    dossier: CognitiveDecisionDossier


class CognitiveDecisionGate:
    """Applies deterministic governance policy to a cognitive decision dossier."""

    def __init__(
        self,
        *,
        explainer: CognitiveDecisionExplainer,
        policy: DecisionPolicy | None = None,
        audit_sink: AuditSink | None = None,
    ) -> None:
        self.explainer = explainer
        self.policy = policy or DecisionPolicy()
        self.audit_sink = audit_sink

    def evaluate(self, *, session_id: str, object_id: str) -> GovernedDecision:
        dossier = self.explainer.explain(session_id=session_id, object_id=object_id)
        confidence = dossier.confidence.propagated_confidence
        reasons: list[str] = []
        reservations = list(dossier.reservations)
        audit_evidence_verified = dossier.audit_integrity_verified and bool(dossier.audit_records)

        if self.policy.require_verified_audit and not audit_evidence_verified:
            disposition = DecisionDisposition.BLOCKED
            reasons.append("AUDIT_NON_VERIFICATO")
        elif self.policy.block_on_contradictions and dossier.confidence.contradicting_object_ids:
            disposition = DecisionDisposition.BLOCKED
            reasons.append("CONTRADDIZIONI_BLOCCANTI")
        elif confidence >= self.policy.approval_threshold:
            if len(reservations) <= self.policy.max_reservations_for_approval:
                disposition = DecisionDisposition.APPROVED
                reasons.append("SOGLIA_APPROVAZIONE_RAGGIUNTA")
            else:
                disposition = DecisionDisposition.APPROVED_WITH_RESERVATION
                reasons.append("SOGLIA_RAGGIUNTA_CON_RISERVE")
        elif confidence >= self.policy.reservation_threshold:
            disposition = DecisionDisposition.APPROVED_WITH_RESERVATION
            reasons.append("SOGLIA_RISERVA_RAGGIUNTA")
        else:
            disposition = DecisionDisposition.MANUAL_REVIEW
            reasons.append("CONFIDENZA_INSUFFICIENTE")

        if dossier.confidence.contradicting_object_ids:
            reasons.append("CONTRADDIZIONI_PRESENTI")
        if not audit_evidence_verified:
            reservations.append("AUDIT_NON_VERIFICATO")

        decision = GovernedDecision(
            session_id=session_id,
            object_id=object_id,
            disposition=disposition,
            confidence=confidence,
            reasons=tuple(dict.fromkeys(reasons)),
            reservations=tuple(dict.fromkeys(reservations)),
            dossier=dossier,
        )
        persist_audit(
            self.audit_sink,
            (
                AuditEvent.create(
                    session_id=session_id,
                    component="DECISION_GATE",
                    event_type="DECISIONE_GOVERNATA",
                    object_id=object_id,
                    details={
                        "disposition": disposition.value,
                        "confidence": confidence,
                        "reasons": list(decision.reasons),
                        "reservations": list(decision.reservations),
                    },
                ),
            ),
        )
        return decision
