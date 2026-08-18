# Cycle 0167 — Expose diagnostic references directly in the freshness inventory

Date: 2026-08-18
Status: completed

## Question

Expose diagnostic references directly in the freshness inventory

## Decision

The freshness inventory now explicitly records diagnostic snapshot references
alongside captures, failures, state, summary, and graph artifacts.

## Evidence and provenance

Evidence: updated inventory and state digest, validator enforcement, and
executable inventory regression coverage.

## Disconfirming evidence sought

The expanded inventory remains complete; 183 tests, compilation, and the full
four-check audit pass.

## Next action

Bind diagnostic references into the versioned self-validation state schema.
