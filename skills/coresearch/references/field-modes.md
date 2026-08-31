# Field Modes and Narrative Spines

Use this when routing `research-design`, `research-write`, `research-review`, or `research-engineer`. Pick one primary mode and, when needed, one venue lens.

## Systems / Cloud — `systems_cloud`

Primary venues: OSDI, SOSP, NSDI, EuroSys, SoCC.

Narrative spine:

```text
operating need → measured bottleneck → design insight → mechanism/system → claim-bearing evaluation → limits
```

Must foreground representative workloads, operating envelope, baseline and configuration fairness, platform and topology, warmup and repetitions, tail behavior, scale, failure model, variance, cost when claimed, and limits. For SoCC work, make multitenancy, cloud variability, scale, cost, and failures explicit when the claims depend on them. For NSDI work, make topology, network conditions, distributed failure assumptions, and end-to-end behavior explicit.

## ML Systems — `ml_systems`

Primary venue: MLSys.

Narrative spine:

```text
ML workload/SLO → systems bottleneck → co-design → quality/performance/cost frontier → limits
```

Must foreground model and dataset/workload versions, quality parity, SLOs, latency/throughput/tail metrics, resource and cost accounting, training/serving configuration, baseline and tuning fairness, scale, ablations, repetitions, and limits. A systems improvement measured at unequal model quality is not a valid efficiency comparison unless the quality tradeoff is itself the stated claim.

## Computer Architecture / Workloads — `computer_architecture`

Primary venues: ISCA, MICRO, HPCA, IISWC.

Narrative spine:

```text
workload trend → architectural insight → mechanism → validated methodology → PPA/complexity tradeoffs → sensitivity
```

Must foreground representative workloads, configuration disclosure, simulator or model fidelity and validation, warmup and measurement windows, repetitions, baseline fairness, power/performance/area assumptions, complexity and feasibility, sensitivity, and limits. For IISWC work, measurement or workload characterization may be the primary contribution when it yields reusable findings, methodology, traces, or benchmarks.

## Venue lenses

Record one of these when it materially sharpens the mode:

- `general_systems`: end-to-end operating need, mechanism, and representative evaluation; typical for OSDI, SOSP, and EuroSys.
- `networked_distributed`: topology, protocols, consistency/failure assumptions, scale, and network conditions; typical for NSDI and distributed-systems work.
- `cloud`: multitenancy, elasticity, variance, failures, scale, and cost; typical for SoCC.
- `cross_layer`: paired hardware/software claims with matched evidence; use for ASPLOS.
- `workload_characterization`: rigorous measurement, representativeness, methodology, and implications; use for IISWC-style work.

### Hybrid — ASPLOS cross-layer contract

Do not average hardware and software tones. State two linked claims: what the hardware mechanism makes possible under explicit constraints, and what the software/runtime/compiler exposes or exploits. Evaluate both claims, their interface, and cross-layer tradeoffs; two disconnected contributions do not make a cross-layer paper.

## Style guardrails

- **Ha**-style technical systems writing: mechanism-first, precise, operational, measurable. “Our system enables X under operating constraint Y using mechanism Z; evaluation W supports the claim.”
- **Oh**-style measurement/workload writing: context, findings, implications, and scoped transfer. “Across operating context A, measurement method B reveals X, implying Y within boundary Z.”
- Preserve JooYoung’s distinction: use Ha for mechanism-led papers, Oh for measurement and workload studies, and Hybrid for paired hardware/software claims.
- Avoid unsupported words: novel, robust, intuitive, general, efficient, expressive, seamless, significant, SOTA.
- `research-qualitative` may support mixed-method evidence when appropriate, but it is an optional method rather than a field mode.
