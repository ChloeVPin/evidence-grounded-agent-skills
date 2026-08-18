---
name: resilience-and-retry-design
description: Design and review timeouts, retries, backoff, circuit breakers, rate limits, bulkheads, and graceful degradation for unreliable dependencies. Use when an AI coding agent changes network calls, queues, workers, caches, or failure handling.
---

Lifecycle: `draft`

# Resilience and Retry Design

## Purpose and scope

Keep failures bounded and recoverable without hiding outages, duplicating effects, or amplifying load. This skill covers dependency interaction and graceful degradation; it does not replace service-specific SLOs, incident response, concurrency review, or capacity planning.

## Triggers and prerequisites

Trigger when adding or changing retries, timeouts, polling, backoff, circuit breakers, rate limits, queue handling, fallbacks, cache behavior, or dependency failure paths. Prerequisites: dependency contract, operation idempotence, latency/error distribution, load limits, caller and downstream budgets, user-visible consequences, and recovery/observability capabilities.

## Decision criteria

- A timeout bounds waiting; it does not cancel work or undo a side effect unless the dependency guarantees that behavior.
- Retry only failures that are transient and safe to repeat or have an idempotency mechanism. Backoff and jitter must respect the total deadline and downstream capacity.
- A fallback is correct only when its stale, partial, degraded, or unsafe semantics are explicit and acceptable.
- Resilience controls must fail predictably under overload; adding retries without a budget can turn one failure into a larger outage.

## Procedure

1. Map the call chain, dependency ownership, operation side effects, concurrency, queues, caches, deadlines, and user-visible failure behavior. Identify retry multiplication across layers.
2. Classify outcomes: success, permanent failure, transient failure, timeout/unknown outcome, overload, cancellation, partial response, and dependency recovery. Define which are retryable and why.
3. Set an end-to-end deadline and budget across callers, retries, backoff, connection, and downstream work. Do not let nested defaults exceed the user or system budget.
4. Make repeated operations safe through idempotency keys, deduplication, transactions, conditional writes, or an explicit non-retry policy. Define what happens when the outcome is unknown after a timeout.
5. Choose backoff, jitter, retry count, circuit behavior, rate limits, bulkheads, queue limits, and fallback semantics from observed latency, error, and capacity evidence—not folklore.
6. Preserve meaningful errors and cancellation. Avoid retrying validation, authorization, deterministic failures, or caller cancellation; avoid fallback data that violates freshness, privacy, or correctness requirements.
7. Instrument attempts, reasons, delays, outcomes, deadlines, saturation, queue age, circuit state, and fallback use without logging secrets or creating unbounded metrics.
8. Test transient/permanent failures, timeouts, slow responses, duplicate delivery, partial side effects, cancellation, overload, recovery, retry storms, concurrent callers, and exhausted budgets.
9. Compare load and dependency impact before and after the change. Verify that the system recovers without exceeding downstream limits and that users receive an honest result.
10. Record assumptions, retry/fallback contract, budgets, evidence, residual risk, runbook/recovery action, owner, and review trigger.

## Examples and counterexamples

Good: A read-only request retries a bounded set of transient transport failures with exponential backoff and jitter, respects an overall deadline, and exposes exhaustion distinctly from an empty result.

Bad: Retry every exception three times, including authorization failures and user cancellation.

Good: A payment operation uses an idempotency key and reconciliation path because a timeout leaves the remote outcome unknown.

Bad: Retry a timed-out charge blindly and risk double payment.

Good: A stale-cache fallback states its freshness limit, records fallback use, and is disabled for operations requiring current authorization or data.

Bad: Return cached sensitive data indefinitely because the dependency is unavailable.

## Failure modes and recovery

If idempotence or timeout semantics are unknown, do not add retries; resolve the dependency contract or use a non-retry path. If retry amplification or overload appears, stop retries, shed load, protect the dependency, and follow incident procedures. If a fallback may violate correctness, privacy, or authorization, fail safely and escalate. If a circuit or queue remains open, preserve evidence and define recovery rather than adding unlimited retries.

## Validation evidence and provenance

- The governing research emphasizes failure recovery, empirical failure analysis, unknown-unknown detection, simplicity, tradeoffs, and reversible decisions.
- Reliability behavior is workload- and dependency-specific: observed latency, errors, capacity, and side effects are evidence; retry or fallback choices are hypotheses and recommendations until tested.
- Trace dependency behavior to authoritative contracts and independent operational evidence; repeated retry recipes are not independent proof of safety.
- Confidence: high for bounded budgets, idempotence, explicit failure classes, and overload protection; medium for parameter values and fallback semantics until measured in the target system.
- Freshness: review when dependency contracts, load, latency/error distributions, queueing, user impact, or failure modes change.

## Related skills and conflicts

Related: `concurrency-and-shared-state`, `evidence-driven-debugging`, `observability-and-instrumentation`, `performance-regression-analysis`, `api-contract-compatibility`, `secure-coding-review`, `release-and-rollback-safety`, and `repository-change-verification`. This skill does not authorize infinite retries, hiding failures, duplicating side effects, or weakening correctness for apparent availability.
