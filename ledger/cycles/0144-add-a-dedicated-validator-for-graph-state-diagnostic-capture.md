# Cycle 0144 — Add a dedicated validator for graph-state diagnostic captures

Date: 2026-08-18
Status: completed

## Question

Add a dedicated validator for graph-state diagnostic captures

## Decision

Added `validate_graph_state_diagnostic_capture`, enforcing command provenance,
graph reference availability, policy-digest equality, and passing result.
Valid and tampered captures are covered.

## Evidence and provenance

Evidence: the 0143 graph-state capture, graph artifact, dedicated validator, and
integration test.

## Disconfirming evidence sought

The validator binds graph policy provenance but does not itself replay graph
mutations; executable temporary-root tests cover those mutations.

## Next action

Use the dedicated validator in the executable audit path.
