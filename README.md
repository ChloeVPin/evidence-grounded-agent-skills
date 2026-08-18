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
