---
name: research-gap
description: Literature Gap Scout for systems/cloud, ML-systems, and computer architecture. Find important, testable, insufficiently resolved research opportunities (importance x tractability x novelty). Use when asked what is missing, next paper, where are contradictions, is this novel, or what would make work publishable. Not uncrowded topics.
version: 1
depends_on:
  - ../coresearch/references/evidence-grounding.md
produces:
  - docs/research/literature/gap-report.md
  - docs/research/evidence/*.yaml
---

# research-gap — Literature Gap Scout

Find gaps worth a paper — not topics nobody happens to have written about.
"Uncrowded" can mean unimportant / infeasible / known-to-fail: not a gap.

## What & When

Surfaces important, testable, insufficiently resolved opportunities, ranked on
importance × tractability × novelty. Use when: "what is missing", "next paper", "where are
contradictions", "is this novel", "what would make this OSDI/SOSP/NSDI/EuroSys/SoCC,
MLSys, ISCA/MICRO/HPCA/IISWC, or ASPLOS publishable". Primary modes are
`systems_cloud`, `ml_systems`, and `computer_architecture`; ASPLOS supplies the
`cross_layer` lens. Research-qualitative is an optional method, never a default
gap category or substitute for technical evidence.
Not for: mapping work by stream → research-survey; why papers disagree + a
mechanism → research-dialectic; auditing one paper → research-audit.

## Procedure

- **A. Field claim** — the capability the field wants.
- **B. Assumptions** — recurring assumptions behind current systems, workloads,
  operating envelopes, configurations, models, and hardware/software layers.
- **C. Consensus map** — groups supporting it, workloads/benchmarks and operating
  envelopes, baseline/configuration choices, empirical vs rhetorical support,
  and operator/developer populations only when optional qualitative evidence matters.
- **D. Contradictions** — direct empirical / workload-boundary / metric-tail /
  scale-failure / cloud-variance / quality-cost / simulator-hardware / PPA /
  cross-layer / historical.
- **E. Candidate gaps** — "Field wants A. Methods rely on B. B fails under C.
  Work has not resolved D because E. Promising contribution is F."
- **F. Falsify each** — closest work, alternate terminology, adjacent layers and
  fields, unpublished benchmarks/workshops/workloads, differing configurations
  or operating envelopes, partial solutions, and scientific insight vs unfinished
  implementation task. Test whether a claimed gap disappears under fair baselines,
  representative workloads, quality parity, or validated simulation/PPA assumptions.
- **G. Rank** — Importance, Tractability, Novelty. Each high/medium/low + one-line
  why — **never one number**.

## Output

- Field Objective
- Dominant Consensus
- Repeated Assumptions
- Contradictory Evidence (evidence objects)
- Candidate Gaps, each with: gap statement / why it matters / supporting
  evidence / closest prior work / why insufficient / candidate mechanism /
  testable hypothesis / expected contribution / falsification risks /
  recommended venue [OSDI / SOSP / NSDI / EuroSys / SoCC / MLSys / ISCA / MICRO /
  HPCA / IISWC / ASPLOS] / claim-bearing evaluation contract (representative
  workloads, operating envelope, fair baselines/configurations, warmup and
  repetitions, distributions/tails, scale/failures/cloud variance, plus ML quality
  parity or simulator-fidelity/PPA where applicable), PLUS the two mandatory fields:
  - `absence_classification:` **one of** `no_papers|few_papers|none_on_mechanism|unresolved_limitations|actual_testable_gap` — distinguishes "search found nothing" from "a real gap exists". Default to the most conservative that fits; never write `actual_testable_gap` unless closest-work falsification (step F) passed.
  - `ranking:` {importance, tractability, novelty} each high/medium/low + one-line why — not a single score.
- Rejected Gaps (candidate + reason)
- Search Coverage + Uncertainty (terminology variants, adjacent fields, what could not be reached)

Confidence: three-dim per evidence-grounding.md.

## Reject when (gates 3,7,8 + these)

- based only on a missing keyword match;
- merely a feature request;
- merely unfinished engineering, integration, optimization, or artifact completion without a research hypothesis;
- solved in an adjacent field;
- cannot be evaluated;
- depends on unrealistic data/hardware;
- relies on unrepresentative workloads, an undefined operating envelope, or an
  unfair baseline/configuration and offers no feasible correction;
- makes an ML-systems efficiency claim without a quality-parity test, or an
  architecture claim without a credible simulator-fidelity/PPA path;
- **novelty is only a new application domain** ("apply X to domain Y") — not a gap;
- unclear primary contribution;
- proposed solution does not address the stated bottleneck;
- cannot place the gap in one of the 5 absence classes → leave `uncertain`, do not promote.

## State & Handoff

State: reads `hypothesis_state.unidentifiable` (from research-causal) and
`source_state.state = audited` (from research-audit) to seed and revise gaps;
writes ledger `gap_state.{candidates,falsified,surviving}`; no regenerate
of a falsified gap without new evidence. Next: research-dialectic (active
disagreement) / research-causal (mechanism) / research-audit (load-bearing
papers). Artifacts: gap-report.md + evidence/*.yaml. Carry forward coverage blind
spots as warnings.

Re-entry: return to `coresearch` to re-route the next stage.
