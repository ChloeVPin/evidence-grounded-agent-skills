---
name: evidence-driven-debugging
description: Diagnose software failures by reproducing the symptom, separating observations from hypotheses, testing competing explanations, and making the smallest verified fix. Use for bugs, regressions, flaky behavior, failing builds, and unexplained runtime errors in AI coding-agent work.
---

Lifecycle: `draft`

# Evidence-Driven Debugging

## Purpose and scope

Find and correct the cause of a software failure without confusing a plausible story with evidence. Use this skill for code, tests, builds, deployments, and runtime behavior. It does not replace incident response, security triage, or domain-specific safety procedures.

## Triggers and prerequisites

Trigger when behavior is broken, surprising, flaky, slower than required, or contradicted by a test or specification. Before changing code, collect the exact symptom, expected behavior, reproduction inputs, environment/version, relevant revision, logs or traces, and the narrowest command that demonstrates the problem.

## Concepts and decision criteria

- An **observation** is directly reproduced or measured; a **hypothesis** explains it but remains unverified.
- A useful experiment changes one relevant variable and produces outcomes that distinguish competing hypotheses.
- A fix is not validated by making one symptom disappear if the root cause, boundary behavior, and regression risk remain unknown.
- Prefer the smallest reversible experiment and the smallest change that explains all observed evidence.

## Procedure

1. State the expected behavior and the actual symptom in observable terms. Record what is known, what is inferred, and what is missing.
2. Reproduce the failure with the smallest reliable input and command. Capture the baseline result before editing. If it is intermittent, characterize frequency and conditions instead of calling it fixed after one successful run.
3. Map the execution path from the failing interface to the relevant state, inputs, dependencies, and side effects. Inspect callers and tests before selecting a change.
4. Generate at least two plausible hypotheses, including one explanation that would make the current theory wrong. Rank them by evidence, not familiarity.
5. Design the smallest discriminating check for the highest-risk hypothesis. Use a focused test, trace, boundary input, controlled configuration change, or source/documentation check. Do not change production code merely to gather an unrecorded guess.
6. Update the hypothesis table from the result: supported, weakened, refuted, or unresolved. Repeat only while the next experiment can change the decision.
7. Implement the narrowest root-cause fix. Avoid suppressing errors, broadening permissions, loosening assertions, adding retries, or changing unrelated behavior unless evidence establishes that as the cause and the tradeoff is explicit.
8. Add or update a regression check for the original symptom and at least one nearby boundary or failure path when practical. Preserve a reproduction for bugs that could recur.
9. Verify in layers: reproduce the original case, run focused regression checks, inspect affected interfaces and side effects, then run broader project checks when warranted.
10. Report the causal evidence, changed behavior, checks run and not run, residual uncertainty, and the condition that should trigger another investigation.

## Examples and counterexamples

Good: A request intermittently hangs. Measure when it happens, isolate the input and dependency state, compare traces for hanging and completing runs, then fix the demonstrated wait condition and retain a timeout/regression case.

Bad: Add a timeout because the request hangs, without determining whether the timeout hides data loss, a deadlock, or a slow but valid operation.

Good: A test fails only on one platform. Reproduce with the platform and version recorded, compare path, locale, filesystem, and dependency assumptions, and change the code only after identifying the platform-specific cause.

Bad: Skip the test or hard-code the observed output because the local platform passes.

## Failure modes and recovery

If the failure cannot be reproduced, preserve the report and add instrumentation or a controlled reproduction before changing behavior. If multiple causes remain plausible, do not choose by intuition; run a discriminating experiment or state the blocker. If the proposed fix changes the symptom but not the causal evidence, revert it and return to hypothesis testing. If the issue may be security-related, stop ordinary debugging and follow the repository’s security disclosure and containment process.

## Validation evidence and provenance

Separate observed symptoms from hypotheses and recommendations. Record confidence and freshness, and verify whether supporting reports or documentation are genuinely independent.

- The governing research emphasizes falsifiability, disconfirming evidence, adversarial review, empirical failure analysis, regression testing, and preserving failure learning.
- The skill’s procedure applies the scientific method operationally: observations precede hypotheses, experiments distinguish explanations, and conclusions remain proportional to evidence.
- Confidence: high for the general debugging workflow; medium for any diagnosis until the specific reproduction and regression evidence exist.
- Freshness: review when debugging tooling, runtime architecture, or the repository’s incident and testing practices materially change.

## Related skills and conflicts

Related: `repository-change-verification`, `test-effectiveness-analysis`, `differential-patch-review`, `contradiction-resolution`, and `dependency-security-audit`. This skill does not authorize skipping security response, muting failures, or claiming a root cause without discriminating evidence.
