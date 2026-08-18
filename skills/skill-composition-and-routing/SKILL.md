---
name: skill-composition-and-routing
description: Select, order, and combine skills for an AI coding-agent task without activating irrelevant, duplicate, or conflicting guidance. Use when several skills may apply, a workflow spans phases, or a skill library is being extended.
---

Lifecycle: `draft`

# Skill Composition and Routing

## Purpose and scope

Turn a task and available skill descriptions into a small, coherent working set. This skill governs discovery, ordering, conflict handling, and handoff between skills; it does not override a repository instruction, invent capabilities, or replace the procedures inside selected skills.

## Triggers and prerequisites

Trigger when more than one skill appears relevant, a task crosses requirements, implementation, testing, security, maintenance, or review phases, or a skill’s trigger is broad enough to cause accidental activation. Prerequisites: the user’s task, repository context, available skill metadata, and any explicit priority or safety constraints.

## Decision criteria

- Select by the task’s actual need and the skill’s trigger, not by keyword similarity or artifact count.
- Prefer the smallest complete set: one skill may own a phase; supporting skills add distinct constraints or evidence.
- Order skills by dependency: clarify the target before implementation, establish safety boundaries before risky actions, implement before verification, and maintenance after a decision exists.
- Resolve conflicts by authority, scope, evidence, and explicit decision boundaries. Do not merge contradictory instructions into vague compromise language.
- A skill is not applicable merely because its subject appears in a file; its trigger and prerequisites must hold.

## Procedure

1. State the task, desired outcome, affected surface, risk, and current phase. Separate the user’s request from repository instructions and skill suggestions.
2. Scan skill metadata first. For each candidate, record trigger match, prerequisites available, phase owned, outputs produced, and known conflicts.
3. Classify candidates as primary, supporting, deferred, or irrelevant. Reject candidates whose trigger is only lexical, whose prerequisites are absent, or whose procedure duplicates a selected skill.
4. Draw the minimal sequence and handoffs. For example: requirements → implementation/debugging → regression tests → security review → change verification; adapt the sequence to the actual task.
5. Check for instruction conflicts. Apply higher-authority repository and user constraints first, then choose the skill with the narrower relevant scope or stronger evidence. If the conflict changes the requested outcome, ask before proceeding.
6. Pass only the outputs needed by the next skill: acceptance criteria, observations, hypotheses, changed behavior, test evidence, findings, residual risk, or review triggers. Do not pass assumptions as facts.
7. Re-evaluate routing when the task changes, a failure reveals a new risk, or a selected skill’s prerequisite becomes false. Do not continue a stale workflow to preserve momentum.
8. At handoff, state which skills were used, why each applied, what each established, what remains unverified, and which skill or human decision owns the next step.

## Examples and counterexamples

Good: For an authorization bug, route requirements-to-acceptance first, secure-coding-review for trust boundaries, regression-test-design for denial cases, and repository-change-verification at the end. Defer dependency review because no dependency changed.

Bad: Activate every security, testing, and maintenance skill because the task touches a repository. More instructions can create contradictions and dilute attention.

Good: If evidence-driven-debugging discovers that the issue is actually a dependency vulnerability, hand off to dependency-security-audit and preserve the original observations.

Bad: Keep debugging application code after the evidence shows the vulnerable behavior comes from an unreviewed external package.

## Failure modes and recovery

If no skill clearly applies, use the task’s repository guidance and record the gap rather than forcing a poor match. If two skills claim the same phase, compare scope and evidence, then narrow or revise one. If selected skills conflict materially, stop and ask or record the unresolved boundary; never silently apply both. If routing repeatedly causes unnecessary context or steps, simplify the composition and retain the reason.

## Validation evidence and provenance

- The governing research recommends composable skills, explicit dependency relationships, dynamic taxonomies, conflict resolution, and depth over volume.
- Routing is treated as a hypothesis about task fit; the agent should revise it when failures, overlap, or contradictory outcomes provide disconfirming evidence.
- Confidence: medium-high for phase-based routing; medium for any specific ordering when repository constraints or risk requirements differ.
- Freshness: review when skill triggers, dependencies, conflicts, or the library’s taxonomy materially change.

## Related skills and conflicts

Related: every task skill in this library, especially `requirements-to-acceptance`, `epistemic-coding`, `repository-change-verification`, `contradiction-resolution`, and `knowledge-maintenance`. This skill does not override a selected skill’s safety boundary or authorize skipping a required phase to reduce context.
