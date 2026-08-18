# Cycle 0027 — Live Dependency Lookup Boundary

Date: 2026-08-18
Status: in progress

## Question

What is the smallest trustworthy boundary for incorporating live registry and vulnerability-advisory lookups into Hermes evidence?

## Decision

_To be determined._

## Evidence and provenance

_Record adapter contract and tests for success, unavailable, and contradictory lookup results._

## Disconfirming evidence sought

_Do not turn network failure or an empty response into verified status._

## Next action

Define a lookup adapter that returns explicit verified, vulnerable, or unknown results with source, timestamp, and raw-output digest.
