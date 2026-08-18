# Cycle 0191 — Bind the expanded state case into the next provenance summary

Date: 2026-08-18
Status: completed

## Question

Bind the expanded state case into the next provenance summary

## Decision

The aggregate summary now explicitly binds state-failure artifacts through a
`state_failure_refs` set.

## Evidence and provenance

Evidence: updated 0146 summary, synchronized summary/state capture digests, and
executable summary validation.

## Disconfirming evidence sought

The expanded summary remains complete; 183 tests, compilation, and the full
four-check audit pass.

## Next action

Expose state-failure provenance directly in the freshness inventory.
