---
name: safe-git-workflow
description: Use Git safely while an AI coding agent investigates, edits, reviews, commits, rebases, merges, or publishes repository changes. Use when branch state, uncommitted work, history, conflicts, or destructive commands could affect recoverability or collaboration.
---

Lifecycle: `draft`

# Safe Git Workflow

## Purpose and scope

Preserve user work and make repository history accurately communicate reviewed changes. This skill covers inspection, staging, commits, synchronization, conflict recovery, and reversible cleanup; it does not replace repository-specific contribution policy, release approval, or code review.

## Triggers and prerequisites

Trigger before modifying Git state, switching branches, resetting, rebasing, merging, resolving conflicts, committing, pushing, deleting files, or cleaning generated artifacts. Prerequisites: repository root, current branch and upstream, worktree status, user authorization, intended scope, remote policy, and whether existing changes belong to the user or another task.

## Decision criteria

- Inspect before mutating: current branch, upstream, worktree, staged diff, untracked files, and recent history are part of the task state.
- Preserve unrelated or pre-existing changes; never assume every worktree change was created by the current task.
- Prefer reversible operations and explicit targets. Destructive history or filesystem operations require clear authorization and a recoverable plan.
- A commit is a verified claim about its diff, not proof that the whole repository or product is correct.

## Procedure

1. Confirm repository root, branch, upstream, remotes, worktree status, staged/unstaged/untracked files, and relevant recent commits. Record unexpected state before editing.
2. Define the requested change boundary and identify files that must not be touched. Separate existing user changes from task changes; ask if they overlap materially.
3. Make focused edits and inspect the complete diff. Check whitespace, deleted files, generated artifacts, secrets, dependency changes, and unintended scope before staging.
4. Stage explicit paths, review the staged diff and status, then run the relevant verification. Do not stage the entire worktree when unrelated changes exist.
5. Commit with a specific message that describes the verified change. Do not rewrite, squash, or amend existing history unless authorized and the consequences are understood.
6. Before synchronization, inspect upstream divergence and remote policy. Fetch or pull using the repository’s documented strategy; do not overwrite remote work with a force push unless explicitly authorized.
7. Resolve conflicts by reconstructing both sides’ intent and invariants. Do not choose “ours” or “theirs” blindly; inspect the result and re-run relevant checks.
8. For cleanup or rollback, identify exact targets and whether recovery exists. Prefer moving or reverting narrowly; never use broad recursive deletion, reset, or checkout to guess at the desired state.
9. After mutation, verify status, branch/upstream relationship, commit contents, and remote result. Report what changed, what was preserved, what was not verified, and how to recover.

## Examples and counterexamples

Good: Discover unrelated uncommitted files, leave them untouched, stage only the requested skill, inspect the staged diff, and commit that isolated change.

Bad: Run `git add .` and commit every worktree change because the repository is “already dirty.”

Good: A conflict in a behavior change is resolved by comparing both versions’ acceptance criteria and adding back the invariant each side requires.

Bad: Accept the conflict tool’s default or choose one side without reading the surrounding code.

Good: A requested rollback identifies the exact commit and uses a reversible revert after checking downstream dependents.

Bad: Run a broad hard reset or recursive deletion to make the tree look clean without confirming targets and authorization.

## Failure modes and recovery

If worktree ownership or scope is unclear, stop mutation and ask. If a destructive operation was started, preserve remaining state, inspect reflog/backups or platform recovery, and report the exact loss or uncertainty. If a push is rejected, inspect divergence and integrate deliberately rather than force-pushing. If a conflict cannot be resolved from evidence, preserve both versions and escalate the decision.

## Validation evidence and provenance

- The governing research prioritizes reversibility, explicit scope, failure recovery, change justification, and truth over confidence.
- Git state inspection and diffs are direct repository observations; interpretations of ownership or intended history are hypotheses until confirmed; commit/revert strategy is a recommendation constrained by authorization.
- [Git documentation: reset, restore, and revert](https://git-scm.com/docs/git-reset): distinguishes recovery and history-changing operations that have different safety and collaboration consequences.
- Trace repository policy and upstream history to their origin; repeated commit messages or copied contribution instructions are not independent confirmation.
- Confidence: high for inspect-before-mutate and explicit-target principles; medium for conflict and synchronization strategy because repository policy and collaboration model vary.
- Freshness: review when remote policy, branching model, hosting workflow, or repository contribution rules change.

For material conclusions, seek disconfirming evidence, distinguish observations from hypotheses and recommendations, record tradeoffs and uncertainty, and note confidence, freshness, and source independence.

## Related skills and conflicts

Related: `repository-exploration`, `repository-change-verification`, `behavior-preserving-refactoring`, `requirements-to-acceptance`, `release-and-rollback-safety`, `prompt-injection-resistance`, and `skill-quality-review`. This skill does not authorize destroying user work, rewriting shared history, exposing secrets, or claiming a clean tree without checking it.
