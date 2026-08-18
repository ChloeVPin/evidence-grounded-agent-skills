# Cycle 0014 — Operating Rhythm

Date: 2026-08-18
Status: validated with bounded operating policy

## Question

How should Hermes alternate exploration, validation, maintenance, and restructuring without confusing activity with progress?

## Decision

Alternate modes are `exploration`, `exploitation`, `maintenance`, and `restructuring`. Continue only with a concrete next action; stop on a blocker; reprioritize after two consecutive no-gain cycles.

## Evidence and provenance

Implemented in `scripts/cycle_policy.py` with four policy tests in `tests/test_cycle_policy.py`.

## Disconfirming evidence sought

Repeated no-gain cycles stop for reprioritization, while a single no-gain cycle may continue only when it has an explicit evidence-gathering action.

## Next action

Validation passed locally. Limitation: policy decisions still require a cycle record to supply honest quality deltas; the policy cannot detect fabricated metrics. Next cycle: define the progress ledger fields and a durable cycle transition record.
