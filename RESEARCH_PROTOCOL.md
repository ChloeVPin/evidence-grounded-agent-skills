# Research Protocol

## Skill research process

1. Define the coding-agent task, scope, and likely failure modes.
2. State one falsifiable question the skill must answer.
3. Prioritize by impact, uncertainty, mistake severity, reuse, and change rate.
4. Gather primary sources first; trace repeated claims to their origin.
5. Separate facts from recommendations and unresolved hypotheses.
6. Write the strongest counterargument and likely failure modes.
7. Build the smallest useful `SKILL.md` or record why no skill should be built.
8. Validate with tests, examples, counterexamples, and adversarial cases.
9. Record the decision, evidence, confidence, and next review trigger.

## Prioritization

Use a qualitative score: `impact × uncertainty × mistake_severity × reuse × change_rate`. Do not use the score as a substitute for judgment; explain the ranking.

## Stopping rules

Stop when the question is answered to the stated confidence, evidence has diminishing returns, or the question is blocked by missing external facts. Record the blocker. Never manufacture skills to preserve activity.

## Maintenance

Review skills when their dependencies change, evidence is superseded, failures recur, or the review date arrives. Deprecated skills remain in the ledger with their reason and replacement.
