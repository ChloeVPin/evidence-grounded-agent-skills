---
name: api-contract-compatibility
description: Design, change, or review APIs and serialized interfaces while making compatibility, versioning, errors, and migration behavior explicit. Use for HTTP, RPC, CLI, event, library, configuration, and file-format interfaces used by other code or people.
---

Lifecycle: `draft`

# API Contract and Compatibility

## Purpose and scope

Make an interface’s observable contract explicit and prevent accidental breakage for callers, consumers, operators, and stored data. This skill covers interface design and evolution; it does not replace domain requirements, security review, performance analysis, or a service owner’s release policy.

## Triggers and prerequisites

Trigger when adding or changing endpoints, function signatures, commands, schemas, events, configuration, serialized data, error responses, or compatibility behavior. Prerequisites: consumers and ownership, current contract or examples, versioning policy, supported environments, data lifecycle, and the intended change.

## Decision criteria

- An interface includes successful results, errors, validation, defaults, ordering, side effects, permissions, limits, timing expectations, and serialization—not only a method name or URL.
- Compatibility is relative to identified consumers and versions; “backward compatible” without a consumer set is an unsupported claim.
- Prefer additive, tolerant, and reversible evolution when consumers cannot migrate atomically; reject ambiguity rather than silently reinterpret data.
- A deprecation or version signal is useful only with an effective boundary, migration path, and owner.

## Procedure

1. Inventory consumers, producers, stored representations, generated clients, documentation, monitoring, and dynamic or out-of-repository callers. Identify who owns each boundary.
2. Write the current and proposed contract: inputs, outputs, required/optional fields, defaults, validation, errors, ordering, idempotency, side effects, limits, permissions, and version semantics.
3. Classify the change for each consumer: additive, behavior change, source incompatible, binary/serialization incompatible, operationally incompatible, or ambiguous. Do not assume an apparently optional field is safe for strict parsers.
4. Define decision boundaries for unknown, missing, null, extra, malformed, duplicate, stale, and future-version values. Specify whether clients reject, ignore, preserve, or migrate them.
5. Choose an evolution path: compatible addition, adapter, explicit version, staged rollout, dual read/write, migration, deprecation, or intentional breaking release. Record why alternatives do not fit.
6. Check security and resource implications at the boundary: authorization scope, data exposure, validation, amplification, rate/size limits, and error detail. Route deeper concerns to the relevant security skill.
7. Verify with representative existing consumers, contract examples, malformed and boundary inputs, old/new version combinations, retries, partial rollout, and rollback or migration recovery where applicable.
8. Compare the changed interface against the baseline and inspect generated artifacts, schemas, clients, documentation, observability, and operational runbooks for drift.
9. Publish the contract and migration/deprecation instructions with owner, effective dates or version boundary, compatibility limits, and review trigger. Preserve old behavior until the stated migration condition is met.

## Examples and counterexamples

Good: Add a response field only after checking strict consumers, documenting its optionality, testing old clients against new responses, and defining when it becomes required.

Bad: Add a field and call it backward compatible because the server still compiles.

Good: Change an event schema through versioned messages or an additive transition with dual consumers and a rollback plan.

Bad: Rename a serialized field and rely on every consumer upgrading at the same instant.

## Failure modes and recovery

If consumers are unknown, treat compatibility as uncertain and use telemetry, repository search, or an explicit version boundary before breaking the interface. If old and new behavior cannot coexist, stage the migration or require an intentional breaking release. If documentation and runtime behavior disagree, report the contract as unresolved and fix the boundary before claiming compatibility. If rollback cannot restore the old contract, document the irreversible migration and require stronger review.

## Validation evidence and provenance

- The governing research emphasizes explicit skill anatomy, dependency graphs, lifecycle/versioning, reversibility, conflict resolution, and maintenance of temporal knowledge.
- [RFC 9110 HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110): standardized method, status, representation, and compatibility semantics for HTTP interfaces.
- [Semantic Versioning 2.0.0](https://semver.org/): a public contract for communicating incompatible, additive, and patch-level changes, subject to its stated assumptions.
- [Google API Design Guide](https://cloud.google.com/apis/design): resource-oriented API design, compatibility, versioning, and evolution guidance.
- Trace compatibility claims to their originating specification or consumer evidence; repeated recommendations copied across guides are not independent confirmation.
- Confidence: medium-high for explicit contract and staged-evolution principles; medium for a particular compatibility classification until actual consumers and deployment constraints are known.
- Freshness: review when consumers, version policy, serialization standards, deployment topology, or migration tooling changes.

## Related skills and conflicts

Related: `requirements-to-acceptance`, `behavior-preserving-refactoring`, `secure-coding-review`, `performance-regression-analysis`, `regression-test-design`, `knowledge-maintenance`, and `repository-change-verification`. This skill does not authorize breaking unknown consumers, exposing data, or treating a version number as a substitute for migration evidence.
