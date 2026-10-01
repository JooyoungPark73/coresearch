# Research design and experiments

Connect an important operating need, workload trend, or failed assumption to a
measured bottleneck, design insight or finding, and a scoped contribution.
Building a system alone does not establish novelty or significance. A measurement
study, benchmark, experience report, or negative result can contribute reusable
knowledge without proposing a new system.

Compare credible alternatives and closest work. Judge importance, tractability,
and novelty separately; identify what would falsify the explanation or make the
contribution unimportant. Astra owns this judgment; workers can gather
baselines, implement bounded components, and execute agreed evaluations.

## Match evidence to the claim

| Research direction | Relevant evaluation controls |
|---|---|
| Conventional systems | Representative workloads and operating envelope; baseline versions, tuning and resource parity; throughput, latency/tails, scale, cost, correctness and reliability as claimed. For distributed systems, state topology, consistency and failure assumptions; for cloud systems, include tenancy, placement and temporal variability. |
| ML systems | Model/data versions, task-quality parity or an explicit quality tradeoff, training/serving configuration, precision, batching, SLOs, latency/throughput, memory, resource and cost accounting. Tie improvements to the systems mechanism and disclose changes in model quality or workload. |

A faster run at lower model quality does not establish equal-quality efficiency.
For workload characterization, establish collection methodology, coverage,
uncertainty, reusable findings and transfer limits. Hardware or simulated results
need platform/configuration disclosure, measurement or simulator validation,
and relevant sensitivity; power or cost claims need explicit accounting assumptions.

For each important claim, identify the comparison, metric and units, controlled
and varied conditions, and the evidence that could support or contradict it.
Distinguish end-to-end benefit from mechanism evidence. Ablations, breakdowns and
sensitivity studies do not alone establish causal identification. Correctness,
performance, reliability and generality need their own supporting evidence.

Specify warmup or steady-state criteria, measurement windows, experimental units,
repetitions/seeds where applicable, aggregation and meaningful uncertainty. Do not
treat correlated samples as independent trials or use an average to justify a
tail-latency claim. Preserve failed, timed-out and censored runs and explain their
treatment. Baseline tuning and exclusions must remain visible.

## Executable work

Define the question, inputs, comparison, observable result, resource budget and
completion criterion in existing configs or notes. Keep commands, code revision
and dirty changes, environment/hardware, resolved configurations, workload/data
versions, metric definitions and raw result paths sufficient to reproduce reported
numbers. Planned results remain planned.

Validate the smallest meaningful path before expensive runs. Testing and repair
follow observed failures and measurement risks. A worker reports actual outcomes;
Astra decides whether they answer the question or expose missing evidence.
A build or smoke test establishes executability, not the empirical claim.

For an autonomous search loop, make the metric/validator executable, separate
tuning from final evaluation, and set a real compute/time/iteration budget and
scientific stop condition. Changing the validator changes the comparison and
belongs to the lead. Preserve prior results and protocol deviations. Use the
host's existing job lifecycle for long runs.

Restricted traces, external publication, production changes and expensive runs
remain subject to the actual authorization and project constraints. A valid
negative finding can complete the research task.
