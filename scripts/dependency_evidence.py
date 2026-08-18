#!/usr/bin/env python3
"""Validate provenance and lookup evidence for dependency decisions."""
from datetime import datetime

STATUSES = {"verified", "vulnerable", "unknown"}


def validate_dependency_evidence(evidence: dict, packages: dict) -> tuple[str, ...]:
    errors: list[str] = []
    for name in packages:
        item = evidence.get(name)
        if not isinstance(item, dict):
            errors.append(f"missing:{name}")
            continue
        if not item.get("source"):
            errors.append(f"source:{name}")
        if item.get("status") not in STATUSES:
            errors.append(f"status:{name}")
        try:
            datetime.fromisoformat(item.get("looked_up_at", "").replace("Z", "+00:00"))
        except (AttributeError, ValueError):
            errors.append(f"looked_up_at:{name}")
    return tuple(errors)
