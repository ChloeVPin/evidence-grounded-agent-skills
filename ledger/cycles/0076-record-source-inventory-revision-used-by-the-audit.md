# Cycle 0076 — Record source-inventory revision used by the audit

Date: 2026-08-18
Status: completed

## Question

Record source-inventory revision used by the audit

## Decision

Migration provenance now includes a stable SHA-256 digest of the sorted source
entry inventory used by the audit.

## Evidence and provenance

Tests recompute the digest from the four archived failure IDs and migration
validation rejects malformed digest values.

## Disconfirming evidence sought

The digest proves which IDs were enumerated, not that the inventory is complete
or that source entries are semantically unchanged.

## Next action

Validation passed locally. Next cycle: detect source-inventory drift after a new
decision entry is added.
