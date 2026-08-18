import unittest

from scripts.decision_ledger import validate_entry


class DecisionLedgerTest(unittest.TestCase):
    def test_contextual_entry_is_valid(self):
        result = validate_entry({
            "entry_id": "c-1", "claims": ["a", "b"], "outcome": "contextual",
            "evidence": ["different contexts"], "decision": "retain both",
        })
        self.assertTrue(result.valid)

    def test_unresolved_entry_requires_next_action(self):
        entry = {
            "entry_id": "c-2", "claims": ["a", "b"], "outcome": "unresolved",
            "evidence": ["equal strength"], "decision": "defer",
        }
        self.assertFalse(validate_entry(entry).valid)
        entry["next_action"] = "run discriminating experiment"
        self.assertTrue(validate_entry(entry).valid)

    def test_failure_requires_mechanism_correction_and_guard(self):
        entry = {
            "entry_id": "f-1", "claims": ["skill claim"], "outcome": "failure",
            "evidence": ["reproduction"], "decision": "deprecate",
        }
        self.assertFalse(validate_entry(entry).valid)
        entry.update(mechanism="stale assumption", corrective_action="revise skill", regression_trigger="add test")
        self.assertTrue(validate_entry(entry).valid)

    def test_empty_evidence_is_rejected(self):
        result = validate_entry({
            "entry_id": "c-3", "claims": ["a"], "outcome": "supported_refuted",
            "evidence": [], "decision": "accept a",
        })
        self.assertFalse(result.valid)


if __name__ == "__main__":
    unittest.main()
