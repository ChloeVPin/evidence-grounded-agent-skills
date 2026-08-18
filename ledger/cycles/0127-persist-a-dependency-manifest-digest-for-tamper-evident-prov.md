# Cycle 0127 — Persist a dependency-manifest digest for tamper-evident provenance

Date: 2026-08-18
Status: completed

## Question

Persist a dependency-manifest digest for tamper-evident provenance

## Decision

Added a canonical SHA-256 over the sorted dependency paths and required it in
the manifest validator. Both path-set drift and digest tampering are rejected.

## Evidence and provenance

Evidence: `ledger/evidence/0125-audit-dependencies.json`, the digest gate in
`scripts/decision_ledger.py`, and its mutation tests.

## Disconfirming evidence sought

The digest authenticates the manifest’s path set, not the contents of each
referenced file; existing content-digest manifests cover those file contents.

## Next action

Bind the dependency digest into a versioned audit state record.
