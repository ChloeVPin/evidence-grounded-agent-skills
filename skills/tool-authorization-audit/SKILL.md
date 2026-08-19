---
name: tool-authorization-audit
description: Review AI-agent tools and proposed calls for least privilege, bounded parameters, explicit authorization, isolation, and auditable high-impact actions. Use when tools, credentials, scopes, or permissions change.
---

Lifecycle: `draft`

# Tool Authorization Audit

## Purpose and scope

Use this skill to review an AI agent's tool definitions and proposed tool calls for least privilege, explicit authorization, bounded parameters, and auditable high-impact actions. It covers policy and review artifacts; it does not prove the downstream system enforces the declared permissions or that the agent's intent is benign.

## Triggers and prerequisites

Trigger when tools, MCP servers, credentials, scopes, command allowlists, parameter schemas, or high-impact workflows change. Prerequisites: task purpose, tool inventory, caller identity/trust level, granted scopes, target resources, and approval policy.

## Decision criteria

Authorize only the least privilege needed for the stated task, with bounded targets, enforceable parameters, and accountable approval for high-impact actions. If enforcement or downstream identity cannot be verified, restrict use and record the assumption rather than treating policy text as proof.

## Procedure

1. State the task's required capabilities and separate read, write, destructive, network, credential, and administrative actions.
2. Inventory every tool, server, credential, scope, parameter, downstream identity, and reachable resource. Include transitive tool or server behavior.
3. Compare granted authority with required authority. Remove tools and permissions not necessary for the task; do not use unrestricted shell or wildcard resource access as a default.
4. Validate parameter schemas and reject undeclared fields, ambiguous resource selectors, unsafe paths, unbounded quantities, and commands outside the task allowlist.
5. Classify high-impact or irreversible actions. Require independent authorization or human approval before execution, with a clear reviewer and rationale.
6. Check isolation between trust levels, users, agents, and servers. Review delegation, token lifetime, revocation, and confused-deputy paths.
7. Require audit records for authorization decision, tool call, target, result, identity, and time. Redact secrets and sensitive payloads from logs.
8. Probe negative cases: unauthorized tool, over-broad parameter, cross-resource target, expired approval, prompt-injected request, and repeated or cascading calls.
9. Record residual risk, enforcement assumptions, review trigger, and decision. A policy declaration alone is not runtime proof.

## Acceptance checklist

- [ ] Required capabilities are separated from granted authority.
- [ ] Tool, server, credential, scope, and downstream identity inventory is complete.
- [ ] Least-privilege scopes and resource boundaries are explicit.
- [ ] Parameters reject undeclared, ambiguous, unsafe, or unbounded values.
- [ ] High-impact actions require independent approval.
- [ ] Delegation, expiry, revocation, and trust-level isolation are addressed.
- [ ] Authorization and tool-call audit records are defined with redaction.
- [ ] Negative and prompt-injection cases were tested or recorded as limitations.

## Examples and counterexamples

Good: A tool request needs one repository file, so the review rejects unrestricted filesystem access and checks an out-of-scope path.

Bad: Approve broad shell or wildcard access because the current prompt appears harmless.

## Failure modes and recovery

If the required authority cannot be distinguished from the granted authority, stop and escalate. If a tool exposes unrestricted shell or wildcard resources, constrain it or keep it untrusted. If approval identity or expiry cannot be verified, do not execute high-impact actions. If logs contain secrets, revoke and rotate affected credentials and repair the logging boundary.

## Validation evidence and provenance

Record confidence and freshness for each authorization conclusion, separate observations from hypotheses and recommendations, and verify the independence of corroborating evidence.

- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html): tool security, least privilege, explicit authorization, and high-impact action controls.
- [NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative): agent authentication and identity infrastructure research priorities.
- [OWASP MCP Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/MCP_Security_Cheat_Sheet.html): minimum permissions, strict parameter schemas, and server isolation guidance.
- Label observed tool scopes and call behavior separately from abuse hypotheses and recommended permission changes; a theoretical path is not evidence of exploitation.

Confidence: medium. Freshness review: after tool, identity, or permission-model changes and at least quarterly.

For material conclusions, seek disconfirming evidence, distinguish observations from hypotheses and recommendations, record tradeoffs and uncertainty, and note confidence, freshness, and source independence.

## Related skills and conflicts

Related: `repository-change-verification`, `dependency-security-audit`, `secure-coding-review`, and `prompt-injection-resistance`. This skill does not override platform authorization or human approval requirements.
