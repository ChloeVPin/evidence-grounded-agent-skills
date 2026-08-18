---
name: implementation-planning
description: Turn verified coding requirements into a minimal, dependency-aware implementation plan with risks, verification evidence, and stopping conditions. Use before multi-file, cross-boundary, risky, or ambiguous AI coding-agent changes.
---

Lifecycle: `draft`

# Implementation Planning

## Purpose and scope

Choose an efficient, bounded path from acceptance criteria to a verified repository change. This skill covers decomposition, sequencing, risk, and handoffs; it does not authorize work beyond the request, replace technical design, or make an uncertain requirement disappear through planning language.

## Triggers and prerequisites

Trigger when a task spans multiple files or components, has dependencies or migrations, carries security/data/release risk, or has more than one plausible implementation path. Prerequisites: stable or explicitly provisional acceptance criteria, repository model, constraints, baseline, available verification, and required approvals.

## Decision criteria

- Every step must serve an acceptance criterion or reduce a stated uncertainty; activity is not progress.
- Sequence discovery and reversible experiments before expensive or irreversible changes.
- Prefer the smallest plan that covers dependencies, failure paths, verification, and recovery; do not plan speculative extensibility.
- A plan is a hypothesis about the path, not evidence that the change will work. Revise it when observations contradict its assumptions.

## Procedure

1. Restate the outcome, constraints, non-goals, assumptions, and evidence required for success. Resolve material ambiguity with `requirements-to-acceptance` first.
2. Map the change surface: files, callers, interfaces, data, dependencies, workflows, permissions, generated artifacts, and owners. Identify coupling and ordering constraints.
3. Break the work into small steps with one purpose each. Mark each step as discovery, implementation, migration, verification, review, or cleanup; define its output and completion evidence.
4. Identify risks and disconfirming observations for each step: hidden consumers, incompatible versions, data loss, security exposure, performance change, concurrency, irreversibility, or unavailable verification.
5. Choose the sequence: baseline/reproduction, smallest safe change, focused verification, boundary checks, broader verification, review, and cleanup. Put approval gates before high-impact actions.
6. Define alternatives and decision points. State when to stop, ask, revert, split the work, or route to another skill rather than continuing a failing plan.
7. Implement only the current step, inspect the result, and update the plan from evidence. Do not pre-commit to later steps that the new evidence invalidates.
8. At completion, compare the final diff with the plan and acceptance criteria. Record skipped steps, changed assumptions, residual uncertainty, and the next review trigger.

## Examples and counterexamples

Good: For an API change with a schema migration, plan contract clarification, consumer inventory, compatible schema expansion, application change, backfill verification, rollout, and cleanup with separate evidence for each.

Bad: Plan “update API, migrate database, update tests, deploy” without ordering, compatibility, rollback, consumer, or failure criteria.

Good: If the first experiment shows the issue is dependency behavior, stop the application-code plan and route to dependency review.

Bad: Continue implementing the original plan because changing direction would make the task look incomplete.

## Failure modes and recovery

If acceptance criteria are unstable, pause planning and clarify them. If dependencies or callers are unknown, add bounded discovery rather than guessing. If a step cannot be verified, narrow its claim or obtain the required environment/approval. If the plan grows with speculative branches, return to the stated outcome and remove steps that do not reduce a demonstrated risk or satisfy a criterion.

## Validation evidence and provenance

- The governing research emphasizes reconnaissance, prioritization, simplicity, reversibility, explicit dependencies, falsifiable questions, and meaningful progress over busyness.
- [Google SRE: Release Engineering](https://sre.google/sre-book/release-engineering/): repeatable, automated, and staged delivery practices reduce release risk while preserving evidence about what changed.
- Plan observations are repository or experiment evidence; causal explanations are hypotheses; sequencing and implementation choices are recommendations that must be revised when evidence changes.
- Trace dependency and architecture claims to their originating code, specifications, or owners; repeated planning assumptions are not independent confirmation.
- Confidence: high for bounded decomposition and evidence-driven sequencing; medium for a plan’s predicted effort and risk until discovery and experiments run.
- Freshness: replan when requirements, repository structure, dependencies, risk, environment, or verification results change.

For material conclusions, seek disconfirming evidence, distinguish observations from hypotheses and recommendations, record tradeoffs and uncertainty, and note confidence, freshness, and source independence.

## Related skills and conflicts

Related: `requirements-to-acceptance`, `repository-exploration`, `skill-composition-and-routing`, `epistemic-coding`, `repository-change-verification`, `safe-git-workflow`, and `skill-quality-review`. This skill does not authorize scope expansion, irreversible actions without approval, or claiming completion because a plan was written.
