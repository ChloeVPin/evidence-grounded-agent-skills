#!/usr/bin/env python3
"""Map freshness outcomes to permitted knowledge lifecycle decisions."""
from dataclasses import dataclass


@dataclass(frozen=True)
class LifecycleDecision:
    allowed: bool
    state: str
    reason: str


def decide_lifecycle(
    *, current_state: str, freshness: str, revalidation_evidence: bool = False,
) -> LifecycleDecision:
    if freshness == "fresh":
        if current_state in {"trusted", "validated", "experimental"}:
            return LifecycleDecision(True, current_state, "fresh artifact may retain state")
        return LifecycleDecision(False, current_state, "deprecated or superseded artifact needs replacement")
    if freshness == "review_due":
        if revalidation_evidence:
            return LifecycleDecision(True, "validated", "revalidation evidence recorded")
        return LifecycleDecision(False, "experimental", "review due; trust suspended pending revalidation")
    if freshness == "deprecated":
        return LifecycleDecision(False, "deprecated", "deprecated artifact cannot be trusted")
    if freshness == "superseded":
        return LifecycleDecision(False, "superseded", "superseded artifact cannot be trusted")
    return LifecycleDecision(False, "experimental", "unknown freshness prevents trust")
