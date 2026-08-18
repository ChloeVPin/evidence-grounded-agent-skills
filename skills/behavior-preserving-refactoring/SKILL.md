---
name: behavior-preserving-refactoring
description: Restructure code without changing its observable contract. Use when an AI coding agent extracts modules, renames interfaces, reduces duplication, changes control flow, or modernizes implementation while behavior should remain stable.
---

Lifecycle: `draft`

# Behavior-Preserving Refactoring

## Purpose and scope

Improve structure, readability, maintainability, or local performance while preserving the agreed observable behavior. This skill covers incremental refactoring and compatibility review; it does not authorize changing requirements, fixing unrelated bugs, or hiding a behavior change behind the word “refactor.”

## Triggers and prerequisites

Trigger when a change is described as a refactor, cleanup, modernization, extraction, deduplication, rename, or internal optimization. Prerequisites: the baseline revision, a clear preservation contract, callers and dependents, relevant tests or reproductions, and any public, persistence, serialization, or operational interfaces.

## Decision criteria

- “Same behavior” includes successful outputs, errors, side effects, ordering, timing constraints, permissions, resource use, persistence, and compatibility where those are part of the contract.
- A refactor should reduce a named complexity or maintenance risk; changed behavior must be treated as a separate feature or bug fix.
- Small, independently reversible steps provide stronger evidence than one broad rewrite.
- Textual similarity, passing narrow tests, or a cleaner design is not proof of behavioral equivalence.

## Procedure

1. State the structural problem and the behavior that must not change. Identify explicitly allowed behavior changes, if any, and keep them separate from the refactor.
2. Map the affected callers, public interfaces, data formats, persistence boundaries, configuration, concurrency, error paths, and side effects. Find hidden consumers before moving or renaming code.
3. Establish a baseline: run relevant tests or reproductions, inspect representative outputs and errors, and record known limitations. Add a characterization test when the intended behavior is undocumented but must be preserved.
4. Choose one small transformation with a clear invariant: extract, rename, introduce an adapter, simplify control flow, or replace an implementation behind the same interface.
5. Apply the transformation without mixing formatting churn, dependency upgrades, feature work, or opportunistic bug fixes. Keep the diff reviewable and reversible.
6. Verify the invariant at the interface boundary: inputs, outputs, errors, side effects, state transitions, permissions, ordering, and relevant performance or resource limits. Use differential checks when a baseline can run.
7. Probe boundaries and failure paths near the changed code. Check alternate callers, null or empty values, retries, concurrency, cleanup, serialization, and configuration variants that the contract makes relevant.
8. Inspect the diff for accidental API changes, weakened validation, lost observability, changed exception semantics, altered initialization order, or new coupling. If behavior differs, classify it as intentional, tolerated, unexplained, or incorrect.
9. Keep the refactor only when the structural objective and preservation evidence both hold. Revert or split the change when the cause of a difference is not understood.
10. Record what improved, what was compared, what was not observable, residual uncertainty, and the condition that should trigger revalidation.

## Examples and counterexamples

Good: Extract a parser behind the same interface, run characterization and boundary tests, compare errors and serialized output, and preserve the old adapter until callers migrate.

Bad: Rewrite the parser and update snapshots until they pass. Changed snapshots may conceal a compatibility regression.

Good: Rename an internal function after searching all callers, generated references, reflection/configuration paths, and documentation that acts as an interface.

Bad: Rename a symbol because the compiler is clean while ignoring dynamic lookup or external consumers.

Good: Split a large change into extraction, verification, then a separately justified optimization.

Bad: Combine a refactor with a dependency upgrade and a behavior fix, making failures impossible to attribute.

## Failure modes and recovery

If the preservation contract is unclear, use `requirements-to-acceptance` or ask before editing. If baseline behavior cannot be observed, narrow the claim and add characterization or instrumentation first. If a difference appears, stop broadening the refactor; reproduce it, classify it, and either restore behavior or record a separately reviewed change. If rollback is difficult, reduce the step size before proceeding.

## Validation evidence and provenance

- The governing research prioritizes simplicity, reversibility, composability, explicit tradeoffs, adversarial review, regression analysis, and evidence over convention.
- Differential comparison and characterization testing are used as evidence of preserved behavior, with explicit limits for unobservable or environment-dependent behavior.
- Label measured behavior as observations, causal explanations as hypotheses, and proposed transformations as recommendations; do not present one as another.
- Confidence: high for incremental, boundary-based refactoring practice; medium for equivalence claims when coverage, consumers, or runtime environments are incomplete.
- Freshness: review when interfaces, architecture, test strategy, or compatibility policy changes.

## Related skills and conflicts

Related: `repository-change-verification`, `differential-patch-review`, `requirements-to-acceptance`, `regression-test-design`, `evidence-driven-debugging`, and `knowledge-maintenance`. This skill does not authorize breaking public behavior, deleting compatibility paths, or treating a refactor label as permission to skip review.
