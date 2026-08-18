---
name: accessibility-review
description: Review user-facing software changes for accessibility barriers across semantics, keyboard and other input, focus, structure, content, feedback, and assistive technology behavior. Use for web, mobile, desktop, CLI, and interactive UI changes; adapt the checks to the platform.
---

Lifecycle: `draft`

# Accessibility Review

## Purpose and scope

Find and reduce barriers that prevent people with disabilities from perceiving, operating, understanding, or using software. This skill covers accessible behavior and review planning; it does not certify legal conformance, replace disabled-user testing, or assume that an automated scan detects every barrier.

## Triggers and prerequisites

Trigger when changing user interfaces, interaction flows, forms, navigation, media, documents, authentication, notifications, errors, keyboard behavior, or content presentation. Prerequisites: target platform and assistive technologies, supported browsers/devices where relevant, user/task flows, design constraints, accessibility policy or conformance target, and the complete change.

## Decision criteria

- Evaluate the user task and interaction path, not only markup or visual appearance.
- Accessibility requires perceivable content, operable controls, understandable behavior, and robust interoperability; a passing automated rule set is only partial evidence.
- Use native platform semantics and controls when they express the intended behavior; custom widgets carry their own keyboard, focus, name, state, and event obligations.
- Do not infer disability needs from a single persona or declare a design accessible without checking affected users and assistive technology behavior.

## Procedure

1. Identify affected tasks, users, content, input modes, output modes, and failure states. Define the applicable platform guidance and target conformance level without overstating it.
2. Inspect structure and semantics: headings, landmarks, labels, names/roles/states, language, reading order, relationships, tables, alternatives for non-text content, and meaningful document structure.
3. Exercise the task without a mouse or pointer. Check focus visibility and order, keyboard operability, shortcuts, traps, drag alternatives, target size, timing, cancellation, and touch or switch input where relevant.
4. Check presentation and perception: contrast, text resizing/reflow, zoom, motion, color independence, captions/transcripts, audio control, and state/error information that is not conveyed by color alone.
5. Check forms and dynamic behavior: instructions, required fields, input purpose, validation, error identification, recovery, status announcements, focus movement, dialogs, loading, and content changes for assistive technologies.
6. Test with representative browsers, devices, accessibility settings, and assistive technologies where applicable. Combine manual task testing, automated checks, source inspection, and user feedback; record each method’s blind spots.
7. Check authentication, privacy, security, and performance tradeoffs. Do not remove accessible recovery or expose sensitive information merely to simplify an interaction.
8. Classify findings by blocked task, affected users, reproducibility, conformance impact, and practical risk. Fix the underlying interaction or provide an equivalent path; do not hide the problem with cosmetic changes.
9. Re-run the affected task and nearby boundaries: empty/error states, validation failures, dynamic updates, zoom/reflow, keyboard-only use, reduced motion, high contrast, localization, and slow or interrupted loading as relevant.
10. Record evidence, tools and assistive technologies used, untested combinations, residual barriers, target conformance, confidence, and the next review trigger.

## Examples and counterexamples

Good: A custom dialog has a programmatic name, correct focus entry and return, keyboard escape behavior where appropriate, background interaction blocked, announced errors, and tests for slow loading and validation failure.

Bad: Add an ARIA role to a clickable `div` and call the dialog accessible without implementing focus, keyboard, state, and announcement behavior.

Good: A chart provides a meaningful text summary or data table and does not rely on color alone to communicate trends.

Bad: Increase contrast in a screenshot while leaving the chart’s data inaccessible to screen readers or keyboard users.

## Failure modes and recovery

If the platform, users, or conformance target is unknown, narrow the claim and ask for the missing context. If automated tooling passes but a manual task fails, trust the observed barrier and investigate the interaction. If a barrier cannot be fixed immediately, provide an equivalent usable path, document the limitation and owner, and do not claim conformance. If testing requires assistive technology or user expertise that is unavailable, record the gap and seek qualified review.

## Validation evidence and provenance

- The governing research requires explicit scope, failure modes, adversarial review, uncertainty, primary evidence, and validation beyond superficial activity metrics.
- [W3C WCAG 2 Overview](https://www.w3.org/WAI/standards-guidelines/wcag/): WCAG 2.2 is a stable technical standard organized around perceivable, operable, understandable, and robust principles with testable success criteria.
- [W3C WCAG 2.2 Recommendation](https://www.w3.org/TR/WCAG22/): normative success criteria and conformance framework.
- [W3C WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/): interaction and keyboard patterns for accessible custom widgets.
- Treat standards, automated results, and user reports as distinct evidence only when their provenance is independent; repeated guidance from one source is one line of evidence.
- Confidence: medium-high for the review principles; medium for any conformance or barrier conclusion until the target platform, assistive technology coverage, and affected-user testing are known.
- Freshness: review when WCAG/platform guidance, supported devices, interaction patterns, or accessibility policy changes.

## Related skills and conflicts

Related: `api-contract-compatibility`, `requirements-to-acceptance`, `secure-coding-review`, `regression-test-design`, `observability-and-instrumentation`, `performance-regression-analysis`, and `repository-change-verification`. This skill does not authorize claiming legal conformance, replacing disabled-user evaluation with automation, or weakening accessibility to satisfy a visual or performance target.
