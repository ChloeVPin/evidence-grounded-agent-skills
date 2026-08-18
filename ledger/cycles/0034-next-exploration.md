# Cycle 0034 — Next Exploration

Date: 2026-08-18
Status: decision recorded; next skill drafted

## Question

Which next high-leverage skill gap should Hermes explore after repository verification, dependency security, and test-effectiveness foundations?

## Mode

`exploration`

## Decision

Select least-privilege tool authorization and audit as the next skill.

## Evidence and provenance

Evidence: [OWASP AI Agent Security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html) identifies tool abuse, privilege escalation, excessive autonomy, and high-impact actions, and recommends per-tool permission scoping; [NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative) identifies agent authentication and identity infrastructure as active research priorities; [OWASP MCP Security](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html) recommends minimum permissions and strict tool parameter schemas.

Candidate ranking: tool authorization—very high mistake severity, high reuse, bounded validation surface; differential testing—high reuse but overlaps current test-effectiveness foundation; live connector trust—important but external-service dependent.

## Disconfirming evidence sought

Disconfirming evidence: a static permission policy cannot prove runtime intent, identity, or downstream authorization; the skill will be a policy gate and audit record, not a complete security guarantee.

## Next action

Build and validate `skills/tool-authorization-audit/SKILL.md`.
