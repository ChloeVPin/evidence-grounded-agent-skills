---
name: concurrency-and-shared-state
description: Design, debug, or review concurrent and asynchronous code for race freedom, state invariants, ordering, cancellation, resource ownership, and failure recovery. Use when an AI coding agent changes threads, tasks, queues, locks, caches, events, retries, or shared mutable state.
---

Lifecycle: `draft`

# Concurrency and Shared State

## Purpose and scope

Make concurrent behavior correct, bounded, and diagnosable under interleaving, failure, cancellation, and load. This skill covers reasoning and review of asynchronous, parallel, and distributed state; it does not replace language-specific memory-model expertise, formal verification, or production incident response.

## Triggers and prerequisites

Trigger when changing threads, async tasks, workers, locks, atomics, queues, caches, transactions, event handlers, retries, cancellation, timeouts, or any state accessed by more than one execution context. Prerequisites: state ownership, invariants, lifecycle, ordering requirements, memory/transaction model, failure semantics, and representative workload or schedule.

## Decision criteria

- Every shared state has an owner, synchronization rule, consistency requirement, and lifecycle; “probably serialized” is not a rule.
- Correctness must hold across allowed interleavings, not only the observed schedule.
- Locking, queues, actors, immutability, transactions, idempotence, and coordination are alternatives with different liveness, throughput, and failure tradeoffs.
- A fix that removes one race but introduces deadlock, starvation, unbounded backlog, duplicate side effects, lost cancellation, or data corruption is not a fix.

## Procedure

1. State the safety and liveness properties: invariants, permitted orderings, at-most/at-least/exactly-once expectations, progress, cancellation, deadlines, and recovery behavior.
2. Map actors, shared resources, ownership transfers, reads/writes, queues, locks, transactions, external effects, and shutdown paths. Identify the concurrency and memory/transaction model actually in use.
3. Choose the simplest ownership and synchronization design that enforces the invariants. Prefer immutable or isolated state; make lock order, transaction boundaries, queue limits, and cancellation propagation explicit.
4. Enumerate adversarial schedules and failures: simultaneous reads/writes, reorderings, duplicate delivery, delayed consumers, partial completion, timeout during a side effect, worker crash, retry, shutdown, and resource exhaustion.
5. Design focused tests or model checks that force relevant interleavings and assert observable outcomes, not merely absence of an exception. Use race/deadlock detectors, stress runs, deterministic schedulers, or formal methods when appropriate and record their limits.
6. Check liveness and capacity: lock contention, starvation, deadlock cycles, queue/backpressure behavior, retry amplification, cancellation leaks, cleanup, and bounded memory or connection use.
7. Verify external side effects are coordinated or idempotent. Define reconciliation for partial failure and make ownership of recovery explicit.
8. Inspect the diff for widened critical sections, inconsistent lock order, unsynchronized access, blocking in async contexts, lost errors, unbounded concurrency, and changes to shutdown or timeout semantics.
9. Run baseline and changed behavior under representative and adversarial schedules. Record environment, workload, detector coverage, surviving uncertainty, and the condition that should trigger another review.

## Examples and counterexamples

Good: A worker queue has a bounded capacity, explicit ownership of messages, cancellation propagation, retry/idempotence rules, and tests for duplicate delivery and shutdown while work is in flight.

Bad: Add a mutex around one write while leaving related reads, cache invalidation, and external side effects outside the same consistency rule.

Good: A shared counter’s invariant and atomicity requirement are stated, then verified under concurrent updates and failure recovery.

Bad: Run a stress test once without controlling schedules and conclude that no race exists because it did not reproduce.

## Failure modes and recovery

If the memory or transaction model is unknown, stop and resolve it before reasoning about safety. If a failure is schedule-dependent, preserve the schedule or add deterministic instrumentation rather than adding sleeps or retries. If deadlock, data loss, or duplicate external effects are possible, contain exposure and follow incident/recovery procedures. If correctness depends on an unverified timing assumption, narrow the claim and redesign around explicit coordination.

## Validation evidence and provenance

- The governing research identifies concurrency and correctness-critical systems as candidates for empirical and formal validation, adversarial testing, and explicit failure recovery.
- Concurrent correctness is a property of allowed interleavings and the language/runtime model; a passing sequential test is insufficient evidence.
- Check whether concurrency guidance and observed failures come from independent models or merely repeat one assumption; distinguish a source specification from an implementation-specific observation.
- Confidence: medium-high for ownership, invariant, interleaving, liveness, and idempotence principles; medium for any implementation strategy until its model and schedules are tested.
- Freshness: review when language/runtime memory semantics, workload, synchronization primitives, failure model, or external side effects change.

For material conclusions, seek disconfirming evidence, distinguish observations from hypotheses and recommendations, record tradeoffs and uncertainty, and note confidence, freshness, and source independence.

## Related skills and conflicts

Related: `evidence-driven-debugging`, `regression-test-design`, `test-effectiveness-analysis`, `performance-regression-analysis`, `observability-and-instrumentation`, `secure-coding-review`, `data-migration-safety`, and `repository-change-verification`. This skill does not authorize weakening synchronization, hiding races with sleeps, or claiming concurrency safety from a single stress run.
