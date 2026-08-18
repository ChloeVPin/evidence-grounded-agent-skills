# Cycle 0131 — Add a validator for diagnostic snapshots and bind it to audit evidence

Date: 2026-08-18
Status: completed

## Question

Add a validator for diagnostic snapshots and bind it to audit evidence

## Decision

Added `validate_dependency_diagnostic_snapshot` with exact case/reason
requirements and composed it into the executable freshness gate. Snapshot drift
now fails the audit rather than remaining passive documentation.

## Evidence and provenance

Evidence: the 0130 snapshot, validator, CLI binding, and mutation test.

## Disconfirming evidence sought

Diagnostic expectations are deliberately exact for the two currently supported
state mutations; adding a new failure mode requires a new versioned snapshot.

## Next action

Persist a diagnostic-snapshot digest for provenance.
