---
name: research-adversary
description: Adversarial Bias Auditor. Challenge the evidence chain of a research conclusion before it becomes narrative, across retrieval, selection, citation, methodological, funding, and narrative bias. Critiques external literature AND the agent's own synthesis. Skepticism is a check, never a substitute for evidence.
version: 1
depends_on:
  - ../coresearch/references/evidence-grounding.md
produces:
  - docs/research/audits/adversary-review.md
---

# research-adversary — Adversarial Bias Auditor

Pressure-test a conclusion before it hardens into a story. Apply to external
sources AND your own synthesis. Bias hunting is a check on evidence — never a
replacement for it.

## What & When

Find what falsifies a claim, what evidence the chain missed, what claim survives.
Use when a conclusion is about to become narrative, reviewing a synthesis you or
another agent produced, "what would a skeptic attack first". Not for: one-citation
fact check → research-verify; one paper's experimental design → research-audit;
competing causal mechanisms → research-causal.

## Procedure

Run each lens; record evidence, not vibes.

- **Retrieval bias** — framing-privileged terms, prominent venues only, negative studies hard to find, recent obscures historical, adjacent-field terminology.
- **Selection bias** — narrative-supporting inclusion, inconsistent dismissal standards, successful-only.
- **Citation bias** — copied without checking original, partial-sentence support, speculation promoted to fact, survey cited instead of primary.
- **Methodological bias** — workload or benchmark favors the proposed system;
  operating envelope excludes unfavorable load/scale; baseline/config/resource
  parity is missing; warm-up, repetitions, distributions/tails, overload, or
  failures are omitted. For cloud results, inspect temporal/placement variance;
  for ML systems, task-quality parity; for architecture, simulator fidelity and
  power-area-performance (PPA) assumptions. Also inspect novelty-favoring user
  studies, expert populations, excluded failures, and superficial metrics.
- **Funding/incentive** — identify → inspect design → examine safeguards → evaluate independently. Potential incentive is NOT invalid.
- **Researcher confirmation** — search vocab from assumptions, preferred-method default, post-hoc reframing, strength-designed eval.
- **Narrative bias** — clean-story forcing, removed uncertainty, venue-exaggeration, weak findings merged into one broad claim.

Per claim: what falsifies it? was that searched? alternative mechanism? survives
strongest baseline under the same workload, operating envelope, configuration,
and budget? holds outside the benchmark and at scale/failure boundaries? warm-up,
repetitions, tails, and variance visible? cloud placement/time controlled? ML
quality held constant? simulator and PPA evidence grounded? cited evidence
primary + independent? omits conditions? claim type
(causal/comparative/descriptive/speculative)? what would a skeptic attack first?

## Output

- Claim Under Review (evidence ids supporting + contradicting)
- Retrieval / Selection-Citation / Methodological / Funding-Incentive bias risks,
  including applicable workload-envelope, baseline/config, measurement, cloud,
  quality-parity, simulator-fidelity, and PPA threats
- Alternative Explanations
- Missing Counterevidence
- Strongest Skeptical Interpretation — mandatory `skeptic_first_attack:` the single thing a skeptic attacks first
- Claim That Survives — carries three-dim confidence
- Required Corrections

## Reject when (gates 1,3,9 + must-not)

- no contradicting-evidence search run → cannot clear gate 3; mark review incomplete, do not pass;
- treat all industry-funded work as compromised;
- assume disagreement = misconduct;
- use skepticism as a substitute for evidence;
- apply stronger standards only to opposing findings;
- reject inconvenient results;
- accept a passing build, test, or smoke as evidence for a scientific claim;
- invent untestable alternative explanations;
- surviving claim relies on a bias you cannot rule out → downgrade confidence, name residual risk.

## State & Handoff

State: ledger `quality_state.{missing_counterevidence,unsupported_claims}`;
downgrade affected `claim_state`. Next: back to the synthesis skill that produced
the claim (with Required Corrections) / research-audit (weak load-bearing paper). Artifacts: adversary-review.md.

Re-entry: return to `coresearch` to re-route the next stage.
