# Cycle 0128 — Bind the dependency digest into a versioned audit state record

Date: 2026-08-18
Status: completed

## Question

Bind the dependency digest into a versioned audit state record

## Decision

The versioned self-validation state now records the dependency manifest
reference and paths digest. The executable validator compares both against the
live manifest and rejects stale state.

## Evidence and provenance

Evidence: `ledger/state/0113-complete-self-validation-gate.json`, the extended
state validator, and manifest-binding tests.

## Disconfirming evidence sought

The state’s digest binds only the manifest path set; referenced-file content
integrity remains covered by the existing content-digest gates.

## Next action

Expose dependency-state freshness as a distinct diagnostic reason.
