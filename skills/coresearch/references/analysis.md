# Analytical research

Choose the analysis that resolves the uncertainty. These lenses are independent;
there is no mandatory gap-to-causal-to-review pipeline.

**Gaps and contradictions.** Distinguish a missing paper from an important,
tractable question. Compare the nearest alternatives and seek work that would
invalidate the novelty claim. When results disagree, separate populations,
measurement, interventions, assumptions, and boundary conditions before proposing
a reconciling mechanism. State a discriminating prediction rather than forcing
agreement. Keep rejected directions and the evidence that ruled them out.

**Causal explanation.** Specify the estimand and competing mechanisms. Make
confounding, selection, measurement, and identification assumptions explicit;
a diagram is useful when it clarifies them. Separate identified effects from
assumption-dependent interpretations. Suggest an intervention or observation
that distinguishes live explanations; do not turn an association into causation.

When interpreting measurements, examine workload mix, resource allocation,
configuration, placement, timing, model quality, and simulator assumptions as
possible competing explanations where relevant. An ablation can support a
mechanism interpretation without ruling out these alternatives. Tie criticism
to the affected claim and conclude with the strongest defensible wording and
the smallest discriminating measurement.

**Measurement and tradeoffs.** Check whether the metric measures the claimed
benefit: throughput under a latency SLO, tail behavior rather than only a mean,
or efficiency at comparable task quality. Inspect workload coverage, sampling,
correlated trials, aggregation, exclusions and failed runs. Separate an effect
within the measured operating envelope from a claim about other loads, hardware
or deployments. Distinguish a mechanism's benefit from its overhead and limits.

**Methodology and evidence-chain audit.** Examine whether the design and measures
support the stated claim; then examine how the evidence was selected. Look for
shared datasets/groups, publication and retrieval bias, circular citations,
missing counterevidence, and methodological weaknesses that survive replication.
Distinguish a flaw in the study from a flaw in a later interpretation of it.

A decision-ready result identifies the supported conclusion, its source locators,
the strongest alternative or counterexample, unresolved assumptions, and the
next observation that would materially change the decision. This can be a short
answer; it does not require a new ledger, scorecard, or worker for each lens.
