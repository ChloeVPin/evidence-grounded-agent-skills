---
name: skill-quality-review
description: Review a proposed or existing SKILL.md before publication for practical scope, precise triggers, evidence quality, counterexamples, safety, overlap, composability, and honest lifecycle status. Use when creating, revising, promoting, deprecating, or merging agent skills.
---

Lifecycle: `draft`

# Skill Quality Review

## Purpose and scope

Decide whether a skill materially improves an AI coding-agent library and whether its claims and instructions are supported well enough for their stated lifecycle. This skill reviews skill content and interoperability; it does not prove that every downstream implementation or agent outcome will be correct.

## Triggers and prerequisites

Trigger before publishing a new skill, promoting its lifecycle, revising a trusted skill, merging overlapping guidance, or deprecating a skill. Prerequisites: the candidate `SKILL.md`, existing skill index, intended users and tasks, research sources, known alternatives, and the evidence or examples used to support its procedure.

## Decision criteria

- The skill must solve a concrete, recurring coding-agent problem with a scope narrow enough to apply reliably.
- Its trigger must distinguish when it applies from neighboring skills; its procedure must be actionable without hiding important decisions.
- Claims, confidence, and lifecycle must not exceed the evidence. A polished document is not validation.
- A skill should add depth, coverage, or a safer composition—not merely rename existing guidance or increase file count.

## Procedure

1. Identify the task, user benefit, failure mode, and expected output. State why an existing skill cannot cover it without unacceptable ambiguity or overload.
2. Inspect frontmatter name/description, purpose, triggers, prerequisites, decision criteria, procedure, examples, counterexamples, failure recovery, provenance, confidence, freshness, lifecycle, related skills, and conflicts. Confirm the name matches its directory, the file is a standalone `SKILL.md`, and no application code, runtime, test suite, or audit machinery is bundled.
3. Test trigger precision with positive, negative, and neighboring-task examples. Check whether an agent could know when to activate, defer, or stop the skill.
4. Trace material claims to authoritative sources, experiments, or observed failures. Check source independence, publication/version context, assumptions, and whether recommendations are being presented as facts.
5. Seek disconfirming evidence: strongest counterargument, plausible misuse, boundary input, conflicting guidance, outdated source, hidden consumer, and scenario where the procedure creates harm or busywork.
6. Inspect the procedure for missing decision boundaries, permissions, side effects, failure recovery, uncertainty, and verification evidence. Check that examples demonstrate behavior rather than slogans.
7. Compare the candidate with existing skills. Classify the relationship as complementary, composable, overlapping, contradictory, or replacement; define routing and handoff if it remains. Confirm the candidate is linked from the repository index and every related-skill reference resolves to an existing skill or is explicitly marked as an external dependency.
8. Review safety and operational limits: secrets, privacy, security, accessibility, data loss, irreversible actions, resource cost, and required human or specialist review.
9. Assign a decision: publish draft, revise, accept at current lifecycle, defer for evidence, merge with another skill, or deprecate. Record the evidence, unresolved uncertainty, and next review trigger.

## Examples and counterexamples

Good: Reject a proposed “better coding” skill because its procedure duplicates repository verification; ask the author to narrow it to a distinct failure mode or merge the relevant guidance.

Bad: Publish every relevant paragraph as a separate skill because more files look like progress.

Good: Keep a security skill at draft status when its sources are general and no representative threat model or evaluation exists; state exactly what evidence would support promotion.

Bad: Mark a skill trusted because it has citations and confident wording without checking source fit, counterexamples, or actual use.

## Failure modes and recovery

If the skill’s target or evidence is ambiguous, defer publication and ask for the missing decision or research. If it overlaps another skill, merge, narrow, or define a clear routing boundary instead of leaving competing instructions. If a source is unavailable or stale, lower confidence and lifecycle status. If a skill causes repeated misuse or no longer reflects evidence, preserve the rationale, revise or deprecate it, and identify dependents that need review.

## Validation evidence and provenance

- The governing research requires depth over volume, explicit skill anatomy, adversarial review, source hierarchy and independence, lifecycle management, contradiction handling, and progress measured by usefulness.
- [Agent Skills specification](https://agentskills.io/specification): `SKILL.md` metadata must identify the skill and when it should be used; format compliance is necessary for interoperability but does not establish procedural quality.
- Review observations, hypotheses, and recommendations separately. Treat a review decision as a recommendation supported by evidence, not as proof that the skill cannot fail in use.
- Confidence: high for the review criteria; medium for predicting generalization until the skill is exercised on representative agent tasks.
- Freshness: review when the skill library, source evidence, agent behavior, risk model, or intended task population changes.

For material conclusions, seek disconfirming evidence, distinguish observations from hypotheses and recommendations, record tradeoffs and uncertainty, and note confidence, freshness, and source independence.

## Related skills and conflicts

Related: `skill-composition-and-routing`, `epistemic-coding`, `requirements-to-acceptance`, `knowledge-maintenance`, `contradiction-resolution`, and every skill being reviewed. This skill does not authorize rejecting a skill solely because it is unfamiliar, promoting a skill without evidence, or overriding user and repository instructions.
