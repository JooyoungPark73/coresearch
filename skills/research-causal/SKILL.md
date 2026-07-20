---
name: research-causal
description: Causal Hypothesis Mapper. Represent competing causal explanations over one internal model to prevent correlation-as-mechanism. Produces a competing-hypothesis matrix, a causal-graph ledger, and a proxy/measurement audit. Governs causal language strictly - "causes" only with an identification strategy.
version: 1
depends_on:
  - ../coresearch/references/evidence-grounding.md
produces:
  - docs/research/hypotheses/causal-map.md
---

# research-causal — Causal Hypothesis Mapper

Stop correlation dressed as mechanism. Hold competing explanations in one model
and name what would tell them apart.

## What & When

Maps candidate causes, mediators, moderators, confounders, proxies against one
outcome, then proposes the intervention/natural experiment that distinguishes
them. Enforces honest causal language. Use when: "why does X happen", multiple
mechanisms plausibly explain an outcome, designing an experiment needing
identification. Not for: reconciling two disagreeing papers → research-dialectic;
auditing a paper's design → research-audit.

Variable types: treatment/intervention, outcome, mediator, moderator, confounder,
proxy, collider, latent_variable, measurement_variable, selection_variable.

## Procedure

1. state outcome → 2. candidate causes → 3. mediators → 4. moderators/boundaries
→ 5. confounders → 6. proxies/measurement error → 7. selection-affected variables
→ 8. mark unsupported edges → 9. propose intervention/natural experiment → 10.
distinguishing predictions. For systems claims, encode workload and operating
envelope, baseline/config/resource parity, warm-up/cache state, repetition and
tail behavior, scale/failure regime, and cloud time/placement as possible causes,
moderators, or confounders. For ML systems, separate systems effects from model
quality; for architecture, separate simulated effects from simulator error and
PPA-model assumptions.

## Output — three views over one model

**View A — Competing Hypothesis Matrix:** Hypothesis | Proposed Cause |
Mechanism | Predicted Outcome | Boundary Conditions | Distinguishing Evidence.

**View B — Causal Graph Ledger (text graph):** per edge `{from, to, relationship:
causal|hypothesized|correlational|measurement, evidence, identification_strategy,
confidence}`. Every edge MUST carry `identification_strategy` — an edge without
one is `correlational` at best, never `causal`.

**View C — Proxy and Measurement Audit:** Target Construct | Observed Proxy |
Why Proxy | Failure Mode | Alternative Measurement.

For each distinguishing evaluation, state the intervention, fixed workload and
configuration, operating envelope, baseline parity, repetitions, measurements,
and failure conditions. Require task-quality parity for ML-systems comparisons;
require simulator-fidelity or hardware validation and explicit
power-area-performance (PPA) methodology for architecture claims.

Confidence three-dim per edge and per hypothesis.

## Reject when (gate 5)

- an edge labeled `causal` without an identification_strategy → downgrade to `correlational`;
- View C empty (proxy presented as the target construct);
- competing hypotheses given no distinguishing predictions;
- a claimed systems cause is indistinguishable from workload, warm-up, placement,
  scale, failure, quality, simulator, or PPA confounding;
- no feasible intervention AND no controlled mechanism test → hypotheses go to `hypothesis_state.unidentifiable`, not promoted to causal.

## State & Handoff

State: ledger `hypothesis_state.{candidates,distinguishable,unidentifiable}`;
edges downgraded causal→correlational logged. Next: research-audit (test a
load-bearing causal claim) / research-adversary (challenge strongest hypothesis)
/ research-gap (if an
unidentifiable hypothesis is itself the gap). Artifacts: causal-map.md.

Re-entry: return to `coresearch` to re-route the next stage.
