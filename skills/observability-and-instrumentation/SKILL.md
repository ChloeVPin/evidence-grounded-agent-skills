---
name: observability-and-instrumentation
description: Add or review logs, metrics, traces, and diagnostic signals so AI coding agents can understand real behavior and failures without excessive cost, noise, or data exposure. Use when changing production behavior, debugging intermittent issues, or operating asynchronous and distributed code.
---

Lifecycle: `draft`

# Observability and Instrumentation

## Purpose and scope

Make important behavior measurable and diagnosable through appropriate signals. This skill covers instrumentation design, signal quality, privacy, cost, and operational use; it does not replace incident response, service-level objective design, or security review.

## Triggers and prerequisites

Trigger when failures are difficult to reproduce, behavior crosses process or queue boundaries, a change affects latency or reliability, an asynchronous path lacks visibility, or logs/metrics/traces cannot answer an operational question. Prerequisites: the behavior to observe, users or operators who need the signal, deployment topology, data sensitivity, existing telemetry conventions, and relevant performance budget.

## Decision criteria

- Start with a question the signal must answer; do not instrument merely because data might be interesting to collect.
- Logs describe discrete events, metrics summarize comparable measurements, and traces connect work across boundaries; choose the least expensive signal that answers the question.
- A signal is decision-relevant only when it has sufficient context, stable semantics, actionable thresholds, and a known owner or response.
- Diagnostic value must be balanced against privacy, cardinality, storage, latency, cost, and attack surface.

## Procedure

1. State the operational question and failure hypothesis: what must an operator distinguish, at which boundary, and within what time?
2. Map the request or job path, state transitions, retries, queues, dependencies, and failure exits. Identify correlation identifiers and the boundary where each signal should be emitted.
3. Select signals: structured logs for event details, counters and gauges for rates or state, histograms for distributions, and traces for causal timing across components. Define names, units, labels, sampling, retention, and severity.
4. Record enough context to diagnose the question: operation, outcome, version, dependency, bounded identifiers, and relevant timing. Never emit secrets, raw credentials, unnecessary personal data, or unbounded user-controlled labels.
5. Define normal and abnormal behavior, alert or dashboard interpretation, and the action a signal should prompt. Avoid alerts with no owner or response.
6. Implement instrumentation at stable boundaries and failure paths, including retries, timeouts, cancellations, partial results, and queue loss. Preserve correct success/error semantics and avoid changing business behavior unintentionally.
7. Validate signal correctness with representative success, failure, retry, timeout, concurrency, and sampling cases. Check cardinality, overhead, redaction, clock behavior, and correlation across components.
8. Review for blind spots and misleading signals: swallowed errors, duplicated retries, dropped spans, aggregate averages hiding tails, logs emitted after failure, or labels that change meaning across versions.
9. Document the signal contract, ownership, retention, privacy assumptions, cost limits, and deprecation path. Revisit it when topology, data policy, or the failure mode changes.

## Examples and counterexamples

Good: For an intermittent queue timeout, record queue age, attempt number, timeout outcome, bounded job type, and trace correlation; measure latency distribution rather than only average latency.

Bad: Log the entire request, including credentials and personal data, whenever a timeout occurs.

Good: A metric label uses a bounded route template such as `/users/:id` and separates status class from raw user input.

Bad: Use the raw URL, exception text, or user identifier as a metric label and create an unbounded-cardinality metric.

## Failure modes and recovery

If no operational question exists, do not add speculative telemetry. If signals are too noisy or expensive, reduce cardinality, sampling, volume, or retention while preserving the diagnostic question. If sensitive data has been emitted, follow incident and credential/data-handling procedures rather than merely masking future events. If telemetry changes behavior or timing, isolate the cause and revise the instrumentation boundary.

## Validation evidence and provenance

- The governing research emphasizes anomaly detection, unknown-unknown discovery, empirical failure analysis, SRE-inspired incident learning, and maintenance based on real-world change.
- [OpenTelemetry documentation](https://opentelemetry.io/docs/concepts/observability-primer/): logs, metrics, and traces as complementary signals for understanding system behavior.
- [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/concepts/semantic-conventions/): stable names and attributes improve interoperability and analysis.
- [Google SRE book: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/): monitoring should support actionable operational questions and distinguish signal from noise.
- Check whether telemetry conventions and observed signals are independently supported; multiple dashboards built from one instrument are not independent evidence.
- Confidence: high for the question-first and signal-boundary principles; medium for thresholds, sampling, retention, and ownership because they depend on system risk and operations.
- Freshness: review when telemetry standards, topology, privacy policy, cost limits, or operational failure modes change.

For material conclusions, seek disconfirming evidence, distinguish observations from hypotheses and recommendations, record tradeoffs and uncertainty, and note confidence, freshness, and source independence.

## Related skills and conflicts

Related: `evidence-driven-debugging`, `secure-coding-review`, `requirements-to-acceptance`, `knowledge-maintenance`, `dependency-security-audit`, and `repository-change-verification`. This skill does not authorize logging sensitive data, treating telemetry as proof of correctness, or adding alerts without an actionable response.
