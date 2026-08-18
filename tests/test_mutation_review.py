import unittest

from scripts.mutation_review import assess_mutations


class MutationReviewTest(unittest.TestCase):
    def test_classifies_all_outcomes(self):
        result = assess_mutations(["killed", "survived", "equivalent", "invalid", "unexecuted"])
        self.assertEqual((result.killed, result.survived, result.equivalent, result.invalid, result.unexecuted), (1, 1, 1, 1, 1))
        self.assertEqual(result.score, 0.5)

    def test_excluded_outcomes_do_not_change_score_denominator(self):
        result = assess_mutations(["killed", "equivalent", "invalid", "unexecuted"])
        self.assertEqual(result.score, 1.0)

    def test_no_valid_mutants_has_no_score(self):
        self.assertIsNone(assess_mutations(["equivalent", "invalid"]).score)

    def test_unknown_status_is_rejected(self):
        with self.assertRaises(ValueError):
            assess_mutations(["passed"])


if __name__ == "__main__":
    unittest.main()
