---
name: agent-evaluation-and-benchmarking
description: Design and interpret evaluations of AI coding-agent behavior across realistic tasks, correctness, safety, usefulness, and maintainability. Use when creating benchmarks, comparing agents or skills, measuring regressions, or making claims about agent capability.
---

Lifecycle: `draft`

# Agent Evaluation and Benchmarking

## Purpose and scope

Measure whether an AI coding agent improves outcomes on a defined task population without confusing activity, benchmark gaming, or one successful patch with general capability. This skill covers evaluation design, execution, analysis, and claims; it does not replace human review, domain safety assessment, or a production service-level evaluation.

## Triggers and prerequisites

Trigger when comparing agents, models, prompts, skills, tools, workflows, or versions; when a benchmark is proposed; or when an agent claim needs evidence. Prerequisites: target users and tasks, baseline or comparator, task sampling frame, environment, access boundaries, success criteria, evaluator/oracle, resources, and intended decision.

## Decision criteria

- Define success across correctness, completeness, relevance, actionability, robustness, safety, maintainability, and cost/time according to the task’s risk and objective; do not reduce quality to completion or pass rate.
- The evaluation population and sampling process determine what the result supports. A benchmark does not establish performance outside its distribution.
- Separate agent behavior from evaluator behavior, environment failures, flaky tasks, invalid tasks, and unobservable outcomes.
- Prefer independent or held-out tasks and evaluators; repeated attempts or leaked reference answers can inflate results.

## Procedure

1. State the decision the evaluation will inform and the falsifiable claim. Define the target task distribution, exclusions, baseline, comparison, budget, allowed tools, and safety boundaries.
2. Construct or sample tasks that represent real use, difficulty, languages/frameworks, failure modes, security boundaries, and negative or ambiguous cases. Keep evaluation inputs independent from training, prompt construction, and tuning where possible.
3. Define observable acceptance criteria and an evaluation protocol before running candidates. Specify exact outputs, tests, human rubric, reviewer independence, timeouts, retries, and treatment of partial or unsafe work.
4. Protect integrity: isolate secrets and production systems, prevent task leakage, control environment versions, record agent/tool/model revisions, and detect attempts to modify the evaluator or hide failures.
5. Run baseline and candidates under comparable conditions. Capture raw artifacts, patches, tests, tool calls, failures, costs, time, refusals, and safety incidents—not only aggregate scores.
6. Classify outcomes: correct, partially correct, incorrect, unsafe, incomplete, invalid task, infrastructure failure, evaluator disagreement, or unknown. Do not silently convert missing evidence into failure or success.
7. Analyze variance, confidence, task-level distribution, subgroup/regime performance, error modes, and tradeoffs. Check whether a small number of tasks, retries, graders, or easy wins dominate the result.
8. Seek disconfirming evidence: held-out adversarial tasks, unseen repositories, alternate evaluators, mutation or differential checks, human review, and cases where the claimed improvement should not apply.
9. Decide what the evidence supports: adopt, experiment, restrict, investigate, or reject. State the claim’s scope, limitations, residual risk, reproducibility, and next review trigger.

## Examples and counterexamples

Good: Compare two coding agents on held-out tasks with independent correctness review, security checks, cost/time, regression behavior, and task-level failures reported rather than only average pass rate.

Bad: Claim an agent is better because it produced more patches or passed a benchmark whose reference tests it could inspect.

Good: Report that an agent improved performance on Python bug fixes but had insufficient evidence on frontend, concurrency, or security tasks.

Bad: Generalize from a narrow benchmark to “works for coding” without checking task distribution or evaluator blind spots.

## Failure modes and recovery

If no trustworthy oracle or representative task sample exists, narrow the claim and improve the evaluation before ranking agents. If evaluator disagreement is high, investigate the rubric and task ambiguity rather than averaging it away. If task leakage or environment drift is discovered, quarantine affected results and rerun or label them. If a metric improves while safety, maintainability, or failure severity worsens, reject the metric as the optimization target.

## Validation evidence and provenance

- The governing research requires meaningful progress measures, adversarial validation, empirical failure analysis, benchmark anti-gaming, source independence, and explicit uncertainty.
- [SWE-bench](https://www.swebench.com/): a benchmark for evaluating language models on real GitHub software-engineering issues, with task and evaluation assumptions that must be understood before generalizing.
- [Are “Solved Issues” in SWE-bench Really Solved Correctly?](https://arxiv.org/abs/2503.15223): evidence that benchmark-passing patches can still contain behavioral discrepancies, motivating broader evaluation.
- Label task outcomes and measurements as observations, causal explanations as hypotheses, and adoption decisions as recommendations; trace repeated benchmark claims to independent datasets and evaluators.
- Confidence: high for distribution-aware and multi-dimensional evaluation principles; medium for any benchmark’s external validity until its sampling, leakage, evaluator, and environment limits are examined.
- Freshness: review when models, tools, task distributions, evaluators, benchmarks, or safety expectations change.

## Related skills and conflicts

Related: `test-effectiveness-analysis`, `regression-test-design`, `differential-patch-review`, `performance-regression-analysis`, `secure-coding-review`, `prompt-injection-resistance`, `skill-quality-review`, and `knowledge-maintenance`. This skill does not authorize benchmarking on production data, exposing secrets, optimizing for a misleading metric, or claiming general capability from a narrow result.
