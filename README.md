<p align="center">
  <img src="logo.png" alt="Open Agent Skills logo" width="160">
</p>

<h1 align="center">Open Agent Skills</h1>

<p align="center">
  <a href="https://skills.sh/ChloeVPin/open-agent-skills"><img src="https://skills.sh/b/ChloeVPin/open-agent-skills" alt="Install with skills.sh"></a>
  <a href="https://github.com/ChloeVPin/open-agent-skills/stargazers"><img src="https://img.shields.io/github/stars/ChloeVPin/open-agent-skills?style=flat" alt="GitHub stars"></a>
</p>

Research-backed, vendor-neutral `SKILL.md` skills for AI coding agents. Use them for debugging, API compatibility, refactoring, security review, migrations, performance, accessibility, localization, release safety, and evidence-driven repository work.

The skills are vendor-neutral Markdown guidance intended for any coding agent that can read `SKILL.md`. They do not require a particular model, host application, plugin, runtime, tool protocol, or programming language; adapt tool names and repository commands to the agent and codebase in scope.

The goal is useful skills: clear triggers, bounded procedures, failure handling, examples, provenance, and review conditions. A file is not valuable merely because it exists.

## Operating model

1. Identify a concrete coding-agent task and its failure modes.
2. Research authoritative sources and separate facts from advice.
3. Write one focused `SKILL.md` with explicit scope and triggers.
4. Review it adversarially with counterexamples and disconfirming evidence.
5. Validate usefulness, correctness, safety, and maintainability.
6. Revise, deprecate, or replace skills when evidence changes.

The deliverables are the directories under [`skills/`](skills/). Each contains a standalone `SKILL.md`; no runtime, test suite, or audit framework is required.

## Install with `npx skills`

This repository uses the open Agent Skills layout, so the existing `npx skills` CLI can discover and install these files directly:

```bash
# Browse the available skills first
npx skills add ChloeVPin/open-agent-skills --list

# Install one skill into the current project
npx skills add ChloeVPin/open-agent-skills --skill evidence-driven-debugging

# Install several selected skills
npx skills add ChloeVPin/open-agent-skills \\
  --skill repository-exploration \\
  --skill requirements-to-acceptance \\
  --skill repository-change-verification

# Install all skills globally for supported agents
npx skills add ChloeVPin/open-agent-skills --all -g
```

Without `-g`, installation is project-scoped; with `-g`, it is user-scoped. The CLI can target supported agents, list installed skills, update them, and remove them without this repository shipping a custom installer or runtime.

### Why this is useful

- One familiar command makes the library discoverable without cloning or manually copying files.
- Users can install only the skill that matches the task instead of loading the entire catalog into an agent’s context.
- Project-scoped installation supports reproducible team workflows; global installation supports personal reuse across repositories.
- The shared `SKILL.md` format allows the same guidance to work across many coding agents, while the CLI handles agent-specific install locations.
- Updates and removal have a defined workflow instead of leaving unmanaged copies scattered across agent directories.

Skills are instructions that influence agent behavior. Inspect the source, provenance, lifecycle status, and requested permissions before installing; installation is not proof that a skill is safe or correct. Prefer a reviewed revision and avoid granting tools or credentials merely because a skill requests them.

## Start with a path

Install only the path that matches the work. The sequence is a routing suggestion, not a requirement to load every skill.

### Fix a bug

Use this path when behavior is broken, surprising, flaky, or contradicted by a specification.

```bash
npx skills add ChloeVPin/open-agent-skills \\
  --skill repository-exploration \\
  --skill evidence-driven-debugging \\
  --skill regression-test-design \\
  --skill repository-change-verification
```

Route to `secure-coding-review` if the evidence points to a trust boundary, and to `dependency-security-audit` if an external package or build artifact is involved. Do not use a regression check as proof of a root cause that was never established.

### Add a feature or change an interface

Use this path when requirements are incomplete, the change crosses files or components, or callers may depend on the current behavior.

```bash
npx skills add ChloeVPin/open-agent-skills \\
  --skill requirements-to-acceptance \\
  --skill implementation-planning \\
  --skill api-contract-compatibility \\
  --skill repository-change-verification
```

Use only the domain skill required by the change—for example, `data-migration-safety`, `concurrency-and-shared-state`, or `internationalization-and-localization`. If the request has two materially different interpretations, clarify it before implementation.

### Change security-sensitive behavior

Use this path when code handles authorization, credentials, untrusted input, sensitive data, dependencies, CI permissions, or agent tools.

```bash
npx skills add ChloeVPin/open-agent-skills \\
  --skill repository-exploration \\
  --skill secure-coding-review \\
  --skill configuration-and-secrets-safety \\
  --skill repository-change-verification
```

Add `privacy-and-data-handling`, `dependency-security-audit`, `build-and-ci-integrity`, or `tool-authorization-audit` only when its trigger is actually met. Security review does not authorize bypassing approval, exposing secrets, or claiming safety from a checklist alone.

Browse the wider ecosystem at [skills.sh](https://skills.sh/) after understanding the source and trust boundary of a skill.

## Skill structure

Each skill should state its purpose, triggers, procedure, examples, failure recovery, evidence, confidence, freshness, and related skills. Keep skills focused on helping AI coding agents perform real work.

## Evidence standard

Every material conclusion in a skill must distinguish direct observations from hypotheses and recommendations. Authors should seek disconfirming evidence, trace repeated claims to their originating source, record tradeoffs and uncertainty, and state confidence and freshness. Reachable citations are necessary but do not prove that a skill is correct; each skill remains draft until representative use, adversarial review, and applicable verification provide stronger evidence.

`Lifecycle: draft` means the skill is usable guidance under review, not a guarantee of correctness. A future `validated`, `trusted`, `deprecated`, or `superseded` state must be earned and explained by current evidence; lifecycle labels never override repository instructions, user authorization, or specialist review.

## Publication gate

Before adding or materially revising a skill, confirm:

- [ ] The task is recurring and distinct from every existing skill; overlap is narrowed or explicitly composed.
- [ ] Trigger, prerequisites, decision boundaries, permissions, side effects, and stopping conditions are concrete.
- [ ] Observations, hypotheses, recommendations, confidence, uncertainty, and tradeoffs are labeled.
- [ ] Authoritative evidence is cited, source independence is checked, and disconfirming cases are recorded.
- [ ] Examples, counterexamples, failure recovery, misuse limits, freshness, lifecycle, and review triggers are present.
- [ ] Related references resolve, the README index is updated, and only the standalone `SKILL.md` plus minimal documentation is added.

## Using the library

1. Start with [repository exploration](skills/repository-exploration/SKILL.md) and [requirements to acceptance](skills/requirements-to-acceptance/SKILL.md) when the codebase or target is unclear.
2. Use [skill composition and routing](skills/skill-composition-and-routing/SKILL.md) to select the smallest relevant set; do not load every skill for every task.
3. Follow the selected skill’s triggers and prerequisites, then pass its outputs to the next applicable skill.
4. Finish with the relevant verification, security, performance, accessibility, release, or maintenance skill, and report evidence limits honestly.

Skills are guidance, not guarantees. Repository instructions, user authorization, specialist review, and applicable standards remain authoritative.

## Skill index

### Foundation and routing

- [Epistemic coding](skills/epistemic-coding/SKILL.md) — evidence-first decisions and uncertainty.
- [Requirements to acceptance](skills/requirements-to-acceptance/SKILL.md) — turn intent into observable criteria.
- [Skill composition and routing](skills/skill-composition-and-routing/SKILL.md) — select and order applicable skills.
- [Repository exploration](skills/repository-exploration/SKILL.md) — map code, callers, boundaries, and verification paths.
- [Skill quality review](skills/skill-quality-review/SKILL.md) — assess evidence, scope, overlap, and lifecycle before publication.
- [Implementation planning](skills/implementation-planning/SKILL.md) — sequence bounded work with risks and verification.
- [Architecture decision-making](skills/architecture-decision-making/SKILL.md) — compare system designs and record tradeoffs.

### Change and diagnosis

- [Evidence-driven debugging](skills/evidence-driven-debugging/SKILL.md) — reproduce failures and test competing causes.
- [Behavior-preserving refactoring](skills/behavior-preserving-refactoring/SKILL.md) — restructure without accidental contract changes.
- [Dead code and comment cleanup](skills/dead-code-and-comment-cleanup/SKILL.md) — remove proven dead code and redundant comments without losing intent or public behavior.
- [API contract and compatibility](skills/api-contract-compatibility/SKILL.md) — evolve interfaces without hidden consumer breakage.
- [Differential patch review](skills/differential-patch-review/SKILL.md) — compare candidate and trusted behavior.
- [Repository change verification](skills/repository-change-verification/SKILL.md) — assess a complete patch before acceptance.
- [Safe Git workflow](skills/safe-git-workflow/SKILL.md) — preserve work and history while changing repositories.

### Testing and performance

- [Regression test design](skills/regression-test-design/SKILL.md) — create focused behavior and boundary tests.
- [Test-effectiveness analysis](skills/test-effectiveness-analysis/SKILL.md) — find faults that tests fail to detect.
- [Static analysis and type safety](skills/static-analysis-and-type-safety/SKILL.md) — interpret diagnostics without hiding risk.
- [Concurrency and shared state](skills/concurrency-and-shared-state/SKILL.md) — reason about interleavings, ownership, and liveness.
- [Resilience and retry design](skills/resilience-and-retry-design/SKILL.md) — bound dependency failures and recovery behavior.
- [Performance regression analysis](skills/performance-regression-analysis/SKILL.md) — measure changes against representative workloads.
- [Agent evaluation and benchmarking](skills/agent-evaluation-and-benchmarking/SKILL.md) — measure agent capability without metric gaming.
- [Observability and instrumentation](skills/observability-and-instrumentation/SKILL.md) — add useful, safe diagnostic signals.
- [Accessibility review](skills/accessibility-review/SKILL.md) — check user tasks across input modes and assistive technology.
- [Internationalization and localization](skills/internationalization-and-localization/SKILL.md) — handle locales, scripts, formats, and translations safely.
- [Release and rollback safety](skills/release-and-rollback-safety/SKILL.md) — stage delivery and recover safely.
- [Data migration safety](skills/data-migration-safety/SKILL.md) — evolve persisted data with integrity and recovery boundaries.

### Security and maintenance

- [Secure coding review](skills/secure-coding-review/SKILL.md) — inspect application trust boundaries and abuse cases.
- [Privacy and data handling](skills/privacy-and-data-handling/SKILL.md) — minimize and govern sensitive data across its lifecycle.
- [Configuration and secrets safety](skills/configuration-and-secrets-safety/SKILL.md) — manage environment settings and credentials safely.
- [Build and CI integrity](skills/build-and-ci-integrity/SKILL.md) — protect workflows, artifacts, and build provenance.
- [Dependency security audit](skills/dependency-security-audit/SKILL.md) — review dependency and supply-chain changes.
- [Tool authorization audit](skills/tool-authorization-audit/SKILL.md) — review agent permissions and high-impact calls.
- [Prompt-injection resistance](skills/prompt-injection-resistance/SKILL.md) — separate untrusted content from authority and actions.
- [Contradiction resolution](skills/contradiction-resolution/SKILL.md) — handle conflicting evidence and failures.
- [Knowledge maintenance](skills/knowledge-maintenance/SKILL.md) — track freshness, deprecation, and supersession.
