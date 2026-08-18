# Cycle 0156 — Persist a digest for the freshness capture inventory

Date: 2026-08-18
Status: completed

## Question

Persist a digest for the freshness capture inventory

## Decision

Added a canonical SHA-256 over the freshness inventory payload and required it
in validation. Digest tampering is rejected separately from reference drift.

## Evidence and provenance

Evidence: the 0154 inventory’s `inventory_sha256`, validator, and digest mutation
coverage.

## Disconfirming evidence sought

The digest binds inventory structure and references; the individual captures
retain their own provenance and output digests.

## Next action

Bind the inventory digest into versioned state.
