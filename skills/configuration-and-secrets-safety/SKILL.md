---
name: configuration-and-secrets-safety
description: Design and review application configuration, environment handling, and secret use without unsafe defaults, accidental disclosure, or environment drift. Use when an AI coding agent changes config files, environment variables, deployment settings, credentials, keys, or feature flags.
---

Lifecycle: `draft`

# Configuration and Secrets Safety

## Purpose and scope

Keep configuration explicit, validated, environment-appropriate, and safe while limiting secret exposure and operational surprises. This skill covers configuration contracts and secret lifecycle handling; it does not replace a dedicated security review, provider-specific secret-manager guidance, or release approval.

## Triggers and prerequisites

Trigger when changing configuration schemas, defaults, environment variables, feature flags, credentials, certificates, keys, CI/CD settings, containers, deployment manifests, or startup behavior. Prerequisites: environments, configuration sources and precedence, ownership, data sensitivity, secret provider, rotation/revocation process, compatibility policy, and deployment path.

## Decision criteria

- Configuration is an interface: define names, types, requiredness, defaults, validation, precedence, reload behavior, and failure semantics.
- A default must be safe for its environment; development convenience must not silently become production behavior.
- Secrets should be least-privilege, short-lived or rotatable, attributable, revocable, and absent from source, logs, images, committed configuration, and error output.
- A configuration change is incomplete until affected environments, consumers, and rollback behavior are understood.

## Procedure

1. Inventory every changed configuration source and precedence path: code defaults, files, environment, flags, deployment manifests, CI, secret providers, and operator overrides.
2. Classify each value as public configuration, sensitive data, credential, key, certificate, or derived runtime state. Identify owner, scope, audience, lifetime, and blast radius.
3. Define the configuration contract: type, requiredness, valid range, default, environment restrictions, startup/reload behavior, error response, and compatibility with old versions.
4. Remove secrets from code, examples, image layers, generated artifacts, command lines, logs, dumps, and test fixtures. Use the approved secret provider with least-privilege access and attribution.
5. Define secret lifecycle: creation, provisioning, access, rotation, overlap, revocation, expiry, recovery, detection, and response to exposure. Check dependent services and rollback during rotation.
6. Validate configuration before use and fail safely. Reject unknown or dangerous values where appropriate, avoid fail-open security settings, and distinguish missing from intentionally disabled behavior.
7. Compare each environment and deployment path. Check drift, redaction, permissions, interpolation/quoting, encoding, shell expansion, container inheritance, and fork or artifact exposure.
8. Test valid, missing, malformed, boundary, conflicting, stale, rotated, revoked, and unauthorized configurations without placing real secrets in test output. Verify errors do not disclose sensitive values.
9. Document owners, examples with placeholders, precedence, safe defaults, rollout/rollback behavior, review trigger, and how to rotate or revoke affected secrets. Record uncertainty rather than guessing provider behavior.

## Examples and counterexamples

Good: A required production credential is fetched from an approved provider, access is scoped to one service, rotation supports overlap, logs redact values, and startup fails closed when retrieval is unauthorized.

Bad: Put a credential in a sample `.env`, Dockerfile `ENV`, command line, or CI log because the repository is private.

Good: A feature flag defines type, owner, environments, expiry/review date, safe fallback, and behavior when the flag service is unavailable.

Bad: Add a boolean flag with a permissive default and no plan to remove or review it.

## Failure modes and recovery

If configuration precedence or secret ownership is unclear, stop and resolve it before changing behavior. If a secret may be exposed, revoke/rotate it through the responsible process, preserve evidence, and inspect copies and logs; deleting the visible file is not sufficient. If a provider is unavailable, use an explicitly safe fallback or fail closed according to the contract, not an improvised credential. If environments drift, reconcile from an authorized source and verify before release.

## Validation evidence and provenance

- The governing research emphasizes explicit uncertainty, reversibility, failure recovery, least-privilege tool use, lifecycle maintenance, and evidence over convention.
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html): centralized management, least privilege, rotation, revocation, attribution, and avoiding secret leakage in code and pipelines.
- [OWASP CI/CD Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html): secrets should not be hardcoded in repositories or CI/CD configuration and pipeline exposure must be controlled.
- Label observed configuration behavior separately from hypotheses about provider or environment effects and recommendations about defaults or rotation; trace repeated guidance to independent sources.
- Confidence: high for secret lifecycle and explicit configuration-contract principles; medium for provider-specific implementation and safe fallback until the environment is known.
- Freshness: review when secret providers, deployment environments, configuration precedence, rotation policy, or CI/CD tooling changes.

## Related skills and conflicts

Related: `secure-coding-review`, `privacy-and-data-handling`, `tool-authorization-audit`, `prompt-injection-resistance`, `release-and-rollback-safety`, `api-contract-compatibility`, and `repository-change-verification`. This skill does not authorize handling real secrets in chat, weakening access controls, or assuming a private repository makes a credential safe.
