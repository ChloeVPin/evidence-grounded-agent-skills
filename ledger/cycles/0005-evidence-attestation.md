# Cycle 0005 — Evidence Attestation

Date: 2026-08-18
Status: validated with execution capture

## Question

How can Hermes reduce the gap between a claimed test result and a command that actually ran in the reviewed repository state?

## Decision

Use a non-shell command runner that records the repository revision before execution, exact command string, exit status, and SHA-256 digest of combined output.

## Evidence and provenance

Implemented in `scripts/capture_evidence.py` with success and failure tests in `tests/test_capture_evidence.py`.

## Disconfirming evidence sought

The failing-command test proves a nonzero exit status remains nonzero in the record. The digest binds the captured output to the record, but does not prove the command was the right test or that the test is sufficient.

## Next action

Validation passed locally. Limitation: the utility does not provide a trusted remote attestation; a local operator can still choose a misleading command or alter the environment. Next cycle: bind evidence to declared acceptance criteria and changed revision.
