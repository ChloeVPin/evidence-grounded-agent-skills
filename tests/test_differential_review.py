import unittest

from scripts.differential_review import compare


def reference(value):
    return value >= 0


def equivalent_candidate(value):
    return not value < 0


def divergent_candidate(value):
    return value > 0


class DifferentialReviewTest(unittest.TestCase):
    def test_equivalent_implementation_has_no_divergence(self):
        result = compare(reference, equivalent_candidate, [-1, 0, 1])
        self.assertTrue(result.equivalent)
        self.assertEqual(result.checked, 3)

    def test_happy_path_can_miss_boundary_divergence(self):
        result = compare(reference, divergent_candidate, [1])
        self.assertTrue(result.equivalent)

    def test_boundary_input_exposes_divergence(self):
        result = compare(reference, divergent_candidate, [0])
        self.assertFalse(result.equivalent)
        self.assertEqual(result.divergences, ((0, True, False),))


if __name__ == "__main__":
    unittest.main()
