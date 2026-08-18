# Cycle 0140 — Persist an independent graph-policy digest

Date: 2026-08-18
Status: completed

## Question

Persist an independent graph-policy digest

## Decision

Added a canonical SHA-256 over the independent expected graph node set and
required it in graph validation. Policy-digest tampering is now rejected.

## Evidence and provenance

Evidence: the 0137 graph’s `policy_sha256`, the validator, and digest-mutation
coverage.

## Disconfirming evidence sought

The digest binds node-policy membership; edge-shape validation remains a
separate graph invariant.

## Next action

Bind the graph-policy digest into versioned state.
