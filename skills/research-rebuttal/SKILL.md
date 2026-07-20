---
name: research-rebuttal
description: Rebuttal and response-planning workflow for systems/cloud, ML-systems, and computer-architecture paper reviews. Use when the user provides reviewer comments, scores, meta-reviews, or discussion-phase feedback and wants a response strategy, score movement forecast, experiments or clarifications to add, or concise rebuttal text for OSDI, SOSP, NSDI, EuroSys, SoCC, MLSys, ISCA, MICRO, HPCA, IISWC, or ASPLOS.
---

# research-rebuttal — Review Response Planner

Turn reviews into a score-moving strategy: lead with factual corrections and
consensus clarifications, never fight every sentence. Planning artifact only —
no new experiments unless execution mode is explicit.

## What & When

Use when reviews already exist — reviewer comments, scores, meta-reviews, or
discussion feedback provided — and the user wants a response strategy, score
movement forecast, or concise rebuttal for OSDI/SOSP/NSDI/EuroSys/SoCC, MLSys,
ISCA/MICRO/HPCA/IISWC, or ASPLOS. Also use to decide what clarification, experiment, table, figure, or
wording change can realistically move scores. Not for: running new experiments →
research-engineer; adversarial replies; post-hoc or invented claims.
Primary modes are `systems_cloud`, `ml_systems`, and `computer_architecture`;
ASPLOS uses the `cross_layer` lens and paired hardware/software claims.
Research-qualitative evidence is an optional response method only when the
paper already makes a claim it can support; do not add it as a generic remedy.

## Procedure

1. **Parse each review.** Likely score, confidence, positive anchors,
   score-blocking concerns. Infer stance at low–moderate confidence if scores missing.
2. **Classify concerns.** Factual misunderstanding / missing explanation / missing
   experiment / novelty overlap / weak evidence / workload or operating-envelope
   mismatch / baseline or configuration unfairness / insufficient repetitions,
   tails, scale, failures, or variance / ML quality-parity gap / simulator-fidelity
   or PPA gap / missing cross-layer connection / writing issue / fundamental flaw.
3. **Estimate leverage** — high / medium / low / very low score-movement potential
   via the guide below.
4. **Build global strategy.** Lead with consensus corrections and score-moving
   clarifications. Do not fight every point.
5. **Plan additions.** Feasible experiments, tables, figures, citations, or text
   changes — only if allowed and the user confirms feasibility. Prefer the smallest
   addition that bears the disputed claim: representative workloads, envelope and
   configuration disclosure, fair reruns, warmup/repetitions and distributions,
   tails, scale/failure/cloud-variance tests, ML quality-parity checks, or simulator/PPA validation.
6. **Draft response bullets.** Concise, respectful, evidence-based.
7. **Forecast movement.** Post-rebuttal scores and decision path.

Leverage guide:

| Concern type | Typical leverage |
|---|---|
| Factual misunderstanding | High |
| Explanation already present but missed | Medium to high |
| Missing quick experiment or analysis | Medium |
| Missing fairness, variance, or operating-envelope clarification backed by existing evidence | Medium to high |
| Missing quality parity or simulator/PPA validation central to the claim | Low unless feasible evidence already exists |
| Missing weeks-long experiment | Low |
| Novelty concern with strong prior overlap | Low unless distinction is crisp |
| Weak venue fit | Low to medium |
| Writing clarity | Medium to high |
| Fundamental technical flaw | Very low |

## Output

- **Global Strategy** — 3–5 bullets in priority order.
- **Review-by-Review Diagnosis** (one block per reviewer): likely score / stance;
  confidence; positive anchors; score-moving concerns; legitimate weaknesses;
  possible misunderstandings; rebuttal leverage (high / medium / low / very low);
  best response strategy.
- **Cross-Reviewer Themes** — table: Theme | Reviewers | Severity | Response
  priority | Evidence needed.
- **Prioritized Response Bullets** — each point paired with its evidence.
- **Additions if Allowed** — table: Addition | Addresses | Feasibility | Expected
  score impact.
- **Risks and What Not to Say** — risks plus overclaims / defensive phrasing to avoid.
- **Predicted Score Movement** — table: Reviewer | Before | After forecast | Reason.
- **Draft Rebuttal Skeleton** — concise paragraph/bullet structure, not padded prose.

## Reject when (gates)

- promising an experiment or edit the user has not confirmed feasible (or venue disallows);
- attacking reviewers, or any defensive / adversarial tone;
- unsupported or post-hoc claims;
- a legitimate weakness left unacknowledged — acknowledge it and scope the claim.
- presenting a build, integration, or bug fix as if it resolves a research-evidence concern;
- promising representative workloads, fair configurations, repetitions/tails,
  scale/failure/cloud-variance tests, quality parity, or simulator/PPA evidence
  that has not actually been produced and checked.

## State & Handoff

Planning/handoff artifact only; no experiment execution. Next: research-engineer
(feasible additions identified) / research-write (prose polish) / research-audit
(load-bearing weakness needs verification). Carry Prioritized Response Bullets +
Additions if Allowed forward.

Re-entry: return to `coresearch` to re-route the next stage.
