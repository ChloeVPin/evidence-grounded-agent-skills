# Cycle 0036 — Tool Audit Records

Date: 2026-08-18
Status: validated with redacted audit records

## Question

What durable evidence should accompany each tool authorization decision and call?

## Decision

Audit records bind caller, tool, action, resource, parameters, decision, approval, timestamp, and output digest; credential-like parameter keys are recursively redacted.

## Evidence and provenance

Implemented in `scripts/tool_audit.py` with three tests in `tests/test_tool_audit.py`.

## Disconfirming evidence sought

Required identity/decision fields and timestamp syntax are enforced; output is digest-bound and secrets are not retained in parameters.

## Next action

Validation passed locally. Limitation: a local digest does not authenticate the caller or prevent a privileged operator from rewriting records. Next cycle: connect audit records to authorization decisions and test denied, approved, and tampered-call paths.
