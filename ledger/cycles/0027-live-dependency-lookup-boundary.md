# Cycle 0027 — Live Dependency Lookup Boundary

Date: 2026-08-18
Status: validated with explicit lookup boundary

## Question

What is the smallest trustworthy boundary for incorporating live registry and vulnerability-advisory lookups into Hermes evidence?

## Decision

The adapter normalizes clean resolution to `verified`, advisory findings to `vulnerable`, and unavailable, unresolved, or malformed responses to `unknown`.

## Evidence and provenance

Implemented in `scripts/lookup_adapter.py` with four tests covering clean, unavailable, advisory, and malformed responses.

## Disconfirming evidence sought

Network-unavailable and malformed responses remain `unknown`; raw output receives a SHA-256 digest for audit binding.

## Next action

Validation passed locally. Limitation: this adapter does not perform network requests; connectors must supply raw responses and authoritative source identifiers. Next cycle: feed adapter records into generated dependency evidence and complete review.
