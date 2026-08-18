#!/usr/bin/env python3
"""Bounded operating-rhythm policy for perpetual Hermes work."""
from dataclasses import dataclass

MODES = ("exploration", "exploitation", "maintenance", "restructuring")


@dataclass(frozen=True)
class CycleAssessment:
    mode: str
    continue_work: bool
    reason: str


def assess_cycle(
    mode: str, *, quality_delta: float, next_action: bool,
    blocker: bool = False, consecutive_no_gain: int = 0,
) -> CycleAssessment:
    if mode not in MODES:
        raise ValueError(f"unknown cycle mode: {mode}")
    if blocker:
        return CycleAssessment(mode, False, "record blocker and stop")
    if not next_action:
        return CycleAssessment(mode, False, "no concrete next action")
    if consecutive_no_gain >= 2 and quality_delta <= 0:
        return CycleAssessment(mode, False, "re-prioritize after repeated no-gain cycles")
    if quality_delta <= 0:
        return CycleAssessment(mode, True, "continue only with explicit evidence-gathering action")
    return CycleAssessment(mode, True, "measurable quality gain recorded")
