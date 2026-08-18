---
name: regression-test-design
description: Design focused regression tests for AI-generated or human software changes from observable behavior, failure modes, and boundaries. Use when fixing a bug, adding behavior, changing an interface, or strengthening a weak test suite.
---

Lifecycle: `draft`

# Regression Test Design

## Purpose and scope

Create tests that distinguish the intended behavior from the plausible wrong behaviors most likely to recur. This skill covers test selection, assertions, boundaries, and maintainability; it does not claim that a test suite proves correctness or replace integration, security, performance, or domain-specific evaluation.

## Triggers and prerequisites

Trigger when a defect is fixed, behavior changes, a test is added or rewritten, a regression escaped, or existing tests assert only execution or implementation details. Prerequisites: the observable contract, a reproduction or representative example, baseline behavior, test framework conventions, and known dependencies or side effects.

## Decision criteria

- Test externally meaningful behavior: outputs, errors, state, permissions, side effects, ordering, and relevant resource limits.
- A regression test should fail for the original bug or a representative mutation and pass for the intended behavior.
- Prefer a small deterministic test with one reason to fail; use broader tests when the contract is inherently cross-component.
- Test selection follows risk and boundary coverage, not a fixed count or coverage percentage.

## Procedure

1. State the behavior under test and the failure it must prevent. Separate the observed symptom from the suspected implementation cause.
2. Identify the interface boundary, valid and invalid inputs, state transitions, permissions, external effects, and invariants that matter to callers.
3. Locate the nearest existing tests and follow their setup, naming, isolation, cleanup, and assertion conventions. Reuse real interfaces rather than testing private details unless the private contract is explicit.
4. Write the smallest test that reproduces the failure before the fix when practical. Confirm it fails for the right reason, not because of a broken fixture or environment.
5. Add the normal case and the highest-risk boundary or negative cases: empty, malformed, minimum, maximum, missing, duplicate, unauthorized, repeated, stale, or downstream-failure inputs as applicable.
6. Assert the complete relevant outcome, including error type or status, persisted state, emitted effects, and security boundaries. Avoid snapshots or broad mocks that can pass while behavior is wrong.
7. Check test independence and determinism. Control time, randomness, ordering, network, filesystem, and shared state only to the degree needed to isolate the contract.
8. Consider plausible surviving mutations: inverted condition, skipped call, wrong boundary, wrong error, wrong resource, missing cleanup, or changed side effect. Add the smallest distinguishing assertion for important survivors.
9. Run the focused tests, then relevant integration and broader checks. Record what the tests cover and what they cannot establish.
10. Keep the test aligned with the public behavior. Update it when the contract intentionally changes; do not weaken it merely to make an implementation pass.

## Examples and counterexamples

Good: A bug returned another user’s record when given a valid identifier. The regression test uses two principals, asserts the permitted result, asserts denial for the other record, and checks that no unauthorized state or response data is emitted.

Bad: Assert only that the handler returns a non-null value. The test can pass while authorization is completely broken.

Good: A parser fix tests a valid value, empty input, malformed input, and the exact documented error without depending on internal helper calls.

Bad: Mock the parser’s return value and assert that the mock was called; the real parsing boundary is never exercised.

## Failure modes and recovery

If the contract is unclear, use `requirements-to-acceptance` before writing the test. If the test is flaky, isolate uncontrolled time, randomness, ordering, external services, or shared state before adding retries. If the test cannot reproduce the defect, preserve the limitation and improve observability rather than claiming regression coverage. If a test depends on unstable implementation details, move the assertion to the nearest stable interface.

## Validation evidence and provenance

- The governing research requires automated validation, empirical failure analysis, adversarial testing, boundary cases, and honest accounting of limitations.
- Mutation testing is used here as a diagnostic question—“what plausible wrong behavior would this test miss?”—not as a universal correctness score.
- Confidence: high for behavior-first and boundary-oriented test design; medium for the right test level and tooling in any particular repository.
- Freshness: review when the project’s test framework, architecture, risk profile, or evaluation strategy changes.

## Related skills and conflicts

Related: `test-effectiveness-analysis`, `requirements-to-acceptance`, `evidence-driven-debugging`, `repository-change-verification`, `secure-coding-review`, and `differential-patch-review`. This skill does not authorize deleting failing tests, inflating coverage metrics, or treating green tests as proof of every behavior.
