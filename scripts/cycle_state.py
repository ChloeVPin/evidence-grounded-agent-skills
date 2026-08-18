#!/usr/bin/env python3
"""Validate and advance durable Hermes cycle state."""
from dataclasses import dataclass

from scripts.cycle_policy import MODES
from scripts.progress_record import assess_progress

STATUSES = ("in_progress", "completed", "stopped")
TERMINAL = {"completed", "stopped"}


@dataclass(frozen=True)
class StateAssessment:
    valid: bool
    reason: str


def validate_state(state: dict) -> StateAssessment:
    required = ("schema_version", "cycle_id", "mode", "status", "progress", "decision", "next_action")
    missing = [field for field in required if field not in state]
    if missing:
        return StateAssessment(False, f"missing fields: {', '.join(missing)}")
    if state["schema_version"] != 1:
        return StateAssessment(False, "unsupported schema version")
    if state["mode"] not in MODES:
        return StateAssessment(False, "unknown mode")
    if state["status"] not in STATUSES:
        return StateAssessment(False, "unknown status")
    if not isinstance(state["progress"], dict) or not state["decision"]:
        return StateAssessment(False, "progress and decision are required")
    if state["status"] == "in_progress" and not state["next_action"]:
        return StateAssessment(False, "active cycle requires next action")
    return StateAssessment(True, "valid cycle state")


def transition(state: dict, status: str, decision: str, next_action: str = "") -> dict:
    assessment = validate_state(state)
    if not assessment.valid:
        raise ValueError(assessment.reason)
    if state["status"] in TERMINAL:
        raise ValueError("terminal cycle cannot transition")
    if status not in TERMINAL:
        raise ValueError("transition status must be completed or stopped")
    if status == "completed":
        progress = assess_progress(state["progress"])
        if not progress.valid:
            raise ValueError(f"cannot complete cycle: {progress.reason}")
    updated = dict(state)
    updated.update(status=status, decision=decision, next_action=next_action)
    final = validate_state(updated)
    if not final.valid:
        raise ValueError(final.reason)
    return updated
