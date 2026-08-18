#!/usr/bin/env python3
"""Compare observable outputs of candidate and reference implementations."""
from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True)
class DifferentialResult:
    checked: int
    divergences: tuple[tuple[object, object, object], ...]

    @property
    def equivalent(self) -> bool:
        return not self.divergences


def compare(
    reference: Callable[[object], object], candidate: Callable[[object], object],
    inputs: Iterable[object],
) -> DifferentialResult:
    divergences = []
    checked = 0
    for value in inputs:
        expected = reference(value)
        actual = candidate(value)
        checked += 1
        if expected != actual:
            divergences.append((value, expected, actual))
    return DifferentialResult(checked, tuple(divergences))
