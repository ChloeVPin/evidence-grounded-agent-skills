---
name: secure-coding-review
description: Review an AI-generated coding change for application security risks at trust boundaries, including input handling, authorization, secrets, data exposure, injection, and unsafe failure behavior. Use before accepting security-relevant features, bug fixes, or refactors.
---

Lifecycle: `draft`

# Secure Coding Review

## Purpose and scope

Identify and reduce security risk introduced by a repository change. Review observable behavior, data flow, trust boundaries, and misuse cases rather than relying on style or a passing test suite. This skill does not replace a specialist penetration test, incident response, threat model for a high-risk system, or the repository’s disclosure process.

## Triggers and prerequisites

Trigger when a change handles untrusted input, identity, authorization, secrets, sensitive data, network requests, serialization, file paths, commands, templates, cryptography, multi-tenant state, or security-sensitive errors. Prerequisites: the requested behavior, baseline and proposed diff, deployment context, trust boundaries, data classification, relevant security policy, and available tests or static-analysis results.

## Decision criteria

- Treat every external input, persisted value, dependency output, and model/tool output as untrusted until the code establishes the required property.
- Authentication identifies a principal; authorization independently checks whether that principal may perform the specific action on the specific resource.
- A control is credible only when its enforcement point, failure behavior, and bypass paths are understood.
- Severity depends on impact, exploitability, reachability, affected data, and exposure—not on a generic checklist score.

## Procedure

1. Restate the intended behavior and security-relevant acceptance criteria. Identify assets, principals, trust boundaries, privileged operations, and failure consequences.
2. Inspect the complete diff and its callers, configuration, schemas, routes, background jobs, and tests. Trace data from entry to storage, rendering, logging, external calls, and side effects.
3. Enumerate plausible abuse cases: forged identity, missing or confused authorization, injection into interpreters or queries, path or resource escape, secret disclosure, unsafe deserialization, replay, denial of service, cross-tenant access, and information leakage through errors or timing.
4. For each relevant boundary, verify canonical validation, normalization, encoding, parameterization, least privilege, secret handling, rate/resource limits, safe defaults, and fail-closed behavior. Check both direct and alternate code paths.
5. Test negative and boundary cases with representative untrusted values, absent or altered credentials, wrong-resource identifiers, malformed data, repeated requests, oversized inputs, and downstream failures. Use a static analyzer or security scanner when appropriate, but inspect its scope and false negatives.
6. Check whether the change weakens an existing control, expands permissions, exposes new data, changes logging or redaction, relies on mutable external behavior, or makes recovery harder. Compare against the baseline and documented security assumptions.
7. Classify findings by concrete impact and reachability. Require a fix, containment, explicit risk acceptance, or specialist escalation; do not hide uncertainty behind a low score.
8. Add regression coverage for confirmed risks and verify the intended behavior, denial behavior, and unaffected authorization/data boundaries. Record checks that could not run and why.
9. Report findings, evidence, assumptions, residual risk, reviewer or escalation requirement, and the condition that should trigger another review.

## Examples and counterexamples

Good: A handler checks that a session is valid, then verifies the requested record belongs to that principal before returning it; tests cover another principal’s identifier, missing credentials, and malformed identifiers.

Bad: “The endpoint is authenticated, so it is secure.” Authentication alone does not establish object-level authorization.

Good: A query uses the repository’s parameterized interface, and the review checks all alternate filters and raw-query paths.

Bad: Escape one visible input field while leaving a second concatenated query path reachable.

Good: A failure response avoids secrets and unnecessary internal detail while logs retain a redacted diagnostic identifier for authorized investigation.

Bad: Return a stack trace or token because it helps debugging in development without verifying the deployment mode or redaction boundary.

## Failure modes and recovery

If the trust boundary or deployment context is unknown, narrow the review and escalate rather than assuming a safe environment. If a scanner is unavailable, perform focused manual abuse-case review and label the limitation. If a vulnerability may be exploitable, contain exposure and follow the repository’s security response process before ordinary refactoring. If the intended security property is ambiguous, stop and clarify it before choosing an implementation.

## Validation evidence and provenance

- The governing research requires adversarial review, explicit failure modes, safety evaluation, source hierarchy, and evidence proportional to risk.
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/): input validation, output encoding, authentication, access control, cryptographic practices, error handling, and logging controls.
- [OWASP Top 10](https://owasp.org/www-project-top-ten/): recurring application-security risk categories and prevention guidance.
- [CWE](https://cwe.mitre.org/): weakness descriptions and mitigations for reasoning about concrete failure mechanisms.
- Label observed data flows and failures separately from exploitability hypotheses and recommended controls; do not report a possibility as a confirmed vulnerability without evidence.
- Confidence: high for the boundary-review principles; medium for severity and applicability until the deployment context and threat model are known.
- Freshness: review when security standards, deployment architecture, threat model, or relevant dependencies materially change.

For material conclusions, seek disconfirming evidence, distinguish observations from hypotheses and recommendations, record tradeoffs and uncertainty, and note confidence, freshness, and source independence.

## Related skills and conflicts

Related: `dependency-security-audit`, `tool-authorization-audit`, `repository-change-verification`, `requirements-to-acceptance`, `evidence-driven-debugging`, and `test-effectiveness-analysis`. This skill does not authorize bypassing security policy, exposing secrets for diagnosis, or substituting a checklist for specialist review of high-risk systems.
