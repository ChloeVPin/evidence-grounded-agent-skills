# Hermes: Epistemic Institution

Hermes is an executable research institution for building, validating, and maintaining evidence-grounded skills for AI coding agents.

Its objective is not to produce files indefinitely. Its objective is to make the skill ecosystem more correct, useful, composable, current, and auditable.

## Operating model

1. Reconnaissance maps domains, dependencies, gaps, and risk.
2. Prioritization selects the highest-leverage tractable question.
3. Research traces claims to independent primary evidence.
4. Construction records a skill with explicit scope, uncertainty, and provenance.
5. Adversarial review searches for disconfirmation and failure modes.
6. Validation tests usefulness, correctness, safety, and maintainability.
7. Maintenance detects decay, contradictions, and regressions.

The first cycle is recorded in [`ledger/cycles/0001-institutional-bootstrap.md`](ledger/cycles/0001-institutional-bootstrap.md).

## Repository map

- [`CONSTITUTION.md`](CONSTITUTION.md): non-negotiable epistemic rules.
- [`RESEARCH_PROTOCOL.md`](RESEARCH_PROTOCOL.md): the repeatable research loop.
- [`SKILL_SPEC.md`](SKILL_SPEC.md): schema for skills.
- [`QUALITY_RUBRIC.md`](QUALITY_RUBRIC.md): release gates.
- [`KNOWLEDGE_LEDGER.md`](KNOWLEDGE_LEDGER.md): provenance and decisions.
- [`skills/`](skills/): validated and experimental skills.
- [`ledger/`](ledger/): cycle records, rejected hypotheses, and change history.
- [`scripts/cycle.py`](scripts/cycle.py): creates the next cycle workspace without pretending work is complete.
- [`scripts/change_review.py`](scripts/change_review.py): deterministic pre-review gate for scope and sensitive paths.
- [`scripts/evidence_review.py`](scripts/evidence_review.py): checks that review records contain minimum test evidence.
- [`scripts/capture_evidence.py`](scripts/capture_evidence.py): captures command status, repository revision, and output digest.

## Running a cycle

```bash
python3 scripts/cycle.py --list
python3 scripts/cycle.py --start --question "What high-leverage skill gap should be researched next?"
```

Each cycle must end with evidence, a decision, and an explicit next action. Empty activity is not progress.
