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

The research and design notes are retained as supporting material; the deliverables are the files under [`skills/`](skills/).

## Repository map

- [`CONSTITUTION.md`](CONSTITUTION.md): governing principles for skill quality.
- [`RESEARCH_PROTOCOL.md`](RESEARCH_PROTOCOL.md): the repeatable skill-research process.
- [`SKILL_SPEC.md`](SKILL_SPEC.md): schema for skills.
- [`QUALITY_RUBRIC.md`](QUALITY_RUBRIC.md): release gates.
- [`KNOWLEDGE_LEDGER.md`](KNOWLEDGE_LEDGER.md): provenance and decisions supporting skills.
- [`skills/`](skills/): validated and experimental skills.
- [`QUALITY_RUBRIC.md`](QUALITY_RUBRIC.md): release criteria for each skill.
