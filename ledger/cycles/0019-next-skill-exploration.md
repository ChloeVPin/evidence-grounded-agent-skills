# Cycle 0019 — Next Skill Exploration

Date: 2026-08-18
Status: decision recorded; next skill drafted

## Question

Which next skill gap should Hermes explore after repository-change verification: test design, dependency/security auditing, agent runtime safety, or another gap supported by evidence?

## Mode

`exploration`

## Decision

Select dependency and supply-chain security auditing as the next skill to build.

## Evidence and provenance

Candidate map:

| Candidate | Impact | Reuse | Uncertainty | Decision |
|---|---:|---:|---:|---|
| Dependency/security auditing | high | high | medium | selected |
| Test design and mutation analysis | high | medium | medium | next candidate |
| Agent runtime safety | very high | high | high | requires deeper threat model |

Evidence: [GitHub dependency review](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review) describes dependency-diff scanning and enforcement; [OWASP Secure Coding with AI](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Coding_with_AI_Cheat_Sheet.html) identifies hallucinated package names, outdated CVEs, and AI-modified build paths; [NIST AI RMF GenAI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) provides authoritative lifecycle risk-management guidance.

## Disconfirming evidence sought

Mutation-testing research reports stronger test suites but also meaningful cost and tool/operator limitations; runtime safety has greater severity but insufficiently bounded scope for the next artifact. Dependency auditing is the most immediately executable extension of the existing change-verification foundation. Revisit this ranking after validation.

## Next action

Build and validate `skills/dependency-security-audit/SKILL.md`.
