# Cycle 0002 — Which high-leverage AI coding-agent skill gap should Hermes research first?

Date: 2026-08-18
Status: decision recorded; skill drafted for validation

## Question

Which high-leverage AI coding-agent skill gap should Hermes research first?

## Decision

Select repository change verification for AI-generated patches as the first skill.

## Evidence and provenance

1. Jimenez et al., [SWE-bench](https://arxiv.org/abs/2310.06770): real issue resolution requires coordinating multiple files and execution-environment interaction; the benchmark's best reported model solved only 1.96% of issues in the original study.
2. Wang, Pradel, and Liu, [Are “Solved Issues” in SWE-bench Really Solved Correctly?](https://arxiv.org/abs/2503.15223): 7.8% of plausible patches failed when all developer tests were run; 29.6% differed behaviorally from reference patches; tests alone are insufficient evidence of correctness.
3. [GitHub pull request documentation](https://docs.github.com/en/pull-requests/get-started/about-pull-requests): reviewable diffs, checks, discussion, and isolated branches are part of a quality-preserving change workflow.
4. [OWASP Secure Coding with AI](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Coding_with_AI_Cheat_Sheet.html): AI changes to build scripts, CI/CD, package scripts, and deployment infrastructure require heightened scrutiny and explicit review.

Knowledge labels: observations from published studies and official guidance; recommendation for Hermes.
Confidence: high that verification is foundational; medium that this is the single highest-leverage first skill.

## Disconfirming evidence sought

The first SWE-bench study is from 2023 and its absolute solve rate is not a current measure of frontier performance. The later correctness study examines selected tools and benchmarks, not every coding agent. A security-first skill could be more urgent, but verification subsumes security-sensitive file review and is more broadly reusable. This selection should be revisited after the first validation cycle.

## Next action

Create and validate `skills/repository-change-verification/SKILL.md`; use its checklist against the next Hermes change.
