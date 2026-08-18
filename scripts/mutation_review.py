#!/usr/bin/env python3
"""Classify mutation outcomes without treating the score as correctness."""
from dataclasses import dataclass

STATUSES = {"killed", "survived", "equivalent", "invalid", "unexecuted"}


@dataclass(frozen=True)
class MutationAssessment:
    killed: int
    survived: int
    equivalent: int
    invalid: int
    unexecuted: int

    @property
    def score(self) -> float | None:
        denominator = self.killed + self.survived
        return self.killed / denominator if denominator else None


def assess_mutations(statuses: list[str]) -> MutationAssessment:
    invalid_statuses = sorted(set(statuses) - STATUSES)
    if invalid_statuses:
        raise ValueError(f"unknown mutation status: {invalid_statuses[0]}")
    return MutationAssessment(
        killed=statuses.count("killed"),
        survived=statuses.count("survived"),
        equivalent=statuses.count("equivalent"),
        invalid=statuses.count("invalid"),
        unexecuted=statuses.count("unexecuted"),
    )
