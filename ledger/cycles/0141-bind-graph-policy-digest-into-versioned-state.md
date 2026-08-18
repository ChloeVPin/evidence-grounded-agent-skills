# Cycle 0141 — Bind graph-policy digest into versioned state

Date: 2026-08-18
Status: completed

## Question

Bind graph-policy digest into versioned state

## Decision

Versioned state now records the graph reference and independent policy digest;
the state validator compares both against the live graph and rejects stale
policy provenance.

## Evidence and provenance

Evidence: the updated 0113 state artifact, validator binding, and stale graph
policy-digest test.

## Disconfirming evidence sought

The graph policy digest is checked in addition to graph structure; both layers
remain necessary to detect different classes of drift.

## Next action

Expose graph-state freshness failures as distinct diagnostics.
