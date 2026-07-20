---
name: research-write
description: Rewrite systems/cloud, ML-systems, and computer-architecture paper sections with venue-aware argument, structure, and claim calibration. Use for abstracts, introductions, related work, methods, systems, evaluations, findings, discussions, limitations, conclusions, captions, and contribution bullets. Outputs polished text first, then concise diagnostics and remaining evidence risks.
---

# research-write — Paper Section Rewriter

Rewrite paper text to be clearer, more rigorous, and reviewer-evaluable; preserve the actual work and evidence.

## What & When

Rewrites and calibrates paper sections for `systems_cloud` (OSDI, SOSP, NSDI,
EuroSys, SoCC), `ml_systems` (MLSys), `computer_architecture` (ISCA, MICRO,
HPCA, IISWC), or an ASPLOS `cross_layer` lens — abstracts, introductions, related work, methods/systems,
evaluations/findings, discussions, limitations, conclusions, captions,
contribution bullets — matching each field's narrative while preserving author
intent and supplied evidence. Use when: "rewrite this section", "tighten the
argument", "make reviewer-ready", "explain a concept / decompose a mechanism".
Not for: inventing results/citations/participants/datasets/baselines/novelty;
acceptance scoring → research-review. Research-qualitative is an optional
method, not a primary venue mode or a substitute for technical evidence.

## Procedure

Pick a spine (Ha technical systems / Oh context-findings-implications / Hybrid
ASPLOS paired hardware/software); use Ha for a mechanism and evidence argument.
Use Oh for measurement/workload-characterization papers, including IISWC, where
context → findings → implications is the primary contribution. Use Hybrid for
paired hardware and software/system claims connected by a cross-layer mechanism. Match mode
tone — systems operational and measurable, ML systems parity-aware, architecture
configuration- and fidelity-explicit, ASPLOS cross-layer and causal; infer venue if missing and state it.
Inputs: venue/mode, contribution, evidence + limitations, word limit, voice
constraints. Five passes → field rules; polished text first, diagnostics second.
- **Argument** — align title, abstract, intro, contributions, conclusion around one central claim.
- **Structure** — make each section's role explicit; cut paragraphs not serving the claim.
- **Evidence** — soften claims that exceed supplied evidence.
- **Venue** — adjust norms for OSDI/SOSP/NSDI/EuroSys/SoCC, MLSys, ISCA/MICRO/HPCA/IISWC, or ASPLOS.
- **Style** — strip hype, vague nouns, promotional and unsupported language.

**Field rewrite rules:**
- Systems/Cloud (`systems_cloud`) — state the systems bottleneck and mechanism;
  name representative workloads, operating envelope, baseline/configuration
  fairness, scale, failures, tail behavior, cost, and cloud variance when supplied.
- ML Systems (`ml_systems`) — state model/task/data/hardware scope and quality
  parity before throughput, latency, energy, or cost gains; preserve convergence
  and output-quality qualifications.
- Computer Architecture/Workloads (`computer_architecture`) — name workload and
  configuration selection, warmup/sampling/repetitions, simulator fidelity or
  hardware validation, sensitivity, and the source/model for PPA claims.
- ASPLOS (`cross_layer`) — make the cross-layer dependency and causal mechanism
  explicit; show how software workloads and hardware effects are co-evaluated.
- Optional research-qualitative — report only method-backed insights and negative
  cases; keep this method separate from the Ha/Oh/Hybrid spine choice and from
  the primary technical or measurement claim.

**Section patterns (the write modes):**
- Abstract — contribution, problem/context, method/system/study, strongest
  evidence, field-level takeaway, in that order.
- Introduction — spine: domain value → core difficulty → prior-work streams →
  opportunity/gap → proposed approach → evidence → contribution bullets.
- Related Work — turn annotated bibliography into synthesis. Per stream: what it
  enabled, the assumption that matters, how this paper builds on or differs.
- Method or System — explain mechanism, not just components: inputs, outputs,
  state, control/data path, invariants, constraints, evaluation-relevant
  implementation details, operating envelope, and failure modes.
- Evaluation or Findings — lead each result with an analytical claim, then
  evidence, interpretation, implication. State workload representativeness,
  fair configurations, warmup/repetitions, dispersion and tails, scale/failures,
  and cloud variance; add ML quality parity or simulator-fidelity/PPA evidence
  when the mode requires it. Not chronological unless sequence is the finding.
- Discussion and Limitations — generalize carefully. Per limitation: what it
  affects, what it does not, what future evidence would test.

**Concept-decomposition mode** (trigger: "explain a concept", "decompose a
mechanism"). Decompose in five layers: problem → intuition → mechanism →
formalization → boundary conditions. The worked example must match the formal
definition; mark illustrative examples as illustrative; introduce no new factual
claims beyond supplied evidence. Emit as prose, then the same diagnostics.

## Output

```markdown
[Polished rewritten text first.]
## Diagnostics
- Venue mode assumed: [mode]
- Narrative spine used: [Ha / Oh / Hybrid]
- Main change: [one sentence]
- Claims softened or scoped: [bullets]
- Evidence still needed: [bullets]
- Likely score impact: [high / medium / low, with reason]
```

## Reject when (guardrails)

- would require inventing references, numbers, participants, datasets, baselines, or results;
- "novel", "first", "SOTA", "significant", "robust", or "general" asserted without evidence;
- request is to rewrite into product language;
- an engineering milestone (builds, integrates, deploys, passes tests) is rewritten as a research contribution without claim-bearing evidence;
- a performance claim obscures workload/configuration scope, warmup/repetition policy, relevant tails or variance, or fairness caveats supplied by the author;
- an ML-systems efficiency claim drops quality-parity conditions, or an architecture claim drops simulator-fidelity/PPA qualifications;
- optional qualitative evidence is generalized beyond its sampled context or used to replace technical evaluation;
- concept decomposition adds a claim not in supplied evidence, or the worked example diverges from the formal definition.

## State & Handoff

State: rewritten text carries inline diagnostics; softened/scoped claims flagged
for author confirmation; evidence-still-needed tracked. Next: research-review (venue-fit + scoring) / research-audit (softened claim needs methodology backing). Artifacts: section md + diagnostics.

Re-entry: return to `coresearch` to re-route the next stage.
