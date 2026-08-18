# Cycle 0023 — Unknown Dependency Policy

Date: 2026-08-18
Status: validated with explicit freshness policy

## Question

When dependency evidence is explicitly unknown or stale, should Hermes block, escalate, or permit the change under a documented exception?

## Decision

Fresh verified evidence passes; vulnerable or malformed evidence blocks; unknown or stale evidence escalates and cannot silently pass.

## Evidence and provenance

Implemented in `scripts/dependency_policy.py` with four boundary tests in `tests/test_dependency_policy.py`.

## Disconfirming evidence sought

Unknown, stale, vulnerable, and malformed statuses have distinct tested outcomes.

## Next action

Validation passed locally. Limitation: the default 90-day freshness window is a policy choice, not a universal truth; it must be adjusted by ecosystem and risk. Next cycle: integrate policy outcomes with complete review and explicit escalation records.
