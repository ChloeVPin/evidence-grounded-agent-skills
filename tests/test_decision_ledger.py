import unittest
import json
from pathlib import Path

from scripts.decision_ledger import (
    PARAPHRASE_MIN_SHARED_TERMS, candidate_metrics, evaluate_labeled_queries,
    find_matching_entries, find_paraphrase_candidates, validate_entry,
)
from scripts.contradiction_policy import Claim, resolve_claims


class DecisionLedgerTest(unittest.TestCase):
    def test_contextual_entry_is_valid(self):
        result = validate_entry({
            "entry_id": "c-1", "cycle_id": "0050", "artifacts": ["skill.md"],
            "claims": ["a", "b"], "outcome": "contextual",
            "evidence": ["different contexts"], "decision": "retain both",
        })
        self.assertTrue(result.valid)

    def test_unresolved_entry_requires_next_action(self):
        entry = {
            "entry_id": "c-2", "cycle_id": "0050", "artifacts": ["skill.md"],
            "claims": ["a", "b"], "outcome": "unresolved",
            "evidence": ["equal strength"], "decision": "defer",
        }
        self.assertFalse(validate_entry(entry).valid)
        entry["next_action"] = "run discriminating experiment"
        self.assertTrue(validate_entry(entry).valid)

    def test_failure_requires_mechanism_correction_and_guard(self):
        entry = {
            "entry_id": "f-1", "cycle_id": "0050", "artifacts": ["skill.md"],
            "claims": ["skill claim"], "outcome": "failure",
            "evidence": ["reproduction"], "decision": "deprecate",
        }
        self.assertFalse(validate_entry(entry).valid)
        entry.update(mechanism="stale assumption", corrective_action="revise skill", regression_trigger="add test")
        self.assertTrue(validate_entry(entry).valid)

    def test_empty_evidence_is_rejected(self):
        result = validate_entry({
            "entry_id": "c-3", "cycle_id": "0050", "artifacts": ["skill.md"],
            "claims": ["a"], "outcome": "supported_refuted",
            "evidence": [], "decision": "accept a",
        })
        self.assertFalse(result.valid)

    def test_missing_cycle_or_artifact_link_is_rejected(self):
        result = validate_entry({
            "entry_id": "c-4", "claims": ["a"], "outcome": "contextual",
            "evidence": ["context"], "decision": "retain",
        })
        self.assertFalse(result.valid)

    def test_archived_contextual_entry_is_valid_and_matches_policy(self):
        path = Path("ledger/decisions/0052-contextual-contradiction.json")
        entry = json.loads(path.read_text())
        result = resolve_claims(
            Claim("a", "low latency", 1), Claim("b", "high throughput", 1),
            discriminating_evidence=False,
        )
        self.assertEqual(result.outcome, "contextual")
        self.assertTrue(validate_entry(entry).valid)
        self.assertEqual(entry["cycle_id"], "0052")

    def test_archived_failure_entry_preserves_correction_and_regression_guard(self):
        path = Path("ledger/decisions/0053-boundary-mutant-failure.json")
        entry = json.loads(path.read_text())
        assessment = validate_entry(entry)
        self.assertTrue(assessment.valid)
        self.assertEqual(entry["outcome"], "failure")
        self.assertIn("zero-value", entry["corrective_action"])
        self.assertIn("survives", entry["regression_trigger"])

    def test_prior_failure_is_found_before_rediscovery(self):
        paths = sorted(Path("ledger/decisions").glob("*-failure.json"))
        entries = [json.loads(path.read_text()) for path in paths]
        entry = next(item for item in entries if item["entry_id"] == "0053-boundary-mutant-failure")
        matches = find_matching_entries(
            entries, "mutation survival is evidence of an incomplete test oracle",
        )
        self.assertEqual([item["entry_id"] for item in matches], [entry["entry_id"]])
        tool_matches = find_matching_entries(
            entries, "wildcard authority can bypass least-privilege boundaries",
        )
        self.assertEqual([item["entry_id"] for item in tool_matches], ["0055-wildcard-authority-failure"])
        self.assertEqual(find_matching_entries(entries, "new failure"), [])

    def test_paraphrase_lookup_returns_candidates_without_merging(self):
        entries = [
            {"entry_id": "boundary", "claims": ["happy-path-only tests can miss a boundary regression"]},
            {"entry_id": "tool", "claims": ["wildcard authority can bypass least-privilege boundaries"]},
        ]
        candidates = find_paraphrase_candidates(
            entries, "missing boundary coverage can let a regression survive",
        )
        self.assertEqual([entry["entry_id"] for entry in candidates], ["boundary"])
        self.assertEqual(
            find_paraphrase_candidates(entries, "database schema migration"), [],
        )

    def test_candidate_metrics_expose_precision_and_recall(self):
        metrics = candidate_metrics({"boundary", "tool"}, {"boundary", "noise"})
        self.assertEqual(metrics["true_positive"], 1)
        self.assertEqual(metrics["false_positive"], 1)
        self.assertEqual(metrics["false_negative"], 1)
        self.assertEqual(metrics["precision"], 0.5)
        self.assertEqual(metrics["recall"], 0.5)

    def test_expanded_labeled_set_measures_current_lookup(self):
        entries = [
            json.loads(path.read_text())
            for path in sorted(Path("ledger/decisions").glob("*-failure.json"))
        ]
        labels = json.loads(Path("ledger/evaluations/0057-paraphrase-labels.json").read_text())
        metrics = evaluate_labeled_queries(entries, labels)
        self.assertEqual(len(labels), 9)
        self.assertEqual(metrics["true_positive"], 7)
        self.assertEqual(metrics["false_positive"], 1)
        self.assertEqual(metrics["false_negative"], 0)
        self.assertAlmostEqual(metrics["precision"], 7 / 8)
        self.assertEqual(metrics["recall"], 1.0)

    def test_adversarial_alias_query_is_only_a_review_candidate(self):
        entries = [{
            "entry_id": "tool",
            "claims": ["wildcard authority can bypass least-privilege boundaries"],
        }]
        candidates = find_paraphrase_candidates(entries, "unrestricted authority decisions")
        self.assertEqual([entry["entry_id"] for entry in candidates], ["tool"])

    def test_threshold_is_explicit_and_conservative(self):
        self.assertEqual(PARAPHRASE_MIN_SHARED_TERMS, 2)
        entries = [{"entry_id": "one", "claims": ["boundary regression"]}]
        self.assertEqual(
            [entry["entry_id"] for entry in find_paraphrase_candidates(entries, "boundary regression")],
            ["one"],
        )

    def test_labeled_metrics_do_not_hide_cross_query_false_positive(self):
        entries = [{"entry_id": "one", "claims": ["boundary regression"]}]
        labels = [
            {"query": "boundary regression", "expected_ids": ["one"]},
            {"query": "boundary regression again", "expected_ids": []},
        ]
        metrics = evaluate_labeled_queries(entries, labels)
        self.assertEqual(metrics["true_positive"], 1)
        self.assertEqual(metrics["false_positive"], 1)
        self.assertEqual(metrics["false_negative"], 0)
        self.assertEqual(metrics["precision"], 0.5)

    def test_explicit_aliases_recall_authorization_variant(self):
        entries = [{
            "entry_id": "tool",
            "claims": ["wildcard authority can bypass least-privilege boundaries"],
        }]
        candidates = find_paraphrase_candidates(
            entries, "unrestricted authorization can escape declared scope",
        )
        self.assertEqual([entry["entry_id"] for entry in candidates], ["tool"])


if __name__ == "__main__":
    unittest.main()
