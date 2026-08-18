---
name: contradiction-resolution
description: Resolve conflicting claims, evidence, tests, or failures without forcing false consensus. Use when sources or observed behavior disagree and the coding agent must preserve uncertainty and decision boundaries.
---

# Contradiction Resolution and Failure Learning

Lifecycle: `draft`

## Purpose and scope

Use this skill when sources, skills, tests, reviewers, or real-world failures disagree. It produces an auditable decision or preserves an unresolved contradiction with explicit boundaries. It does not force consensus, average incompatible evidence, or declare an authority correct without tracing the claim.

## Triggers and prerequisites

Trigger when two claims conflict, a validation result contradicts a trusted skill, a production failure recurs, or reviewers disagree on a material decision. Prerequisites: claims, provenance, contexts, affected artifacts, and the observed failure or counterexample.

## Procedure

1. State each competing claim separately, including scope, assumptions, knowledge label, confidence, and intended decision.
2. Trace each claim to primary evidence and identify circular, dependent, stale, or non-independent sources.
3. Normalize the comparison: same inputs, versions, definitions, populations, risk tolerance, and success criteria. Do not compare context-free slogans.
4. Seek disconfirming evidence for each claim and design the smallest discriminating experiment, test, or source lookup.
5. Classify the relationship: one claim is refuted, claims apply in different contexts, evidence is insufficient, or the contradiction remains unresolved.
6. Record decision boundaries, affected skills, rejected hypotheses, and required follow-up. Preserve the losing claim and rationale rather than deleting it.
7. For failures, record symptom, impact, root cause, contributing conditions, detection gap, corrective action, and regression guard. Avoid substituting blame for mechanism.
8. Update dependent artifacts only after the decision is evidenced; mark confidence and freshness changes explicitly.

## Acceptance checklist

- [ ] Competing claims and contexts are stated separately.
- [ ] Evidence lineage and source independence are recorded.
- [ ] Disconfirming evidence was sought for each material claim.
- [ ] A discriminating test, experiment, or source check was run or its blocker recorded.
- [ ] Outcome is classified as refuted, contextual, insufficient, or unresolved.
- [ ] Decision boundaries and affected dependents are explicit.
- [ ] Rejected hypotheses and failure mechanisms are preserved.
- [ ] Corrective action has a regression or review trigger.

## Examples and counterexamples

Good: Two sources disagree because one describes a newer version; compare versions and scope, preserve the older boundary, and record which claim applies when.

Bad: Choose the source with the larger audience or average incompatible claims without checking provenance.

## Failure modes and recovery

If evidence is incomparable, split the claims by context instead of choosing a winner. If evidence is insufficient, keep the contradiction open and lower confidence. If a failure has no reproducible mechanism, record the uncertainty and prioritize instrumentation or reproduction before changing foundational guidance.

## Validation evidence and provenance

- Governing research report: contradiction hunting, adversarial review, preserved rejected hypotheses, failure recovery, and provenance notes improve agent reliability.
- [NIST AI RMF GenAI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf): monitoring, incident/error tracking, after-action assessment, and continual improvement guidance.
- Label observed conflicts separately from explanatory hypotheses and recommended resolutions; preserve uncertainty when the evidence does not decide between them.

Confidence: medium. Freshness review: after material failures, contradictory evidence, or methodology changes.

## Related skills and conflicts

Related: differential-patch-review, knowledge-maintenance, and repository-change-verification. This skill does not authorize silently weakening governing principles to resolve local disagreement.
