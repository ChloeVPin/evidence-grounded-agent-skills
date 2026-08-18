#!/usr/bin/env python3
"""Bind knowledge revalidation to the complete attested review flow."""
from scripts.lifecycle_policy import decide_lifecycle
from scripts.review_change import review_change


def revalidate(current_state: str, freshness: str, review_record: dict):
    review = review_change(review_record)
    return decide_lifecycle(
        current_state=current_state,
        freshness=freshness,
        revalidation_evidence=review.accepted,
    )
