import unittest

from scripts.cycle_state import transition, validate_state


def state():
    return {
        "schema_version": 1,
        "cycle_id": "0016",
        "mode": "maintenance",
        "status": "in_progress",
        "progress": {
            "quality_delta": 1, "coverage_delta": 0,
            "evidence_quality_delta": 0, "validation_delta": 0,
            "uncertainty_delta": 0, "evidence": ["test"],
        },
        "decision": "reviewing",
        "next_action": "run checks",
    }


class CycleStateTest(unittest.TestCase):
    def test_active_state_is_valid(self):
        self.assertTrue(validate_state(state()).valid)

    def test_completed_transition_is_valid(self):
        result = transition(state(), "completed", "validated", "open next cycle")
        self.assertEqual(result["status"], "completed")

    def test_terminal_state_cannot_continue(self):
        completed = transition(state(), "completed", "validated")
        with self.assertRaisesRegex(ValueError, "terminal"):
            transition(completed, "completed", "again")

    def test_active_state_without_next_action_is_invalid(self):
        current = state()
        current["next_action"] = ""
        self.assertFalse(validate_state(current).valid)

    def test_activity_only_progress_cannot_complete(self):
        current = state()
        current["progress"] = {
            "quality_delta": 0, "coverage_delta": 0,
            "evidence_quality_delta": 0, "validation_delta": 0,
            "uncertainty_delta": 0, "file_count_delta": 4,
            "evidence": ["four files created"],
        }
        with self.assertRaisesRegex(ValueError, "cannot complete"):
            transition(current, "completed", "validated")


if __name__ == "__main__":
    unittest.main()
