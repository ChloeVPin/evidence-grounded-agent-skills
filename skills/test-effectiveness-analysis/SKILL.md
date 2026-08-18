# Test-Effectiveness Analysis

Lifecycle: `draft`

## Purpose and scope

Use this skill to evaluate whether tests detect meaningful behavioral faults, especially in AI-generated changes. It supplements ordinary test execution with boundary cases, negative cases, differential checks, and mutation-oriented diagnostics. It does not claim that mutation score proves correctness or prescribe one universal threshold.

## Triggers and prerequisites

Trigger when a change adds or modifies behavior, when tests are newly generated, when a patch passes tests but remains semantically uncertain, or when regressions recur. Prerequisites: acceptance criteria, baseline behavior, executable tests, and a way to create or obtain representative mutations.

## Procedure

1. Translate the requested behavior into observable positive, negative, boundary, and invariant cases.
2. Run the baseline tests and record their revision, command, exit status, and output digest.
3. Inspect whether tests assert externally meaningful behavior rather than only execution, non-null values, or implementation details.
4. Introduce representative fault mutations near the changed behavior: operator/branch changes, boundary shifts, omitted calls, altered errors, and incorrect side effects where applicable.
5. Run the test suite against each mutation and classify killed, surviving, equivalent, invalid, or unexecuted mutations. Do not count invalid mutants as surviving evidence.
6. Investigate surviving mutations. Add the smallest test that distinguishes the intended behavior when the mutation represents a plausible fault.
7. Use differential or oracle comparison when a reference implementation exists, and check that tests cover unaffected behavior to detect regressions.
8. Record mutation selection, test results, limitations, residual uncertainty, and the next review trigger. Treat mutation results as diagnostic evidence, not a correctness certificate.

## Acceptance checklist

- [ ] Acceptance criteria include positive, negative, boundary, or invariant cases as applicable.
- [ ] Baseline and focused tests were run with captured evidence.
- [ ] Assertions check meaningful behavior and side effects.
- [ ] Representative mutations were selected and classified.
- [ ] Surviving plausible mutations were investigated or explicitly accepted with rationale.
- [ ] Regression behavior outside the changed path was checked.
- [ ] Mutation limitations, equivalent mutants, and residual uncertainty are recorded.

## Examples and counterexamples

Good: A mutation removes a required authorization check and the relevant negative test fails, showing that the test detects the security behavior.

Bad: Count invalid or equivalent mutants as evidence that the suite is weak, or treat a mutation score as correctness proof.

## Failure modes and recovery

If mutation tooling cannot run, record the exact blocker and use manually designed fault injections only as limited evidence. If a mutation is equivalent, document why rather than weakening the test. If mutation score improves while behavior coverage worsens, reject the metric as misleading and inspect the test assertions.

## Validation evidence and provenance

- [Petrović et al., Long Term Effects of Mutation Testing](https://research.google/pubs/long-term-effects-of-mutation-testing/): longitudinal analysis of approximately 15 million mutants and their relation to test-suite improvement and historical faults.
- [Roman and Mnich, TDD with mutation testing](https://link.springer.com/article/10.1007/s11219-020-09534-x): controlled experimental evidence with stated sample and coverage limitations.

Confidence: medium. Freshness review: annually and after material changes to testing tools or benchmark methodology.

## Related skills and conflicts

Related: repository-change-verification, test-design, differential-testing, and dependency-security-audit. This skill does not override project-specific test policy or human review.
