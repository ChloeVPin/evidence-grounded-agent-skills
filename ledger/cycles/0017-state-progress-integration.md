# Cycle 0017 — State and Progress Integration

Date: 2026-08-18
Status: validated with completion gate

## Question

Can Hermes prevent a cycle from completing when its progress record is activity-only or unsupported by evidence?

## Decision

`completed` transitions require `assess_progress` to accept a substantive numeric delta with evidence. Activity-only records cannot complete; they may be stopped or reprioritized.

## Evidence and provenance

`cycle_state.transition` now calls `assess_progress` for completion, with integrated tests in `tests/test_cycle_state.py`.

## Disconfirming evidence sought

File-count-only progress is rejected for completion.

## Next action

Validation passed locally. Limitation: truthful deltas still depend on evidence quality and review; the gate prevents unsupported shape, not dishonest claims. Next cycle: record a real completed cycle state for the live review work and begin a new research mode.
