#!/usr/bin/env python3
"""Policy for fresh, stale, unknown, and vulnerable dependency evidence."""
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class DependencyDecision:
    outcome: str
    reason: str


def assess_dependency_evidence(
    item: dict, *, now: datetime, max_age_days: int = 90,
) -> DependencyDecision:
    status = item.get("status")
    if status == "vulnerable":
        return DependencyDecision("block", "known vulnerability requires remediation")
    if status == "unknown":
        return DependencyDecision("escalate", "unknown status requires explicit review")
    if status != "verified":
        return DependencyDecision("block", "missing or invalid status")
    try:
        looked_up = datetime.fromisoformat(item["looked_up_at"].replace("Z", "+00:00"))
    except (KeyError, AttributeError, ValueError):
        return DependencyDecision("block", "invalid lookup timestamp")
    if looked_up < now - timedelta(days=max_age_days):
        return DependencyDecision("escalate", "evidence is stale")
    return DependencyDecision("pass", "verified evidence is fresh")
