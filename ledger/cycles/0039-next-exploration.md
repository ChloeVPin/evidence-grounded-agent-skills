# Cycle 0039 — Next Exploration

Date: 2026-08-18
Status: decision recorded; next skill drafted

## Question

Which next high-leverage skill gap should Hermes explore after repository verification, dependency security, test effectiveness, and tool authorization foundations?

## Mode

`exploration`

## Decision

Select differential patch review as the next skill.

## Evidence and provenance

Evidence: [Are “Solved Issues” in SWE-bench Really Solved Correctly?](https://arxiv.org/abs/2503.15223) found behaviorally divergent plausible patches and used differentiating tests to expose them; [GitHub pull-request guidance](https://docs.github.com/en/pull-requests/get-started/about-pull-requests) establishes reviewable diffs and checks as the normal change boundary. Differential review complements Hermes' existing test-effectiveness and attestation foundations.

## Disconfirming evidence sought

Disconfirming evidence: candidate/reference divergence is not automatically incorrect; specifications may permit multiple implementations. The skill must compare observable contract behavior, not textual similarity.

## Next action

Build and validate `skills/differential-patch-review/SKILL.md`.
