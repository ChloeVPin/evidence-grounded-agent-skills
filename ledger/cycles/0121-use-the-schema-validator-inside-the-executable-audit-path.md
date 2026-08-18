# Cycle 0121 — Use the schema validator inside the executable audit path

Date: 2026-08-18
Status: completed

## Question

Use the schema validator inside the executable audit path

## Decision

The executable audit now loads and validates the versioned 0119 capture schema
as part of its freshness gate. A missing `checks` field produces
`AUDIT_GATE_FAILED` with `freshness: false`.

## Evidence and provenance

Evidence: `scripts/audit_current_assertion.py`, the 0119 capture, and the
temporary-root malformed-capture integration test.

## Disconfirming evidence sought

The public output remains four checks; capture-schema validity is intentionally
composed into freshness rather than exposed as a fifth contract key.

## Next action

Persist a capture-schema failure reason in the audit evidence ledger.
