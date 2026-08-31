# Causal reasoning

Load only for causal-hypothesis planning or causal-claim audit. Maintain one
outcome-centered model; the views below are projections of that model, not
separate explanations.

## Model

Record the outcome and all relevant treatments or interventions, mediators,
moderators, confounders, proxies, colliders, latent variables, measurement
variables, and selection variables. Include workload, configuration, resource,
placement, timing, quality, simulator, or modeling effects when they could
explain a systems result.

Produce three views:

1. **Competing explanations:** hypothesis, proposed cause, mechanism, predicted
   outcome, boundary conditions, and distinguishing evidence.
2. **Causal-edge ledger:** `{from, to, relationship, evidence,
   identification_strategy, confidence}`.
3. **Proxy audit:** target construct, observed proxy, why it is used, failure
   mode, and alternative measurement.

Every competing explanation needs a distinguishing prediction. Every edge
labeled causal needs an identification strategy that addresses credible
alternatives. Without one, downgrade the edge to `hypothesized`,
`correlational`, or `measurement` and record that provenance. A proxy must not
silently become the target construct.

## Planning versus audit

Planning proposes the smallest feasible intervention, natural experiment, or
controlled mechanism test and records
`hypothesis_state.{candidates,distinguishable,unidentifiable}`. If no feasible
identification exists, use `unidentifiable`, not causal language.

Audit tests an existing claim against the same model. It reports the strongest
credible alternative, identification strengths and failures, proxy risks,
allowed wording, and evidence needed. Audit does not generate a new research
direction unless the user asks to return to design.
