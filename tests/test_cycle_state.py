import unittest

from scripts.cycle_state import transition, validate_state


def state():
    return {
        "schema_version": 1,
        "cycle_id": "0016",
        "mode": "maintenance",
        "status": "in_progress",
        "progress": {"quality_delta": 1, "evidence": ["test"]},
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


if __name__ == "__main__":
    unittest.main()
