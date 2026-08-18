---
name: privacy-and-data-handling
description: Review software changes that collect, use, store, transmit, log, infer, share, or delete personal or sensitive data. Use to reduce privacy risk through purpose limitation, minimization, access control, retention, redaction, and lifecycle-aware design.
---

Lifecycle: `draft`

# Privacy and Data Handling

## Purpose and scope

Reduce problems individuals may experience from data processing while preserving the stated product purpose. This skill covers engineering decisions across collection, use, storage, sharing, inference, access, retention, and disposal; it does not provide legal advice or determine jurisdiction-specific compliance.

## Triggers and prerequisites

Trigger when a change handles identifiers, account data, content, location, health or financial information, telemetry, logs, recordings, inferred attributes, model prompts/outputs, exports, or deletion/access workflows. Prerequisites: purpose, data subjects and roles, data classification, processing flow, retention/deletion policy, recipients, deployment jurisdictions, security controls, and privacy or legal owner where required.

## Decision criteria

- Collect and retain the minimum data needed for a stated purpose and duration; convenience is not a purpose.
- Treat derived, linked, pseudonymous, and “non-sensitive” data as potentially identifying when combined with other data.
- Access, sharing, logging, and model/tool exposure are data processing events that need explicit boundaries and accountability.
- De-identification reduces risk but is not automatically irreversible; do not claim anonymity without evidence appropriate to the threat model.

## Procedure

1. State the user-facing purpose and expected benefit. Inventory each data field, source, transformation, recipient, storage location, access path, inference, log, export, backup, and deletion path.
2. Classify data and identify affected individuals, vulnerable groups, reasonable expectations, misuse consequences, and cross-system linkage or re-identification risks.
3. Challenge necessity: remove fields, shorten retention, aggregate, redact, process locally, or use a less identifying representation when the purpose still works. Record why each retained field is needed.
4. Define access and sharing boundaries by role, tenant, purpose, environment, and support/debugging workflow. Check exports, analytics, model/tool calls, logs, backups, and third-party processors.
5. Define lifecycle behavior: collection notice or control where applicable, correction, access, export, retention, deletion, legal hold, backup expiry, and recovery. Make failure and partial deletion visible.
6. Check implementation for accidental collection, secrets or personal data in logs, broad queries, implicit joins, unsafe caches, copied environments, verbose errors, analytics defaults, and data crossing trust or jurisdiction boundaries.
7. Test representative and adversarial cases: unauthorized subject, wrong tenant, deleted record, linked identifiers, redaction failure, export scope, retention boundary, backup restore, and downstream failure. Inspect actual payloads where safe.
8. Review residual risk and tradeoffs with the privacy/security owner when impact, sensitivity, scale, or uncertainty warrants escalation. Do not substitute an engineering assumption for required review.
9. Record purpose, fields and flows, controls, evidence, untested paths, retention/deletion assumptions, residual risk, owner, and the trigger for re-review.

## Examples and counterexamples

Good: A diagnostic event records a bounded operation type and coarse outcome, excludes raw user content and identifiers not needed for the question, applies retention, and documents who can access it.

Bad: Log full requests “temporarily” for debugging without redaction, access controls, expiry, or a deletion plan.

Good: A search feature stores a short-lived tokenized identifier only where needed and separately tests tenant isolation, export behavior, and deletion.

Bad: Call data anonymous because names were removed while retaining a uniquely linkable combination of attributes.

## Failure modes and recovery

If purpose, data classification, recipients, or retention is unknown, pause the change and resolve the uncertainty. If sensitive data was exposed or over-collected, contain access, preserve evidence, notify the responsible privacy/security process, and follow incident requirements; do not merely delete the visible log. If deletion is incomplete, identify copies and backups and record the residual state. If a less invasive design cannot meet the purpose, document the tradeoff and obtain the required owner decision.

## Validation evidence and provenance

- The governing research requires explicit uncertainty, source hierarchy, failure recovery, safety evaluation, provenance, and maintenance across an artifact’s lifecycle.
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework): a voluntary risk-management framework for identifying and managing privacy risk across data processing and its ecosystem.
- [NIST Privacy Framework: Getting Started](https://www.nist.gov/privacy-framework/getting-started-0): privacy problems can arise throughout the lifecycle from collection through disposal and can affect individuals and groups.
- Trace privacy claims to the originating framework, policy, or user-impact evidence; copied compliance summaries do not independently establish safety or legality.
- Confidence: medium-high for purpose, minimization, lifecycle, and impact analysis; medium for risk severity and control sufficiency until jurisdiction, threat model, scale, and owner review are known.
- Freshness: review when data flows, models/tools, recipients, jurisdictions, retention policy, security controls, or privacy guidance changes.

## Related skills and conflicts

Related: `secure-coding-review`, `tool-authorization-audit`, `observability-and-instrumentation`, `data-migration-safety`, `api-contract-compatibility`, `requirements-to-acceptance`, and `knowledge-maintenance`. This skill does not authorize collecting data, making legal compliance claims, weakening access controls, or exposing sensitive records for convenience.
