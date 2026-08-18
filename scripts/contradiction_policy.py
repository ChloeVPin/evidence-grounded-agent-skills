#!/usr/bin/env python3
"""Classify competing claims without forcing unsupported synthesis."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Claim:
    name: str
    context: str
    evidence_strength: int


@dataclass(frozen=True)
class ContradictionResult:
    outcome: str
    winner: str | None
    reason: str


def resolve_claims(
    first: Claim, second: Claim, *, discriminating_evidence: bool,
) -> ContradictionResult:
    if first.context != second.context:
        return ContradictionResult("contextual", None, "claims apply in different contexts")
    if not discriminating_evidence:
        return ContradictionResult("unresolved", None, "no discriminating evidence")
    if first.evidence_strength == second.evidence_strength:
        return ContradictionResult("unresolved", None, "evidence does not distinguish claims")
    winner = first if first.evidence_strength > second.evidence_strength else second
    loser = second if winner is first else first
    return ContradictionResult(
        "supported_refuted", winner.name,
        f"{winner.name} supported over {loser.name} by stronger evidence",
    )
