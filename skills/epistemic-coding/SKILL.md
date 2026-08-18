---
name: epistemic-coding
description: Apply an evidence-first philosophy while investigating, changing, or explaining a software repository. Use when correctness, uncertainty, scope, or the evidence behind a coding decision matters.
---

Lifecycle: `draft`

# Evidence-First Coding

## Purpose and scope

Produce repository changes that are justified by evidence, explicit about uncertainty, and proportionate to the request. This skill governs investigation and decision-making; it does not replace project-specific instructions, tests, security review, or human approval.

## Triggers and prerequisites

Use when a task involves a bug, design choice, refactor, new dependency, incomplete specification, or a claim that code is correct. Before acting, identify the repository instructions, the files and callers in scope, the requested outcome, and the available ways to verify it.

## Knowledge labels

Label material claims as facts, observations, heuristics, conventions, recommendations, hypotheses, or speculation. Facts and observations need direct provenance; heuristics and conventions need scope and limits; recommendations need tradeoffs; hypotheses and speculation must remain visibly uncertain until evidence supports them.

## Procedure

1. Translate the request into an observable outcome. If two interpretations would produce materially different changes, ask before editing.
2. Inspect the relevant code, its callers, tests, and repository instructions. Separate facts observed in the repository from assumptions, conventions, recommendations, hypotheses, and speculation.
3. State the smallest change that could satisfy the outcome. Prefer reversible decisions when evidence is incomplete; do not add features for imagined future needs.
4. Seek disconfirming evidence: ask, “What would make this conclusion wrong?” Check boundary inputs, failure paths, security effects, unrelated behavior, and the strongest plausible alternative explanation.
5. Implement only the justified change. Preserve unrelated behavior and record meaningful tradeoffs rather than presenting one context-dependent choice as universal.
6. Verify the outcome with the narrowest relevant reproduction or test, then run broader checks when the change warrants them. Read the actual results.
7. Report what is proven, what remains uncertain, and the next review trigger. Never call a change correct merely because it looks plausible or a test happens to pass.

## Examples and counterexamples

Good: “The caller expects a 404 for a missing record; the current code raises an uncaught exception. I reproduced it, added the missing-case regression test, and changed only the boundary handling.”

Bad: “This pattern is standard, so I refactored the module.” Popularity is not evidence that the pattern fits this repository or request.

Good: “The test suite passes, but it does not exercise authorization failure; confidence is limited until that boundary is checked.”

Bad: “All tests pass, therefore the feature is correct.” Green tests are evidence with coverage limits, not a proof of every behavior.

## Failure modes and recovery

If the evidence is contradictory, preserve the competing explanations and use the smallest discriminating test or source check. If evidence is insufficient, narrow the claim and mark the decision uncertain. If verification cannot run, record the exact limitation and do not claim completion. If the requested change conflicts with repository instructions or a protected rule, surface the conflict before editing.

## Validation evidence and provenance

- Governing principles: truth over confidence, evidence over convention, verification over assertion, tradeoffs, simplicity, reversibility, and explicit disconfirmation.
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework): risk-management guidance emphasizes valid and reliable evaluation, transparency, and managing uncertainty across an AI system’s lifecycle.
- Research basis: distinguish facts from advice, trace important claims to authoritative sources, review adversarially, validate with examples and counterexamples, and maintain skills when evidence changes.
- Check source independence: trace repeated claims to their origin and do not count copied summaries as separate confirmation.
- Quality standard: correctness, completeness, usefulness, robustness, maintainability, safety, and provenance.
- Governing research report: an evidence-first agent must distinguish knowledge types, seek disconfirming evidence, preserve uncertainty, and measure substantive improvement rather than activity.

Source independence is a required check for material claims: repeated summaries do not become independent evidence merely because they appear in different places.

Confidence: high for the governing principles; medium for any domain-specific conclusion reached while applying them. Freshness review: when the governing principles or source evidence changes.

## Related skills and conflicts

Related: `repository-change-verification`, `contradiction-resolution`, `test-effectiveness-analysis`, `differential-patch-review`, `dependency-security-audit`, and `knowledge-maintenance`. This skill does not authorize ignoring project instructions, skipping required verification, or weakening constitutional rules to finish faster.
