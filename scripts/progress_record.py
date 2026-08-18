#!/usr/bin/env python3
"""Validate substantive progress claims for a Hermes cycle."""
from dataclasses import dataclass

SUBSTANTIVE = (
    "quality_delta", "coverage_delta", "evidence_quality_delta",
    "validation_delta", "uncertainty_delta",
)


@dataclass(frozen=True)
class ProgressAssessment:
    valid: bool
    reason: str


def assess_progress(record: dict) -> ProgressAssessment:
    missing = [field for field in SUBSTANTIVE if field not in record]
    if missing:
        return ProgressAssessment(False, f"missing substantive fields: {', '.join(missing)}")
    try:
        values = [float(record[field]) for field in SUBSTANTIVE]
    except (TypeError, ValueError):
        return ProgressAssessment(False, "substantive fields must be numeric")
    if all(value == 0 for value in values):
        return ProgressAssessment(False, "no substantive improvement recorded")
    if record.get("file_count_delta", 0) != 0 and all(value == 0 for value in values):
        return ProgressAssessment(False, "artifact count is not progress")
    if not record.get("evidence"):
        return ProgressAssessment(False, "substantive delta requires evidence")
    return ProgressAssessment(True, "substantive improvement recorded with evidence")
