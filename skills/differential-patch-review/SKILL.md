# Differential Patch Review

Lifecycle: `draft`

## Purpose and scope

Use this skill when an AI-generated patch passes ordinary tests but semantic alignment remains uncertain. Compare the candidate against a trusted baseline, reference patch, or independently specified behavior using differentiating inputs. It detects observable divergence; it does not declare every divergence incorrect.

## Triggers and prerequisites

Trigger when a patch changes multiple behaviors, passes a narrow test suite, has an under-specified issue, or differs materially from a known-good implementation. Prerequisites: candidate and baseline/reference revisions, executable environment, acceptance criteria, and a source of behavioral expectations.

## Procedure

1. Define the observable contract: inputs, outputs, errors, side effects, permissions, ordering, and relevant performance constraints.
2. Establish the comparison pair and justify its trust: baseline, human patch, independent implementation, specification oracle, or generated expected behavior.
3. Run shared tests against both versions and record commands, revisions, outcomes, and limitations.
4. Generate or design differentiating inputs near changed branches, boundaries, error paths, state transitions, and security-sensitive behavior.
5. Classify differences as expected contract changes, permitted implementation variation, unexplained divergence, or clear violation.
6. Investigate unexplained divergence by tracing it to the acceptance criteria, issue, source code, and tests. Add a regression test when the behavior is incorrect or under-specified.
7. Check for overreach: behavior changed beyond the requested scope, including error messages, permissions, resource use, and side effects.
8. Record the comparison pair, differentiating evidence, decision, residual uncertainty, and review trigger. Do not use textual patch similarity as correctness evidence.

## Acceptance checklist

- [ ] Observable contract and comparison trust basis are explicit.
- [ ] Both versions ran the shared checks or the blocker is recorded.
- [ ] Differentiating inputs cover boundaries and changed behavior.
- [ ] Divergences are classified by contract, not textual similarity.
- [ ] Unexplained or incorrect differences have regression coverage or an explicit decision.
- [ ] Out-of-scope behavior and security-sensitive side effects were checked.
- [ ] Residual uncertainty and review trigger are recorded.

## Examples and counterexamples

Good: A candidate and baseline return the same result on ordinary inputs but differ on malformed input; classify the difference against the contract instead of ignoring it.

Bad: Treat textual similarity or matching happy-path output as proof of equivalence.

## Failure modes and recovery

If no trusted comparison exists, narrow the claim to specification-based testing and label it accordingly. If the environment cannot run both versions, do not call the comparison validated. If versions legitimately differ under the contract, record the allowed difference rather than forcing textual convergence.

## Validation evidence and provenance

- [Wang, Pradel, and Liu, Are “Solved Issues” in SWE-bench Really Solved Correctly?](https://arxiv.org/abs/2503.15223): differential tests exposed behavioral discrepancies in plausible patches that passed benchmark validation.
- [GitHub: About pull requests](https://docs.github.com/en/pull-requests/get-started/about-pull-requests): reviewable diffs, discussion, and checks form the change-validation boundary.

Confidence: medium-high for the need; medium for generalization across languages and test environments. Freshness review: after material changes to evaluation methods.

## Related skills and conflicts

Related: repository-change-verification, test-effectiveness-analysis, evidence-attestation, and dependency-security-audit. This skill does not replace domain-specific oracle construction or human review.
