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

    def test_matching_return_but_changed_error_is_divergence(self):
        def reference_contract(value):
            return {"value": value, "error": None, "effects": ["read"]}

        def candidate_contract(value):
            return {"value": value, "error": "warning", "effects": ["read"]}

        result = compare(reference_contract, candidate_contract, [1])
        self.assertFalse(result.equivalent)

    def test_matching_return_but_changed_side_effect_is_divergence(self):
        def reference_contract(value):
            return {"value": value, "error": None, "effects": ["read"]}

        def candidate_contract(value):
            return {"value": value, "error": None, "effects": ["read", "write"]}

        result = compare(reference_contract, candidate_contract, [1])
        self.assertFalse(result.equivalent)


if __name__ == "__main__":
    unittest.main()
