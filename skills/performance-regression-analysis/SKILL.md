---
name: performance-regression-analysis
description: Investigate and validate software performance changes using representative workloads, baselines, variance-aware measurements, and resource tradeoffs. Use when an AI coding agent is asked to make code faster, reduce latency or cost, increase throughput, or diagnose a performance regression.
---

Lifecycle: `draft`

# Performance Regression Analysis

## Purpose and scope

Determine whether a change materially improves the performance property that matters without trading away correctness, safety, reliability, or maintainability unintentionally. This skill covers measurement and decision-making; it does not replace capacity planning, production incident response, or domain-specific performance modeling.

## Triggers and prerequisites

Trigger when a task says faster, lower latency, higher throughput, cheaper, more efficient, less memory, or when a performance regression is suspected. Prerequisites: a defined workload, target metric and percentile, baseline revision or measurement, environment, resource constraints, correctness criteria, and an acceptable measurement method.

## Decision criteria

- Performance is a property of a workload and environment, not an intrinsic label on an implementation.
- Define the metric, unit, percentile or distribution, steady-state/warm-up behavior, sample size, and practical significance before comparing results.
- A speedup is not an improvement if it changes semantics, increases error rate, worsens tail latency, exhausts resources, weakens security, or shifts cost elsewhere.
- Prefer a measured bottleneck and reversible change over optimization by convention or intuition.

## Procedure

1. Translate the request into a measurable target: workload, operation, metric, threshold, percentile, resource budget, and correctness constraints. Identify what must not regress.
2. Establish a baseline at a known revision. Use representative inputs, realistic data size and distribution, stable environment, warm-up policy, and enough repetitions to characterize variance.
3. Form hypotheses about the bottleneck from profiling, traces, resource measurements, or algorithmic analysis. Separate measured observations from guesses and identify at least one alternative explanation.
4. Design the smallest experiment that distinguishes the hypotheses. Change one material variable where practical, isolate confounders, and avoid benchmarking a synthetic path that does not represent the claim.
5. Implement the narrowest optimization. Preserve output, error, ordering, authorization, durability, concurrency, and resource-safety behavior; keep unrelated refactors separate.
6. Measure baseline and candidate under the same protocol. Report distributions and variance, not only a favorable run or average. Check CPU, memory, I/O, network, allocations, energy, cost, and error rate when relevant.
7. Validate boundary workloads: empty and large inputs, cache hit/miss, cold/warm state, concurrency, contention, timeouts, partial failure, and adversarial or worst-case inputs as applicable.
8. Investigate any tradeoff or unexplained difference. Reject benchmark gaming, input-specific wins presented as general improvement, and changes whose practical significance is smaller than measurement noise.
9. Record workload, environment, revisions, commands or tooling, raw/summary results, limitations, decision, rollback path, and the trigger for remeasurement. Add a durable benchmark or regression guard only when its maintenance cost is justified.

## Examples and counterexamples

Good: A query optimization is evaluated on representative data with cold and warm caches, p50 and p99 latency, error rate, memory, and result equivalence before acceptance.

Bad: Report one local happy-path timing as proof that the query is faster in production.

Good: A cache reduces average latency but increases stale-data risk; the decision records the freshness boundary and rejects the change where that tradeoff is unacceptable.

Bad: Optimize a loop until a microbenchmark improves while ignoring increased memory use, tail latency, or the real workload.

## Failure modes and recovery

If no representative workload or baseline exists, narrow the claim and build measurement first; do not invent a win. If results vary materially, investigate environment, warm-up, contention, randomness, and workload distribution before selecting a favorable sample. If profiling is inconclusive, preserve uncertainty and test competing hypotheses. If a performance change alters correctness or safety, treat it as a separate behavioral change and route it through the appropriate review skills.

## Validation evidence and provenance

- The governing research requires empirical validation, benchmarking, substantive progress measures, boundary analysis, and tradeoffs over dogma.
- Benchmark results are observations conditioned on workload and environment; they do not prove universal performance or correctness.
- [Google SRE: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/): explains why latency distributions and high percentiles can reveal regressions hidden by averages.
- Treat repeated benchmark claims as one line of evidence when they share the same workload, implementation, environment, or source; seek an independent workload or measurement method before generalizing.
- Confidence: high for baseline/measurement discipline; medium for optimization choices until profiling and representative results support them.
- Freshness: review when workload distribution, hardware, runtime, dependencies, architecture, or performance targets change.

For material conclusions, seek disconfirming evidence, distinguish observations from hypotheses and recommendations, record tradeoffs and uncertainty, and note confidence, freshness, and source independence.

## Related skills and conflicts

Related: `evidence-driven-debugging`, `observability-and-instrumentation`, `behavior-preserving-refactoring`, `differential-patch-review`, `regression-test-design`, `secure-coding-review`, and `repository-change-verification`. This skill does not authorize weakening correctness, security, or reliability to obtain a benchmark improvement.
