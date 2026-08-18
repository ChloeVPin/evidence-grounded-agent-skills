import unittest

from scripts.cycle_policy import MODES, assess_cycle


class CyclePolicyTest(unittest.TestCase):
    def test_all_operating_modes_are_supported(self):
        for mode in MODES:
            self.assertTrue(assess_cycle(mode, quality_delta=1, next_action=True).continue_work)

    def test_repeated_no_gain_reprioritizes(self):
        result = assess_cycle(
            "exploration", quality_delta=0, next_action=True, consecutive_no_gain=2,
        )
        self.assertFalse(result.continue_work)
        self.assertIn("re-prioritize", result.reason)

    def test_blocker_stops_cycle_with_reason(self):
        result = assess_cycle("maintenance", quality_delta=0, next_action=True, blocker=True)
        self.assertFalse(result.continue_work)
        self.assertIn("blocker", result.reason)

    def test_unknown_mode_is_rejected(self):
        with self.assertRaises(ValueError):
            assess_cycle("busywork", quality_delta=1, next_action=True)


if __name__ == "__main__":
    unittest.main()
