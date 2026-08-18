import unittest
import json
from pathlib import Path

from scripts.decision_ledger import validate_entry
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


if __name__ == "__main__":
    unittest.main()
