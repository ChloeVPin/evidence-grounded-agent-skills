---
name: dependency-security-audit
description: Review dependency and supply-chain changes for provenance, vulnerabilities, integrity, execution behavior, and residual risk. Use when manifests, lockfiles, build scripts, or external artifacts change.
---

Lifecycle: `draft`

# Dependency and Supply-Chain Security Audit

## Purpose and scope

Use this skill when an AI-generated or human-proposed change adds, removes, upgrades, or changes the execution behavior of a dependency. It covers direct and transitive dependency review, provenance, known vulnerabilities, lockfile consistency, and install/build scripts. It does not replace a full threat model, license review, or maintainer security process.

## Triggers and prerequisites

Trigger on changes to manifest files, lockfiles, package scripts, build configuration, container definitions, CI workflows, generated dependency metadata, or code that downloads and executes external artifacts. Prerequisites: baseline and proposed revisions, package manager, resolved dependency graph, and repository security policy.

## Decision criteria

Accept only when provenance, graph impact, integrity, execution behavior, advisory status, and residual risk are understood at the repository’s required assurance level. Escalate or reject when a critical fact is unverifiable, stale, or outside the reviewer’s authority.

## Procedure

1. Inventory every changed manifest, lockfile, package script, build step, and external download. Treat generated lockfile changes as consequential.
2. Compare the resolved graph before and after the change, including transitive additions, removals, version ranges, integrity hashes, and platform-specific branches.
3. Verify each new package and action through its authoritative registry or maintainer source. Reject names or versions that cannot be independently resolved; AI suggestions are not provenance.
4. Check advisories and repository security tooling for known vulnerabilities, affected ranges, reachability, and available fixes. Record the advisory source and lookup date.
5. Inspect install, prepare, build, test, and deploy scripts for network access, arbitrary command execution, credential access, or behavior newly activated by the dependency.
6. Require immutable or policy-approved references for executable third-party actions and artifacts. Record exceptions with explicit reviewer approval.
7. Run the package manager's lockfile, integrity, audit, and relevant test checks. Capture command, revision, exit status, and output digest using the repository evidence tools.
8. Record direct and transitive risk, residual uncertainty, decision, and the next review trigger. Do not mark the audit trusted solely because installation succeeds.

## Acceptance checklist

- [ ] Changed manifests, lockfiles, scripts, and external artifacts are inventoried.
- [ ] Direct and transitive graph changes are understood.
- [ ] Every new package/action has authoritative provenance.
- [ ] Vulnerability and fix status were checked at a recorded time.
- [ ] Install/build/deploy execution paths were inspected.
- [ ] Integrity, audit, and relevant regression checks passed with captured evidence.
- [ ] Exceptions, residual risk, and review trigger are recorded.

## Examples and counterexamples

Good: A lockfile adds a transitive package; trace its origin, integrity, scripts, advisory status, and reachability before accepting it.

Bad: Approve the package because installation succeeds or because it is popular.

## Failure modes and recovery

If a package cannot be resolved from an authoritative source, stop and reject or escalate; do not guess. If advisory data is unavailable or stale, record the limitation and keep the change below trusted status. If a lockfile changes without an understandable graph explanation, regenerate from a clean baseline and review the full diff.

## Validation evidence and provenance

Record confidence and freshness for each advisory or risk conclusion, distinguish observed facts from hypotheses and recommendations, and verify that corroborating sources are independent.

- [GitHub dependency review documentation](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review): dependency diffs can be scanned and enforced in pull requests.
- [OWASP Secure Coding with AI](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Coding_with_AI_Cheat_Sheet.html): hallucinated dependencies, outdated CVEs, and AI-modified build/deploy paths are explicit risks.
- [NIST AI RMF: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf): lifecycle risk-management guidance for generative AI systems.
- Label resolved package facts and advisory observations separately from inferred exploitability and recommended action; do not treat an unresolved hypothesis as a finding.

Confidence: medium-high for the audit procedure; medium for prioritization as the next skill. Freshness review: on dependency-policy changes and at least quarterly.

For material conclusions, seek disconfirming evidence, distinguish observations from hypotheses and recommendations, record tradeoffs and uncertainty, and note confidence, freshness, and source independence.

## Related skills and conflicts

Related: `repository-change-verification`, `build-and-ci-integrity`, `secure-coding-review`, `configuration-and-secrets-safety`, and `regression-test-design`. This skill does not override repository-specific security policies or required human approval.
