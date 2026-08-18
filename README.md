# Evidence-Grounded Agent Skills

This repository contains practical, evidence-grounded `SKILL.md` files for AI coding agents.

The goal is useful skills: clear triggers, bounded procedures, failure handling, examples, provenance, and review conditions. A file is not valuable merely because it exists.

## Operating model

1. Identify a concrete coding-agent task and its failure modes.
2. Research authoritative sources and separate facts from advice.
3. Write one focused `SKILL.md` with explicit scope and triggers.
4. Review it adversarially with counterexamples and disconfirming evidence.
5. Validate usefulness, correctness, safety, and maintainability.
6. Revise, deprecate, or replace skills when evidence changes.

The deliverables are the directories under [`skills/`](skills/). Each contains a standalone `SKILL.md`; no runtime, test suite, or audit framework is required.

## Skill structure

Each skill should state its purpose, triggers, procedure, examples, failure recovery, evidence, confidence, freshness, and related skills. Keep skills focused on helping AI coding agents perform real work.

## Skill index

### Foundation and routing

- [Epistemic coding](skills/epistemic-coding/SKILL.md) — evidence-first decisions and uncertainty.
- [Requirements to acceptance](skills/requirements-to-acceptance/SKILL.md) — turn intent into observable criteria.
- [Skill composition and routing](skills/skill-composition-and-routing/SKILL.md) — select and order applicable skills.

### Change and diagnosis

- [Evidence-driven debugging](skills/evidence-driven-debugging/SKILL.md) — reproduce failures and test competing causes.
- [Behavior-preserving refactoring](skills/behavior-preserving-refactoring/SKILL.md) — restructure without accidental contract changes.
- [API contract and compatibility](skills/api-contract-compatibility/SKILL.md) — evolve interfaces without hidden consumer breakage.
- [Differential patch review](skills/differential-patch-review/SKILL.md) — compare candidate and trusted behavior.
- [Repository change verification](skills/repository-change-verification/SKILL.md) — assess a complete patch before acceptance.

### Testing and performance

- [Regression test design](skills/regression-test-design/SKILL.md) — create focused behavior and boundary tests.
- [Test-effectiveness analysis](skills/test-effectiveness-analysis/SKILL.md) — find faults that tests fail to detect.
- [Performance regression analysis](skills/performance-regression-analysis/SKILL.md) — measure changes against representative workloads.
- [Observability and instrumentation](skills/observability-and-instrumentation/SKILL.md) — add useful, safe diagnostic signals.

### Security and maintenance

- [Secure coding review](skills/secure-coding-review/SKILL.md) — inspect application trust boundaries and abuse cases.
- [Dependency security audit](skills/dependency-security-audit/SKILL.md) — review dependency and supply-chain changes.
- [Tool authorization audit](skills/tool-authorization-audit/SKILL.md) — review agent permissions and high-impact calls.
- [Contradiction resolution](skills/contradiction-resolution/SKILL.md) — handle conflicting evidence and failures.
- [Knowledge maintenance](skills/knowledge-maintenance/SKILL.md) — track freshness, deprecation, and supersession.
