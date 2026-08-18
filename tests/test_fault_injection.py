import unittest

from fixtures.fault_target import is_non_positive, mutated_is_non_positive
from scripts.mutation_review import assess_mutations


class FaultInjectionTest(unittest.TestCase):
    def test_happy_path_does_not_kill_boundary_mutation(self):
        self.assertFalse(is_non_positive(1))
        self.assertFalse(mutated_is_non_positive(1))
        self.assertEqual(assess_mutations(["survived"]).survived, 1)

    def test_boundary_case_kills_mutation(self):
        self.assertTrue(is_non_positive(0))
        self.assertFalse(mutated_is_non_positive(0))
        self.assertEqual(assess_mutations(["killed"]).killed, 1)


if __name__ == "__main__":
    unittest.main()
