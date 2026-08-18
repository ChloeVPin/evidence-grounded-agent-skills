# Cycle 0149 — Bind the summary digest into versioned state

Date: 2026-08-18
Status: completed

## Question

Bind the summary digest into versioned state

## Decision

Versioned state now records the 0146 summary reference and digest; the executable
state validator compares them against the live summary and rejects stale state.

## Evidence and provenance

Evidence: updated 0113 state, validator binding, and summary-digest mutation test.

## Disconfirming evidence sought

The summary digest binds the exact capture/state/policy reference summary; it does
not replace individual evidence-content validation.

## Next action

Expose summary-state freshness failures as distinct diagnostics.
