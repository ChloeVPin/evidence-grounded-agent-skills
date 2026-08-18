# Cycle 0016 — Cycle State

Date: 2026-08-18
Status: validated with durable transitions

## Question

What durable state should connect cycle mode, progress assessment, stopping decision, and next action across runs?

## Decision

Schema version 1 requires cycle ID, operating mode, lifecycle status, progress record, decision, and next action. Active cycles require a next action; terminal cycles cannot transition.

## Evidence and provenance

Implemented in `scripts/cycle_state.py` with four transition and validation tests in `tests/test_cycle_state.py`.

## Disconfirming evidence sought

Missing next actions and transitions from terminal states are rejected.

## Next action

Validation passed locally. Limitation: state validation checks the progress record shape only; it does not independently establish the truth of the recorded delta. Next cycle: connect cycle state to the progress assessor and enforce substantive progress before completion.
