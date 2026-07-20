---
name: research-audit
description: Methodology Auditor. Audit whether a paper's evidence supports its claims, at single-paper and cross-paper level, across claim definition, workloads and experimental units, baselines/configurations, measurement and statistics, scale/failures, ML quality parity, simulator/PPA assumptions, generalization, and reproducibility. Severity-rated issues plus a revised defensible claim.
version: 1
depends_on:
  - ../coresearch/references/evidence-grounding.md
produces:
  - docs/research/audits/<paper>-audit.md
---

# research-audit — Methodology Auditor

Check whether evidence supports claims. Attack the logic, not the author. Always
end with what the evidence DOES support.

## What & When

Single-paper audit; cross-paper methodological comparison. Use when: "is this
paper's methodology sound", "would reviewers attack this", auditing a
load-bearing source. Not for: venue score → research-review; one-citation fact
check → research-verify; challenging your own synthesis chain → research-adversary.

## Procedure

Audit each dimension; tie every finding to the claim it affects.

- **Claim definition** — capability/correctness/performance/scalability/efficiency/
  reliability/cost/measurement/causal/deployment; broader than evidence?
- **Experimental unit** — requests, flows, nodes, clusters, workload instances,
  traces, models, seeds, runs, benchmark regions, or microarchitectural events;
  users/tasks only when a human study is actually part of the evidence.
- **Sampling** — workloads, traces, configurations, platforms, run times, and
  repetitions representative? hard cases or failed/censored runs excluded?
  training/tuning/test roles separated where applicable?
- **Workloads and operating envelope** — representative workload mix, trace or
  benchmark? claimed load, concurrency, dataset/model size, hardware, network,
  scale, and deployment conditions actually evaluated? hidden favorable region?
- **Baselines** — strongest included? faithful implementation and disclosed
  version/tuning/configuration? same workload, hardware, resource/compute budget,
  and measurement path? ML-systems comparisons at task-quality parity rather
  than quality sacrificed for speed or cost?
- **Metrics** — measures the claim? units and aggregation correct? averages hiding
  tails or failures? throughput/latency/load relationship coherent? gameable?
  consistent with prior work and the stated operating envelope?
- **Measurement protocol** — warm-up and steady state justified? enough independent
  repetitions/seeds? distributions and tail percentiles reported? scale and
  overload/failure/recovery exercised rather than inferred from a happy path?
- **Cloud variance** — provider/region/zone, instance type, placement/tenancy,
  run time, throttling, and temporal/placement variance recorded and repeated?
- **Architecture fidelity and PPA** — simulator validated or calibrated against
  hardware/accepted references? workloads and configurations match the claim?
  power-area-performance tools, technology node, clock, synthesis, normalization,
  and uncertainty disclosed rather than mixing incomparable estimates?
- **Statistical reasoning** — independence? right test? repeated measures? multiple comparisons? effect sizes? CIs? significance vs relevance?
- **Ablations** — isolates the mechanism? independent removal? changes budget/capacity? interactions?
- **Optional human evidence** — when present, formative/summative/comparative/
  exploratory? real task? trained? novelty bias? behavior vs preference?
  qualitative evidence traceable?
- **Generalization** — unseen workloads, traces, scales, topologies, platforms,
  models, configurations, and failure regimes. Never generalize beyond the
  measured operating envelope.
- **Reproducibility** — code/data/workload/baseline versions, resolved configs,
  seeds, platform/hardware/cloud placement, commands, result manifests, and
  failed/censored runs.

## Output

- Paper + Claim
- Claim-to-Evidence Alignment — mandatory `claim_type:` (empirical_result/methodological/.../reviewer_interpretation) and whether the paper's stated claim type is broader than evidence supports
- Experimental Design / Workload and Operating-Envelope Boundaries / Baseline and
  Configuration Fairness / Metric and Measurement Validity / Warm-up,
  Repetition, Tail, Scale, and Failure Protocol / Cloud Variance / Quality Parity
  / Simulator Fidelity and PPA, as applicable / Statistical Validity / Ablation
  Validity / Generalization Claims / Reproducibility
- Critical Issues table: Severity | Issue | Evidence | Effect on Claim | Required Fix (severity: critical/major/moderate/minor/uncertain)
- Valid Contributions
- Revised Defensible Claim — what the evidence actually supports; carries three-dim confidence
- Recommended Additional Experiment

## Reject when (gates 2,4,5,6,7)

- audit incomplete without a Revised Defensible Claim (attacking without stating what survives is not an audit);
- abstract-only paper + central claim → mark statistical/repro dims `uncertain`, say so, do not guess.
- passing artifact tests are treated as scientific validation without a
  claim-bearing benchmark, testbed, simulation, measurement, training/serving,
  or hardware evaluation.

## State & Handoff

State: ledger `source_state=audited`; unsupported claims to
`quality_state.unresolved_methodology_issues`. Next: research-causal (causal claim
survived) / research-adversary (chain bias) / research-review (venue-fit) /
research-gap (if load-bearing paper fails, the gap changes). Artifacts: audit md
+ revised-claim block.

Re-entry: return to `coresearch` to re-route the next stage.
