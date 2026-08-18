# Cycle 0030 — Next Exploration

Date: 2026-08-18
Status: decision recorded; next skill drafted

## Question

Which next high-leverage skill gap should Hermes explore after repository verification and dependency-security foundations?

## Mode

`exploration`

## Decision

Select test-effectiveness analysis with mutation-oriented validation as the next skill.

## Evidence and provenance

Evidence: [Petrović et al., Long Term Effects of Mutation Testing](https://research.google/pubs/long-term-effects-of-mutation-testing/) analyzed 15 million mutants and reported that mutation testing helped developers improve test suites and was coupled with historical faults; [Roman and Mnich, TDD with mutation testing](https://link.springer.com/article/10.1007/s11219-020-09534-x) found stronger coverage outcomes in a controlled experiment. [NIST’s GenAI profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf) supports runtime safety as important but does not bound a first coding-skill artifact.

Candidate ranking: test effectiveness—high impact, high reuse, medium uncertainty; runtime safety—very high impact, high uncertainty and broad scope; live connector trust—high impact but dependent on external services and already bounded by cycle 0027.

## Disconfirming evidence sought

Disconfirming evidence: mutation score is not semantic correctness, mutation tools can be expensive, and the studies do not prove every project benefits equally. The skill must use mutation evidence as a diagnostic signal, not a universal threshold.

## Next action

Build and validate `skills/test-effectiveness-analysis/SKILL.md`.
