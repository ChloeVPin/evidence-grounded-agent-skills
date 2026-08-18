---
name: release-and-rollback-safety
description: Plan and review safe software releases with explicit preconditions, staged exposure, health signals, rollback boundaries, and recovery evidence. Use when an AI coding agent changes deployable behavior, migrations, configuration, or release automation.
---

Lifecycle: `draft`

# Release and Rollback Safety

## Purpose and scope

Reduce the blast radius of a change by making release, detection, rollback, and recovery behavior explicit. This skill covers delivery planning and review; it does not replace an organization’s change-approval, incident-response, compliance, or service-ownership process.

## Triggers and prerequisites

Trigger when a change will be deployed, changes runtime configuration, schema or data state, feature exposure, dependencies, infrastructure, or release automation. Prerequisites: the change and baseline, deployment topology, owners, health signals, compatibility constraints, rollback authority, data/migration behavior, and an acceptable maintenance window or rollout strategy.

## Decision criteria

- A release plan is incomplete without detection, decision ownership, rollback or forward-recovery action, and verification after recovery.
- Prefer progressive exposure and reversible changes when uncertainty or blast radius is high.
- Rollback is not automatically safe when data, schema, queues, external side effects, or irreversible migrations changed; define compatibility and recovery explicitly.
- A green deployment command is not evidence that users received correct behavior or that the system is healthy.

## Procedure

1. State the intended user and operational outcome, affected components, risk, blast radius, and what must remain unchanged.
2. Inventory release prerequisites: artifact identity, configuration, dependencies, migrations, feature flags, permissions, backups, capacity, observability, approvals, and dependency compatibility.
3. Define pre-release checks and a release invariant. Include version/configuration verification, migration safety, health criteria, and the evidence required before exposure increases.
4. Choose an exposure strategy appropriate to risk: canary, staged rollout, blue/green, feature flag, maintenance window, or another justified path. Define who can pause or abort it.
5. Define actionable health signals and thresholds for errors, latency, saturation, correctness, data integrity, security, and user impact. Assign an owner and observation window; avoid thresholds with no response.
6. Write the rollback or forward-recovery procedure, including commands or actions, authorization, compatible versions, data/schema handling, queued or external side effects, and how to prevent repeated damage.
7. Release to the smallest intended exposure, observe the defined signals, and compare with the baseline. Do not expand exposure because a fixed timer elapsed if the evidence is incomplete.
8. If a threshold is crossed, pause exposure and follow the predeclared response. Preserve evidence, communicate scope, contain harm, and do not improvise irreversible actions without authorization.
9. After completion or recovery, verify user behavior, data integrity, dependencies, observability, and cleanup. Record what happened, what was learned, residual risk, and the next review trigger.

## Examples and counterexamples

Good: A schema change uses an expand/migrate/contract sequence, keeps old and new versions compatible during rollout, monitors errors and data integrity, and defines what happens if the application rollback occurs after the migration.

Bad: Roll back application binaries while assuming the database can always be restored automatically.

Good: A canary has a named owner, bounded exposure, p95 latency and error thresholds, a pause action, and a post-rollout verification period.

Bad: Deploy to all users and decide whether it worked from the absence of an immediate alert.

## Failure modes and recovery

If rollback is unsafe or unknown, stop the rollout and design forward recovery or a compatible transition before exposure increases. If health signals are missing, keep the change below trusted release status and add the minimum useful observability. If an external side effect cannot be undone, contain further effects, record the irreversibility, and escalate. If a release partially succeeds, preserve the exact state and versions before attempting repair.

## Validation evidence and provenance

- The governing research emphasizes reversibility, failure recovery, lifecycle maintenance, anomaly detection, meaningful progress, and explicit stopping rules.
- [Google SRE: Release Engineering](https://sre.google/sre-book/release-engineering/): reproducible releases, automation, and controlled delivery reduce operational risk.
- [Google SRE: Managing Incidents](https://sre.google/sre-book/managing-incidents/): clear roles, communication, mitigation, and learning during failures.
- [DORA: Continuous Delivery](https://dora.dev/capabilities/continuous-delivery/): small batches, automation, and reliable delivery practices, subject to organizational context.
- Check whether release guidance and health signals come from independent evidence; repeated deployment advice or metrics derived from one source do not confirm safety by themselves.
- Confidence: medium-high for staged exposure, explicit health signals, and recovery planning; medium for a particular rollout strategy until system topology and irreversibility are known.
- Freshness: review when deployment topology, release tooling, data lifecycle, ownership, or incident policy changes.

For material conclusions, seek disconfirming evidence, distinguish observations from hypotheses and recommendations, record tradeoffs and uncertainty, and note confidence, freshness, and source independence.

## Related skills and conflicts

Related: `api-contract-compatibility`, `observability-and-instrumentation`, `secure-coding-review`, `dependency-security-audit`, `performance-regression-analysis`, `knowledge-maintenance`, and `repository-change-verification`. This skill does not authorize production changes, bypass approvals, or claim rollback safety without checking data and external side effects.
