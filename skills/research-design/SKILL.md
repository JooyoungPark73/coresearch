---
name: research-design
description: Complete research planning workflow for systems/cloud, ML-systems, and computer-architecture paper ideas, drafts, projects, or repos. Use when the user says research-design, wants to design a paper, clarify contribution, choose a venue, plan claim-bearing evidence, build a claim ledger, outline the paper, or make a venue-aware score plan. Produces an in-chat design contract by default and only writes files when requested.
---

# research-design — Paper Design

Turn a rough idea, draft, experiment set, or codebase into a reviewer-legible research plan.

## What & When

Use when: "design a paper", "clarify contribution", "choose a venue", "plan
evidence", "build a claim ledger", "outline the paper", "make a venue-aware
score plan". Primary modes: `systems_cloud` (OSDI, SOSP, NSDI, EuroSys, SoCC),
`ml_systems` (MLSys), and `computer_architecture` (ISCA, MICRO, HPCA, IISWC),
with ASPLOS as a `cross_layer` lens. Research-qualitative is an optional method,
not a primary field mode. Not for: final prose → `research-write`; verified literature search →
`research-survey`; implementation or experiment code → `research-engineer`
(or `$ralplan` if OMX is installed).

## Procedure

1. **Select mode, lens, and venue** — use `systems_cloud` with `general_systems` for OSDI/SOSP/EuroSys, `networked_distributed` for NSDI, or `cloud` for SoCC; use `ml_systems` for MLSys; use `computer_architecture` for ISCA/MICRO/HPCA and add `workload_characterization` for IISWC. ASPLOS applies `cross_layer` to whichever primary mode carries the load-bearing claim.
2. **Identify the field object and insight** — apply the field-object test: what can the field define, measure, build, compare, or reuse differently? Object is one of system, protocol, runtime, scheduler, storage/network mechanism, ML pipeline/compiler, architecture or microarchitecture, workload/benchmark, measurement methodology, evaluation protocol, theory/model, or artifact package. State the reusable research insight or testable hypothesis before planning implementation; buildability alone is not a contribution.
3. **Identify contribution and claim class** — `intended_contribution` is exactly one of `method|system|representation|theory|dataset|benchmark|empirical_finding|design_knowledge|architecture|measurement_characterization`; `claim_class` is exactly one of `capability|correctness|performance|scalability|efficiency|reliability|cost|quality_performance_tradeoff|power_area_performance|generality|measurement|causal`.
4. **Draft the central claim** — one sentence, scoped to evidence, using claim architecture:
   - **Ha technical systems:** "We enable X within operating envelope Y using mechanism Z, supported by claim-bearing evidence W."
   - **Oh measurement/workload characterization:** "Across context and operating envelope X, we measure Y, find Z, and derive implication W." Make context → findings → implications the spine; IISWC can treat `measurement_characterization` as the primary contribution.
   - **Hybrid ASPLOS:** pair a hardware claim and a software/system claim, each with its own evidence path, then state the cross-layer mechanism connecting them.
   - Research-qualitative may support a scoped claim as an optional method; it is separate from Oh and never substitutes for technical or measurement evidence.
5. **Build contribution bullets** — two to four concrete, parallel, non-overlapping.
6. **Seed the claim ledger** — per claim: claim class, evidence needed, current evidence, section, risk, status.
7. **Plan evidence** — experiments, analyses, ablations, baselines, figures, proofs, hardware trials, and optional qualitative analyses that directly support each claim. Specify representative workloads, operating envelope, baseline/configuration fairness, warmup and repetitions, central and tail metrics, scale and failures, and cloud variance where relevant. Require task/model quality parity before ML-systems speed/cost claims; require simulator validation and defensible performance/power/area (PPA) methodology for architecture claims.
8. **Map related work** — streams, closest competitors, enabling, adjacent work, missing citation categories, novelty risks.
9. **Outline the paper** — section-level argumentative spine.
10. **Forecast score** — current likely score, target score, blockers, score-up conditions, score-down risks, reviewer variance.
11. **Define next actions** — prioritized by expected score impact.

## Output

Paper Design Contract (in chat by default; files only when requested):

- **1. Project Objective** — artifact produced or revised.
- **2. Venue Mode and Reviewer Model** — primary mode [`systems_cloud` / `ml_systems` / `computer_architecture`]; lens [`general_systems` / `networked_distributed` / `cloud` / `cross_layer` / `workload_characterization`]; primary venue [OSDI / SOSP / NSDI / EuroSys / SoCC / MLSys / ISCA / MICRO / HPCA / IISWC / ASPLOS]; narrative spine [Ha technical systems / Oh context-findings-implications / Hybrid ASPLOS paired hardware/software]; secondary venue; reviewer expectations; likely objections; venue-rule status [verified / unverified / needs official check].
- **3. Field Object and Contribution Thesis** — field object (define/measure/build/compare/reuse differently); `intended_contribution` [`method` / `system` / `representation` / `theory` / `dataset` / `benchmark` / `empirical_finding` / `design_knowledge` / `architecture` / `measurement_characterization`]; `claim_class` [`capability` / `correctness` / `performance` / `scalability` / `efficiency` / `reliability` / `cost` / `quality_performance_tradeoff` / `power_area_performance` / `generality` / `measurement` / `causal`]; one-sentence central claim; 2-4 concrete non-overlapping contribution bullets.
- **4. Claim Ledger Seed** — Claim | Claim class | Evidence needed | Current evidence | Section | Risk | Status.
- **5. Evidence Plan** — Claim | Evidence to add or strengthen | Priority | Feasibility | Score impact.
- **6. Related Work Plan** — direct competitors; enabling; adjacent; missing citation categories; novelty risks.
- **7. Paper Structure** — section outline with each section's argumentative job.
- **8. Figure Plan** — Figure | Claim supported | Panels/assets | Caption thesis | Risk answered.
- **9. Score Plan** — scale [official if verified, else internal]; current estimate; target; main blockers; score-up conditions; score-down risks; reviewer variance [low/medium/high].
- **10. Next Actions** — prioritized by score impact.
- **11. Human Decisions Needed** — only decisions the user must make.

## Reject when

- central claim is not one sentence;
- field object is not explicit and reusable;
- bullets are not concrete or overlap;
- any claim has no evidence path and is not marked unsupported;
- evidence plan follows venue folklore rather than the claims;
- evaluation omits workload representativeness, the operating envelope, baseline/configuration fairness, or warmup/repetition policy without explicitly scoping the affected claim;
- mean-only performance hides tails or run-to-run/cloud variance relevant to the claim, or scale/failure claims lack stress and failure evidence;
- an ML-systems efficiency claim lacks quality parity, or an architecture claim lacks simulator-fidelity and PPA support;
- engineering completion (the system builds, runs, or integrates) is treated as research evidence without a claim-bearing result;
- score blockers or score movement conditions are not explicit;
- any fabricated citation, baseline, result, or participant detail introduced.

## State & Handoff

State: design contract in chat by default; write files only when requested.
Inputs: target venue(s); abstract/notes/draft/figures/results/code/system;
workloads and operating envelope; baselines/configurations; evidence available +
planned; constraints (deadline, page limit, anonymity, available experiments or
hardware). Ask at most one clarifying question if target venue or
central artifact is impossible to infer; otherwise state assumptions and
proceed. Next: executable implementation plan → native executor / chat-only
plan (default), or `$ralplan` if OMX is installed; autonomous experiment
steering → `research-loop` (default) / `$autoresearch` if OMX is installed,
after the contract is clear.

Re-entry: return to `coresearch` to re-route the next stage.
