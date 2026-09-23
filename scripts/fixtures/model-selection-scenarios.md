# Assignment model-selection checks

For an independent decision test, give only the request and the installed
`coresearch/references/agent-routing.md` to an evaluator. Ask for role, model,
effort, rationale, validator, and escalation condition without executing work.
Do not give the assessment column to the evaluator. These cases assess policy
decisions, not measured capability or cost.

| Request | Assessment |
| --- | --- |
| Start a durable mission with a clear evaluation contract and validated work to integrate. | Parent Sol medium; every worker still gets explicit model and effort. |
| Replan a mission with complex dependencies but a settled scientific contract. | Sol high is appropriate; preserve dependencies and validators. |
| Evidence conflicts require changing the scientific evaluation contract. | Request Astra planning or verification and inspect the evidence; do not silently switch the parent session. |
| Extract supplied DOI and year fields from 200 complete structured records; validate exact equality against source fields. | Luna is appropriate for a directly checkable transformation; preserve missing values and provenance. |
| Implement a clearly specified parser extension in two owned files with existing input/output fixtures and tests. | Sol medium is a reasonable initial choice; bounded scope, testable outputs, explicit effort. |
| Investigate a multi-module parsing failure and propose a minimal fix after two observed failures, with logs and reproduction supplied. | Sol or Astra depending on uncertainty; debugger remains read-only, no blind retry ladder. |
| Independently decide whether a throughput comparison supports a causal claim despite workload and quality confounds. | Astra verifier; evidence, ambiguity, and error consequence outweigh token price. |
| A Luna metadata transformation cannot read its input because the file is missing. | Resolve/report the missing input rather than escalating through models. |
| A Sol implementation passes simple tests but demonstrably fails a supplied interacting edge case after bounded diagnosis. | Consider Sol at higher effort or Astra for a new scoped attempt within remaining budget; preserve failure evidence, new attempt ID, and prior requested routing. |
| The requested Luna model is unavailable. Astra is accessible and within the approved fallback budget. | Record the failed attempt; explicitly request Astra in a new attempt without marking the Luna route verified. |

## Comparative task evaluation

Before claiming quality, cost, or latency improvements, run representative
assignments with the same input artifacts, validators, permissions, and output
requirements across Astra, Sol, and Luna. Fix task-specific effort settings
before comparison and include Astra at low effort as a baseline. Use isolated
workspaces, preserve failures, and include parent correction and retries in total
work. Record requested/observed model and effort, correctness verdicts, wall time,
available token usage, total cost under the actual billing surface, and parent
correction effort. Missing usage or billing metadata remains unknown.

Do not infer task quality from an echo probe or a selection response. Live
named-role availability checks use only the explicit
`harness doctor --strict --surface codex --probe-models --probe-role <role>
--probe-model <approved-model>` path. Task comparisons are separate, authorized
experiment runs with declared budgets and terminal evidence; do not run them as
part of offline validation or claim they have run from fixture results.
