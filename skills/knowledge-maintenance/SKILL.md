---
name: knowledge-maintenance
description: Keep coding-agent skills and guidance current by tracking provenance, freshness, deprecation, supersession, contradictions, and review triggers. Use when evidence, dependencies, versions, or failures change.
---

# Knowledge Maintenance and Freshness

Lifecycle: `draft`

## Purpose and scope

Use this skill to keep skills, evidence, decisions, and taxonomic relationships current over time. It identifies review triggers, freshness windows, deprecation, supersession, and uncertainty. A freshness signal is not proof that knowledge is false; it determines when evidence must be rechecked.

## Triggers and prerequisites

Trigger when a review date arrives, a dependency/tool/version changes, a source is deprecated or superseded, a failure contradicts a skill, or a new authoritative source changes the decision boundary. Prerequisites: artifact provenance, lifecycle state, last validation, review window, owner/process, and known dependents.

## Decision criteria

Retain, revise, deprecate, or supersede knowledge according to current authoritative evidence, contradiction status, dependent impact, and confidence. Staleness or missing evidence lowers trust; it does not by itself prove the guidance false.

## Procedure

1. Classify the artifact's temporal behavior: stable, slowly changing, or fast-changing. Choose a review window proportional to risk and change rate.
2. Record provenance, publication/version date, last validation date, next review trigger, confidence, and known dependent artifacts.
3. Monitor authoritative sources and repository failures for changes, contradictions, advisories, and deprecation signals. Trace repeated claims back to their source.
4. When a trigger fires, compare the current artifact with new evidence. Preserve the old decision and record what changed, why, and which dependents may be affected.
5. Mark artifacts `experimental`, `validated`, `trusted`, `deprecated`, or `superseded` according to evidence. Do not silently overwrite a deprecated decision.
6. For deprecation, record effective date or review deadline, replacement/migration guidance when available, and the limits of any sunset signal. Treat dates as signals, not guarantees.
7. Re-run relevant validation and differential checks. Lower confidence or restrict use when evidence is stale, contradictory, unavailable, or not independently verifiable.
8. Record the maintenance decision, evidence, residual uncertainty, next trigger, and impact on taxonomy and dependents.

## Acceptance checklist

- [ ] Temporal class and review window are explicit.
- [ ] Provenance, confidence, last validation, and next trigger are recorded.
- [ ] Authoritative source and failure monitoring are identified.
- [ ] Changes preserve prior decisions and dependent-impact analysis.
- [ ] Deprecated or superseded artifacts are retained with rationale.
- [ ] Replacement or migration guidance is recorded when available.
- [ ] Stale, contradictory, or unavailable evidence lowers confidence or blocks trust.
- [ ] Maintenance result and next trigger are auditable.

## Examples and counterexamples

Good: A tool version changes a documented API; preserve the old skill, record the affected boundary, revalidate dependents, and supersede it only after evidence.

Bad: Update the wording silently because the new version is assumed to be compatible.

## Failure modes and recovery

If freshness cannot be determined, label it unknown and keep the artifact below trusted status. If a source disappears, preserve the last evidence and seek an independent replacement. If evidence conflicts, do not average or silently choose; open a contradiction-resolution cycle. If a replacement is not equivalent, record the decision boundary rather than treating it as a drop-in successor.

## Validation evidence and provenance

Record confidence and freshness for retained knowledge, label observations, hypotheses, and recommendations separately, and trace corroboration to independent origins.

- [RFC 9745: Deprecation HTTP Response Header Field](https://www.rfc-editor.org/rfc/rfc9745.html): deprecation signaling and documentation/migration links.
- [RFC 8594: Sunset HTTP Header Field](https://www.rfc-editor.org/info/rfc8594/): sunset signaling and its status as a hint rather than a guarantee.
- [NIST AI RMF GenAI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf): monitoring, incident tracking, and measurable continual improvement.
- Label freshness measurements and source changes as observations, explanations of impact as hypotheses, and lifecycle actions as recommendations until evidence supports them.

Confidence: medium-high for lifecycle principles; medium for default review windows, which are domain- and risk-dependent.

For material conclusions, seek disconfirming evidence, distinguish observations from hypotheses and recommendations, record tradeoffs and uncertainty, and note confidence, freshness, and source independence.

## Related skills and conflicts

Related: evidence-attestation, dependency-security-audit, differential-patch-review, and cycle-state. This skill does not authorize silent deletion or override a source owner's deprecation policy.
