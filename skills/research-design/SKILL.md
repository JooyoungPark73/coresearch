---
name: research-design
description: Design a research contribution and its claim-bearing evidence; also handles explicit gap analysis and causal-hypothesis planning without implementing experiments or writing final prose.
---

# Research design

Turn an idea, draft, result set, or repository into a reviewer-legible research
plan. Choose exactly one mode; do not silently expand an ordinary design request
into every analysis.

## Modes

| Mode | Use when | Conditional reference |
| --- | --- | --- |
| **Paper design** | contribution, claims, evidence, venue, or outline is unclear | shared evidence and field contracts |
| **Gap analysis** | the user asks what is missing, novel, or worth a paper | [gap-analysis.md](references/gap-analysis.md) |
| **Causal hypothesis** | competing mechanisms need distinguishing evidence | [causal-reasoning.md](../coresearch/references/causal-reasoning.md) |

Use [evidence-grounding.md](../coresearch/references/evidence-grounding.md) for
claim/evidence objects and [field-modes.md](../coresearch/references/field-modes.md)
only when field or venue norms change the plan.

## Method

1. State the research question, non-goals, consequential assumptions, and the
   field object that the community can define, measure, build, compare, or
   reuse differently. Buildability alone is not a contribution.
2. Name one intended contribution and a reusable research insight or testable
   hypothesis. Select Ha for mechanism-led systems work, Oh for
   context–findings–implications, or Hybrid for coupled hardware/software
   claims. Do not force every paper into a new-system narrative.
3. Write one scoped central claim and two to four non-overlapping contribution
   bullets. Bind every claim to needed evidence before implementation; mark
   unsupported claims rather than filling gaps with plans.
4. Define the smallest claim-bearing evaluation: workloads or data, operating
   envelope, baselines, configurations, metrics, provenance, falsifiers, and
   applicable field controls. Tests may establish artifact correctness but not
   scientific validity.
5. Map closest work, claim risks, paper sections, figures, and human decisions.
   Verify current venue rules from official sources when exactness matters.
6. Prioritize actions by evidence value and feasibility. Hand implementation to
   engineering only after claim, artifact, and validator are concrete.

## Output

Return the requested artifact first. For a full paper-design request, provide:

- objective, non-goals, field mode, venue lens, and assumptions;
- field object, intended contribution, narrative spine, central claim, and
  contribution bullets;
- claim ledger seed: claim, class, evidence needed, current evidence, scope,
  risk, and status;
- evaluation and closest-work plans;
- section and figure jobs;
- ranked blockers, next actions, and human decisions.

Gap and causal modes use their reference output shapes. Default to in-chat
output. Write durable state only when requested or mission-declared, using the
canonical ledger rather than a parallel schema.

## Boundaries

Do not claim novelty before closest-work falsification, causal effect without
identification, or generality beyond the planned operating envelope. Do not
invent sources, measurements, feasibility, or venue rules. Final prose belongs
to writing; source discovery to survey; code and experiment execution to
engineering; methodology attacks to verification.
