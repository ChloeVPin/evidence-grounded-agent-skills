#!/usr/bin/env python3
"""Policy for artifact freshness and lifecycle states."""
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class FreshnessDecision:
    outcome: str
    reason: str


def assess_artifact(
    *, state: str, last_validated: str | None, now: datetime,
    review_window_days: int,
) -> FreshnessDecision:
    if state == "deprecated":
        return FreshnessDecision("deprecated", "artifact is explicitly deprecated")
    if state == "superseded":
        return FreshnessDecision("superseded", "replacement artifact is authoritative")
    if state not in {"validated", "trusted", "experimental"}:
        return FreshnessDecision("unknown", "lifecycle state is unknown")
    if not last_validated:
        return FreshnessDecision("unknown", "validation date is missing")
    try:
        validated = datetime.fromisoformat(last_validated.replace("Z", "+00:00"))
    except ValueError:
        return FreshnessDecision("unknown", "validation date is invalid")
    if validated < now - timedelta(days=review_window_days):
        return FreshnessDecision("review_due", "review window has elapsed")
    return FreshnessDecision("fresh", "artifact is within review window")
