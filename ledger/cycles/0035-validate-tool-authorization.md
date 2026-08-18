# Cycle 0035 — Validate Tool Authorization

Date: 2026-08-18
Status: validated with deterministic authorization fixture

## Question

Can tool authorization policy distinguish least-privilege calls from over-broad, undeclared, or high-impact requests?

## Decision

The fixture allows scoped reads, requires approval for writes, rejects out-of-scope resources and undeclared parameters, and forbids wildcard authority.

## Evidence and provenance

Implemented in `scripts/tool_policy.py` with six policy tests in `tests/test_tool_policy.py`.

## Disconfirming evidence sought

Scope, parameter, approval, action, and wildcard bypass attempts are rejected.

## Next action

Validation passed locally. Limitation: this evaluator does not enforce permissions in a real tool server or authenticate approvers. Next cycle: bind authorization decisions to durable audit records and test high-impact actions.
