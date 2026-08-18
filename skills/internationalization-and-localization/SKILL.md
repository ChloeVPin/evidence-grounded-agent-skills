---
name: internationalization-and-localization
description: Design and review software for multiple languages, locales, scripts, regions, calendars, currencies, units, and text directions. Use when an AI coding agent adds user-facing text, formatting, sorting, input, translation, or locale-sensitive behavior.
---

Lifecycle: `draft`

# Internationalization and Localization

## Purpose and scope

Make software behave correctly across supported languages, locales, scripts, regions, and cultural conventions without making one locale an invisible default. This skill covers internationalization design, localization integration, and test planning; it does not replace professional translation, language-community review, legal localization requirements, or product decisions about supported locales.

## Triggers and prerequisites

Trigger when changing user-facing text, dates, times, numbers, currency, units, sorting, search, parsing, input validation, layout, text direction, pluralization, calendars, time zones, or translation resources. Prerequisites: supported locales and fallback policy, target platforms, message/catalog format, formatting library/data version, product terminology, and representative localized content.

## Decision criteria

- Store and transmit canonical values; localize presentation at the user or audience boundary.
- Locale is not the same as language: region, script, calendar, numbering system, time zone, and user preference can independently affect behavior.
- Use locale data and message-formatting facilities rather than hard-coded punctuation, word order, plural rules, or assumptions about names and addresses.
- Translation completeness and grammatical correctness are distinct from layout, accessibility, security, and semantic correctness.

## Procedure

1. Identify user-visible strings and locale-sensitive values, their source meaning, context, placeholders, units, time zone, direction, and fallback behavior. Mark content that must not be translated or reformatted.
2. Define canonical storage and wire formats separately from localized display and input. Specify precision, rounding, timezone semantics, parsing strictness, collation, and invalid-input behavior.
3. Use established Unicode/CLDR-aware libraries and locale identifiers. Keep translations, plural/select rules, number/date/currency formats, and terminology in maintainable resources rather than scattered literals.
4. Design for text expansion, line wrapping, missing translations, long names, combining characters, non-Latin scripts, right-to-left direction, bidirectional isolation, font fallback, and input method behavior.
5. Test representative and adversarial locales: different decimal/group separators, calendars, time zones, plural categories, scripts, directions, long and short translations, missing resources, daylight-saving transitions, and Unicode edge cases.
6. Check sorting, searching, case conversion, normalization, collation, identifiers, and security-sensitive comparisons with the correct semantics. Do not use display labels or locale-dependent strings as stable identifiers.
7. Review translated messages for placeholder preservation, gender/plural context, accessibility, error meaning, date/time ambiguity, and cultural or domain terminology. Treat machine translation as a draft requiring review where impact warrants it.
8. Verify that fallback, resource loading, caching, and version changes are observable and do not silently mix incompatible message or formatting data.
9. Record supported locales, known exclusions, source terminology, library/data versions, test matrix, unresolved language questions, confidence, and the trigger for revalidation.

## Examples and counterexamples

Good: Store an instant in a canonical representation and render it using the user’s time zone and locale, with tests around daylight-saving transitions and ambiguous local input.

Bad: Store a formatted date string such as `03/04/25` and assume every user interprets it the same way.

Good: Format a currency amount with locale data, explicit currency and rounding rules, and tests for zero, negative, large, and fractional values.

Bad: Replace a decimal point, add a currency symbol, or pluralize by concatenating strings designed for one language.

Good: Apply direction-aware layout and isolate embedded left-to-right values in right-to-left text, then test keyboard navigation and screen-reader output.

Bad: Mirror the entire interface or reverse strings without checking semantic order and bidirectional text behavior.

## Failure modes and recovery

If supported locales or terminology are unknown, narrow the claim and ask the product or language owner. If a library lacks required locale data, do not silently approximate culturally meaningful output; document the limitation or choose a supported fallback. If parsing is ambiguous, reject or request clarification rather than guessing. If a translation changes meaning, pause release of the affected content and obtain qualified review.

## Validation evidence and provenance

- The governing research emphasizes adaptable taxonomies, explicit uncertainty, temporal maintenance, primary evidence, and distinguishing facts from conventions.
- [Unicode UTS #35 / LDML](https://www.unicode.org/reports/tr35/): normative locale data and algorithms covering identifiers, numbers, dates, collation, calendars, keyboards, and message formatting through CLDR.
- [Unicode CLDR](https://cldr.unicode.org/): maintained locale data used by major software systems and updated through an open review process.
- Label observed formatting or translation behavior separately from language hypotheses and localization recommendations; repeated examples from one locale are not independent evidence for another.
- Confidence: high for canonical-data and locale-data principles; medium for language-specific wording, cultural fit, and coverage until qualified review and representative users are involved.
- Freshness: review when Unicode/CLDR data, supported locales, formatting libraries, terminology, translation resources, or user populations change.

## Related skills and conflicts

Related: `accessibility-review`, `api-contract-compatibility`, `privacy-and-data-handling`, `requirements-to-acceptance`, `regression-test-design`, `observability-and-instrumentation`, and `knowledge-maintenance`. This skill does not authorize hard-coded locale assumptions, exposing personal data for localization, or claiming translation quality from automated output alone.
