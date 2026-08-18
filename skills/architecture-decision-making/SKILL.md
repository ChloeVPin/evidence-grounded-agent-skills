---
name: architecture-decision-making
description: Evaluate and record software architecture choices using constraints, alternatives, evidence, decision boundaries, and reversible consequences. Use when an AI coding agent changes system boundaries, data ownership, integration patterns, concurrency models, or long-term structure.
---

Lifecycle: `draft`

# Architecture Decision-Making

## Purpose and scope

Choose a system structure that fits current constraints while making tradeoffs and future change explicit. This skill covers architecture reasoning and decision records; it does not replace requirements ownership, threat modeling, formal design review, or domain-specialist approval for critical systems.

## Triggers and prerequisites

Trigger when a change introduces or removes a service/module boundary, changes data ownership, selects an integration or storage pattern, changes deployment topology, or creates a long-lived dependency or operational obligation. Prerequisites: desired outcomes, quality attributes, constraints, current architecture, owners, workloads, failure model, security/data requirements, and alternatives worth considering.

## Decision criteria

- Architecture is a set of observable consequences and constraints, not a diagram or fashionable pattern.
- Compare alternatives against the same criteria: correctness, security, privacy, performance, reliability, operability, cost, complexity, team capability, and reversibility.
- Separate constraints from preferences and evidence from assumptions. A local optimization must not silently weaken protected principles.
- Prefer the simplest design that satisfies demonstrated requirements; preserve an escape route when uncertainty is high.

## Procedure

1. State the problem, desired outcome, scope, non-goals, stakeholders, quality attributes, constraints, and decision deadline. Identify which claims require evidence.
2. Map the current system: boundaries, data/control flow, owners, dependencies, interfaces, state, failure paths, deployment, and operational responsibilities. Confirm the model with code and runtime evidence where possible.
3. Generate at least two plausible alternatives, including keeping the current design when appropriate. Describe each alternative’s assumptions, consequences, and migration path.
4. Define decision criteria and weights only when justified. Consider normal, boundary, failure, scale, security, privacy, maintenance, and organizational scenarios rather than only the happy path.
5. Trace evidence to primary specifications, measurements, existing constraints, incidents, and independent implementations. Ask what evidence would make the leading choice wrong.
6. Identify irreversible commitments, coupling, lock-in, data migration, operational burden, blast radius, and exit strategy. Prefer a reversible experiment or staged seam when evidence is insufficient.
7. Choose or defer the decision. Record the chosen boundary, rejected alternatives and reasons, assumptions, tradeoffs, confidence, consequences, and triggers for revisiting it.
8. Translate the decision into acceptance criteria, ownership, interfaces, migration steps, observability, security controls, and verification evidence. Route implementation to the relevant task skills.
9. Re-evaluate after implementation or new evidence. If the observed system contradicts the decision, preserve the record and revise or supersede it rather than silently changing the rationale.

## Examples and counterexamples

Good: Compare an in-process queue, a durable broker, and the current synchronous path against delivery guarantees, failure recovery, throughput, operations, cost, and migration before selecting one.

Bad: Choose a broker because distributed systems are “more scalable” without defining workload, delivery semantics, or operational capacity.

Good: Record that a temporary adapter preserves compatibility while evidence is gathered, plus the condition and date for removing it.

Bad: Introduce an abstraction layer “for future flexibility” without a current problem, owner, or removal boundary.

## Failure modes and recovery

If requirements or quality attributes conflict, use `requirements-to-acceptance` or ask the owner; do not hide the conflict in a weighted score. If the current architecture cannot be mapped confidently, investigate before proposing a replacement. If evidence is insufficient, choose a reversible experiment or defer rather than pretending certainty. If a decision causes unexpected coupling or failure, contain impact, preserve the original rationale, and create a superseding decision with the new evidence.

## Validation evidence and provenance

- The governing research emphasizes dynamic ontologies, dependency graphs, tradeoffs over dogma, simplicity, reversibility, adversarial review, and explicit methodological change.
- Architecture observations should cite code, interfaces, measurements, or operational evidence; design explanations are hypotheses; the selected structure is a recommendation with stated tradeoffs.
- Trace repeated pattern claims to their originating specification, measurement, or implementation; popularity and copied architecture diagrams are not independent evidence.
- Confidence: medium-high for explicit alternatives, criteria, tradeoffs, and reversible seams; medium for predicted long-term outcomes until the design is exercised in the target workload and organization.
- Freshness: review when requirements, workload, ownership, dependencies, deployment, failure model, or quality targets change.

For material conclusions, seek disconfirming evidence, distinguish observations from hypotheses and recommendations, record tradeoffs and uncertainty, and note confidence, freshness, and source independence.

## Related skills and conflicts

Related: `requirements-to-acceptance`, `repository-exploration`, `implementation-planning`, `api-contract-compatibility`, `concurrency-and-shared-state`, `data-migration-safety`, `performance-regression-analysis`, `secure-coding-review`, and `skill-quality-review`. This skill does not authorize architecture changes without owner approval, confuse a pattern with evidence, or preserve a failed decision for consistency’s sake.
