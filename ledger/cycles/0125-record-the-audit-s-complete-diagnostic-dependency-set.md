# Cycle 0125 — Record the audit’s complete diagnostic dependency set

Date: 2026-08-18
Status: completed

## Question

Record the audit’s complete diagnostic dependency set

## Decision

Persisted `ledger/evidence/0125-audit-dependencies.json` enumerates the exact
assertion, bundle, capture, state, diagnostic, and executable-script inputs.
Its validator rejects both drift and unavailable references.

## Evidence and provenance

Evidence: the 0125 dependency manifest, `validate_audit_dependency_manifest`,
and its exact-set integration test.

## Disconfirming evidence sought

The manifest is not yet an executable gate; until the next binding cycle, the
CLI’s dependency discovery remains authoritative.

## Next action

Bind the dependency manifest into the executable audit.
