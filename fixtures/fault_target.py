"""Tiny target used to demonstrate boundary-sensitive mutation testing."""


def is_non_positive(value: int) -> bool:
    return value <= 0


def mutated_is_non_positive(value: int) -> bool:
    """Plausible mutant: excludes the boundary value zero."""
    return value < 0
