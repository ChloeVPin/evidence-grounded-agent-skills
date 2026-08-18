# Cycle 0136 — Use the dedicated validator inside the executable audit path

Date: 2026-08-18
Status: completed

## Question

Use the dedicated validator inside the executable audit path

## Decision

The executable audit now validates the 0134 snapshot-diagnostic capture as part
of freshness. Tampering its snapshot digest fails with `AUDIT_GATE_FAILED` and
the dedicated diagnostic reason.

## Evidence and provenance

Evidence: the capture-validator binding in `scripts/audit_current_assertion.py`
and the temporary-root tamper test.

## Disconfirming evidence sought

The public contract remains four checks; capture validation is composed into
freshness with the other diagnostic dependencies.

## Next action

Persist a complete freshness dependency graph.
