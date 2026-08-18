---
name: build-and-ci-integrity
description: Review and improve build systems and CI workflows for reproducibility, least privilege, trustworthy artifacts, controlled inputs, and useful verification. Use when an AI coding agent changes build commands, workflow files, runners, artifact publication, release checks, or provenance.
---

Lifecycle: `draft`

# Build and CI Integrity

## Purpose and scope

Ensure that build and CI results are meaningful, repeatable, and protected from unintended workflow or artifact tampering. This skill covers workflow behavior, build inputs, permissions, caching, artifacts, and provenance; it does not replace dependency security, release approval, or provider-specific operations guidance.

## Triggers and prerequisites

Trigger when changing CI workflows, build scripts, runners, containers, caches, artifacts, release checks, signing/provenance, test commands, or permissions. Prerequisites: intended build outputs, source and dependency inputs, workflow triggers, runner trust model, secrets, artifact consumers, required checks, and repository/provider policy.

## Decision criteria

- A green workflow is evidence only for the jobs, inputs, environment, and assertions it actually exercised.
- Build integrity includes source identity, dependency identity, toolchain, configuration, runner, artifact digest, and provenance—not merely a successful command.
- CI permissions and secrets must be limited to the job and event that require them; untrusted contributions must not gain write access through workflow context.
- Reproducibility is a goal with measurable limits: record nondeterministic inputs and distinguish bit-for-bit reproducibility from functional equivalence.

## Procedure

1. Inventory workflow triggers, permissions, jobs, reusable workflows, runners, containers, actions, scripts, secrets, caches, generated files, artifacts, and publication destinations.
2. Define the build contract: canonical source revision, commands, toolchain/runtime, dependency lock state, configuration, expected artifacts, checks, retention, and consumer verification.
3. Trace trust boundaries for pull requests, forks, branches, tags, release events, generated code, cache restore/save, artifact upload/download, and deployment or signing steps.
4. Minimize permissions and secret exposure. Pin third-party actions or equivalent inputs immutably where policy requires, verify ownership, separate untrusted validation from privileged publication, and prevent logs/artifacts from containing secrets.
5. Make inputs explicit and stable: lock dependencies, identify toolchains, control locale/time/randomness where relevant, avoid mutable downloads, isolate caches, and distinguish generated artifacts from source.
6. Verify that required checks assert meaningful behavior and cannot be bypassed by skipped, conditional, empty, or untrusted jobs. Inspect failure, cancellation, timeout, and partial-artifact behavior.
7. Produce or verify artifact identity and provenance: source revision, builder, process, inputs, digest, and signing/attestation where the system requires it. Do not claim provenance that the workflow does not generate or verify.
8. Exercise changed workflows with normal, fork/untrusted, failed, retried, canceled, cache-hit/miss, and release paths. Check permissions, artifact contents, logs, timing, and reproducibility limits.
9. Compare behavior and access against the baseline. Record residual risk, provider assumptions, required human approvals, recovery path, review trigger, and evidence that supports the lifecycle status.

## Examples and counterexamples

Good: A release workflow separates untrusted tests from privileged publication, pins external actions, grants publish permissions only to the release job, records the source digest and artifact provenance, and tests fork behavior.

Bad: Give every pull-request job write permissions and secrets because the workflow is convenient to share.

Good: A build records toolchain and dependency inputs and declares when timestamps or platform-specific binaries prevent bit-for-bit reproducibility.

Bad: Call an artifact reproducible because the same command passed twice on one runner.

## Failure modes and recovery

If workflow permissions, runner trust, or artifact ownership is unclear, stop privileged publication and resolve the boundary. If a secret may have reached logs, artifacts, or an untrusted job, revoke/rotate it and follow the security process. If an artifact lacks trustworthy provenance, mark it unverified and rebuild or attest it through an approved path. If a required check can be bypassed or produces false confidence, fix the gate before relying on it.

## Validation evidence and provenance

- The governing research emphasizes source hierarchy, failure analysis, reproducibility, supply-chain integrity, tool authorization, and verification over assertion.
- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use): immutable action references and workflow permission controls reduce tampering and privilege risk.
- [SLSA build levels](https://slsa.dev/spec/v1.0/levels): build provenance and increasing protections against artifact or build-process tampering.
- Label observed workflow behavior and artifact measurements separately from hypotheses about trust or reproducibility and recommendations about controls; trace repeated guidance to independent sources.
- Confidence: high for explicit inputs, least privilege, artifact identity, and provenance principles; medium for a particular provider or reproducibility guarantee until its runner and build model are verified.
- Freshness: review when CI provider behavior, runner images, workflow permissions, build tools, dependency policy, artifact consumers, or provenance standards change.

For material conclusions, seek disconfirming evidence, distinguish observations from hypotheses and recommendations, record tradeoffs and uncertainty, and note confidence, freshness, and source independence.

## Related skills and conflicts

Related: `dependency-security-audit`, `configuration-and-secrets-safety`, `release-and-rollback-safety`, `safe-git-workflow`, `secure-coding-review`, `performance-regression-analysis`, and `repository-change-verification`. This skill does not authorize privileged workflow changes, exposing secrets, trusting mutable actions, or calling an artifact verified without provenance evidence.
