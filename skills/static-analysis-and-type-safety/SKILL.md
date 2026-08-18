---
name: static-analysis-and-type-safety
description: Use linters, type checkers, security analyzers, and other static checks as evidence while changing a codebase. Use when fixing diagnostics, introducing types, changing analyzer configuration, or deciding whether a warning is real, irrelevant, or dangerous to suppress.
---

Lifecycle: `draft`

# Static Analysis and Type Safety

## Purpose and scope

Improve code safety and maintainability through meaningful static checks without confusing tool output with complete correctness. This skill covers selecting, interpreting, configuring, and responding to static analysis; it does not replace runtime tests, security review, formal verification, or domain-specific reasoning.

## Triggers and prerequisites

Trigger when a change produces lint/type/analyzer diagnostics, modifies type or lint configuration, adds a static check, migrates untyped code, or uses a clean report as evidence of correctness. Prerequisites: tool and version, scope/configuration, baseline report, relevant language semantics, intended behavior, generated/vendor boundaries, and policy for warnings or suppressions.

## Decision criteria

- A diagnostic is evidence to investigate, not automatically a defect; a suppressed diagnostic is not automatically harmless.
- Static checks are sound only for the properties and code paths they model. Know whether the tool is advisory, unsound, incomplete, path-sensitive, or affected by configuration.
- Prefer fixing the underlying issue or narrowing the tool scope over broad suppression, disabling rules, or weakening types.
- Type correctness does not establish runtime validation, authorization, resource safety, semantic correctness, or compatibility.

## Procedure

1. Record the baseline tool, version, configuration, targets, and diagnostics. Distinguish new findings from existing debt, generated code, and environment noise.
2. Classify each finding: real defect, potential defect, contract mismatch, false positive, unsupported pattern, duplicate signal, or unknown. Trace it to the relevant code and intended behavior.
3. Reproduce or inspect the behavior at the boundary. Check callers, types, validation, control flow, data flow, generated artifacts, and runtime assumptions that the analyzer may not see.
4. Decide the smallest response: fix the code, improve the type/contract, refine the analyzer configuration, isolate generated code, document a justified local suppression, or escalate unresolved uncertainty.
5. Make suppressions narrow, explicit, justified, attributable, and reviewable. Include an expiry or recheck condition where the repository supports it; never suppress an entire class merely to obtain a green report.
6. Check analyzer interactions: inconsistent nullability, unsafe casts, stale generated types, rule conflicts, configuration precedence, dependency versions, and CI/local drift.
7. Run static checks on changed and affected code, then run relevant runtime tests and boundary checks. Inspect both new diagnostics and diagnostics that disappeared unexpectedly.
8. Seek disconfirming evidence with negative cases, alternate configurations, type-invalid inputs, generated/runtime paths, and a second analyzer or manual review where risk warrants it.
9. Report findings, tool/version/configuration, limits, suppressions, residual uncertainty, and the condition that should trigger reanalysis.

## Examples and counterexamples

Good: A nullability warning leads to a contract decision, runtime boundary validation, a focused fix, and a test for the missing-value path.

Bad: Add a non-null assertion or disable null checks because the local input “should always exist.”

Good: A generated file produces repetitive warnings; exclude only the generated boundary, keep analysis on the generator and consumers, and document regeneration behavior.

Bad: Disable the analyzer for the whole repository because generated code is noisy.

Good: A security analyzer flags a possible injection; inspect data flow and validation, then route confirmed risk to secure-coding review.

Bad: Mark the finding false positive because ordinary tests happen to pass.

## Failure modes and recovery

If the tool’s semantics or configuration are unknown, establish them before relying on the report. If a diagnostic cannot be classified, preserve it as unresolved and seek a reproduction or specialist review. If a suppression is necessary, narrow and document it rather than weakening global policy. If the analyzer is too noisy or expensive, tune scope and rules using measured false-positive and missed-risk evidence; do not optimize the metric by hiding findings.

## Validation evidence and provenance

- The governing research emphasizes verification over assertion, explicit uncertainty, adversarial testing, source independence, simplicity, and tradeoffs over dogma.
- Static-analysis results are observations conditioned on tool/version/configuration and modeled properties; explanations are hypotheses; fixes or suppressions are recommendations until runtime and boundary evidence support them.
- Trace analyzer rules and language semantics to primary documentation and distinguish independent findings from multiple tools sharing the same model or source.
- Confidence: high for treating diagnostics as bounded evidence and suppressions as risk decisions; medium for any particular tool’s coverage until its configuration and blind spots are known.
- Freshness: review when language/runtime versions, analyzer rules, generated code, type contracts, repository policy, or CI configuration changes.

## Related skills and conflicts

Related: `regression-test-design`, `test-effectiveness-analysis`, `secure-coding-review`, `requirements-to-acceptance`, `behavior-preserving-refactoring`, `build-and-ci-integrity`, and `repository-change-verification`. This skill does not authorize disabling checks, hiding warnings, or treating type/static correctness as proof of runtime or security correctness.
