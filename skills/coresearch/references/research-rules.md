# Core Research Rules

Use this when a project is being framed, scored, or converted from “interesting demo” into paper-grade research.

## Importance doctrine

Important research changes at least one community habit:

- what the field treats as a problem;
- what it can define, measure, design, operate, architect, or compare;
- what artifact, method, dataset, benchmark, taxonomy, protocol, or failure theory others can reuse.

A strong topic usually has this form:

```text
The field wants A, but bottleneck B prevents C.
We change the problem with D, enabling E.
```

If that sentence is weak, do not compensate with prose. Rework the problem.

## Field-object test

Before writing or reviewing, answer:

> After this paper, what can the community define, measure, build, compare, or reuse differently?

Valid field objects include:

- formulation or representation;
- algorithm or solver;
- design space or grammar;
- benchmark, dataset, metric, or evaluation protocol;
- architecture, mechanism, protocol, scheduler, runtime, or resource-management policy;
- workload characterization, trace, simulator/model validation, or measurement methodology;
- reproducible system or experimentation pipeline;
- taxonomy or failure-mode theory;
- reproducible implementation or artifact package.

A demo, feature, implementation, or passing build alone is not enough. Every implementation unit must instantiate an insight, test a hypothesis, or produce claim-bearing evidence. The system or artifact must produce reusable knowledge; production hardening is valuable only when it enables or validates a research claim.

## Contribution taxonomy

Pick one primary contribution and at most two supporting ones:

| Type | Core question |
|---|---|
| Method | Does it enable a computation, optimization, representation, or control capability that was blocked before? |
| System / artifact | Does it expose a new workflow, design space, or reusable technical substrate? |
| Empirical | Does it reveal a reliable fact about how people, models, robots, or systems behave? |
| Theory / framework | Does it change the vocabulary or assumptions the field uses? |
| Dataset / benchmark | Does it let future work compare or measure something better? |
| Design knowledge | Does it make domain design principles reusable beyond examples? |
| Architecture | Does a hardware, software, or cross-layer mechanism change a capability or tradeoff under explicit constraints? |
| Measurement characterization | Does rigorous measurement reveal a reusable workload or system fact, boundary, trace, or methodology? |

## Claim-evidence fit

| Claim | Evidence required |
|---|---|
| Faster / lower latency / higher throughput | representative workload, tuned and configuration-matched baselines, warmup, repetitions, tail distributions where relevant, and uncertainty/variance |
| More scalable / reliable | scale and topology sweep, operating envelope, explicit failure model, recovery behavior, bottleneck analysis, and adversarial or degraded conditions |
| Lower cloud cost | resource-normalized cost, multitenancy and variance controls, workload/SLO parity, pricing assumptions, and sensitivity |
| Better ML-systems efficiency | matched model/data/quality target, training or serving configuration, latency/throughput/resource/cost frontier, tuned baselines, and ablations |
| Better power/performance/area | validated simulator/model or hardware method, disclosed configurations, representative workloads, PPA assumptions, complexity/feasibility, and sensitivity |
| More general | multiple workloads/platforms/operating regimes, boundary cases, stress tests, failures, and scoped limits |
| New problem definition | taxonomy, counterexamples, design-space map, case analysis |
| Measurement / workload contribution | representativeness argument, collection methodology, warmup/measurement window, repetitions, uncertainty, trace or dataset provenance, and actionable implications |
| System contribution | end-to-end claim-bearing evaluation, implementation detail, workload/baseline adapters, explicit configurations, result provenance, and reproducibility package |

Use the venue lens to select—not replace—these requirements: `general_systems` for end-to-end mechanisms, `networked_distributed` for topology/protocol/failure assumptions, `cloud` for multitenancy/elasticity/variance/cost, `cross_layer` for paired hardware/software claims, and `workload_characterization` for measurement methodology and implications.

## Research impact screen

Use this compact screen:

```text
Impact = Problem Centrality × New Insight × Evidence Quality × Reusability × Timing × Framing
```

One zero weakens the paper. Diagnose the zero before polishing language.
