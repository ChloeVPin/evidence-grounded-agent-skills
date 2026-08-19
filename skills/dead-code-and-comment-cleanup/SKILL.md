---
name: dead-code-and-comment-cleanup
description: Identify dead code, duplicated literals, drift-prone declarations, and comments that restate implementation without deleting anything until usage and intent are verified. Use when an AI coding agent is asked to clean up unused code or redundant comments.
---

Lifecycle: `draft`

# Dead Code and Comment Cleanup

## Purpose and scope

Reduce maintenance noise without deleting behavior, public surface, compatibility logic, or rationale-bearing documentation by mistake. This skill covers candidate discovery, repository-wide evidence, findings, approval, and narrow cleanup; it does not replace behavior-preserving refactoring, security review, or project-specific ownership rules.

## Triggers and prerequisites

Trigger when asked to remove unused code, duplicate declarations, stale comments, dead branches, drift-prone literals, or unreachable-looking configuration. Prerequisites: repository instructions, baseline revision, source and generated-file boundaries, language/tooling conventions, public API/entry-point knowledge, and authorization to modify the identified files.

## Decision criteria

- Treat every declaration, export, route, registration, configuration key, and comment as live until repository evidence supports a narrower claim.
- A static search or analyzer warning is a candidate observation, not proof of deadness; account for re-exports, reflection, dynamic imports, generated code, plugins, tests, configuration, and external consumers.
- Remove a comment only when it restates behavior the code already communicates. Keep comments that explain intent, constraints, history, compatibility, security, workarounds, or non-obvious tradeoffs.
- Present findings and obtain the required approval before deletion when ownership, public compatibility, dynamic use, or intent is uncertain.

## Procedure

1. Define the cleanup boundary, non-goals, protected files, public surfaces, and approval requirement. Do not combine cleanup with unrelated refactoring.
2. Build candidates using existing repository tooling and targeted search. Classify them as unreferenced declarations, duplicate declarations, drift-prone literals, suspicious limits, redundant comments, or uncertain.
3. Verify each candidate across source, tests, configuration, generated inputs/outputs, registration mechanisms, public exports, and repository history. Follow barrel re-exports and dynamic access where applicable.
4. For code, check entry points, public APIs, framework conventions, reflection, environment branches, plugin loading, and external consumers before calling something dead. For comments, inspect adjacent code and `git blame` when history may explain the rationale.
5. Record a findings table with exact item, location, evidence searched, classification, confidence, possible impact, and recommendation. Separate observations from hypotheses about why the item exists.
6. Stop and request approval for uncertain or destructive findings. Do not edit while the candidate list is still being established.
7. Apply only approved, narrow removals. Preserve behavior, exports, error handling, compatibility guards, legal notices, and comments that carry non-obvious reasons.
8. Re-scan the affected references and inspect the diff. Run the repository’s applicable verification commands when authorized; record unavailable checks and residual uncertainty.
9. Report removed items, retained uncertain items, evidence limits, and the next review trigger. If a candidate remains ambiguous, leave it in place and explain why.

## Examples and counterexamples

Good: A private helper has no references after checking source, tests, generated registrations, and dynamic lookup; the agent reports it, receives approval, removes it, and rechecks the diff.

Bad: Delete an exported function because a local search found no callers; external consumers or reflection may depend on it.

Good: Remove a comment that repeats `count += 1` while preserving a nearby comment explaining a compatibility workaround and its expiry condition.

Bad: Remove all comments, or delete a historical warning because the workaround looks unnecessary without checking its issue or version constraint.

## Failure modes and recovery

If tooling reports a candidate but usage cannot be ruled out, classify it as uncertain and keep it. If generated or dynamic behavior prevents complete search, narrow the claim and ask the owner or inspect runtime evidence. If deletion changes behavior, restore the narrow change and route the issue to behavior-preserving refactoring or debugging. If the requested cleanup is destructive or overlaps user changes, stop and obtain explicit approval.

## Validation evidence and provenance

- The governing research requires evidence before deletion, preserved uncertainty, reversible changes, adversarial review, and progress measured by reduced risk rather than file count.
- [TypeScript `noUnusedLocals`](https://www.typescriptlang.org/tsconfig/noUnusedLocals.html): compiler diagnostics can identify unused local declarations while remaining bounded by the compiler’s visibility and language model.
- [ESLint `no-unused-vars`](https://eslint.org/docs/latest/rules/no-unused-vars): static unused-variable findings require configuration and scope interpretation rather than automatic deletion.
- [Git `blame` documentation](https://git-scm.com/docs/git-blame): line history can provide context for comments and compatibility code, but age is not proof that a line is unnecessary.
- Treat analyzer output, search results, history, and owner reports as distinct evidence only when their provenance and blind spots are independent. Label observed references separately from hypotheses about reachability and recommendations about removal.
- Confidence: medium-high for the evidence-first cleanup procedure; medium for any deadness conclusion until dynamic access, external consumers, and ownership boundaries are checked.
- Freshness: review when language tooling, build/registration conventions, public API policy, repository topology, or deployment behavior changes.

For material conclusions, seek disconfirming evidence, distinguish observations from hypotheses and recommendations, record tradeoffs and uncertainty, and note confidence, freshness, and source independence.

## Related skills and conflicts

Related: `behavior-preserving-refactoring`, `repository-exploration`, `repository-change-verification`, `safe-git-workflow`, `static-analysis-and-type-safety`, and `knowledge-maintenance`. This skill does not authorize deleting public APIs, generated files, user work, legal notices, compatibility code, or comments merely because they look redundant.
