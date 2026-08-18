# Cycle 0043 — Next Exploration

Date: 2026-08-18
Status: decision recorded; next skill drafted

## Question

Which next high-leverage skill gap should Hermes explore after verification, dependency security, test effectiveness, tool authorization, and differential review foundations?

## Mode

`exploration`

## Decision

Select knowledge maintenance and freshness management as the next skill.

## Evidence and provenance

Evidence: [RFC 9745](https://www.rfc-editor.org/rfc/rfc9745.html) defines deprecation signaling and migration documentation; [RFC 8594](https://www.rfc-editor.org/info/rfc8594/) defines sunset signaling while warning that timestamps are hints; [NIST AI RMF GenAI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) calls for monitoring, incident/error tracking, and measurable continual improvement.

Candidate ranking: maintenance/freshness—high reuse, high temporal leverage, bounded artifact; identity enforcement—high severity but external authority dependent; formal verification—high assurance but domain-specific and expensive.

## Disconfirming evidence sought

Disconfirming evidence: freshness dates are signals, not proof that content is wrong; timeless knowledge and fast-changing knowledge require different review windows. The skill must support uncertainty, deprecation, supersession, and manual override with provenance.

## Next action

Build and validate `skills/knowledge-maintenance/SKILL.md`.
