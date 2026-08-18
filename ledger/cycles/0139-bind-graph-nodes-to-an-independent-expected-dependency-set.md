# Cycle 0139 — Bind graph nodes to an independent expected dependency set

Date: 2026-08-18
Status: completed

## Question

Bind graph nodes to an independent expected dependency set

## Decision

The executable audit now supplies an independent expected node set rather than
trusting the graph’s own node list. Graph node removal or edge drift fails the
freshness gate.

## Evidence and provenance

Evidence: `EXPECTED_FRESHNESS_GRAPH_NODES` in the executable audit and expanded
graph mutation tests.

## Disconfirming evidence sought

The expected set is code-level policy and must be updated deliberately when the
freshness architecture changes.

## Next action

Persist an independent graph-policy digest.
