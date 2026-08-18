# Cycle 0135 — Add a dedicated validator for snapshot-diagnostic captures

Date: 2026-08-18
Status: completed

## Question

Add a dedicated validator for snapshot-diagnostic captures

## Decision

Added `validate_snapshot_diagnostic_capture`, enforcing execution provenance,
snapshot reference availability, canonical snapshot digest, and passing audit
result. Valid and tampered captures are covered.

## Evidence and provenance

Evidence: the 0134 capture, its source snapshot, the dedicated validator, and
the integration test.

## Disconfirming evidence sought

The validator checks the capture’s binding and digest; it does not independently
replay failure mutations, which remain a separate executable concern.

## Next action

Use the dedicated validator inside the executable audit path.
