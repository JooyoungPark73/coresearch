# Coresearch Stage Map

Use this when the user starts or re-scopes research.

| Stage | Question | Default route |
|---|---|---|
| Intake | What artifact, field mode, confidentiality, deadline? | `coresearch` + one question if missing |
| Idea | What is the central contribution? | `research-design` |
| Survey | What work is closest and what novelty risk exists? | `research-survey` |
| Design | What claims need evidence? | `research-design` |
| Prototype | What code supports which claim? | `research-engineer` |
| Evidence | What experiment/study/benchmark validates claims? | `research-loop` or `research-engineer` |
| Manuscript | What approved argument needs drafting, rewriting, or semantic reconciliation? | `research-write` |
| Review | What score and blockers are likely? | `research-review` |
| Rebuttal | What response can move scores? | `research-rebuttal` |
| Release | Can others reproduce artifacts? | `research-engineer` |

If several stages apply, start at the earliest blocked stage. Do not jump to prose before claim/evidence is clear.

## Analytical stages (router-owned)

These reasoning stages are owned by the Coresearch router and route via `reasoning-skills.md`; each maps to one skill.

| Stage | Question | Default route |
|---|---|---|
| Gap | What is the unsolved problem? | `research-gap` |
| Dialectic | Where do claims conflict? | `research-dialectic` |
| Causal | What causal mechanism holds? | `research-causal` |
| Audit | Is a load-bearing paper sound? | `research-audit` |
| Adversary | What counter-evidence survives? | `research-adversary` |

## Field-mode prompt

When starting research, classify the work before routing:

- `systems_cloud` — OSDI, SOSP, NSDI, EuroSys, SoCC: operating need, measured bottleneck, mechanism, representative evaluation, scale/failures/variance/cost, limits.
- `ml_systems` — MLSys: ML workload and SLO, systems bottleneck, co-design, quality/performance/cost parity, limits.
- `computer_architecture` — ISCA, MICRO, HPCA, IISWC: workload trend, architectural insight, validated methodology, PPA/complexity tradeoffs, sensitivity.

Then select a venue lens when useful: `general_systems`, `networked_distributed`, `cloud`, `cross_layer`, or `workload_characterization`. ASPLOS uses `cross_layer` and a Hybrid pair of hardware/software claims. `research-qualitative` is an optional method, not a primary field mode.
