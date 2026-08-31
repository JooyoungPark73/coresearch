---
name: research-write
description: Realize an author-approved research argument as evidence-bounded paper prose, from local rewriting through section drafting, argument architecture, semantic revision, or concept explanation.
---

# Research write

Produce concrete, structured paper prose without inventing contribution or
evidence. Deliver the smallest complete artifact and preserve author intent.

## Modes

| Mode | Trigger | Reference |
| --- | --- | --- |
| **Local rewrite** | supplied excerpt or bounded section | delivery reference only if section structure matters |
| **Section drafting** | approved claims and evidence need prose | [systems-paper-delivery.md](references/systems-paper-delivery.md) |
| **Argument architecture** | whole-paper thesis, outline, or coherence | [argument-architecture.md](references/argument-architecture.md) |
| **Semantic revision** | feedback or evidence changes meaning beyond one passage | [semantic-revision.md](references/semantic-revision.md) |
| **Concept decomposition** | explain a mechanism or concept | problem → intuition → mechanism → formalization → boundaries |

Local rewrite is the default for a supplied excerpt. Do not force a manuscript
map or global rewrite onto a bounded wording request.

## Method

1. Fix scope, mode, audience, voice, field mode, venue lens when material,
   word limit, approved claims, supplied evidence, and limitations.
2. Load only the reference required by the selected mode. For claim bindings,
   novelty, generalization, or causal language, use
   [evidence-grounding.md](../coresearch/references/evidence-grounding.md).
   For field-specific delivery, use
   [field-modes.md](../coresearch/references/field-modes.md).
3. Preserve the canonical claim and evidence records; create no second ledger.
   Keep fact, author-provided result, planned evidence, interpretation,
   recommendation, and unknown distinct.
4. Match the argument spine: Ha for mechanism-led systems work, Oh for
   context–findings–implications, or Hybrid for coupled hardware/software
   claims. Do not force measurement, benchmark, experience, theory, or proposal
   papers into an implemented-system template.
5. Align claim, section promise, paragraph function, and sentence-level
   epistemic strength only as far upward as the requested change requires.
6. Preserve supplied numbers, configurations, citations, qualifiers, negative
   results, and limitations. Planned evidence must not read as measured;
   implemented code must not read as validated empirical evidence.
7. Causal language requires an identification strategy and credible
   mechanism evidence. Otherwise use correlational or hypothesis language.
8. Revise only affected passages. Preserve unaffected prose and author voice;
   request missing passages when consistency cannot otherwise be checked.

## Output

Return polished or revised text first. Follow with only material diagnostics:
mode, main argument change, claims preserved or scoped, evidence still needed,
and revision propagation. For argument architecture, return coherent payload,
claim dependencies, unsupported edges, section promises, and manuscript plan
before requested draft text. For semantic revision, report changed passages,
inspected but preserved passages, and author-controlled decisions.

An optional transient `manuscript_map` may reference canonical claim and
evidence IDs but must not copy their provenance or status. No second ledger is
created.

## Boundaries

Writing does not choose a new contribution, verify sources, audit methodology,
or forecast acceptance. Route score questions to `research-review` and truth or
method questions to `research-verify`. Never invent a citation, number,
participant, baseline, result, implementation status, or dependency semantics.
