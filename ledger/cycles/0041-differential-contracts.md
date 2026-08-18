# Cycle 0041 — Differential Contracts

Date: 2026-08-18
Status: validated with structured contract fixture

## Question

How should differential review represent contract dimensions beyond return values, especially errors and side effects?

## Decision

Differential comparison now detects divergence in structured return value, error, and side-effect trace, even when the primary return value matches.

## Evidence and provenance

Structured contract tests are in `tests/test_differential_review.py`.

## Disconfirming evidence sought

Changed errors and added writes are both reported as divergence.

## Next action

Validation passed locally. Limitation: side-effect traces are fixture-level observations, not an enforcement mechanism for external systems. Next cycle: archive the differential foundation and open the next exploration mode.
