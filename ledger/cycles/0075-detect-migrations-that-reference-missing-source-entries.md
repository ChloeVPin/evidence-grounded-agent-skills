# Cycle 0075 — Detect migrations that reference missing source entries

Date: 2026-08-18
Status: completed

## Question

Detect migrations that reference missing source entries

## Decision

Migration inventory auditing now optionally binds each migration to a supplied
set of decision-entry IDs and rejects missing source references.

## Evidence and provenance

The current migration passes against the archived decision ledger; the same
record fails when checked against an unrelated source-ID set.

## Disconfirming evidence sought

The check depends on the caller providing a complete source-entry inventory and
does not prove external history has not been deleted.

## Next action

Validation passed locally. Next cycle: add migration inventory provenance and
record the source-inventory revision used by the audit.
